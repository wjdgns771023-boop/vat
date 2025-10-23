
# app_vat_streamlit.py
# 단일 파일 웹 UI: CSV 업로드 → VAT 요약
# 실행:
#   pip install streamlit pandas python-dateutil
#   streamlit run app_vat_streamlit.py
#
# CSV 요구 컬럼(소문자):
#   date (YYYY-MM-DD), type (sale|purchase), category (taxable|zero|exempt),
#   amount (정수; 기본은 총액/부가세포함), tax_rate (과세건 세율; 예: 0.1)
#
# 주의: 학습용/보조용입니다. 실제 신고 전 최신 법령·서식 확인 필수.

import io
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import pandas as pd
import streamlit as st

APP_TITLE = "부가가치세(VAT) 요약 도구"

REQUIRED_COLS = ["date", "type", "category", "amount", "tax_rate"]
TYPE_OPTIONS = ["sale", "purchase"]
CAT_OPTIONS = ["taxable", "zero", "exempt"]

def split_tax_from_gross(amount: int, tax_rate: float) -> tuple[int, int]:
    """
    총액(공급가+세액)과 세율로 공급가/세액을 역산.
    예: 총 110,000원, 세율 10% -> (100,000, 10,000)
    """
    if tax_rate is None or tax_rate <= 0:
        return int(amount), 0
    supply = round(amount / (1 + tax_rate))
    tax = int(amount) - supply
    return int(supply), int(tax)

def split_tax_from_supply(supply: int, tax_rate: float) -> tuple[int, int]:
    """
    공급가와 세율로 세액 및 총액을 산출.
    """
    if tax_rate is None or tax_rate <= 0:
        return int(supply), 0
    tax = round(supply * tax_rate)
    return int(supply), int(tax)

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # 표준화: 컬럼 소문자, 공백 제거
    df.columns = [str(c).strip().lower() for c in df.columns]
    # 필수 컬럼 체크
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"필수 컬럼이 없습니다: {', '.join(missing)}")
    # 타입 정리
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["type"] = df["type"].astype(str).str.strip().str.lower()
    df["category"] = df["category"].astype(str).str.strip().str.lower()
    # 숫자
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0).astype(int)
    df["tax_rate"] = pd.to_numeric(df["tax_rate"], errors="coerce").fillna(0.0).astype(float)
    # 유효성: 값 범위
    df = df[df["type"].isin(TYPE_OPTIONS)]
    df = df[df["category"].isin(CAT_OPTIONS)]
    df = df[df["date"].notna()]
    return df

def summarize(df: pd.DataFrame,
              start: date,
              end: date,
              amount_mode: str = "gross") -> dict:
    """
    amount_mode: 'gross' (총액/부가세포함) 또는 'supply' (공급가)
    """
    mask = (df["date"] >= start) & (df["date"] <= end)
    sub = df.loc[mask].copy()

    s_taxable_supply = s_taxable_tax = 0
    s_zero = s_exempt = 0
    p_taxable_supply = p_taxable_tax = 0

    for _, r in sub.iterrows():
        ttype, cat = r["type"], r["category"]
        amt, rate = int(r["amount"]), float(r.get("tax_rate", 0.0))

        if ttype == "sale":
            if cat == "taxable":
                if amount_mode == "gross":
                    supply, tax = split_tax_from_gross(amt, rate)
                else:
                    supply, tax = split_tax_from_supply(amt, rate)
                s_taxable_supply += supply
                s_taxable_tax += tax
            elif cat == "zero":
                # 영세: 세율 0, 공급가=amount
                s_zero += amt
            elif cat == "exempt":
                s_exempt += amt

        elif ttype == "purchase":
            if cat == "taxable":
                if amount_mode == "gross":
                    supply, tax = split_tax_from_gross(amt, rate)
                else:
                    supply, tax = split_tax_from_supply(amt, rate)
                p_taxable_supply += supply
                p_taxable_tax += tax
            # zero/exempt 매입은 공제 없음

    net_vat = s_taxable_tax - p_taxable_tax
    return {
        "과세매출 공급가액": s_taxable_supply,
        "과세매출 세액": s_taxable_tax,
        "영세매출": s_zero,
        "면세매출": s_exempt,
        "과세매입 공급가액": p_taxable_supply,
        "과세매입 세액": p_taxable_tax,
        "납부(+) / 환급(-) 세액": net_vat
    }

