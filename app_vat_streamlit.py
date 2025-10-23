
# app_vat_form.py
# 일반과세자 부가가치세 신고서 프로그램 (CSV 없이 수기 입력)
# 실행:
#   pip install streamlit pandas python-dateutil
#   streamlit run app_vat_form.py
#
# 주의: 학습/보조용. 실제 신고 전 최신 법령·불공제 항목·한도 확인 필수.

from typing import Tuple
import streamlit as st

st.set_page_config(page_title="부가가치세(VAT) 폼 입력 도구", layout="wide")

# ----------------- Helper -----------------
def split_tax_from_gross(amount: int, tax_rate: float) -> Tuple[int, int]:
    """총액(공급가+세액)과 세율로 공급가/세액 역산."""
    if tax_rate <= 0:
        return int(amount), 0
    supply = round(amount / (1 + tax_rate))
    return int(supply), int(amount - supply)

def split_tax_from_supply(supply: int, tax_rate: float) -> Tuple[int, int]:
    """공급가와 세율로 세액/총액 산출."""
    if tax_rate <= 0:
        return int(supply), 0
    tax = round(supply * tax_rate)
    return int(supply), int(tax)

# ----------------- UI -----------------
st.title("부가가치세(VAT) 폼 입력 도구")
st.caption("각 항목을 클릭하여 금액을 직접 입력하세요. (학습/보조용)")

