import sqlite3
from datetime import date

DB_NAME = "habitwise.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            target REAL NOT NULL,
            unit TEXT NOT NULL,
            created_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            value REAL NOT NULL,
            completed INTEGER NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    conn.commit()
    conn.close()


def add_habit(name, category, target, unit):
    conn = connect()

    conn.execute("""
        INSERT INTO habits
        (name, category, target, unit, created_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, target, unit, str(date.today())))

    conn.commit()
    conn.close()


def get_habits():
    conn = connect()

    cursor = conn.execute("""
        SELECT id, name, category, target, unit, created_date
        FROM habits
        ORDER BY id
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def save_record(habit_id, record_date, value, completed):
    conn = connect()

    # Same habit + same day ko duplicate karne ke bajay update karo
    existing = conn.execute("""
        SELECT id
        FROM daily_records
        WHERE habit_id = ? AND date = ?
    """, (habit_id, record_date)).fetchone()

    if existing:
        conn.execute("""
            UPDATE daily_records
            SET value = ?, completed = ?
            WHERE id = ?
        """, (value, completed, existing[0]))
    else:
        conn.execute("""
            INSERT INTO daily_records
            (habit_id, date, value, completed)
            VALUES (?, ?, ?, ?)
        """, (habit_id, record_date, value, completed))

    conn.commit()
    conn.close()


def get_records():
    conn = connect()

    cursor = conn.execute("""
        SELECT
            daily_records.id,
            habits.name,
            habits.category,
            daily_records.date,
            daily_records.value,
            daily_records.completed,
            habits.target,
            habits.unit,
            daily_records.habit_id
        FROM daily_records
        JOIN habits
        ON daily_records.habit_id = habits.id
        ORDER BY daily_records.date
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def get_records_for_habit(habit_id):
    conn = connect()

    cursor = conn.execute("""
        SELECT date, value, completed
        FROM daily_records
        WHERE habit_id = ?
        ORDER BY date
    """, (habit_id,))

    data = cursor.fetchall()
    conn.close()

    return data


def delete_habit(habit_id):
    conn = connect()

    conn.execute(
        "DELETE FROM daily_records WHERE habit_id = ?",
        (habit_id,)
    )

    conn.execute(
        "DELETE FROM habits WHERE id = ?",
        (habit_id,)
    )

    conn.commit()
    conn.close()