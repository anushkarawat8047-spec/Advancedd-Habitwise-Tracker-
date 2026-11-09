# ============================================================
# main.py
# HabitWise - Smart Habit Tracker
# GUI redesigned to match the reference screenshot
# ============================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ---------------- BACKEND ----------------
from habit_management import add_habit, get_habits, delete_habit
from daily_tracker import save_record, get_records
from dashboard import calculate_dashboard
from insights import get_performance_message
from achievements import get_achievement
from stack_queue import HabitStack, HabitQueue


# ============================================================
# COLORS / FONTS
# ============================================================

# ============================================================
# PREMIUM HABITWISE THEME
# ============================================================

SIDEBAR = "#29264F"
SIDEBAR_DARK = "#1D1B3D"
SIDEBAR_ACTIVE = "#806ED5"
SIDEBAR_HOVER = "#403B70"

BG = "#F5F3FB"
WHITE = "#FFFFFF"
TEXT = "#292743"
MUTED = "#77748D"
BORDER = "#E8E3F1"

RED = "#F06B8A"
PURPLE = "#806ED5"
ORANGE = "#F0A85A"
GREEN = "#43B88C"
BLUE = "#5A9CE6"

FONT = "Segoe UI"

# ============================================================
# DSA OBJECTS
# ============================================================

recent_stack = HabitStack()
pending_queue = HabitQueue()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("HabitWise - Smart Habit Tracker")
root.geometry("1240x800")
root.minsize(900, 600)
root.configure(bg=BG)

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clear_entry(entry):
    entry.delete(0, tk.END)


def make_flat_button(parent, text, command, bg=RED, fg=WHITE,
                     width=16, font_size=10):

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, font_size, "bold"),
        width=width,
        pady=9
    )

    def hover_in(event):
        btn.configure(
            relief="flat",
            highlightthickness=1,
            highlightbackground=bg
        )

    def hover_out(event):
        btn.configure(
            relief="flat",
            highlightthickness=0
        )

    btn.bind("<Enter>", hover_in)
    btn.bind("<Leave>", hover_out)

    return btn

