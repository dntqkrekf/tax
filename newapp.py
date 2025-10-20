import streamlit as st

st.title("💰 소득 수준별 세금 계산기")

# 입력 받기
income = st.number_input("소득 금액을 입력하세요 (단위: 만원)", min_value=0, step=100)
tax = 0

# if-else 문을 이용한 소득 수준 분류
if income < 2000:
    level = "저소득층"
    tax = income * 0.05
elif income < 5000:
    level = "중간소득층"
    tax = income * 0.1
else:
    level = "고소득층"
    tax = income * 0.2

# 결과 출력
st.write("### 📊 계산 결과")
st.write("소득 수준:", level)
st.write("소득 금액:", f"{income:,} 만원")
st.write("예상 세금:", f"{tax:,.1f} 만원")