with st.sidebar:
    st.subheader("입력 설정")
    rate = st.number_input("기본 세율(과세건)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    amount_mode = st.radio("금액 기준", ["총액(부가세 포함)", "공급가(부가세 제외)"], index=0)
    is_gross = amount_mode.startswith("총액")

# ===== 매출자료 =====
st.markdown("### 매출자료")
c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
with c1: st.markdown("**증빙구분**")
with c2: st.markdown("**금액**")
with c3: st.markdown("**세율**")
with c4: st.markdown("**세액(자동)**")

with st.container():
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
    with col1:
        st.write("세금계산서")
    with col2:
        sale_taxinv_amt = st.number_input("sale_taxinv_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_taxinv_rate = st.number_input("sale_taxinv_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4:
        if is_gross:
            s, t = split_tax_from_gross(sale_taxinv_amt, sale_taxinv_rate)
        else:
            s, t = split_tax_from_supply(sale_taxinv_amt, sale_taxinv_rate)
        sale_taxinv_supply, sale_taxinv_tax = s, t
        st.metric(label="세액", value=f"{t:,}")

with st.container():
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
    with col1:
        st.write("신용카드·현금영수증")
    with col2:
        sale_card_amt = st.number_input("sale_card_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_card_rate = st.number_input("sale_card_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4:
        if is_gross:
            s, t = split_tax_from_gross(sale_card_amt, sale_card_rate)
        else:
            s, t = split_tax_from_supply(sale_card_amt, sale_card_rate)
        sale_card_supply, sale_card_tax = s, t
        st.metric(label="세액", value=f"{t:,}")

with st.container():
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
    with col1:
        st.write("현금매출")
    with col2:
        sale_cash_amt = st.number_input("sale_cash_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_cash_rate = st.number_input("sale_cash_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4:
        if is_gross:
            s, t = split_tax_from_gross(sale_cash_amt, sale_cash_rate)
        else:
            s, t = split_tax_from_supply(sale_cash_amt, sale_cash_rate)
        sale_cash_supply, sale_cash_tax = s, t
        st.metric(label="세액", value=f"{t:,}")

sale_tax_total = sale_taxinv_tax + sale_card_tax + sale_cash_tax
sale_supply_total = sale_taxinv_supply + sale_card_supply + sale_cash_supply
st.info(f"**① 매출합계**  공급가액: {sale_supply_total:,} / 세액: {sale_tax_total:,}")
st.markdown("---")

# ===== 매입자료 =====
st.markdown("### 매입자료 (공제가능분)")
c1, c2, c3, c4, c5 = st.columns([1.2, 1, 1, 1, 1])
with c1: st.markdown("**증빙구분**")
with c2: st.markdown("**금액**")
with c3: st.markdown("**세율**")
with c4: st.markdown("**공제가능**")
with c5: st.markdown("**세액(자동)**")

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 1])
    with col1: st.write("세금계산서")
    with col2: buy_taxinv_amt = st.number_input("buy_taxinv_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_taxinv_rate = st.number_input("buy_taxinv_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4: buy_taxinv_ok = st.checkbox("buy_taxinv_ok", value=True, label_visibility="collapsed")
    with col5:
        if is_gross: s, t = split_tax_from_gross(buy_taxinv_amt, buy_taxinv_rate)
        else: s, t = split_tax_from_supply(buy_taxinv_amt, buy_taxinv_rate)
        buy_taxinv_supply, buy_taxinv_tax = s, (t if buy_taxinv_ok else 0)
        st.metric(label="세액", value=f"{buy_taxinv_tax:,}")

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 1])
    with col1: st.write("신용카드·현금영수증")
    with col2: buy_card_amt = st.number_input("buy_card_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_card_rate = st.number_input("buy_card_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4: buy_card_ok = st.checkbox("buy_card_ok", value=True, label_visibility="collapsed")
    with col5:
        if is_gross: s, t = split_tax_from_gross(buy_card_amt, buy_card_rate)
        else: s, t = split_tax_from_supply(buy_card_amt, buy_card_rate)
        buy_card_supply, buy_card_tax = s, (t if buy_card_ok else 0)
        st.metric(label="세액", value=f"{buy_card_tax:,}")

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 1])
    with col1: st.write("현금매입")
    with col2: buy_cash_amt = st.number_input("buy_cash_amt", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_cash_rate = st.number_input("buy_cash_rate", min_value=0.0, max_value=1.0, value=rate, step=0.01, label_visibility="collapsed")
    with col4: buy_cash_ok = st.checkbox("buy_cash_ok(공제가능)", value=False, label_visibility="collapsed")
    with col5:
        if is_gross: s, t = split_tax_from_gross(buy_cash_amt, buy_cash_rate)
        else: s, t = split_tax_from_supply(buy_cash_amt, buy_cash_rate)
        buy_cash_supply, buy_cash_tax = s, (t if buy_cash_ok else 0)
        st.metric(label="세액", value=f"{buy_cash_tax:,}")

buy_tax_total = buy_taxinv_tax + buy_card_tax + buy_cash_tax
buy_supply_total = buy_taxinv_supply + buy_card_supply + buy_cash_supply
st.info(f"**② 매입합계(공제세액)**  공급가액: {buy_supply_total:,} / 세액: {buy_tax_total:,}")
st.markdown("---")

# ===== 공제세액(추가 공제) =====
st.markdown("### 공제세액 (추가)")
colA, colB = st.columns(2)
with colA:
    st.write("의제매입세액 공제")
    deemed_base = st.number_input("의제매입 매입가액(공급가 기준)", min_value=0, value=0, step=1000,
                                  help="업종/품목별 공제율·한도 상이. 신고 전 확인 필요.")
    deemed_rate = st.number_input("의제매입 공제율(예: 0.108)", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
    deemed_credit = round(deemed_base * deemed_rate)
    st.metric("의제매입세액 공제액", f"{deemed_credit:,}")
with colB:
    st.write("기타 공제(전자신고, 신용카드발행 등)")
    other_credit = st.number_input("기타 공제합계(직접 입력)", min_value=0, value=0, step=1000)
total_extra_credit = deemed_credit + other_credit
st.info(f"**③ 추가 공제합계**: {total_extra_credit:,}")
st.markdown("---")

# ===== 요약 =====
st.markdown("### 요약")
net_vat = sale_tax_total - buy_tax_total - total_extra_credit

col1, col2, col3 = st.columns(3)
with col1: st.metric("① 매출세액 합계", f"{sale_tax_total:,}")
with col2: st.metric("② 매입세액(공제) 합계", f"{buy_tax_total:,}")
with col3: st.metric("③ 추가 공제합계", f"{total_extra_credit:,}")

st.success(f"**부가세 예상 납부(+) / 환급(-) 세액 = ① - ② - ③ = {net_vat:,}**")
st.caption("※ 참고: 실제 신고서는 항목/요건/한도 및 가산세 규정이 상세합니다. 본 도구는 학습/보조용으로 결과를 단서로만 활용하세요.")
