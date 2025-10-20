# 소득과 세금 변수 선언
income = 7500  # 단위: 만원
tax = 0

# if-else 문을 이용한 소득 수준 분류
if income < 2000:
    level = "저소득층"
    tax = income * 0.05   # 5% 세율
elif income < 5000:
    level = "중간소득층"
    tax = income * 0.1    # 10% 세율
else:
    level = "고소득층"
    tax = income * 0.2    # 20% 세율

# 결과 출력
print("소득 수준:", level)
print("소득 금액:", income, "만원")
print("예상 세금:", tax, "만원")
