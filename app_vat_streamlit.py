
# app_vat_form_supply_fixed_styled_nochk_nocash.py
# - 세율 고정 10%, 금액=공급가액
# - 숫자만 표시, 박스/음영/합계행 강조, 간격 스케일 유지
# - 매입자료에서 "공제가능" 체크박스 제거
# - 매입자료에서 "현금매입" 행 제거

import streamlit as st

st.set_page_config(page_title="부가가치세(VAT) 신고서 작성 프로그램", layout="wide")
TAX_RATE = 0.10

def tax_from_supply(supply: int) -> int:
    return int(round(supply * TAX_RATE))

# -------- CSS (spacing + styles) --------
st.markdown(
    """
    <style>
      :root{
        --gap-section: 28px;
        --gap-group:   16px;
        --gap-row:      8px;
      }
      .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
      .box {
        border: 1px solid #E5E7EB; border-radius: 14px;
        padding: 16px 16px 8px 16px; background: #FFFFFF;
        box-shadow: 0 1px 2px rgba(16,24,40,.04);
        margin-bottom: var(--gap-section);
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
        margin-bottom: var(--gap-row); border: 1px dashed #E5E7EB;
      }
      .tbl-row:hover { background: #F9FAFB; }
      .total-row {
        display: grid; grid-template-columns: 1.3fr 1fr 1fr;
        padding: 10px 12px; border-radius: 12px; background: #EEF2FF;
        border: 1px solid #C7D2FE; font-weight: 700; color: #1E3A8A;
        margin-top: 4px; margin-bottom: var(--gap-group);
      }
      .total-row-1 {
        display: grid; grid-template-columns: 1fr;
        padding: 10px 12px; border-radius: 12px; background: #EEF2FF;
        border: 1px solid #C7D2FE; font-weight: 700; color: #1E3A8A;
        margin-top: 4px; margin-bottom: var(--gap-group);
      }
      .muted { color: #6B7280; font-size: 0.9rem; }
      .num { text-align: right; font-weight: 700; font-size: 1.25rem; padding-top: 4px; }
    </style>
    """,
    unsafe_allow_html=True
)

def render_num(value: int):
    st.markdown(f'<div class="num">{value:,}</div>', unsafe_allow_html=True)

# -------- Header --------
st.title("부가가치세(VAT) 신고서 작성 프로그램")
st.caption("금액은 공급가액 기준으로 입력하세요. 세율은 10%로 고정되어 자동 계산됩니다. (학습/보조용)")

# ============== 매출자료 ==============
st.markdown('<div class="box"><div class="header">매출자료</div>', unsafe_allow_html=True)
st.markdown('<div class="tbl-head"><div>증빙구분</div><div>금액(공급가액)</div><div>공급세액</div></div>', unsafe_allow_html=True)

# 세금계산서
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1: st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">세금계산서</div>', unsafe_allow_html=True)
with col2: sale_taxinv_supply = st.number_input("sale_taxinv_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3: sale_taxinv_tax = tax_from_supply(sale_taxinv_supply); render_num(sale_taxinv_tax)
st.markdown('</div>', unsafe_allow_html=True)

# 신용카드·현금영수증
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1: st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">신용카드·현금영수증</div>', unsafe_allow_html=True)
with col2: sale_card_supply = st.number_input("sale_card_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3: sale_card_tax = tax_from_supply(sale_card_supply); render_num(sale_card_tax)
st.markdown('</div>', unsafe_allow_html=True)

# (현금매출은 매출쪽에 유지)

sale_supply_total = sale_taxinv_supply + sale_card_supply
sale_tax_total = sale_taxinv_tax + sale_card_tax

st.markdown(
    '<div class="total-row"><div>① 매출합계</div><div>{}</div><div>{}</div></div>'.format(
        f"{sale_supply_total:,}", f"{sale_tax_total:,}"
    ), unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ============== 매입자료 (공제가능분) ==============
st.markdown('<div class="box"><div class="header">매입자료 (공제가능분)</div>', unsafe_allow_html=True)
# 머리글: 체크박스/현금매입 제거 → 3열 구조
st.markdown('<div class="tbl-head"><div>증빙구분</div><div>금액(공급가액)</div><div>공급세액</div></div>', unsafe_allow_html=True)

# 세금계산서 (항상 공제)
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1: st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">세금계산서</div>', unsafe_allow_html=True)
with col2: buy_taxinv_supply = st.number_input("buy_taxinv_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3: buy_taxinv_tax = tax_from_supply(buy_taxinv_supply); render_num(buy_taxinv_tax)
st.markdown('</div>', unsafe_allow_html=True)

# 신용카드·현금영수증 (항상 공제)
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1: st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">신용카드·현금영수증</div>', unsafe_allow_html=True)
with col2: buy_card_supply = st.number_input("buy_card_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3: buy_card_tax = tax_from_supply(buy_card_supply); render_num(buy_card_tax)
st.markdown('</div>', unsafe_allow_html=True)

# (현금매입 제거)

buy_supply_total = buy_taxinv_supply + buy_card_supply
buy_tax_total = buy_taxinv_tax + buy_card_tax

st.markdown(
    '<div class="total-row"><div>② 매입합계(공제세액)</div><div>{}</div><div>{}</div></div>'.format(
        f"{buy_supply_total:,}", f"{buy_tax_total:,}"
    ), unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ============== 공제세액(추가) & 요약 ==============
st.markdown('<div class="box"><div class="header">공제세액 (추가)</div>', unsafe_allow_html=True)
colA, colB = st.columns(2)
with colA:
    st.markdown('<div class="muted">의제매입세액 공제</div>', unsafe_allow_html=True)
    deemed_base = st.number_input("의제매입 매입가액(공급가 기준)", min_value=0, value=0, step=1000)
    deemed_rate = st.number_input("의제매입 공제율(예: 0.108)", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
    deemed_credit = int(round(deemed_base * deemed_rate))
    render_num(deemed_credit)
with colB:
    st.markdown('<div class="muted">기타 공제(전자신고, 신용카드발행 등)</div>', unsafe_allow_html=True)
    other_credit = st.number_input("기타 공제합계(직접 입력)", min_value=0, value=0, step=1000)
total_extra_credit = deemed_credit + other_credit
st.markdown('<div class="total-row-1"><div>③ 추가 공제합계: {}</div></div>'.format(f"{total_extra_credit:,}"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="box"><div class="header">요약</div>', unsafe_allow_html=True)
net_vat = sale_tax_total - buy_tax_total - total_extra_credit
c1, c2, c3 = st.columns(3)
with c1: st.metric("① 매출 '공급세액' 합계", f"{sale_tax_total:,}")
with c2: st.metric("② 매입 '공급세액'(공제) 합계", f"{buy_tax_total:,}")
with c3: st.metric("③ 추가 공제합계", f"{total_extra_credit:,}")
st.markdown('<div class="total-row-1"><div>부가세 예상 납부(+) / 환급(-) 세액 = ① - ② - ③ = {}</div></div>'.format(f"{net_vat:,}"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
