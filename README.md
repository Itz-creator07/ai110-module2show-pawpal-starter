# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Owner / Pet / Task modeling** — an owner manages multiple pets, each with its own care tasks (`pawpal_system.py`).
- **Sorting by time** — `Scheduler.sort_by_time()` orders the day chronologically.
- **Priority-aware daily plan** — `Scheduler.generate_daily_plan()` keeps the highest-priority tasks first and drops low-priority ones when a time budget runs out.
- **Filtering** — by pet (`filter_by_pet`) or by completion status (`filter_by_status`).
- **Conflict warnings** — `detect_conflicts()` flags tasks booked at the same time and returns a friendly message instead of crashing.
- **Recurring tasks** — completing a daily/weekly task auto-schedules the next occurrence (`complete_task` + `Task.next_occurrence`).
- **Streamlit UI** — add pets/tasks and view today's sorted schedule with conflict warnings (`app.py`).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running the CLI demo (`python main.py`):

```
Today's Schedule for Alex - Monday, Jul 06
====================================================

Sorted by time (Scheduler.sort_by_time):
  08:00  Morning feeding (10 min) [priority: high] [todo]
  12:00  Midday meds (5 min) [priority: high] [todo]
  12:00  Litter cleanup (15 min) [priority: medium] [todo]
  18:00  Evening walk (30 min) [priority: medium] [todo]

Filter - only Biscuit's tasks (Scheduler.filter_by_pet):
  18:00  Evening walk (30 min) [priority: medium] [todo]
  08:00  Morning feeding (10 min) [priority: high] [todo]
  12:00  Midday meds (5 min) [priority: high] [todo]

Conflict detection (Scheduler.detect_conflicts):
  WARNING: Conflict at 12:00: Midday meds (Biscuit), Litter cleanup (Mittens)

Recurrence (complete daily 'Morning feeding'):
  Completed today's feeding; next one auto-scheduled for Jul 07 08:00
```

## 🧪 Testing PawPal+

Run the automated suite from the project root:

```bash
python -m pytest
```

**What the tests cover** (`tests/test_pawpal.py`):

- **Core behavior** — `mark_complete()` flips a task's status; adding a task increases a pet's task count.
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order regardless of insertion order.
- **Recurrence logic** — completing a daily task auto-creates a new task for the next day; a one-off task creates no follow-up.
- **Conflict detection** — `detect_conflicts()` flags two tasks at the same time and stays silent when times differ.
- **Edge case** — a pet with no tasks yields an empty plan.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
collected 8 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 12%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 25%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 37%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_instance PASSED [ 50%]
tests/test_pawpal.py::test_completing_one_off_task_creates_no_follow_up PASSED [ 62%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [ 75%]
tests/test_pawpal.py::test_no_conflicts_when_times_differ PASSED         [ 87%]
tests/test_pawpal.py::test_pet_with_no_tasks_has_empty_plan PASSED       [100%]

============================== 8 passed in 0.06s ==============================
```

**Confidence level: ★★★★☆ (4/5)** — the core object behavior and each smart-scheduling algorithm are covered and green. Docking one star because conflict detection only checks exact-time matches (not overlapping durations) and the recurrence tests cover daily intervals but not every edge case (e.g., weekly across month boundaries).

## 📐 Smarter Scheduling

PawPal+ includes several small algorithms in `pawpal_system.py` that make the
scheduler more helpful:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically by due time; a `sorted()` lambda pushes timeless tasks last. `generate_daily_plan()` additionally sorts by priority within a time budget. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter tasks by pet name (case-insensitive) or by completion status. |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight check that flags tasks sharing the exact same start time and returns warning strings instead of raising. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | Completing a daily/weekly task auto-creates the next instance using `timedelta` (e.g., due date + 1 day). |

## 📸 Demo Walkthrough

Launch the UI with `streamlit run app.py`, or run the CLI demo with `python main.py`.

**Main UI features (`app.py`):**

- Set the **owner name**.
- **Add a Pet** — name, species, and optional breed. Pets persist in `st.session_state` across reruns.
- **Schedule a Task** — pick a pet, title, type, time, duration, and priority.
- **Today's Schedule** — a "Generate schedule" button shows the day's tasks in a sorted table, surfaces conflict warnings, and can optionally show completed tasks.

**Example workflow:**

1. Enter the owner name (e.g., "Alex").
2. Add a pet — "Biscuit", a dog.
3. Schedule a task — "Morning feeding" at 08:00, high priority.
4. Add a second pet ("Mittens") and a task that clashes at the same time as another.
5. Click **Generate schedule** to see the sorted plan and a ⚠️ conflict warning.

**Key Scheduler behaviors shown:** chronological sorting (`sort_by_time`), priority-aware planning (`generate_daily_plan`), conflict warnings (`detect_conflicts`), filtering (`filter_by_pet` / `filter_by_status`), and recurring tasks (`complete_task`).

**Sample CLI output** from `python main.py`:

```
Today's Schedule for Alex - Monday, Jul 06
====================================================

Sorted by time (Scheduler.sort_by_time):
  08:00  Morning feeding (10 min) [priority: high] [todo]
  12:00  Midday meds (5 min) [priority: high] [todo]
  12:00  Litter cleanup (15 min) [priority: medium] [todo]
  18:00  Evening walk (30 min) [priority: medium] [todo]

Conflict detection (Scheduler.detect_conflicts):
  WARNING: Conflict at 12:00: Midday meds (Biscuit), Litter cleanup (Mittens)

Recurrence (complete daily 'Morning feeding'):
  Completed today's feeding; next one auto-scheduled for Jul 07 08:00
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
