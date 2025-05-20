# Gym Tracker

This project provides a simple command line application to track your weightlifting workouts.

## Features

- Add new workout entries with date, exercise, weight, reps, and sets.
- List all recorded workouts in a friendly table format.
- Data is stored in a JSON file in your home directory (`~/.gym_tracker.json`).

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

## Installation

No installation is required. Just clone the repository and run the commands above with Python 3.6+ installed.

