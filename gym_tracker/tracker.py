import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.expanduser("~"), '.gym_tracker.json')


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_workout(date, exercise, weight, reps, sets):
    data = load_data()
    workout = {
        'date': date,
        'exercise': exercise,
        'weight': weight,
        'reps': reps,
        'sets': sets
    }
    data.append(workout)
    save_data(data)
    return workout


def list_workouts():
    return load_data()


def print_table(rows):
    if not rows:
        print('No workouts found.')
        return
    headers = ['Date', 'Exercise', 'Weight', 'Reps', 'Sets']
    max_lens = [len(h) for h in headers]
    for row in rows:
        values = [row['date'], row['exercise'], str(row['weight']), str(row['reps']), str(row['sets'])]
        for i, v in enumerate(values):
            max_lens[i] = max(max_lens[i], len(v))
    # print header
    header_line = ' | '.join(h.ljust(max_lens[i]) for i, h in enumerate(headers))
    sep_line = '-+-'.join('-' * max_lens[i] for i in range(len(headers)))
    print(header_line)
    print(sep_line)
    for row in rows:
        values = [row['date'], row['exercise'], str(row['weight']), str(row['reps']), str(row['sets'])]
        line = ' | '.join(values[i].ljust(max_lens[i]) for i in range(len(values)))
        print(line)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Personal Gym Weightlifting Tracker')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a workout entry')
    add_parser.add_argument('exercise', help='Name of the exercise')
    add_parser.add_argument('weight', type=float, help='Weight used')
    add_parser.add_argument('reps', type=int, help='Number of repetitions per set')
    add_parser.add_argument('sets', type=int, help='Number of sets')
    add_parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Date of the workout (YYYY-MM-DD)')

    list_parser = subparsers.add_parser('list', help='List all workouts')

    args = parser.parse_args()

    if args.command == 'add':
        workout = add_workout(args.date, args.exercise, args.weight, args.reps, args.sets)
        print('Added workout:')
        print_table([workout])
    elif args.command == 'list':
        rows = list_workouts()
        print_table(rows)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
