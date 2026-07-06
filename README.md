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
================================================

Biscuit (Golden Retriever) - Dog
  08:00  Morning walk (30 min) [priority: high] [todo]
  09:00  Feeding (10 min) [priority: high] [todo]

Mittens (Tabby) - Cat
  18:30  Litter cleanup (15 min) [priority: medium] [todo]
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
