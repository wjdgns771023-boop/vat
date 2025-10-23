
# app_vat_form_supply_fixed_styled_spacing.py
# - 숫자만 표시 유지
# - 세율 고정 10%, 공급가액 입력
# - 박스/음영/합계행 강조
# - "매출합계"와 "매입자료(공제가능분)" 사이 간격 확대
# - 수준별(섹션/그룹/행) 줄띄우기 간격을 다르게 적용

import streamlit as st

st.set_page_config(page_title="부가가치세(VAT) 신고서 작성 프로그램", layout="wide")
TAX_RATE = 0.10

def tax_from_supply(supply: int) -> int:
    return int(round(supply * TAX_RATE))

# ------------- CSS with spacing scales -------------
st.markdown(
    """
    <style>
      :root{
        --gap-section: 28px;  /* 섹션 간 간격 (큰 줄띄우기) */
        --gap-group:   16px;  /* 그룹 간 간격 (예: 합계행 ↔ 다음 박스) */
        --gap-row:      8px;  /* 행 간 간격 */
      }

      .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

      .box {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 16px 16px 8px 16px;
        background: #FFFFFF;
        box-shadow: 0 1px 2px rgba(16,24,40,.04);
        margin-bottom: var(--gap-section); /* 섹션 하단 간격 */
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
        margin-top: 4px; margin-bottom: var(--gap-group); /* 그룹 간 간격 */
      }

      /* 4-열 합계행용 */
      .total-row-4 {
        display: grid; grid-template-columns: 1.3fr 1fr 0.8fr 1fr;
        padding: 10px 12px; border-radius: 12px; background: #EEF2FF;
        border: 1px solid #C7D2FE; font-weight: 700; color: #1E3A8A;
        margin-top: 4px; margin-bottom: var(--gap-group);
      }

      /* 단일열 합계행용 */
      .total-row-1 {
        display: grid; grid-template-columns: 1fr;
        padding: 10px 12px; border-radius: 12px; background: #EEF2FF;
        border: 1px solid #C7D2FE; font-weight: 700; color: #1E3A8A;
        margin-top: 4px; margin-bottom: var(--gap-group);
      }

      .muted { color: #6B7280; font-size: 0.9rem; }
      .num { text-align: right; font-weight: 700; font-size: 1.25rem; padding-top: 4px; }
      .spacer { height: var(--gap-group); }
      .spacer-lg { height: var(--gap-section); }
    </style>
    """,
    unsafe_allow_html=True
)

def render_num(value: int):
    st.markdown(f'<div class="num">{value:,}</div>', unsafe_allow_html=True)

# ------------- Header -------------
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

# 현금매출
col1, col2, col3 = st.columns([1.3, 1, 1])
with col1: st.markdown('<div class="tbl-row"><div style="display:flex;align-items:center;">현금매출</div>', unsafe_allow_html=True)
with col2: sale_cash_supply = st.number_input("sale_cash_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
with col3: sale_cash_tax = tax_from_supply(sale_cash_supply); render_num(sale_cash_tax)
st.markdown('</div>', unsafe_allow_html=True)

sale_supply_total = sale_taxinv_supply + sale_card_supply + sale_cash_supply
sale_tax_total = sale_taxinv_tax + sale_card_tax + sale_cash_tax

# 합계행 (여기서 group-gap 적용 → 다음 섹션과 줄띄우기 넉넉하게)
st.markdown(
    '<div class="total-row"><div>① 매출합계</div><div>{}</div><div>{}</div></div>'.format(
        f"{sale_supply_total:,}", f"{sale_tax_total:,}"
    ),
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)  # close 매출 box

# ============== 매입자료(공제가능분) ==============
st.markdown('<div class="box"><div class="header">매입자료 (공제가능분)</div>', unsafe_allow_html=True)
st.markdown('<div class="tbl-head" style="grid-template-columns:1.3fr 1fr 0.8fr 1fr"><div>증빙구분</div><div>금액(공급가액)</div><div>공제가능</div><div>공급세액</div></div>', unsafe_allow_html=True)

def input_row(label_key: str, label_text: str, default_ok: bool):
    col1, col2, col3, col4 = st.columns([1.3, 1, 0.8, 1])
    with col1: st.markdown(f'<div class="tbl-row" style="grid-template-columns:1.3fr 1fr 0.8fr 1fr"><div style="display:flex;align-items:center;">{label_text}</div>', unsafe_allow_html=True)
    with col2: supply = st.number_input(f"{label_key}_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: ok = st.checkbox(f"{label_key}_ok", value=default_ok, label_visibility="collapsed")
    with col4: tax = tax_from_supply(supply) if ok else 0; render_num(tax)
    st.markdown('</div>', unsafe_allow_html=True)
    return supply, (tax_from_supply(supply) if ok else 0)

buy_taxinv_supply, buy_taxinv_tax = input_row("buy_taxinv", "세금계산서", True)
buy_card_supply,   buy_card_tax   = input_row("buy_card",   "신용카드·현금영수증", True)
buy_cash_supply,   buy_cash_tax   = input_row("buy_cash",   "현금매입", False)

buy_supply_total = buy_taxinv_supply + buy_card_supply + buy_cash_supply
buy_tax_total = buy_taxinv_tax + buy_card_tax + buy_cash_tax

st.markdown(
    '<div class="total-row-4"><div>② 매입합계(공제세액)</div><div>{}</div><div></div><div>{}</div></div>'.format(
        f"{buy_supply_total:,}", f"{buy_tax_total:,}"
    ),
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)  # close 매입 box

# ============== 공제세액(추가) ==============
st.markdown('<div class="box"><div class="header">공제세액 (추가)</div>', unsafe_allow_html=True)
colA, colB = st.columns(2)
with colA:
    st.markdown('<div class="muted">의제매입세액 공제</div>', unsafe_allow_html=True)
    deemed_base = st.number_input("의제매입 매입가액(공급가 기준)", min_value=0, value=0, step=1000)
    deemed_rate = st.number_input("의제매입 공제율(예: 0.108)", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
    deemed_credit = int(round(deemed_base * deemed_rate))
    st.markdown(f'<div class="num">{deemed_credit:,}</div>', unsafe_allow_html=True)
with colB:
    st.markdown('<div class="muted">기타 공제(전자신고, 신용카드발행 등)</div>', unsafe_allow_html=True)
    other_credit = st.number_input("기타 공제합계(직접 입력)", min_value=0, value=0, step=1000)

total_extra_credit = deemed_credit + other_credit
st.markdown(
    '<div class="total-row-1"><div>③ 추가 공제합계: {}</div></div>'.format(f"{total_extra_credit:,}"),
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)  # close 공제 box

# ============== 요약 ==============
st.markdown('<div class="box"><div class="header">요약</div>', unsafe_allow_html=True)

net_vat = (sale_tax_total) - (buy_tax_total) - (total_extra_credit)

c1, c2, c3 = st.columns(3)
with c1: st.metric("① 매출 '공급세액' 합계", f"{sale_tax_total:,}")
with c2: st.metric("② 매입 '공급세액'(공제) 합계", f"{buy_tax_total:,}")
with c3: st.metric("③ 추가 공제합계", f"{total_extra_credit:,}")

st.markdown(
    '<div class="total-row-1"><div>부가세 예상 납부(+) / 환급(-) 세액 = ① - ② - ③ = {}</div></div>'.format(
        f"{net_vat:,}"
    ),
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)  # close 요약 box