def to_summary_df(summary: dict) -> pd.DataFrame:
    return pd.DataFrame({"항목": list(summary.keys()), "금액": list(summary.values())})

def make_downloadable_csv(df: pd.DataFrame, filename: str) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")

# ------------------ UI ------------------

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("CSV 업로드 → 기간 선택 → 즉시 요약. (학습/보조용)")

with st.sidebar:
    st.subheader("입력 설정")
    amount_mode = st.radio("금액 기준", ["총액(부가세 포함)", "공급가(부가세 제외)"], index=0)
    amount_mode_val = "gross" if "총액" in amount_mode else "supply"
    default_rate = st.number_input("기본 세율(과세건)", min_value=0.0, max_value=1.0, value=0.1, step=0.01,
                                   help="CSV의 tax_rate가 비어있을 때 사용할 기본 세율")

uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

# 템플릿/샘플
sample = pd.DataFrame({
    "date": ["2025-01-05", "2025-01-10", "2025-01-15", "2025-01-20", "2025-02-02"],
    "type": ["sale", "purchase", "sale", "sale", "purchase"],
    "category": ["taxable", "taxable", "zero", "exempt", "taxable"],
    "amount": [110000, 55000, 200000, 30000, 22000],
    "tax_rate": [0.1, 0.1, 0.0, 0.0, 0.1],
    "memo": ["상품A 판매", "원재료 매입", "수출(영세)", "면세도서", "소모품"]
})
with st.expander("CSV 템플릿/샘플 보기", expanded=False):
    st.write("필수 컬럼:", ", ".join(REQUIRED_COLS))
    st.dataframe(sample)
    st.download_button("샘플 CSV 다운로드", data=make_downloadable_csv(sample, "vat_sample.csv"),
                       file_name="vat_sample.csv", mime="text/csv")

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        # 빈 tax_rate는 기본 세율로 채우기(과세건만)
        if "tax_rate" in df.columns:
            df["tax_rate"] = pd.to_numeric(df["tax_rate"], errors="coerce")
            df["tax_rate"] = df["tax_rate"].fillna(0.0)
        else:
            df["tax_rate"] = 0.0

        df = normalize_df(df)
        # 과세건인데 tax_rate==0이면 sidebar 기본세율로 보정
        mask_taxable = df["category"].eq("taxable") & (df["tax_rate"] <= 0)
        df.loc[mask_taxable, "tax_rate"] = float(default_rate)

        st.success(f"업로드 성공! 총 {len(df):,}건")
        st.dataframe(df.head(100), use_container_width=True)

        # 기간 선택: 기본은 데이터의 최소~최대
        min_d = min(df["date"])
        max_d = max(df["date"])
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("시작일", value=min_d, min_value=min_d, max_value=max_d)
        with col2:
            end = st.date_input("종료일", value=max_d, min_value=min_d, max_value=max_d)

        # 요약 계산
        summary = summarize(df, start, end, amount_mode=amount_mode_val)
        summary_df = to_summary_df(summary)

        st.subheader("요약 결과")
        st.dataframe(summary_df, use_container_width=True)

        # 간단 차트(막대)
        try:
            plot_df = summary_df[~summary_df["항목"].isin(["납부(+) / 환급(-) 세액"])].copy()
            st.bar_chart(plot_df.set_index("항목"))
        except Exception:
            pass

        # 다운로드
        colA, colB = st.columns(2)
        with colA:
            st.download_button("요약 CSV 다운로드", data=make_downloadable_csv(summary_df, "vat_summary.csv"),
                               file_name=f"vat_summary_{start}_{end}.csv", mime="text/csv")
        with colB:
            # 필터링된 원본도 다운로드
            mask = (df["date"] >= start) & (df["date"] <= end)
            filtered = df.loc[mask].copy()
            st.download_button("필터링된 원본 CSV 다운로드",
                               data=make_downloadable_csv(filtered, "vat_filtered.csv"),
                               file_name=f"vat_filtered_{start}_{end}.csv",
                               mime="text/csv")

        st.info("※ 이 결과는 학습/보조용입니다. 신고 전 최신 법령·서식 및 불공제 항목 여부 등을 반드시 검토하세요.")

    except Exception as e:
        st.error(f"처리 중 오류가 발생했습니다: {e}")

else:
    st.warning("CSV를 업로드하면 요약을 보여드립니다.")