def premium_popup(title, message, popup_type="success"):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("390x260")
    popup.resizable(False, False)
    popup.configure(bg="#F1ECFF")
    popup.transient(root)
    popup.grab_set()

    popup.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() - 390) // 2
    y = root.winfo_rooty() + (root.winfo_height() - 260) // 2
    popup.geometry(f"+{x}+{y}")

    styles = {
        "success": ("✓", GREEN, "#E5F7EF"),
        "error": ("✕", RED, "#FFE8ED"),
        "warning": ("!", ORANGE, "#FFF2DF")
    }

    icon, color, icon_bg = styles.get(
        popup_type, styles["success"]
    )

    card = tk.Frame(
        popup,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    card.pack(fill="both", expand=True, padx=12, pady=12)

    tk.Label(
        card,
        text=icon,
        font=(FONT, 25, "bold"),
        bg=icon_bg,
        fg=color,
        width=3,
        height=1
    ).pack(pady=(22, 10))

    tk.Label(
        card,
        text=title,
        font=(FONT, 17, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(0, 8))

    tk.Label(
        card,
        text=message,
        font=(FONT, 10),
        bg=WHITE,
        fg=MUTED,
        wraplength=320,
        justify="center"
    ).pack(padx=20, pady=(0, 15))

    make_flat_button(
        card,
        "Okay",
        popup.destroy,
        bg=color,
        width=12
    ).pack(pady=(0, 18))



# ============================================================
# LEFT SIDEBAR
# ============================================================

sidebar = tk.Frame(root, bg=SIDEBAR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


# Logo
logo_frame = tk.Frame(sidebar, bg=SIDEBAR)
logo_frame.pack(fill="x", padx=20, pady=(25, 18))

tk.Label(
    logo_frame,
    text="HabitWise",
    font=(FONT, 22, "bold"),
    bg=SIDEBAR,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    logo_frame,
    text="SMART HABIT TRACKER",
    font=(FONT, 7, "bold"),
    bg=SIDEBAR,
    fg="#BBD2E7"
).pack(anchor="w", pady=(2, 0))


# Sidebar menu
menu_buttons = {}
page_title = tk.StringVar(value="Dashboard")


def set_active(name):
    for key, btn in menu_buttons.items():
        if key == name:
            btn.configure(bg=SIDEBAR_ACTIVE, fg=WHITE)
        else:
            btn.configure(bg=SIDEBAR, fg="#D7E2EC")


def menu_button(name, icon, command):
    btn = tk.Button(
        sidebar,
        text=f"   {icon}   {name}",
        command=command,
        anchor="w",
        bg=SIDEBAR,
        fg="#D7E2EC",
        activebackground=SIDEBAR_HOVER,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=10,
        pady=10
    )
    btn.pack(fill="x", padx=12, pady=2)
    menu_buttons[name] = btn
    return btn


# ============================================================
# RIGHT AREA
# ============================================================

right = tk.Frame(root, bg=BG)
right.pack(side="right", fill="both", expand=True)


# Top bar
topbar = tk.Frame(
    right,
    bg=WHITE,
    height=65,
    highlightbackground=BORDER,
    highlightthickness=1
)
topbar.pack(fill="x")
topbar.pack_propagate(False)

tk.Label(
    topbar,
    text="Your personal space for better habits.",
    font=(FONT, 9),
    bg=WHITE,
    fg=MUTED
).pack(side="left", padx=25)

top_right = tk.Frame(topbar, bg=WHITE)
top_right.pack(side="right", padx=22)

tk.Label(
    top_right,
    text="♙",
    font=(FONT, 18),
    bg=WHITE,
    fg=TEXT
).pack(side="left", padx=8)

tk.Label(
    top_right,
    text="♧",
    font=(FONT, 17),
    bg=WHITE,
    fg=MUTED
).pack(side="left")


# ============================================================
# CONTENT CONTAINER
# ============================================================

# ============================================================
# SCROLLABLE CONTENT AREA
# ============================================================

content_shell = tk.Frame(right, bg=BG)
content_shell.pack(fill="both", expand=True)

content_canvas = tk.Canvas(
    content_shell,
    bg=BG,
    highlightthickness=0
)

content_scrollbar = tk.Scrollbar(
    content_shell,
    orient="vertical",
    command=content_canvas.yview,
    width=12,
    bg="#DCD5EF",
    troughcolor=BG,
    activebackground=PURPLE,
    relief="flat"
)

content_canvas.configure(
    yscrollcommand=content_scrollbar.set
)

content_scrollbar.pack(side="right", fill="y")
content_canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(content_canvas, bg=BG)

content_window = content_canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)

def update_scroll_region(event=None):
    content_canvas.configure(
        scrollregion=content_canvas.bbox("all")
    )

def resize_content(event):
    content_canvas.itemconfigure(
        content_window,
        width=event.width
    )

content.bind("<Configure>", update_scroll_region)
content_canvas.bind("<Configure>", resize_content)


# Mouse-wheel scrolling (Windows)
def mousewheel_scroll(event):
    content_canvas.yview_scroll(
        int(-event.delta / 120),
        "units"
    )

def enable_scroll(event=None):
    content_canvas.bind_all(
        "<MouseWheel>",
        mousewheel_scroll
    )

def disable_scroll(event=None):
    content_canvas.unbind_all("<MouseWheel>")

content_canvas.bind("<Enter>", enable_scroll)
content_canvas.bind("<Leave>", disable_scroll)
# We use separate pages, like the reference dashboard.
pages = {}


def create_page(name):
    frame = tk.Frame(content, bg=BG)
    pages[name] = frame
    return frame


dashboard_page = create_page("Dashboard")
habits_page = create_page("My Habits")
tracker_page = create_page("Daily Tracker")
insights_page = create_page("Insights")
achievement_page = create_page("Achievements")
search_page = create_page("Search & Sort")
stack_page = create_page("Stack")
queue_page = create_page("Queue")
settings_page = create_page("Settings")


def show_page(name):
    for frame in pages.values():
        frame.pack_forget()

    pages[name].pack(fill="both", expand=True)

    page_title.set(name)
    set_active(name)

    content_canvas.yview_moveto(0)
    content_canvas.configure(
        scrollregion=content_canvas.bbox("all")
    )


# ============================================================
# DASHBOARD PAGE
# ============================================================

dash = dashboard_page

# Header
dash_header = tk.Frame(dash, bg=BG)
dash_header.pack(fill="x", padx=28, pady=(28, 8))

left_header = tk.Frame(dash_header, bg=BG)
left_header.pack(side="left")

tk.Label(
    left_header,
    text="Good Evening!  ♡",
    font=(FONT, 25, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

date_label = tk.Label(
    left_header,
    text=datetime.now().strftime("%d %b, %A"),
    font=(FONT, 9),
    bg=BG,
    fg=MUTED
)
date_label.pack(anchor="w", pady=(3, 0))

make_flat_button(
    dash_header,
    "+  Add Habit",
    lambda: show_page("My Habits"),
    bg=RED,
    width=13
).pack(side="right", pady=8)

# ============================================================
# PREMIUM WELCOME BANNER
# ============================================================

hero = tk.Canvas(
    dash,
    height=135,
    bg="#51458D",
    highlightthickness=0
)

hero.pack(fill="x", padx=28, pady=(8, 12))

hero.create_rectangle(
    0, 0, 1500, 135,
    fill="#51458D",
    outline=""
)

# Decorative circles
hero.create_oval(
    700, -80, 900, 120,
    fill="#6659A7",
    outline=""
)

hero.create_oval(
    850, 40, 1010, 200,
    fill="#7568B8",
    outline=""
)

hero.create_oval(
    970, -45, 1090, 75,
    fill="#F18BA4",
    outline=""
)

hero.create_oval(
    1080, 60, 1170, 150,
    fill="#F2B46B",
    outline=""
)

# Banner text
hero.create_text(
    25, 32,
    text="YOUR JOURNEY STARTS HERE",
    anchor="w",
    font=(FONT, 9, "bold"),
    fill="#E7E0FF"
)

hero.create_text(
    25, 66,
    text="Build a better you,",
    anchor="w",
    font=(FONT, 22, "bold"),
    fill=WHITE
)

hero.create_text(
    25, 96,
    text="one habit at a time. ✨",
    anchor="w",
    font=(FONT, 17, "bold"),
    fill="#FFE2EC"
)

hero.create_text(
    25, 120,
    text="Stay consistent  •  Keep growing  •  Celebrate yourself",
    anchor="w",
    font=(FONT, 8),
    fill="#E7E0FF"
)

hero.create_text(
    880, 65,
    text="✦",
    font=(FONT, 48, "bold"),
    fill="#FFF0B8"
)

hero.create_text(
    1040, 95,
    text="♥",
    font=(FONT, 35, "bold"),
    fill="#FFE3EB"
)
# Stats
stats = tk.Frame(dash, bg=BG)
stats.pack(fill="x", padx=28, pady=12)

for i in range(4):
    stats.grid_columnconfigure(i, weight=1)


def stat_card(column, icon, title, value, color):
    c = tk.Frame(
        stats,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    c.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=7,
        pady=5
    )

    tk.Frame(
        c,
        bg=color,
        height=5
    ).pack(fill="x")

    tk.Label(
        c,
        text=icon,
        font=(FONT, 17),
        bg=WHITE,
        fg=color
    ).pack(anchor="w", padx=17, pady=(14, 3))

    value_lbl = tk.Label(
        c,
        text=value,
        font=(FONT, 18, "bold"),
        bg=WHITE,
        fg=TEXT
    )
    value_lbl.pack(anchor="w", padx=17)

    tk.Label(
        c,
        text=title,
        font=(FONT, 8),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", padx=17, pady=(1, 14))

    return value_lbl
completed_stat = stat_card(0, "♨", "COMPLETED TODAY", "0", RED)
consistency_stat = stat_card(1, "✓", "CONSISTENCY", "0%", PURPLE)
streak_stat = stat_card(2, "◉", "CURRENT STREAK", "0", BLUE)
achievement_stat = stat_card(3, "★", "ACHIEVEMENTS", "0", ORANGE)


# Today's habits heading
today_heading = tk.Frame(dash, bg=BG)
today_heading.pack(fill="x", padx=28, pady=(18, 5))

tk.Label(
    today_heading,
    text="Today's Habits",
    font=(FONT, 15, "bold"),
    bg=BG,
    fg=TEXT
).pack(side="left")

tk.Label(
    today_heading,
    text="Track your progress for today",
    font=(FONT, 9),
    bg=BG,
    fg=MUTED
).pack(side="left", padx=12)


# Today's habits area

## Today's habits area
today_card = tk.Frame(
    dash,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
today_card.pack(
    fill="both",
    expand=True,
    padx=28,
    pady=(5, 15)
)

today_inner = tk.Frame(today_card, bg=WHITE)
today_inner.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

today_message = tk.Label(
    today_inner,
    text="✦  Your journey starts here!",
    font=(FONT, 13, "bold"),
    bg=WHITE,
    fg=PURPLE
)
today_message.pack(pady=(55, 8))

today_submessage = tk.Label(
    today_inner,
    text="Add your first habit and start building a better routine.",
    font=(FONT, 9),
    bg=WHITE,
    fg=MUTED
)
today_submessage.pack()



today_inner.pack(fill="both", expand=True, padx=20, pady=15)

today_message = tk.Label(
    today_inner,
    text="✦  Your journey starts here!",
    font=(FONT, 13, "bold"),
    bg=WHITE,
    fg=PURPLE
)
today_message.pack(pady=(55, 8))

today_submessage = tk.Label(
    today_inner,
    text="Add your first habit and start building a better routine.",
    font=(FONT, 9),
    bg=WHITE,
    fg=MUTED
)
today_submessage.pack()


def refresh_dashboard():
    try:
        habits = get_habits()
    except Exception:
        habits = []

    try:
        records = get_records()
    except Exception:
        records = []

    # Basic statistics
    completed = 0
    score = 0

    if records:
        try:
            total, completed, score = calculate_dashboard(records)
        except Exception:
            total = len(records)
            completed = 0
            score = 0

    completed_stat.config(text=str(completed))
    consistency_stat.config(text=f"{score:.0f}%")

    # A simple current streak based on consecutive completed records
    streak = 0
    try:
        for record in reversed(records):
            if isinstance(record, dict):
                value = record.get("completed", record.get("status", 0))
                if value in (1, True, "1", "Completed", "completed"):
                    streak += 1
                else:
                    break
            else:
                break
    except Exception:
        streak = 0

    streak_stat.config(text=str(streak))

    # Achievement count
    achievement_stat.config(text="0" if not records else "1")

    # Today's habit list
        # Today's habit list
    for widget in today_inner.winfo_children():
        if widget not in (today_message, today_submessage):
            widget.destroy()

    if not habits:
        today_message.pack(pady=(55, 8))
        today_submessage.pack()
        draw_progress_graph()
        return

        today_message.pack_forget()
    today_submessage.pack_forget()

    for index, habit in enumerate(habits):
        row = tk.Frame(
            today_inner,
            bg="#F7F5FF",
            highlightthickness=1,
            highlightbackground="#ECE6FA"
        )
        row.pack(fill="x", pady=6, ipady=3)

        tk.Label(
            row,
            text=f"  {habit['name']}",
            font=(FONT, 10, "bold"),
            bg="#FAFBFD",
            fg=TEXT,
            anchor="w"
        ).pack(side="left", fill="x", expand=True, padx=8, pady=10)

        tk.Label(
            row,
            text=f"Target: {habit['target']:g} {habit.get('unit', '')}".strip(),
            font=(FONT, 9),
            bg="#FAFBFD",
            fg=MUTED
        ).pack(side="left", padx=15)

        make_flat_button(
            row,
            "Track",
            lambda h=habit: track_selected_habit(h),
            bg=GREEN,
            width=8,
            font_size=9
        ).pack(side="right", padx=10)

    draw_progress_graph()



# ============================================================
# PROGRESS GRAPH
# ============================================================

graph_heading = tk.Frame(dash, bg=BG)
graph_heading.pack(fill="x", padx=28, pady=(5, 5))

tk.Label(
    graph_heading,
    text="Progress Graph",
    font=(FONT, 15, "bold"),
    bg=BG,
    fg=TEXT
).pack(side="left")

tk.Label(
    graph_heading,
    text="Your daily habit progress",
    font=(FONT, 9),
    bg=BG,
    fg=MUTED
).pack(side="left", padx=12)


graph_card = tk.Frame(
    dash,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)

graph_card.pack(
    fill="x",
    padx=28,
    pady=(5, 20)
)
graph_canvas = tk.Canvas(
    graph_card,
    height=230,
    bg=WHITE,
    highlightthickness=0
)
graph_canvas.pack(fill="x", padx=15, pady=15)


def get_record_value(record):
    """Safely get the numeric progress value from a backend record."""
    if not isinstance(record, dict):
        return None

    for key in ("value", "completed_value", "progress", "amount"):
        if key in record:
            try:
                return float(record[key])
            except (TypeError, ValueError):
                pass

    return None


def get_record_label(record, index):
    """Safely get a short date/label from a backend record."""
    if isinstance(record, dict):
        for key in ("date", "record_date", "created_at", "day"):
            if key in record and record[key]:
                text = str(record[key])
                # Keep only a short readable label.
                return text[:10]

    return f"Day {index}"


def draw_progress_graph():
    graph_canvas.delete("all")

    try:
        records = get_records()
    except Exception:
        records = []

    points = []

    for i, record in enumerate(records, start=1):
        value = get_record_value(record)
        if value is not None:
            points.append(
                (get_record_label(record, i), value)
            )

    # Show an empty-state message
    if not points:
        graph_canvas.create_text(
            500, 105,
            text="No progress data available yet.\nSave daily records to see your graph.",
            font=(FONT, 11, "bold"),
            fill=MUTED,
            justify="center"
        )
        return

    # Display the most recent 7 records.
    points = points[-7:]

    width = max(graph_canvas.winfo_width(), 700)
    height = 230

    left = 55
    right = 25
    top = 25
    bottom = 45

    plot_width = width - left - right
    plot_height = height - top - bottom

    max_value = max(v for _, v in points)
    if max_value <= 0:
        max_value = 1

    # Grid + Y-axis labels
    for i in range(5):
        ratio = i / 4
        y = top + plot_height * ratio
        value = max_value * (1 - ratio)

        graph_canvas.create_line(
            left, y,
            width - right, y,
            fill="#EEF1F5"
        )

        graph_canvas.create_text(
            left - 10,
            y,
            text=f"{value:.0f}",
            font=(FONT, 8),
            fill=MUTED,
            anchor="e"
        )

    # X positions
    count = len(points)
    step = plot_width / max(count - 1, 1)

    coords = []

    for i, (label, value) in enumerate(points):
        x = left + (i * step if count > 1 else plot_width / 2)
        y = top + plot_height - (value / max_value) * plot_height
        coords.append((x, y))

        graph_canvas.create_text(
            x,
            height - 20,
            text=label,
            font=(FONT, 8),
            fill=MUTED
        )

    # Draw line
    if len(coords) > 1:
        for i in range(len(coords) - 1):
            graph_canvas.create_line(
                coords[i][0],
                coords[i][1],
                coords[i + 1][0],
                coords[i + 1][1],
                fill=PURPLE,
                width=3,
                smooth=True
            )

    # Draw points + values
    for (x, y), (_, value) in zip(coords, points):
        graph_canvas.create_oval(
            x - 5, y - 5,
            x + 5, y + 5,
            fill=PURPLE,
            outline=WHITE,
            width=2
        )

        graph_canvas.create_text(
            x,
            y - 14,
            text=f"{value:g}",
            font=(FONT, 8, "bold"),
            fill=TEXT
        )


graph_canvas.bind("<Configure>", lambda event: draw_progress_graph())


# ============================================================
# MONTHLY TRACKING
# ============================================================

monthly_heading = tk.Frame(dash, bg=BG)
monthly_heading.pack(fill="x", padx=28, pady=(0, 5))

tk.Label(
    monthly_heading,
    text="Monthly Tracking",
    font=(FONT, 15, "bold"),
    bg=BG,
    fg=TEXT
).pack(side="left")

tk.Label(
    monthly_heading,
    text="Review your habit progress month by month",
    font=(FONT, 9),
    bg=BG,
    fg=MUTED
).pack(side="left", padx=12)

monthly_card = tk.Frame(
    dash,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)

monthly_card.pack(
    fill="x",
    padx=28,
    pady=(5, 20)
)

monthly_top = tk.Frame(monthly_card, bg=WHITE)
monthly_top.pack(fill="x", padx=20, pady=(15, 5))

tk.Label(
    monthly_top,
    text="Select Month:",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(side="left")

month_var = tk.StringVar()

month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Last 12 months, newest first
now = datetime.now()
month_options = []
for offset in range(12):
    month_number = now.month - offset
    year = now.year

    while month_number <= 0:
        month_number += 12
        year -= 1

    month_options.append(f"{month_names[month_number - 1]} {year}")

month_var.set(month_options[0])

month_menu = tk.OptionMenu(
    monthly_top,
    month_var,
    *month_options,
    command=lambda selected: draw_monthly_tracking()
)
month_menu.configure(
    bg="#F4F6FA",
    fg=TEXT,
    activebackground="#E9ECF3",
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    font=(FONT, 9),
    highlightthickness=0
)
month_menu["menu"].configure(
    font=(FONT, 9),
    bg=WHITE,
    fg=TEXT
)
month_menu.pack(side="left", padx=10)

monthly_stats = tk.Frame(monthly_card, bg=WHITE)
monthly_stats.pack(fill="x", padx=20, pady=8)

monthly_total_label = tk.Label(
    monthly_stats,
    text="Records: 0",
    font=(FONT, 10, "bold"),
    bg=WHITE,
    fg=TEXT
)
monthly_total_label.pack(side="left", padx=(0, 25))

monthly_completed_label = tk.Label(
    monthly_stats,
    text="Completed: 0",
    font=(FONT, 10, "bold"),
    bg=WHITE,
    fg=GREEN
)
monthly_completed_label.pack(side="left", padx=25)

monthly_score_label = tk.Label(
    monthly_stats,
    text="Monthly Consistency: 0%",
    font=(FONT, 10, "bold"),
    bg=WHITE,
    fg=PURPLE
)
monthly_score_label.pack(side="left", padx=25)

monthly_canvas = tk.Canvas(
    monthly_card,
    height=250,
    bg=WHITE,
    highlightthickness=0
)
monthly_canvas.pack(fill="x", padx=15, pady=(5, 18))


def parse_record_date(record):
    """Return a date object when the backend record contains a date."""
    if not isinstance(record, dict):
        return None

    for key in ("date", "record_date", "created_at", "day"):
        value = record.get(key)

        if not value:
            continue

        if isinstance(value, datetime):
            return value.date()

        text = str(value).strip()

        # Common formats used by Python/MySQL
        formats = (
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d"
        )

        for fmt in formats:
            try:
                return datetime.strptime(text[:19], fmt).date()
            except ValueError:
                continue

        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
        except (ValueError, TypeError):
            pass

    return None


def selected_year_month():
    text = month_var.get()
    parts = text.split()

    if len(parts) != 2:
        return now.year, now.month

    year = int(parts[1])
    month = month_names.index(parts[0]) + 1
    return year, month


def record_completed(record):
    if not isinstance(record, dict):
        return False

    value = record.get(
        "completed",
        record.get("status", record.get("is_completed", 0))
    )

    return value in (
        1, True, "1",
        "Completed", "completed",
        "Complete", "complete",
        "Yes", "yes"
    )


def draw_monthly_tracking():
    monthly_canvas.delete("all")

    try:
        records = get_records()
    except Exception:
        records = []

    year, month = selected_year_month()

    monthly_records = []

    for record in records:
        record_date = parse_record_date(record)

        if record_date and record_date.year == year and record_date.month == month:
            monthly_records.append(record)

    total = len(monthly_records)
    completed = sum(
        1 for record in monthly_records
        if record_completed(record)
    )

    score = (completed / total * 100) if total else 0

    monthly_total_label.config(text=f"Records: {total}")
    monthly_completed_label.config(text=f"Completed: {completed}")
    monthly_score_label.config(
        text=f"Monthly Consistency: {score:.0f}%"
    )

    if not monthly_records:
        monthly_canvas.create_text(
            500, 115,
            text=(
                f"No records found for {month_names[month - 1]} {year}.\n"
                "Save daily records to build your monthly history."
            ),
            font=(FONT, 11, "bold"),
            fill=MUTED,
            justify="center"
        )
        return

    # Aggregate completed records by day.
    daily_data = {}

    for record in monthly_records:
        record_date = parse_record_date(record)

        if record_date:
            day = record_date.day
            if day not in daily_data:
                daily_data[day] = [0, 0]

            daily_data[day][0] += 1

            if record_completed(record):
                daily_data[day][1] += 1

    # If dates exist, show a day-by-day monthly bar chart.
    if not daily_data:
        monthly_canvas.create_text(
            500, 115,
            text="Monthly data needs dated daily records.",
            font=(FONT, 11, "bold"),
            fill=MUTED
        )
        return

    days = sorted(daily_data.keys())

    width = max(monthly_canvas.winfo_width(), 700)
    height = 250

    left = 50
    right = 25
    top = 25
    bottom = 45

    plot_width = width - left - right
    plot_height = height - top - bottom

    max_day_value = max(
        max(values[0], values[1])
        for values in daily_data.values()
    )
    max_day_value = max(max_day_value, 1)

    # Horizontal grid
    for i in range(5):
        ratio = i / 4
        y = top + plot_height * ratio
        value = max_day_value * (1 - ratio)

        monthly_canvas.create_line(
            left, y,
            width - right, y,
            fill="#EEF1F5"
        )

        monthly_canvas.create_text(
            left - 8,
            y,
            text=f"{value:.0f}",
            font=(FONT, 8),
            fill=MUTED,
            anchor="e"
        )

    bar_width = max(6, min(22, plot_width / max(len(days) * 1.5, 1)))

    for i, day in enumerate(days):
        x = left + ((i + 0.5) / len(days)) * plot_width

        total_day = daily_data[day][0]
        completed_day = daily_data[day][1]

        total_height = (
            total_day / max_day_value
        ) * plot_height

        completed_height = (
            completed_day / max_day_value
        ) * plot_height

        base_y = top + plot_height

        # Total records bar
        monthly_canvas.create_rectangle(
            x - bar_width / 2,
            base_y - total_height,
            x + bar_width / 2,
            base_y,
            fill="#E8EBF2",
            outline=""
        )

        # Completed records bar
        monthly_canvas.create_rectangle(
            x - bar_width / 2,
            base_y - completed_height,
            x + bar_width / 2,
            base_y,
            fill=GREEN,
            outline=""
        )

        monthly_canvas.create_text(
            x,
            height - 20,
            text=str(day),
            font=(FONT, 8),
            fill=MUTED
        )

    # Legend
    monthly_canvas.create_rectangle(
        width - 180, 12, width - 168, 24,
        fill=GREEN, outline=""
    )
    monthly_canvas.create_text(
        width - 160, 18,
        text="Completed",
        anchor="w",
        font=(FONT, 8),
        fill=MUTED
    )

    monthly_canvas.create_rectangle(
        width - 90, 12, width - 78, 24,
        fill="#E8EBF2", outline=""
    )
    monthly_canvas.create_text(
        width - 70, 18,
        text="Total",
        anchor="w",
        font=(FONT, 8),
        fill=MUTED
    )


monthly_canvas.bind(
    "<Configure>",
    lambda event: draw_monthly_tracking()
)

# ============================================================
# TRACK SELECTED HABIT
# ============================================================


def track_selected_habit(habit):
    show_page("Daily Tracker")

    unit = habit.get("unit", "")

    selected_habit_label.config(
        text=f"Selected Habit: {habit['name']}"
    )

    daily_target_label.config(
        text=f"Daily Target: {habit['target']:g} {unit}".strip()
    )

    selected_habit_label.habit_data = habit


# ============================================================
# MY HABITS PAGE
# ============================================================

hp = habits_page

tk.Label(
    hp,
    text="My Habits",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

tk.Label(
    hp,
    text="Create and manage your daily habits.",
    font=(FONT, 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=30, pady=(0, 18))

habit_form = tk.Frame(
    hp,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
habit_form.pack(fill="x", padx=30, pady=5)

tk.Label(
    habit_form,
    text="Add a New Habit",
    font=(FONT, 14, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(row=0, column=0, columnspan=3, sticky="w", padx=22, pady=(20, 15))

tk.Label(
    habit_form,
    text="Habit Name",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(row=1, column=0, sticky="w", padx=22)

habit_name_entry = tk.Entry(
    habit_form,
    font=(FONT, 11),
    width=30,
    relief="solid",
    bd=1
)
habit_name_entry.grid(row=2, column=0, padx=22, pady=(5, 20), ipady=7)

tk.Label(
    habit_form,
    text="Daily Target",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).grid(row=1, column=1, sticky="w", padx=10)

habit_target_entry = tk.Entry(
    habit_form,
    font=(FONT, 11),
    width=18,
    relief="solid",
    bd=1
)
habit_target_entry.grid(row=2, column=1, padx=10, pady=(5, 20), ipady=7)



def add_habit_gui():
    name = habit_name_entry.get().strip()
    target_text = habit_target_entry.get().strip()

    if not name or not target_text:
        premium_popup(
            "Missing Information",
            "Please enter habit name and daily target.",
            "warning"
        )
        return

    try:
        parts = target_text.split(maxsplit=1)
        target = float(parts[0])
        unit = parts[1] if len(parts) > 1 else ""

    except ValueError:
        premium_popup(
            "Invalid Target",
            "Enter a target like 3 liters or 5000 steps.",
            "error"
        )
        return

    if target <= 0:
        premium_popup(
            "Invalid Target",
            "Target must be greater than 0.",
            "warning"
        )
        return

    try:
        add_habit(name, target, unit)
        pending_queue.enqueue(name)

        premium_popup(
            "Habit Added!",
            f"{name} has been added successfully!\nDaily Target: {target:g} {unit}".strip(),
            "success"
        )

        clear_entry(habit_name_entry)
        clear_entry(habit_target_entry)
        refresh_habit_list()
        refresh_dashboard()

    except Exception as e:
        premium_popup(
            "Something Went Wrong",
            str(e),
            "error"
        )




make_flat_button(
    habit_form,
    "Add Habit",
    add_habit_gui,
    bg=RED,
    width=14
).grid(row=2, column=2, padx=18, pady=(5, 20))


# Habit list
habit_list_card = tk.Frame(
    hp,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)

habit_list_card.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=12
)
tk.Label(
    habit_list_card,
    text="All Habits",
    font=(FONT, 14, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=22, pady=(18, 10))

habit_listbox = tk.Listbox(
    habit_list_card,
    font=(FONT, 10),
    bg="#FAFBFD",
    fg=TEXT,
    relief="flat",
    highlightthickness=0,
    selectbackground=SIDEBAR_ACTIVE
)
habit_listbox.pack(fill="both", expand=True, padx=22, pady=(0, 10))


def refresh_habit_list():
    habit_listbox.delete(0, tk.END)

    try:
        habits = get_habits()
    except Exception:
        habits = []

    if not habits:
        habit_listbox.insert(tk.END, "No habits added yet.")
        return

    for i, habit in enumerate(habits, 1):
        habit_listbox.insert(
            tk.END,
           f"{i}.  {habit['name']}     |     Target: {habit['target']:g} {habit.get('unit', '')}"
        )


def delete_selected_habit():
    selection = habit_listbox.curselection()

    if not selection:
        messagebox.showwarning(
            "Select Habit",
            "Please select a habit from the list."
        )
        return

    index = selection[0]

    try:
        habits = get_habits()
        if index >= len(habits):
            return

        name = habits[index]["name"]
        result = delete_habit(name)

        if result:
            messagebox.showinfo(
                "Deleted",
                f"'{name}' deleted successfully."
            )
            refresh_habit_list()
            refresh_dashboard()
        else:
            messagebox.showerror("Error", "Habit not found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


management_buttons = tk.Frame(habit_list_card, bg=WHITE)
management_buttons.pack(fill="x", padx=22, pady=(0, 18))

make_flat_button(
    management_buttons,
    "Refresh List",
    refresh_habit_list,
    bg=PURPLE,
    width=14
).pack(side="left", padx=(0, 10))

make_flat_button(
    management_buttons,
    "Delete Selected",
    delete_selected_habit,
    bg=RED,
    width=16
).pack(side="left")


# ============================================================
# DAILY TRACKER PAGE
# ============================================================

tp = tracker_page

tk.Label(
    tp,
    text="Daily Tracker",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

tk.Label(
    tp,
    text="Record today's progress for your latest habit.",
    font=(FONT, 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=30, pady=(0, 18))

tracker_card = tk.Frame(
    tp,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
tracker_card.pack(fill="x", padx=30, pady=5)

selected_habit_label = tk.Label(
    tracker_card,
    text="Selected Habit: Latest habit",
    font=(FONT, 12, "bold"),
    bg=WHITE,
    fg=TEXT
)
selected_habit_label.pack(anchor="w", padx=25, pady=(22, 8))

tk.Label(
    tracker_card,
    text="Today's Value",
    font=(FONT, 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", padx=25)

value_entry = tk.Entry(
    tracker_card,
    font=(FONT, 12),
    width=28,
    relief="solid",
    bd=1
)
value_entry.pack(anchor="w", padx=25, pady=(6, 10), ipady=8)
daily_target_label = tk.Label(
    tracker_card,
    text="Daily Target: --",
    font=(FONT, 10, "bold"),
    bg=WHITE,
    fg=GREEN
)
daily_target_label.pack(anchor="w", padx=25, pady=(0, 15))


def save_today():
    try:
        habits = get_habits()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    if not habits:
        messagebox.showwarning(
            "No Habit",
            "Please add a habit first."
        )
        return

    value_text = value_entry.get().strip()

    if not value_text:
        messagebox.showwarning(
            "Missing Value",
            "Please enter today's value."
        )
        return

    try:
        value = float(value_text)
    except ValueError:
        messagebox.showerror(
            "Invalid Value",
            "Today's value must be a number."
        )
        return

    if value < 0:
        messagebox.showerror(
            "Invalid Value",
            "Value cannot be negative."
        )
        return

    habit = getattr(selected_habit_label, "habit_data", habits[-1])

    try:
        completed = save_record(
            habit["name"],
            value,
            habit["target"]
        )

        recent_stack.push(habit["name"])

        if completed == 1:
            try:
                pending_queue.dequeue()
            except Exception:
                pass

            msg = "Habit completed successfully! 🎉"
        else:
            msg = "Record saved. Keep working toward your target!"

        messagebox.showinfo("Record Saved", msg)
        clear_entry(value_entry)
        refresh_dashboard()

    except Exception as e:
        messagebox.showerror("Error", str(e))


make_flat_button(
    tracker_card,
    "Save Today's Record",
    save_today,
    bg=GREEN,
    width=20
).pack(anchor="w", padx=25, pady=(5, 25))


# ============================================================
# INSIGHTS PAGE
# ============================================================

ip = insights_page

tk.Label(
    ip,
    text="Insights",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

insight_card = tk.Frame(
    ip,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
insight_card.pack(fill="x", padx=30, pady=20)

insight_result = tk.Label(
    insight_card,
    text="Click the button to view your performance.",
    font=(FONT, 12),
    bg=WHITE,
    fg=MUTED,
    justify="left",
    anchor="w"
)
insight_result.pack(fill="x", padx=25, pady=25)


def show_insights():
    try:
        records = get_records()
        total, completed, score = calculate_dashboard(records)

        if total == 0:
            insight_result.config(text="No records available yet.")
            return

        performance = get_performance_message(score)
        insight_result.config(
            text=(
                f"Performance: {performance}\n\n"
                f"Total records: {total}\n"
                f"Completed records: {completed}\n"
                f"Consistency: {score:.2f}%"
            ),
            fg=TEXT
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


make_flat_button(
    ip,
    "View My Insights",
    show_insights,
    bg=PURPLE,
    width=18
).pack(anchor="w", padx=30)


# ============================================================
# ACHIEVEMENTS PAGE
# ============================================================


# ================= ACHIEVEMENTS DASHBOARD =================

ap = pages["Achievements"]

# Heading
tk.Label(
    ap,
    text="Your Achievements 🏆",
    font=(FONT, 22, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(15, 5))

tk.Label(
    ap,
    text="Celebrate every small step towards a better you.",
    font=(FONT, 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=30, pady=(0, 18))


# Monthly goal card
goal_card = tk.Frame(
    ap, bg="#29264F",
    highlightthickness=0
)
goal_card.pack(fill="x", padx=30, pady=10)

tk.Label(
    goal_card,
    text="YOUR MONTHLY GROWTH GOAL ✨",
    font=(FONT, 10, "bold"),
    bg="#29264F",
    fg="#E8DFFF"
).pack(anchor="w", padx=22, pady=(18, 5))

goal_value = tk.Label(
    goal_card,
    text="0 / 20 days",
    font=(FONT, 25, "bold"),
    bg="#29264F",
    fg=WHITE
)
goal_value.pack(anchor="w", padx=22)

goal_percent = tk.Label(
    goal_card,
    text="0% completed",
    font=(FONT, 10),
    bg="#29264F",
    fg="#E8DFFF"
)
goal_percent.pack(anchor="w", padx=22, pady=(2, 10))

goal_bar = tk.Canvas(
    goal_card,
    height=12,
    bg="#514B76",
    highlightthickness=0
)
goal_bar.pack(fill="x", padx=22, pady=(0, 20))


def update_goal_bar(percent):
    goal_bar.delete("all")
    width = goal_bar.winfo_width()

    if width > 1:
        goal_bar.create_rectangle(
            0, 0, width * percent / 100, 12,
            fill="#F18BA4", outline=""
        )


# Statistics cards
stats_frame = tk.Frame(ap, bg=BG)
stats_frame.pack(fill="x", padx=22, pady=12)

for i in range(3):
    stats_frame.grid_columnconfigure(i, weight=1)

def create_achievement_stat(column, title, value, symbol, color):
    box = tk.Frame(
        stats_frame,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    box.grid(
        row=0, column=column,
        sticky="nsew", padx=7, pady=5
    )

    tk.Label(
        box, text=symbol,
        font=(FONT, 23),
        bg=WHITE, fg=color
    ).pack(anchor="w", padx=15, pady=(12, 3))

    val = tk.Label(
        box, text=value,
        font=(FONT, 20, "bold"),
        bg=WHITE, fg=TEXT
    )
    val.pack(anchor="w", padx=15)

    tk.Label(
        box, text=title,
        font=(FONT, 9),
        bg=WHITE, fg=MUTED
    ).pack(anchor="w", padx=15, pady=(2, 14))

    return val


days_stat = create_achievement_stat(0, "ACTIVE DAYS", "0", "📅", PURPLE)
score_stat = create_achievement_stat(1, "CONSISTENCY", "0%", "⭐", ORANGE)
streak_goal_stat = create_achievement_stat(2, "CURRENT GOAL", "20 days", "🎯", GREEN)

# ================= INTERACTIVE CALENDAR =================


# ================= INTERACTIVE HABIT CALENDAR =================

import calendar
from datetime import date

calendar_card = tk.Frame(
    ap,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
calendar_card.pack(fill="x", padx=30, pady=15)

tk.Label(
    calendar_card,
    text="Habit Calendar",
    font=(FONT, 18, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=20, pady=(15, 5))

today = date.today()

selected_date = tk.StringVar(
    value=today.strftime("%Y-%m-%d")
)

calendar_header = tk.Frame(calendar_card, bg=WHITE)
calendar_header.pack(fill="x", padx=15, pady=10)

month_var = tk.StringVar(value=today.strftime("%B"))
year_var = tk.IntVar(value=today.year)

months = list(calendar.month_name)[1:]


# Calendar navigation
def change_month(amount):

    month_index = months.index(month_var.get())
    year = year_var.get()

    month_index += amount

    if month_index < 0:
        month_index = 11
        year -= 1

    elif month_index > 11:
        month_index = 0
        year += 1

    month_var.set(months[month_index])
    year_var.set(year)

    draw_calendar()


# Show selected date's habit details
def show_selected_habits():

    records = get_records()
    chosen_date = selected_date.get()

    day_records = [
        r for r in records
        if r.get("date") == chosen_date
    ]

    selected_label.config(
        text="Selected Date: " + chosen_date
    )

    habit_details.delete("1.0", tk.END)

    if not day_records:
        habit_details.insert(
            tk.END,
            "No habit records found for this date."
        )
        return

    habit_details.insert(
        tk.END,
        "Habits tracked on this date:\n\n"
    )

    for record in day_records:

        status = (
            "Completed"
            if record.get("completed") == 1
            else "Not completed"
        )

        habit_details.insert(
            tk.END,
            f"• {record.get('habit', 'Habit')} - {status}\n"
        )


# Select a date
def select_calendar_date(day):

    month = months.index(month_var.get()) + 1
    year = year_var.get()

    selected_date.set(
        f"{year:04d}-{month:02d}-{day:02d}"
    )

    show_selected_habits()
    draw_calendar()


# Draw calendar
def draw_calendar():

    for widget in calendar_days.winfo_children():
        widget.destroy()

    month = months.index(month_var.get()) + 1
    year = year_var.get()

    records = get_records()

    headings = [
        "Mon", "Tue", "Wed",
        "Thu", "Fri", "Sat", "Sun"
    ]

    for col, heading in enumerate(headings):

        tk.Label(
            calendar_days,
            text=heading,
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=PURPLE
        ).grid(row=0, column=col, padx=5, pady=8)

    weeks = calendar.monthcalendar(year, month)

    for row, week in enumerate(weeks, start=1):

        for col, day in enumerate(week):

            if day == 0:
                continue

            date_text = (
                f"{year:04d}-{month:02d}-{day:02d}"
            )

            day_records = [
                r for r in records
                if r.get("date") == date_text
            ]

            completed = sum(
                1 for r in day_records
                if r.get("completed") == 1
            )

            total = len(day_records)

            # Habit completion colours
            if total == 0:
                bg_color = "#E5E7EB"
                fg_color = TEXT

            elif completed == total:
                bg_color = "#16A34A"
                fg_color = WHITE

            elif completed > 0:
                bg_color = "#F59E0B"
                fg_color = WHITE

            else:
                bg_color = "#E5E7EB"
                fg_color = TEXT

            # Highlight selected date with a border
            is_selected = (
                date_text == selected_date.get()
            )

            tk.Button(
                calendar_days,
                text=str(day),
                font=(FONT, 10, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground=PURPLE,
                activeforeground=WHITE,
                relief="solid" if is_selected else "flat",
                bd=2 if is_selected else 0,
                highlightthickness=2 if date(year, month, day) == today else 0,
                highlightbackground=RED,
                width=5,
                command=lambda d=day: select_calendar_date(d)
            ).grid(
                row=row,
                column=col,
                padx=3,
                pady=3
            )


# Previous month
tk.Button(
    calendar_header,
    text="◀",
    command=lambda: change_month(-1),
    bg=PURPLE,
    fg=WHITE,
    relief="flat"
).pack(side="left", padx=5)


# Month selection
tk.OptionMenu(
    calendar_header,
    month_var,
    *months,
    command=lambda value: draw_calendar()
).pack(side="left", padx=5)


# Year selection
year_selector = tk.Spinbox(
    calendar_header,
    from_=1900,
    to=2100,
    textvariable=year_var,
    width=7,
    command=draw_calendar
)
year_selector.pack(side="left", padx=5)

year_selector.bind(
    "<KeyRelease>",
    lambda event: draw_calendar()
)

year_selector.bind(
    "<FocusOut>",
    lambda event: draw_calendar()
)


# Next month
tk.Button(
    calendar_header,
    text="▶",
    command=lambda: change_month(1),
    bg=PURPLE,
    fg=WHITE,
    relief="flat"
).pack(side="left", padx=5)


# Calendar dates area
calendar_days = tk.Frame(
    calendar_card,
    bg=WHITE
)
calendar_days.pack(padx=15, pady=5)


# Selected date heading
selected_label = tk.Label(
    calendar_card,
    text="Selected Date: " + selected_date.get(),
    font=(FONT, 10, "bold"),
    bg=WHITE,
    fg=PURPLE
)
selected_label.pack(anchor="w", padx=20, pady=(12, 5))


# Habit details
habit_details = tk.Text(
    calendar_card,
    height=5,
    font=(FONT, 10),
    bg="#F8F7FC",
    fg=TEXT,
    relief="flat",
    wrap="word"
)
habit_details.pack(
    fill="x",
    padx=20,
    pady=(5, 15)
)

show_selected_habits()
draw_calendar()

# ================= END INTERACTIVE HABIT CALENDAR =================


# ================= END CALENDAR =================

tk.Label(
    ap,
    text="Milestone Badges",
    font=(FONT, 16, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w", padx=30, pady=(20, 10))

badge_frame = tk.Frame(ap, bg=BG)
badge_frame.pack(fill="x", padx=23)

def badge_card(parent, title, description, symbol, color):
    box = tk.Frame(
        parent, bg=WHITE,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    box.pack(
        side="left", expand=True,
        fill="both", padx=7, pady=5
    )

    tk.Label(
        box, text=symbol,
        font=(FONT, 28),
        bg=WHITE, fg=color
    ).pack(pady=(12, 3))

    tk.Label(
        box, text=title,
        font=(FONT, 10, "bold"),
        bg=WHITE, fg=TEXT
    ).pack()

    tk.Label(
        box, text=description,
        font=(FONT, 8),
        bg=WHITE, fg=MUTED,
        wraplength=110,
        justify="center"
    ).pack(padx=5, pady=(3, 12))


badge_card(
    badge_frame, "Starter",
    "Begin your journey",
    "🌱", GREEN
)

badge_card(
    badge_frame, "7 Day Star",
    "Complete 7 active days",
    "🏅", ORANGE
)

badge_card(
    badge_frame, "Consistency",
    "Reach 80% consistency",
    "⭐", PURPLE
)


# Achievement result
achievement_result = tk.Label(
    ap,
    text="Complete your habits and check your achievements!",
    font=(FONT, 11),
    bg=WHITE,
    fg=MUTED,
    justify="left",
    wraplength=650
)
achievement_result.pack(
    fill="x", padx=30, pady=18,
    ipadx=20, ipady=18
)


# Monthly calendar
tk.Label(
    ap,
    text="📅 Monthly Goal Calendar",
    font=(FONT, 16, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w", padx=30, pady=(15, 8))

import calendar
from datetime import date

calendar_frame = tk.Frame(
    ap, bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
calendar_frame.pack(fill="x", padx=30, pady=(0, 15))

today = date.today()

calendar_title = tk.Label(
    calendar_frame,
    text=today.strftime("%B %Y"),
    font=(FONT, 13, "bold"),
    bg=WHITE, fg=TEXT
)
calendar_title.pack(pady=12)

calendar_grid = tk.Frame(calendar_frame, bg=WHITE)
calendar_grid.pack(padx=12, pady=(0, 15), fill="x")

for col in range(7):
    calendar_grid.grid_columnconfigure(col, weight=1)

for col, day_name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    tk.Label(
        calendar_grid,
        text=day_name,
        font=(FONT, 8, "bold"),
        bg=WHITE, fg=MUTED
    ).grid(row=0, column=col, padx=2, pady=5)

month_days = calendar.monthcalendar(today.year, today.month)

for row, week in enumerate(month_days, start=1):
    for col, day in enumerate(week):
        if day:
            bg_color = "#EDE7FA" if day == today.day else "#F7F5FA"
            tk.Label(
                calendar_grid,
                text=str(day),
                font=(FONT, 9, "bold"),
                bg=bg_color,
                fg=TEXT,
                padx=5, pady=7
            ).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")


# Daily reminder time
tk.Label(
    ap,
    text="⏰ Daily Habit Reminder",
    font=(FONT, 16, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w", padx=30, pady=(10, 8))

reminder_frame = tk.Frame(
    ap, bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
reminder_frame.pack(fill="x", padx=30, pady=(0, 15))

tk.Label(
    reminder_frame,
    text="Choose your daily reminder time:",
    font=(FONT, 10),
    bg=WHITE, fg=TEXT
).pack(side="left", padx=15, pady=15)

reminder_time = tk.StringVar(value="08:00 AM")

reminder_options = [
    "06:00 AM", "07:00 AM", "08:00 AM",
    "09:00 AM", "10:00 AM", "06:00 PM",
    "07:00 PM", "08:00 PM", "09:00 PM"
]

reminder_menu = tk.OptionMenu(
    reminder_frame,
    reminder_time,
    *reminder_options
)
reminder_menu.config(
    bg="#EEE9FC",
    fg=TEXT,
    relief="flat",
    font=(FONT, 9)
)
reminder_menu.pack(side="right", padx=15, pady=10)


def show_achievement():
    try:
        records = get_records()
        total, completed, score = calculate_dashboard(records)
        achievement = get_achievement(score)

        score = max(0, min(100, float(score)))
        active_days = len({
            str(record.get("date", ""))
            for record in records
            if isinstance(record, dict)
        })

        monthly_progress = min(active_days, 20)
        percent = monthly_progress / 20 * 100

        goal_value.config(
            text=f"{monthly_progress} / 20 days"
        )
        goal_percent.config(
            text=f"{percent:.0f}% completed"
        )

        days_stat.config(text=str(active_days))
        score_stat.config(text=f"{score:.1f}%")

        update_goal_bar(percent)

        achievement_result.config(
            text=(
                f"🏆 Your Achievement\n\n"
                f"{achievement}\n\n"
                f"Consistency: {score:.2f}%\n"
                f"Active days: {active_days}"
            ),
            fg=TEXT
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


make_flat_button(
    ap,
    "🏆  Check My Achievements",
    show_achievement,
    bg=ORANGE,
    width=24
).pack(anchor="w", padx=30, pady=(0, 25))

# ============================================================
# STACK PAGE
# ============================================================

sp = stack_page

tk.Label(
    sp,
    text="Recent Activities - Stack",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

stack_result = tk.Label(
    sp,
    text="No recent activities.",
    font=(FONT, 11),
    bg=WHITE,
    fg=MUTED,
    justify="left",
    anchor="w"
)
stack_result.pack(fill="x", padx=30, pady=20, ipadx=20, ipady=20)


def show_recent_page():
    try:
        activities = recent_stack.display()

        if not activities:
            stack_result.config(text="No recent activities.")
        else:
            stack_result.config(
                text="\n".join(activities),
                fg=TEXT
            )

    except Exception as e:
        messagebox.showerror("Stack Error", str(e))


make_flat_button(
    sp,
    "Show Recent Activities",
    show_recent_page,
    bg=BLUE,
    width=22
).pack(anchor="w", padx=30)


# ============================================================
# QUEUE PAGE
# ============================================================

qp = queue_page

tk.Label(
    qp,
    text="Pending Habits - Queue",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

queue_result = tk.Label(
    qp,
    text="No pending habits.",
    font=(FONT, 11),
    bg=WHITE,
    fg=MUTED,
    justify="left",
    anchor="w"
)
queue_result.pack(fill="x", padx=30, pady=20, ipadx=20, ipady=20)


def show_pending_page():
    try:
        pending = pending_queue.display()

        if not pending:
            queue_result.config(text="No pending habits.")
        else:
            queue_result.config(
                text="\n".join(pending),
                fg=TEXT
            )

    except Exception as e:
        messagebox.showerror("Queue Error", str(e))


make_flat_button(
    qp,
    "Show Pending Habits",
    show_pending_page,
    bg=PURPLE,
    width=20
).pack(anchor="w", padx=30)


# ============================================================
# SEARCH & SORT PAGE
# ============================================================

search_page_frame = search_page

tk.Label(
    search_page_frame,
    text="Search & Sort",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

tk.Label(
    search_page_frame,
    text="View your habits in a simple list.",
    font=(FONT, 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=30)

search_result = tk.Listbox(
    search_page_frame,
    font=(FONT, 10),
    bg=WHITE,
    fg=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightthickness=1
)
search_result.pack(fill="both", expand=True, padx=30, pady=20)


def load_search():
    search_result.delete(0, tk.END)

    try:
        habits = get_habits()
        habits = sorted(habits, key=lambda x: x["name"].lower())

        for h in habits:
            search_result.insert(
                tk.END,
                f"{h['name']}  |  Target: {h['target']}"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


make_flat_button(
    search_page_frame,
    "Load & Sort Habits",
    load_search,
    bg=BLUE,
    width=20
).pack(anchor="w", padx=30, pady=(0, 20))


# ============================================================
# SETTINGS PAGE
# ============================================================

settings = settings_page

tk.Label(
    settings,
    text="Settings",
    font=(FONT, 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=30, pady=(28, 4))

settings_card = tk.Frame(
    settings,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground=BORDER
)
settings_card.pack(fill="x", padx=30, pady=20)

tk.Label(
    settings_card,
    text="HabitWise",
    font=(FONT, 16, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=25, pady=(25, 5))

tk.Label(
    settings_card,
    text="Smart Habit Tracker\n\nDSA used: Stack (LIFO), Queue (FIFO), Lists",
    font=(FONT, 10),
    bg=WHITE,
    fg=MUTED,
    justify="left"
).pack(anchor="w", padx=25, pady=(0, 25))


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

menu_button("Dashboard", "⌂", lambda: show_page("Dashboard"))
menu_button("My Habits", "✓", lambda: show_page("My Habits"))
menu_button("Daily Tracker", "▣", lambda: show_page("Daily Tracker"))
menu_button("Insights", "◈", lambda: show_page("Insights"))
menu_button("Achievements", "★", lambda: show_page("Achievements"))
menu_button("Search & Sort", "⌕", lambda: show_page("Search & Sort"))
menu_button("Stack", "▤", lambda: show_page("Stack"))
menu_button("Queue", "☷", lambda: show_page("Queue"))

# Spacer
tk.Frame(sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

menu_button("Settings", "⚙", lambda: show_page("Settings"))


# ============================================================
# INITIALIZE
# ============================================================

refresh_habit_list()
refresh_dashboard()
show_page("Dashboard")

root.mainloop()
