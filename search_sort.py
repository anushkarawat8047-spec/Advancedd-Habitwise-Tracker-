import tkinter as tk
from tkinter import ttk

from config import *
from data import habits, completion_percent
from helpers import clear_content, page_header, make_button


def show(frame):
    clear_content(frame)

    page_header(
        frame,
        "Search & Sort",
        "Frontend screen for backend data search and sorting."
    )

    top = tk.Frame(frame, bg=BG)
    top.pack(fill="x", padx=32, pady=(0, 12))

    search = tk.Entry(
        top,
        width=30,
        font=("Segoe UI", 10),
        relief="flat",
        bg=WHITE
    )
    search.pack(side="left", ipady=9, padx=(0, 8))

    table = tk.Frame(
        frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table.pack(fill="both", expand=True, padx=32, pady=5)

    columns = (
        "Habit",
        "Category",
        "Target",
        "Completed",
        "Performance"
    )

    tree = ttk.Treeview(
        table,
        columns=columns,
        show="headings"
    )

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)

    tree.pack(fill="both", expand=True, padx=12, pady=12)

    def display(data):
        for item in tree.get_children():
            tree.delete(item)

        for h in data:
            tree.insert("", "end", values=(
                h.get("name", ""),
                h.get("category", ""),
                h.get("target", ""),
                h.get("done", ""),
                f'{completion_percent(h):.0f}%'
            ))

    def do_search():
        query = search.get().lower()
        result = []

        # Frontend demonstration only.
        # Backend can replace this with its own search response.
        for h in habits:
            if query in h.get("name", "").lower():
                result.append(h)

        display(result)

    def do_sort():
        data = habits.copy()

        # Frontend demonstration only.
        data.sort(
            key=lambda h: completion_percent(h),
            reverse=True
        )

        display(data)

    make_button(
        top,
        "🔍 Search",
        do_search
    ).pack(side="left", padx=4)

    make_button(
        top,
        "↕ Sort",
        do_sort,
        PURPLE
    ).pack(side="left", padx=4)

    if not habits:
        tk.Label(
            table,
            text="No data loaded from the backend.",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=MUTED
        ).place(relx=0.5, rely=0.5, anchor="center")
    else:
        display(habits)
