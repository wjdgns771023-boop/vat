
# app_vat_form_supply_fixed_styled.py
# - 세율 고정 10% (비표시)
# - 금액 = 공급가액
# - "세액(자동)" → "공급세액"
# - 표 박스/음영/합계행 강조 스타일 적용

import streamlit as st

st.set_page_config(page_title="부가가치세(VAT) 신고서 작성 프로그램", layout="wide")

TAX_RATE = 0.10  # 고정 세율

def tax_from_supply(supply: int) -> int:
    return int(round(supply * TAX_RATE))

# -------------------- Global CSS --------------------
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
      .box {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 16px 16px 8px 16px;
        background: #FFFFFF;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        margin-bottom: 16px;
      }
      .box .header { font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; }
      .tbl-head {
        display: grid; grid-template-columns: 1.3fr 1fr 1fr;
        padding: 10px 12px; border-radius: 10px;
        background: #F3F4F6; color: #111827; font-weight: 600; margin-bottom: 6px;
      }
      .tbl-row {
        display: grid; grid-template-columns: 1.3fr 1fr 1fr;
        padding: 8px 12px; border-radius: 10px; background: #FAFAFA;
        margin-bottom: 6px; border: 1px dashed #E5E7EB;
      }
      .tbl-row:hover { background: #F9FAFB; }
      .total-row {
        display: grid; grid-template-columns: 1.3fr 1fr 1fr;
        padding: 10px 12px; border-radius: 12px; background: #EEF2FF;
        border: 1px solid #C7D2FE; font-weight: 700; color: #1E3A8A; margin-top: 4px;
      }
      .muted { color: #6B7280; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Header --------------------
st.title("부가가치세(VAT) 신고서 작성 프로그램")
st.caption("금액은 **공급가액** 기준으로 입력하세요. 세율은 10%로 고정되어 자동 계산됩니다. (학습/보조용)")

# ==================== 매출자료 ====================
st.markdown('<div class="box"><div class="header">매출자료</div>', unsafe_allow_html=True)
st.markdown('<div class="tbl-head"><div>증빙구분</div><div>금액(공급가액)</div><div>공급세액</div></div>', unsafe_allow_html=True)

# 세금계산서
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1:
    st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">세금계산서</div>', unsafe_allow_html=True)
with col2:
    sale_taxinv_supply = st.number_input("sale_taxinv_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3:
    sale_taxinv_tax = tax_from_supply(sale_taxinv_supply)
    st.metric("공급세액", f"{sale_taxinv_tax:,}")
st.markdown('</div>', unsafe_allow_html=True)

# 신용카드/현금영수증
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1:
    st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">신용카드·현금영수증</div>', unsafe_allow_html=True)
with col2:
    sale_card_supply = st.number_input("sale_card_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3:
    sale_card_tax = tax_from_supply(sale_card_supply)
    st.metric("공급세액", f"{sale_card_tax:,}")
st.markdown('</div>', unsafe_allow_html=True)

# 현금매출
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1:
    st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">현금매출</div>', unsafe_allow_html=True)
with col2:
    sale_cash_supply = st.number_input("sale_cash_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3:
    sale_cash_tax = tax_from_supply(sale_cash_supply)
    st.metric("공급세액", f"{sale_cash_tax:,}")
st.markdown('</div>', unsafe_allow_html=True)

sale_supply_total = sale_taxinv_supply + sale_card_supply + sale_cash_supply
sale_tax_total = sale_taxinv_tax + sale_card_tax + sale_cash_tax

# 합계 행
st.markdown(
    '<div class="total-row"><div>① 매출합계</div><div>{}</div><div>{}</div></div></div>'.format(
        f"{sale_supply_total:,}", f"{sale_tax_total:,}"
    ),
    unsafe_allow_html=True
)

# ==================== 매입자료 ====================
st.markdown('<div class="box"><div class="header">매입자료 (공제가능분)</div>', unsafe_allow_html=True)
st.markdown('<div class="tbl-head" style="grid-template-columns:1.3fr 1fr 0.8fr 1fr"><div>증빙구분</div><div>금액(공급가액)</div><div>공제가능</div><div>공급세액</div></div>', unsafe_allow_html=True)

def input_row(label_key: str, label_text: str, default_ok: bool):
    col1, col2, col3, col4 = st.columns([1.3, 1, 0.8, 1])
    with col1:
        st.markdown(f'<div class="tbl-row" style="grid-template-columns:1.3fr 1fr 0.8fr 1fr"><div style="display:flex;align-items:center;">{label_text}</div>', unsafe_allow_html=True)
    with col2:
        supply = st.number_input(f"{label_key}_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        ok = st.checkbox(f"{label_key}_ok", value=default_ok, label_visibility="collapsed")
    with col4:
        tax = tax_from_supply(supply) if ok else 0
        st.metric("공급세액", f"{tax:,}")
    st.markdown('</div>', unsafe_allow_html=True)
    return supply, tax

buy_taxinv_supply, buy_taxinv_tax = input_row("buy_taxinv", "세금계산서", True)
buy_card_supply,   buy_card_tax   = input_row("buy_card",   "신용카드·현금영수증", True)
buy_cash_supply,   buy_cash_tax   = input_row("buy_cash",   "현금매입", False)

buy_supply_total = buy_taxinv_supply + buy_card_supply + buy_cash_supply
buy_tax_total = buy_taxinv_tax + buy_card_tax + buy_cash_tax

st.markdown(
    '<div class="total-row" style="grid-template-columns:1.3fr 1fr 0.8fr 1fr"><div>② 매입합계(공제세액)</div><div>{}</div><div></div><div>{}</div></div></div>'.format(
        f"{buy_supply_total:,}", f"{buy_tax_total:,}"
    ),
    unsafe_allow_html=True
)

# ==================== 공제세액(추가) ====================
st.markdown('<div class="box"><div class="header">공제세액 (추가)</div>', unsafe_allow_html=True)
colA, colB = st.columns(2)
with colA:
    st.markdown('<div class="muted">의제매입세액 공제</div>', unsafe_allow_html=True)
    deemed_base = st.number_input("의제매입 매입가액(공급가 기준)", min_value=0, value=0, step=1000)
    deemed_rate = st.number_input("의제매입 공제율(예: 0.108)", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
    deemed_credit = int(round(deemed_base * deemed_rate))
    st.metric("의제매입세액 공제액", f"{deemed_credit:,}")
with colB:
    st.markdown('<div class="muted">기타 공제(전자신고, 신용카드발행 등)</div>', unsafe_allow_html=True)
    other_credit = st.number_input("기타 공제합계(직접 입력)", min_value=0, value=0, step=1000)

total_extra_credit = deemed_credit + other_credit
st.markdown(
    '<div class="total-row" style="grid-template-columns: 1fr"><div>③ 추가 공제합계: {}</div></div></div>'.format(
        f"{total_extra_credit:,}"
    ),
    unsafe_allow_html=True
)

# ==================== 요약 ====================
st.markdown('<div class="box"><div class="header">요약</div>', unsafe_allow_html=True)

net_vat = sale_tax_total - buy_tax_total - total_extra_credit

c1, c2, c3 = st.columns(3)
with c1: st.metric("① 매출 '공급세액' 합계", f"{sale_tax_total:,}")
with c2: st.metric("② 매입 '공급세액'(공제) 합계", f"{buy_tax_total:,}")
with c3: st.metric("③ 추가 공제합계", f"{total_extra_credit:,}")

st.markdown(
    '<div class="total-row" style="grid-template-columns: 1fr"><div>부가세 예상 납부(+) / 환급(-) 세액 = ① - ② - ③ = {}</div></div></div>'.format(
        f"{net_vat:,}"
    ),
    unsafe_allow_html=True
)

st.caption("※ 본 도구는 학습/보조용입니다. 실제 신고 전 최신 법령·불공제 항목·한도·가산세 등을 검토하세요.")
