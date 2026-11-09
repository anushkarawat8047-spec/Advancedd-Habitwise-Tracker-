# ==========================================
# dashboard.py
# Backend - Dashboard
# ==========================================


def calculate_dashboard(records):

    total = len(records)

    # If there are no records
    if total == 0:

        return 0, 0, 0

    completed = 0

    # Count completed records
    for record in records:

        if record["completed"] == 1:

            completed += 1

    # Calculate percentage
    percentage = (completed / total) * 100

    return total, completed, percentage