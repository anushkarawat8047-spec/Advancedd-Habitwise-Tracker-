# ==========================================
# insights.py
# Backend - Performance Insights
# ==========================================


def get_performance_message(score):

    if score >= 80:

        return "Excellent! Keep going!"

    elif score >= 60:

        return "Good work! Try to improve your consistency."

    elif score >= 40:

        return "Keep practicing and stay consistent."

    else:

        return "You need to work more on your habits."