import tkinter as tk
from config import *


def clear_content(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def page_header(frame, title, subtitle):
    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 25, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", padx=32, pady=(25, 2))

    tk.Label(
        frame,
        text=subtitle,
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED
    ).pack(anchor="w", padx=32, pady=(0, 22))


def make_button(parent, text, command, bg=PINK, fg=WHITE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=PINK_DARK if bg == PINK else bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2",
        padx=16,
        pady=9
    )


def add_stat_card(parent, icon, value, title, color):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=5, ipady=8)

    tk.Label(card, text=icon, font=("Segoe UI", 20),
             bg=WHITE, fg=color).pack(anchor="w", padx=18, pady=(10, 0))

    tk.Label(card, text=value, font=("Segoe UI", 20, "bold"),
             bg=WHITE, fg=TEXT).pack(anchor="w", padx=18)

    tk.Label(card, text=title, font=("Segoe UI", 9),
             bg=WHITE, fg=MUTED).pack(anchor="w", padx=18, pady=(0, 10))


def empty_state(parent, text="No data available yet."):
    box = tk.Frame(parent, bg=WHITE,
                   highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="both", expand=True, padx=32, pady=10)

    tk.Label(
        box,
        text="○",
        font=("Segoe UI", 30),
        bg=WHITE,
        fg=MUTED
    ).pack(pady=(70, 5))

    tk.Label(
        box,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()

    return box
