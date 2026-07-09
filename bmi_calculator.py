def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    elif bmi < 30:
        return "비만"
    else:
        return "고도비만"


def main():
    print("=== BMI 계산기 ===")
    try:
        height = float(input("키(cm)를 입력하세요: "))
        weight = float(input("몸무게(kg)를 입력하세요: "))
    except ValueError:
        print("숫자만 입력해주세요.")
        return

    if height <= 0 or weight <= 0:
        print("키와 몸무게는 0보다 큰 값을 입력해주세요.")
        return

    bmi = calculate_bmi(height, weight)
    category = classify_bmi(bmi)

    print(f"\n당신의 BMI는 {bmi:.2f} 입니다.")
    print(f"체형 분류: {category}")


if __name__ == "__main__":
    main()
