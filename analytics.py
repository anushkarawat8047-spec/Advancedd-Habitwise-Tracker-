from datetime import date, timedelta


def calculate_percentage(completed, total):
    if total == 0:
        return 0

    return round((completed / total) * 100, 2)


def habit_statistics(records):
    total = len(records)

    completed = sum(
        1 for r in records
        if r[2] == 1
    )

    percentage = calculate_percentage(
        completed,
        total
    )

    return total, completed, percentage


def get_performance_message(score):
    if score >= 90:
        return "Excellent! 🔥"

    elif score >= 75:
        return "Very Good! ⭐"

    elif score >= 50:
        return "Good, but you can improve."

    else:
        return "Focus on consistency."


def calculate_streak(records):
    """
    records:
    [(date, value, completed), ...]
    """

    if not records:
        return 0

    completed_dates = {
        r[0] for r in records if r[2] == 1
    }

    if not completed_dates:
        return 0

    current = date.today()

    # Agar aaj record nahi hai to yesterday se streak check
    if str(current) not in completed_dates:
        current -= timedelta(days=1)

    streak = 0

    while str(current) in completed_dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


def best_streak(records):
    if not records:
        return 0

    completed_dates = sorted(
        date.fromisoformat(r[0])
        for r in records
        if r[2] == 1
    )

    if not completed_dates:
        return 0

    best = 1
    current = 1

    for i in range(1, len(completed_dates)):

        difference = (
            completed_dates[i] -
            completed_dates[i - 1]
        ).days

        if difference == 1:
            current += 1
            best = max(best, current)

        else:
            current = 1

    return best


def compare_days(today, yesterday):
    if today > yesterday:
        return f"Improved by {today - yesterday}"

    elif today < yesterday:
        return f"Decreased by {yesterday - today}"

    return "No change"


def improvement_percentage(old_score, new_score):
    return round(new_score - old_score, 2)


def achievement_list(records):
    achievements = []

    total = len(records)
    completed = sum(r[5] for r in records)

    if total >= 1:
        achievements.append("🌱 First Step")

    if completed >= 5:
        achievements.append("🏅 5 Tasks Completed")

    if completed >= 10:
        achievements.append("🏆 10 Tasks Completed")

    # Overall streak
    simple_records = [
        (r[3], r[4], r[5])
        for r in records
    ]

    streak = calculate_streak(simple_records)

    if streak >= 3:
        achievements.append("🔥 3 Day Streak")

    if streak >= 7:
        achievements.append("🔥 7 Day Streak")

    if streak >= 30:
        achievements.append("👑 30 Day Streak")

    if total > 0:
        percentage = calculate_percentage(
            completed,
            total
        )

        if percentage >= 90:
            achievements.append("💯 Consistency Master")

    return achievements