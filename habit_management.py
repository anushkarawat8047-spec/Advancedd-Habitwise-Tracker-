
# ==========================================
# habit_management.py
# Backend - Habit Management
# ==========================================

import json
import os

HABIT_FILE = "habits.json"


# Load saved habits
def load_habits():

    if os.path.exists(HABIT_FILE):

        try:
            with open(HABIT_FILE, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    return []


habits = load_habits()


# Save habits permanently
def save_habits():

    with open(HABIT_FILE, "w") as file:
        json.dump(habits, file, indent=4)


# Add a new habit
def add_habit(name, target, unit=""):

    habit = {
        "name": name,
        "target": target,
        "unit": unit
    }

    habits.append(habit)

    save_habits()

    return True


# Get all habits
def get_habits():
    return habits


# Delete a habit
def delete_habit(name):

    for habit in habits:

        if habit["name"].lower() == name.lower():

            habits.remove(habit)

            save_habits()

            return True

    return False
