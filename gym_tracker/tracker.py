import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

DB_FILE = os.path.join(os.path.expanduser("~"), ".gym_tracker.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    exercise TEXT NOT NULL,
    weight REAL NOT NULL,
    reps INTEGER NOT NULL,
    sets INTEGER NOT NULL
);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


@dataclass
class Workout:
    id: Optional[int]
    date: str
    exercise: str
    weight: float
    reps: int
    sets: int


def add_workout(date: str, exercise: str, weight: float, reps: int, sets: int) -> Workout:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO workouts (date, exercise, weight, reps, sets) VALUES (?, ?, ?, ?, ?)",
            (date, exercise, weight, reps, sets),
        )
        conn.commit()
        return Workout(cur.lastrowid, date, exercise, weight, reps, sets)


def list_workouts(exercise: Optional[str] = None, date: Optional[str] = None) -> List[Workout]:
    query = "SELECT id, date, exercise, weight, reps, sets FROM workouts"
    params = []
    conditions = []
    if exercise:
        conditions.append("exercise LIKE ?")
        params.append(f"%{exercise}%")
    if date:
        conditions.append("date = ?")
        params.append(date)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY date, id"
    with get_conn() as conn:
        rows = conn.execute(query, params).fetchall()
        return [Workout(row["id"], row["date"], row["exercise"], row["weight"], row["reps"], row["sets"]) for row in rows]


def update_workout(workout_id: int, *, date: Optional[str] = None, exercise: Optional[str] = None,
                   weight: Optional[float] = None, reps: Optional[int] = None, sets: Optional[int] = None) -> bool:
    fields = []
    params = []
    if date is not None:
        fields.append("date = ?")
        params.append(date)
    if exercise is not None:
        fields.append("exercise = ?")
        params.append(exercise)
    if weight is not None:
        fields.append("weight = ?")
        params.append(weight)
    if reps is not None:
        fields.append("reps = ?")
        params.append(reps)
    if sets is not None:
        fields.append("sets = ?")
        params.append(sets)
    if not fields:
        return False
    params.append(workout_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE workouts SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        return conn.total_changes > 0


def remove_workout(workout_id: int) -> bool:
    with get_conn() as conn:
        conn.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        conn.commit()
        return conn.total_changes > 0


def print_table(rows: List[Workout]) -> None:
    if not rows:
        print("No workouts found.")
        return
    headers = ["ID", "Date", "Exercise", "Weight", "Reps", "Sets"]
    max_lens = [len(h) for h in headers]
    for w in rows:
        values = [str(w.id), w.date, w.exercise, str(w.weight), str(w.reps), str(w.sets)]
        for i, v in enumerate(values):
            max_lens[i] = max(max_lens[i], len(v))
    header_line = " | ".join(h.ljust(max_lens[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * max_lens[i] for i in range(len(headers)))
    print(header_line)
    print(sep_line)
    for w in rows:
        values = [str(w.id), w.date, w.exercise, str(w.weight), str(w.reps), str(w.sets)]
        line = " | ".join(values[i].ljust(max_lens[i]) for i in range(len(values)))
        print(line)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Personal Gym Weightlifting Tracker")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a workout entry")
    add_parser.add_argument("exercise", help="Name of the exercise")
    add_parser.add_argument("weight", type=float, help="Weight used")
    add_parser.add_argument("reps", type=int, help="Number of repetitions per set")
    add_parser.add_argument("sets", type=int, help="Number of sets")
    add_parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date of the workout (YYYY-MM-DD)")

    list_parser = subparsers.add_parser("list", help="List workouts")
    list_parser.add_argument("--exercise", help="Filter by exercise")
    list_parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")

    edit_parser = subparsers.add_parser("edit", help="Update an existing workout")
    edit_parser.add_argument("id", type=int, help="ID of the workout to edit")
    edit_parser.add_argument("--date", help="New date")
    edit_parser.add_argument("--exercise", help="New exercise name")
    edit_parser.add_argument("--weight", type=float, help="New weight")
    edit_parser.add_argument("--reps", type=int, help="New repetitions")
    edit_parser.add_argument("--sets", type=int, help="New sets")

    rm_parser = subparsers.add_parser("remove", help="Delete a workout")
    rm_parser.add_argument("id", type=int, help="ID of the workout to delete")

    args = parser.parse_args()

    if args.command == "add":
        w = add_workout(args.date, args.exercise, args.weight, args.reps, args.sets)
        print("Added workout:")
        print_table([w])
    elif args.command == "list":
        rows = list_workouts(exercise=args.exercise, date=args.date)
        print_table(rows)
    elif args.command == "edit":
        success = update_workout(args.id, date=args.date, exercise=args.exercise, weight=args.weight,
                                 reps=args.reps, sets=args.sets)
        if success:
            print("Workout updated.")
        else:
            print("Workout not found or no fields provided.")
    elif args.command == "remove":
        success = remove_workout(args.id)
        if success:
            print("Workout removed.")
        else:
            print("Workout not found.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
