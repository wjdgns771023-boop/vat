
# app_vat_form_supply_fixed.py
# 변경사항:
#  - 세율 고정 10% (화면 비표시)
#  - 입력 금액 = 공급가액
#  - "세액(자동)" → "공급세액"
#
# 실행:
#   pip install streamlit
#   streamlit run app_vat_form_supply_fixed.py

import streamlit as st

st.set_page_config(page_title="부가가치세(VAT) 신고서 작성 프로그램", layout="wide")

TAX_RATE = 0.10  # 고정 세율 (화면에 표시하지 않음)

def tax_from_supply(supply: int) -> int:
    return int(round(supply * TAX_RATE))

st.title("부가가치세(VAT) 신고서 작성 프로그램")
st.caption("금액은 **공급가액** 기준으로 입력하세요. 세율은 10%로 고정되어 자동 계산됩니다. (학습/보조용)")

# ===== 매출자료 =====
st.markdown("### 매출자료")
c1, c2, c3 = st.columns([1.3, 1, 1])
with c1: st.markdown("**증빙구분**")
with c2: st.markdown("**금액(공급가액)**")
with c3: st.markdown("**공급세액**")

with st.container():
    col1, col2, col3 = st.columns([1.3, 1, 1])
    with col1: st.write("세금계산서")
    with col2: sale_taxinv_supply = st.number_input("sale_taxinv_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_taxinv_tax = tax_from_supply(sale_taxinv_supply)
        st.metric("공급세액", f"{sale_taxinv_tax:,}")

with st.container():
    col1, col2, col3 = st.columns([1.3, 1, 1])
    with col1: st.write("신용카드·현금영수증")
    with col2: sale_card_supply = st.number_input("sale_card_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_card_tax = tax_from_supply(sale_card_supply)
        st.metric("공급세액", f"{sale_card_tax:,}")

with st.container():
    col1, col2, col3 = st.columns([1.3, 1, 1])
    with col1: st.write("현금매출")
    with col2: sale_cash_supply = st.number_input("sale_cash_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3:
        sale_cash_tax = tax_from_supply(sale_cash_supply)
        st.metric("공급세액", f"{sale_cash_tax:,}")

sale_supply_total = sale_taxinv_supply + sale_card_supply + sale_cash_supply
sale_tax_total = sale_taxinv_tax + sale_card_tax + sale_cash_tax
st.info(f"**① 매출합계**  공급가액: {sale_supply_total:,} / 공급세액: {sale_tax_total:,}")
st.markdown("---")

# ===== 매입자료 =====
st.markdown("### 매입자료 (공제가능분)")
c1, c2, c3, c4 = st.columns([1.3, 1, 1, 1])
with c1: st.markdown("**증빙구분**")
with c2: st.markdown("**금액(공급가액)**")
with c3: st.markdown("**공제가능**")
with c4: st.markdown("**공급세액**")

with st.container():
    col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1])
    with col1: st.write("세금계산서")
    with col2: buy_taxinv_supply = st.number_input("buy_taxinv_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_taxinv_ok = st.checkbox("buy_taxinv_ok", value=True, label_visibility="collapsed")
    with col4:
        t = tax_from_supply(buy_taxinv_supply) if buy_taxinv_ok else 0
        buy_taxinv_tax = t
        st.metric("공급세액", f"{t:,}")

with st.container():
    col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1])
    with col1: st.write("신용카드·현금영수증")
    with col2: buy_card_supply = st.number_input("buy_card_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_card_ok = st.checkbox("buy_card_ok", value=True, label_visibility="collapsed")
    with col4:
        t = tax_from_supply(buy_card_supply) if buy_card_ok else 0
        buy_card_tax = t
        st.metric("공급세액", f"{t:,}")

with st.container():
    col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1])
    with col1: st.write("현금매입")
    with col2: buy_cash_supply = st.number_input("buy_cash_supply", min_value=0, value=0, step=1000, label_visibility="collapsed")
    with col3: buy_cash_ok = st.checkbox("buy_cash_ok(공제가능)", value=False, label_visibility="collapsed")
    with col4:
        t = tax_from_supply(buy_cash_supply) if buy_cash_ok else 0
        buy_cash_tax = t
        st.metric("공급세액", f"{t:,}")

buy_supply_total = buy_taxinv_supply + buy_card_supply + buy_cash_supply
buy_tax_total = buy_taxinv_tax + buy_card_tax + buy_cash_tax
st.info(f"**② 매입합계(공제세액)**  공급가액: {buy_supply_total:,} / 공급세액: {buy_tax_total:,}")
st.markdown("---")

# ===== 공제세액(추가) =====
st.markdown("### 공제세액 (추가)")
colA, colB = st.columns(2)
with colA:
    st.write("의제매입세액 공제")
    deemed_base = st.number_input("의제매입 매입가액(공급가 기준)", min_value=0, value=0, step=1000)
    deemed_rate = st.number_input("의제매입 공제율(예: 0.108)", min_value=0.0, max_value=1.0, value=0.0, step=0.001)
    deemed_credit = int(round(deemed_base * deemed_rate))
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
with col1: st.metric("① 매출 '공급세액' 합계", f"{sale_tax_total:,}")
with col2: st.metric("② 매입 '공급세액'(공제) 합계", f"{buy_tax_total:,}")
with col3: st.metric("③ 추가 공제합계", f"{total_extra_credit:,}")

st.success(f"**부가세 예상 납부(+) / 환급(-) 세액 = ① - ② - ③ = {net_vat:,}**")

st.caption("※ 본 도구는 학습/보조용입니다. 실제 신고 전 최신 법령·불공제 항목·한도·가산세 등을 검토하세요.")
