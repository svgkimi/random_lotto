import tkinter as tk
from tkinter import font as tkfont
import random
import time
import threading

# ── 토스 컬러 팔레트 ─────────────────────────────────────
TOSS_BLUE    = "#0064FF"
TOSS_BLUE_LT = "#EBF2FF"
TOSS_BG      = "#F9FAFB"
TOSS_WHITE   = "#FFFFFF"
TOSS_GRAY1   = "#F2F4F6"
TOSS_GRAY2   = "#8B95A1"
TOSS_GRAY3   = "#4E5968"
TOSS_BLACK   = "#191F28"
TOSS_RED     = "#F04452"
TOSS_YELLOW  = "#FFC107"
TOSS_GREEN   = "#00C073"

# 로또 번호 색상 (1–45)
def ball_color(n):
    if   n <= 10: return "#FBC400", "#000"   # 노랑
    elif n <= 20: return "#69C8F2", "#000"   # 하늘
    elif n <= 30: return "#FF7272", "#fff"   # 빨강
    elif n <= 40: return "#AAB0BE", "#fff"   # 회색
    else:         return "#B0D840", "#000"   # 초록


class RoundedButton(tk.Canvas):
    """캔버스 기반 둥근 버튼"""
    def __init__(self, parent, text, command, width=280, height=56,
                 bg=TOSS_BLUE, fg="#fff", radius=14, font_size=16, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"] if hasattr(parent, "__getitem__") else TOSS_BG,
                         highlightthickness=0, **kwargs)
        self.command   = command
        self.bg_normal = bg
        self.bg_hover  = self._darken(bg)
        self.fg        = fg
        self.radius    = radius
        self.w, self.h = width, height
        self.text_str  = text
        self.font_size = font_size
        self._draw(self.bg_normal)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _darken(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return "#{:02x}{:02x}{:02x}".format(max(r-20,0), max(g-20,0), max(b-20,0))

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        self.create_arc(x1,   y1,   x1+2*r, y1+2*r, start=90,  extent=90,  **kw)
        self.create_arc(x2-2*r, y1, x2,     y1+2*r, start=0,   extent=90,  **kw)
        self.create_arc(x2-2*r, y2-2*r, x2, y2,     start=270, extent=90,  **kw)
        self.create_arc(x1,   y2-2*r, x1+2*r, y2,   start=180, extent=90,  **kw)
        self.create_rectangle(x1+r, y1, x2-r, y2, **kw)
        self.create_rectangle(x1, y1+r, x2, y2-r, **kw)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(0, 0, self.w, self.h, self.radius,
                         fill=color, outline=color)
        self.create_text(self.w//2, self.h//2, text=self.text_str,
                         fill=self.fg,
                         font=("Apple SD Gothic Neo", self.font_size, "bold"))

    def _on_enter(self, _):   self._draw(self.bg_hover)
    def _on_leave(self, _):   self._draw(self.bg_normal)
    def _on_click(self, _):   self._draw(self._darken(self.bg_hover))
    def _on_release(self, _):
        self._draw(self.bg_normal)
        if self.command: self.command()

    def set_text(self, t):
        self.text_str = t
        self._draw(self.bg_normal)

    def set_state(self, state):
        if state == "disabled":
            self._draw("#C4CDD5")
            self.unbind("<Button-1>")
            self.unbind("<Enter>")
            self.unbind("<Leave>")
        else:
            self._draw(self.bg_normal)
            self.bind("<Enter>",    self._on_enter)
            self.bind("<Leave>",    self._on_leave)
            self.bind("<Button-1>", self._on_click)
            self.bind("<ButtonRelease-1>", self._on_release)


class BallCanvas(tk.Canvas):
    """번호 하나를 표시하는 원형 캔버스"""
    def __init__(self, parent, size=62):
        super().__init__(parent, width=size, height=size,
                         bg=TOSS_WHITE, highlightthickness=0)
        self.size = size
        self.draw_empty()

    def draw_empty(self):
        self.delete("all")
        self.create_oval(2, 2, self.size-2, self.size-2,
                         fill=TOSS_GRAY1, outline=TOSS_GRAY1)
        self.create_text(self.size//2, self.size//2,
                         text="?", fill=TOSS_GRAY2,
                         font=("Apple SD Gothic Neo", 20, "bold"))

    def draw_number(self, n):
        self.delete("all")
        bg, fg = ball_color(n)
        self.create_oval(2, 2, self.size-2, self.size-2,
                         fill=bg, outline=bg)
        self.create_text(self.size//2, self.size//2,
                         text=str(n), fill=fg,
                         font=("Apple SD Gothic Neo", 18, "bold"))

    def flash(self, n, callback=None):
        """번호가 반짝이며 나타나는 애니메이션"""
        steps = 6
        delay = 40

        def animate(step):
            if step < steps:
                # 깜빡이며 랜덤 숫자 표시
                tmp = random.randint(1, 45)
                self.delete("all")
                bg, fg = ball_color(tmp)
                alpha_colors = ["#E0E0E0","#C0C0C0","#A0A0A0","#808080","#606060","#404040"]
                self.create_oval(2, 2, self.size-2, self.size-2,
                                 fill=alpha_colors[step % len(alpha_colors)],
                                 outline=alpha_colors[step % len(alpha_colors)])
                self.create_text(self.size//2, self.size//2,
                                 text=str(tmp), fill="#fff",
                                 font=("Apple SD Gothic Neo", 18, "bold"))
                self.after(delay, lambda: animate(step + 1))
            else:
                self.draw_number(n)
                if callback:
                    callback()
        animate(0)


class LottoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("로또 번호 추첨기")
        self.resizable(False, False)
        self.configure(bg=TOSS_BG)

        # 창 크기 & 중앙 정렬
        w, h = 420, 720
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.numbers    = []
        self.history    = []
        self.is_drawing = False

        self._build_ui()

    # ────────────────────────────────────────
    #  UI 구성
    # ────────────────────────────────────────
    def _build_ui(self):
        # ── 상단 헤더 ──
        header = tk.Frame(self, bg=TOSS_WHITE, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🍀  로또 번호 추첨기",
                 bg=TOSS_WHITE, fg=TOSS_BLACK,
                 font=("Apple SD Gothic Neo", 18, "bold")).pack(expand=True)

        # ── 구분선 ──
        tk.Frame(self, bg="#E8EAED", height=1).pack(fill="x")

        # ── 메인 스크롤 영역 ──
        main = tk.Frame(self, bg=TOSS_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ── 카드: 이번 회차 번호 ──
        card = tk.Frame(main, bg=TOSS_WHITE, bd=0, relief="flat")
        card.pack(fill="x", pady=(0, 16))
        self._add_shadow(card)

        tk.Label(card, text="이번 회차 번호",
                 bg=TOSS_WHITE, fg=TOSS_GRAY2,
                 font=("Apple SD Gothic Neo", 12)).pack(anchor="w", padx=20, pady=(20,6))

        # 번호 볼 6개
        ball_frame = tk.Frame(card, bg=TOSS_WHITE)
        ball_frame.pack(pady=(4, 20))
        self.balls = []
        for i in range(6):
            b = BallCanvas(ball_frame, size=54)
            b.pack(side="left", padx=5)
            self.balls.append(b)

        # ── 금액 표시 ──
        self.prize_label = tk.Label(card, text="행운을 기원합니다! 🎰",
                                    bg=TOSS_WHITE, fg=TOSS_GRAY3,
                                    font=("Apple SD Gothic Neo", 13, "bold"))
        self.prize_label.pack(pady=(0, 24))

        # ── 추첨 버튼 ──
        self.draw_btn = RoundedButton(main, text="🎲  번호 추첨하기",
                                      command=self._start_draw,
                                      width=380, height=56,
                                      bg=TOSS_BLUE, fg="#fff", radius=16)
        self.draw_btn.pack(pady=(0, 12))

        # ── 초기화 버튼 ──
        RoundedButton(main, text="↺  다시 추첨",
                      command=self._reset,
                      width=380, height=48,
                      bg=TOSS_GRAY1, fg=TOSS_GRAY3,
                      radius=14, font_size=14).pack(pady=(0, 20))

        # ── 카드: 추첨 히스토리 ──
        hist_card = tk.Frame(main, bg=TOSS_WHITE)
        hist_card.pack(fill="x")
        self._add_shadow(hist_card)

        tk.Label(hist_card, text="추첨 기록",
                 bg=TOSS_WHITE, fg=TOSS_GRAY2,
                 font=("Apple SD Gothic Neo", 12)).pack(anchor="w", padx=20, pady=(16, 8))

        tk.Frame(hist_card, bg="#F2F4F6", height=1).pack(fill="x", padx=20)

        self.hist_frame = tk.Frame(hist_card, bg=TOSS_WHITE)
        self.hist_frame.pack(fill="x", padx=20, pady=(0, 16))

        self._show_empty_history()

    def _add_shadow(self, frame):
        """카드 외곽선 효과"""
        frame.configure(
            highlightbackground="#E8EAED",
            highlightthickness=1,
            bd=0
        )
        # 내부 패딩은 각 요소에서 처리

    def _show_empty_history(self):
        tk.Label(self.hist_frame,
                 text="아직 추첨 기록이 없어요.",
                 bg=TOSS_WHITE, fg=TOSS_GRAY2,
                 font=("Apple SD Gothic Neo", 12)).pack(pady=20)

    # ────────────────────────────────────────
    #  추첨 로직
    # ────────────────────────────────────────
    def _start_draw(self):
        if self.is_drawing:
            return
        self.is_drawing = True
        self.draw_btn.set_state("disabled")

        # 볼 초기화
        for b in self.balls:
            b.draw_empty()

        self.prize_label.config(text="추첨 중... 🎯", fg=TOSS_BLUE)

        nums = sorted(random.sample(range(1, 46), 6))
        self.numbers = nums

        def reveal_sequence(idx=0):
            if idx < 6:
                self.balls[idx].flash(nums[idx],
                    callback=lambda: self.after(120, lambda: reveal_sequence(idx+1)))
            else:
                self._on_draw_complete(nums)

        self.after(200, lambda: reveal_sequence(0))

    def _on_draw_complete(self, nums):
        self.is_drawing = False
        self.draw_btn.set_state("normal")

        # 당첨금 표시 (재미용)
        prizes = ["1등 도전! 🏆", "2등 도전! 🥈", "3등 도전! 🥉",
                  "행운이 가득! 🍀", "이번엔 꼭! 🎯", "대박 예감! 💰"]
        self.prize_label.config(text=random.choice(prizes), fg=TOSS_BLUE)

        # 히스토리 추가
        self.history.insert(0, nums[:])
        if len(self.history) > 5:
            self.history.pop()
        self._update_history()

    def _reset(self):
        if self.is_drawing:
            return
        self.numbers = []
        for b in self.balls:
            b.draw_empty()
        self.prize_label.config(text="행운을 기원합니다! 🎰", fg=TOSS_GRAY3)

    def _update_history(self):
        for w in self.hist_frame.winfo_children():
            w.destroy()

        for i, nums in enumerate(self.history):
            row = tk.Frame(self.hist_frame, bg=TOSS_WHITE)
            row.pack(fill="x", pady=6)

            # 회차 번호
            tk.Label(row,
                     text=f"#{len(self.history)-i}회",
                     bg=TOSS_WHITE, fg=TOSS_GRAY2,
                     font=("Apple SD Gothic Neo", 11),
                     width=4, anchor="w").pack(side="left")

            # 미니 볼들
            for n in nums:
                mini = tk.Canvas(row, width=34, height=34,
                                 bg=TOSS_WHITE, highlightthickness=0)
                mini.pack(side="left", padx=2)
                bg, fg = ball_color(n)
                mini.create_oval(2, 2, 32, 32, fill=bg, outline=bg)
                mini.create_text(17, 17, text=str(n), fill=fg,
                                 font=("Apple SD Gothic Neo", 11, "bold"))

            if i < len(self.history) - 1:
                tk.Frame(self.hist_frame, bg="#F2F4F6", height=1).pack(fill="x")


if __name__ == "__main__":
    app = LottoApp()
    app.mainloop()
