import tkinter as tk
from tkinter import ttk, messagebox

from config import BG, NAVY, NAVY_LIGHT, WHITE, RED
from helpers import make_button

import dashboard
import habit_management
import daily_tracker
import insights
import achievements
import search_sort
import stack_queue


root = tk.Tk()
root.title("HabitWise - Smart Habit Tracker")
root.geometry("1250x760")
root.minsize(1050, 680)
root.configure(bg=BG)


# ==========================================================
# SIDEBAR
# ==========================================================

sidebar = tk.Frame(
    root,
    bg=NAVY,
    width=235
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ==========================================================
# MAIN
# ==========================================================

main = tk.Frame(root, bg=BG)
main.pack(side="right", fill="both", expand=True)


topbar = tk.Frame(
    main,
    bg=WHITE,
    height=65
)

topbar.pack(fill="x")
topbar.pack_propagate(False)


tk.Label(
    topbar,
    text="Your personal space for better habits",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg="#7B8794"
).pack(side="left", padx=32)

tk.Label(
    topbar,
    text="🔔",
    font=("Segoe UI", 16),
    bg=WHITE
).pack(side="right", padx=18)

tk.Label(
    topbar,
    text="👤",
    font=("Segoe UI", 16),
    bg=WHITE
).pack(side="right", padx=4)


content = tk.Frame(
    main,
    bg=BG
)

content.pack(
    fill="both",
    expand=True
)


# ==========================================================
# SIDEBAR TITLE
# ==========================================================

tk.Label(
    sidebar,
    text="HabitWise",
    font=("Segoe UI", 25, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(30, 2))

tk.Label(
    sidebar,
    text="SMART HABIT TRACKER",
    font=("Segoe UI", 8, "bold"),
    bg=NAVY,
    fg="#C9D6E2"
).pack(pady=(0, 25))


nav_buttons = []


def set_active(active):
    for b in nav_buttons:
        b.config(
            bg=NAVY_LIGHT if b == active else NAVY
        )


def nav(text, command):

    def run():
        set_active(btn)
        command()

    btn = tk.Button(
        sidebar,
        text=text,
        command=run,
        bg=NAVY,
        fg=WHITE,
        activebackground=NAVY_LIGHT,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=20,
        pady=12,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )

    btn.pack(
        fill="x",
        padx=12,
        pady=3
    )

    nav_buttons.append(btn)


def open_add_habit():
    habit_management.add_habit_window(
        root,
        lambda: dashboard.show(content, open_add_habit)
    )


nav("🏠   Dashboard",
    lambda: dashboard.show(content, open_add_habit))

nav("✓    My Habits",
    lambda: habit_management.show(content, root))

nav("📅   Daily Tracker",
    lambda: daily_tracker.show(content))

nav("📊   Insights",
    lambda: insights.show(content))

nav("🏆   Achievements",
    lambda: achievements.show(content))

nav("🔍   Search & Sort",
    lambda: search_sort.show(content))

nav("📚   Stack",
    lambda: stack_queue.stack_show(content))

nav("🚶   Queue",
    lambda: stack_queue.queue_show(content))


tk.Frame(
    sidebar,
    bg=NAVY
).pack(expand=True)


make_button(
    sidebar,
    "⚙  Settings",
    lambda: messagebox.showinfo(
        "Settings",
        "Settings will be connected by the backend/application integration."
    ),
    NAVY_LIGHT
).pack(fill="x", padx=12, pady=5)


make_button(
    sidebar,
    "Exit",
    root.destroy,
    RED
).pack(fill="x", padx=12, pady=(5, 20))


# ==========================================================
# TABLE STYLE
# ==========================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Treeview",
    background=WHITE,
    fieldbackground=WHITE,
    foreground="#243B53",
    rowheight=38,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    background="#F6E9EE",
    foreground="#243B53",
    font=("Segoe UI", 9, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#FFE5ED")],
    foreground=[("selected", "#243B53")]
)


# ==========================================================
# START
# ==========================================================

dashboard.show(
    content,
    open_add_habit
)

if nav_buttons:
    set_active(nav_buttons[0])

root.mainloop()
