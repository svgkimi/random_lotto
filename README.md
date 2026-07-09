# 🎲 Random Lotto Picker & BMI Calculator

Python과 Tkinter를 활용하여 개발된 GUI 애플리케이션 모음입니다. 이 프로젝트에는 로또 번호 추첨기와 BMI(체질량 지수) 계산기가 포함되어 있습니다.

## 🚀 기능 (Features)

### 1. 로또 번호 추첨기 (`lotto_picker.py`)
- 직관적이고 깔끔한 GUI 디자인
- 랜덤 로또 번호 자동 생성
- OpenWeather API를 활용한 날씨 정보 연동
- `.env` 파일을 통한 안전한 API 키 관리

### 2. BMI 계산기 (`bmi_calculator_gui.py` / `bmi_calculator.py`)
- 키와 몸무게를 입력받아 BMI 수치 및 비만도 상태 결과 출력
- 간편하게 사용할 수 있는 GUI 제공

## 📦 설치 및 실행 방법 (Installation & Usage)

1. **필수 패키지 설치 (Install dependencies)**
   ```bash
   pip install requests python-dotenv
   ```

2. **환경 변수 설정 (Environment Variables)**
   프로젝트 루트에 `.env` 파일을 생성하고 OpenWeather API 키를 입력하세요.
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **프로그램 실행 (Run)**
   - **로또 번호 추첨기**:
     ```bash
     python lotto_picker.py
     ```
   - **BMI 계산기**:
     ```bash
     python bmi_calculator_gui.py
     ```

## 🛠 사용 기술 (Tech Stack)
- **Language**: Python 3
- **GUI Framework**: Tkinter
- **Environment Management**: python-dotenv
- **API Requests**: requests (OpenWeather API 연동)
