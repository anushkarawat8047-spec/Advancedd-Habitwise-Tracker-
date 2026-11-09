# ==========================================
# achievements.py
# Backend - Achievements
# ==========================================


def get_achievement(score):

    if score >= 90:

        return "Habit Master"

    elif score >= 75:

        return "Excellent Performer"

    elif score >= 50:

        return "Good Progress"

    else:

        return "Keep Improving"