# ============================================================
# FRONTEND DATA INTERFACE
# ============================================================
# IMPORTANT:
# This file intentionally contains NO sample habits or records.
#
# The backend teammate will later provide real data here/API.
# ============================================================

habits = []
activities = []
pending_tasks = []


def completion_percent(habit):
    if not habit or habit.get("target", 0) <= 0:
        return 0
    return min(100, habit.get("done", 0) / habit["target"] * 100)


def overall_completion():
    if not habits:
        return 0
    return sum(completion_percent(h) for h in habits) / len(habits)


def completed_count():
    return sum(
        1 for h in habits
        if h.get("done", 0) >= h.get("target", 1)
    )
