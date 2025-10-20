# 2018 대한민국 종합소득세 계산기 (과세표준 기준, 원)
# 작성자: 당신

import streamlit as st
from dataclasses import dataclass

st.set_page_config(page_title="2018 종합소득세 계산기", page_icon="💰")

st.title("💰 2018 대한민국 종합소득세 계산기")
st.caption("과세표준(원) 기준 · 구간별 누진세율 합산 계산 · 지방소득세(국세의 10%) 포함 가능")

@dataclass
class TaxBracket:
    limit: int
    rate: float

# 2018 과세표준 기준 세율표
BRACKETS_2018 = [
    TaxBracket(12_000_000, 0.06),    # 1,200만원 이하
    TaxBracket(46_000_000, 0.15),    # 4,600만원 이하
    TaxBracket(88_000_000, 0.24),    # 8,800만원 이하
    TaxBracket(150_000_000, 0.35),   # 1억5천만원 이하
    TaxBracket(300_000_000, 0.38),   # 3억원 이하
    TaxBracket(500_000_000, 0.40),   # 5억원 이하
    TaxBracket(1_000_000_000, 0.42), # 10억원 이하
    TaxBracket(None, 0.45),          # 10억원 초과
]

def calc_income_tax_kr_2018(taxable_income: int, include_local_tax: bool = True):
    """2018 과세표준 기준 누진세율 계산"""
    if taxable_income <= 0:
        return 0, 0, 0, []

    remaining = taxable_income
    lower = 0
    national = 0
    details = []

    for b in BRACKETS_2018:
        upper = b.limit if b.limit is not None else taxable_income
        span = (upper - lower) if b.limit is not None else remaining
        taxable_here = max(0, min(remaining, span))
        if taxable_here <= 0:
            break

        tax_here = int(round(taxable_here * b.rate))
        national += tax_here
        details.append({
            "구간": f"{lower:,} ~ {('∞' if b.limit is None else format(upper, ','))} 원",
            "적용 세율": f"{int(b.rate * 100)}%",
            "해당 구간 과세표준": f"{taxable_here:,} 원",
            "구간 세액": f"{tax_here:,} 원"
        })

        remaining -= taxable_here
        lower = upper
        if remaining <= 0:
            break

    local = int(round(national * 0.10)) if include_local_tax else 0
    total = national + local

    return national, local, total, details

# Streamlit UI
with st.form("input_form"):
    taxable_income = st.number_input("과세표준(원)을 입력하세요", min_value=0, step=100_000, value=75_000_000, format="%d")
    include_local = st.checkbox("지방소득세(국세의 10%) 포함", value=True)
    submitted = st.form_submit_button("계산하기")

if submitted:
    national, local, total, details = calc_income_tax_kr_2018(taxable_income, include_local)
    st.subheader("📊 계산 결과")
    st.metric("국세(소득세)", f"{national:,} 원")
    if include_local:
        st.metric("지방소득세 (10%)", f"{local:,} 원")
    st.metric("총 세액", f"{total:,} 원")

    if details:
        st.write("### 📋 구간별 내역")
        st.dataframe(details, use_container_width=True)

st.divider()
st.caption("※ 본 계산기는 2018년 귀속 종합소득세율 기준 예시이며, 공제·감면·누진공제 등은 반영되지 않았습니다.")
