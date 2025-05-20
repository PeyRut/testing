# Gym Tracker

This project provides a command line application to track your weightlifting workouts.

## Features

- Add new workout entries with date, exercise, weight, reps, and sets.
- List, update, or remove recorded workouts.
- Filter the list of workouts by date or exercise name.
- Data is stored in a SQLite database in your home directory (`~/.gym_tracker.db`).

## Usage

Run the tracker with Python:

```bash
python -m gym_tracker.tracker add "Bench Press" 100 8 3
```

This command adds a bench press workout for today with 100 lbs, 8 reps, and 3 sets.

List all workouts:

```bash
python -m gym_tracker.tracker list
```

Update an entry by ID (e.g., to change the weight to 105 for workout 1):

```bash
python -m gym_tracker.tracker edit 1 --weight 105
```

Remove an entry:

```bash
python -m gym_tracker.tracker remove 1
```

## Installation

No installation is required. Just clone the repository and run the commands above with Python 3.7+ installed.
