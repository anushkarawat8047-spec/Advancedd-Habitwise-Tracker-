
import json
import os
from datetime import date

RECORD_FILE = "habit_records.json"


def load_records():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


records = load_records()


# Save daily habit record
def save_record(habit_name, value, target):

    completed = 1 if value >= target else 0

    record = {
        "habit": habit_name,
        "value": value,
        "target": target,
        "completed": completed,
        "date": date.today().strftime("%Y-%m-%d")
    }

    records.append(record)

    with open(RECORD_FILE, "w") as file:
        json.dump(records, file, indent=4)

    return completed


# Get all records
def get_records():
    return records
