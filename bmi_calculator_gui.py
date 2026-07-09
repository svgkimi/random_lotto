import tkinter as tk
from tkinter import messagebox


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


def on_calculate():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("입력 오류", "숫자만 입력해주세요.")
        return

    if height <= 0 or weight <= 0:
        messagebox.showerror("입력 오류", "키와 몸무게는 0보다 큰 값을 입력해주세요.")
        return

    bmi = calculate_bmi(height, weight)
    category = classify_bmi(bmi)

    result_label.config(text=f"BMI: {bmi:.2f}   ({category})")


root = tk.Tk()
root.title("BMI 계산기")
root.geometry("320x220")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="키 (cm)").grid(row=0, column=0, sticky="w", pady=5)
height_entry = tk.Entry(frame, width=15)
height_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="몸무게 (kg)").grid(row=1, column=0, sticky="w", pady=5)
weight_entry = tk.Entry(frame, width=15)
weight_entry.grid(row=1, column=1, pady=5)

calc_button = tk.Button(frame, text="BMI 계산", command=on_calculate)
calc_button.grid(row=2, column=0, columnspan=2, pady=15)

result_label = tk.Label(frame, text="", font=("Arial", 13, "bold"))
result_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
