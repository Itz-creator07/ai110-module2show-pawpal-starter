"""Automated tests for the PawPal+ logic layer.

Covers core object behavior (task completion, task addition) plus the
smart-scheduling algorithms (sorting, recurrence, conflict detection) and
a couple of edge cases (a pet with no tasks, a one-off task).
"""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task, TaskType


def _at(hour: int, minute: int = 0) -> datetime:
    """Helper: a fixed datetime today at the given time."""
    return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)


# --- Core object behavior ----------------------------------------------------

def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from incomplete to complete."""
    task = Task(id="t1", title="Morning walk")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet increases that pet's task count by one."""
    pet = Pet(id="p1", name="Biscuit", species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(id="t1", title="Feeding"))

    assert len(pet.tasks) == 1


# --- Sorting correctness -----------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() returns tasks ordered by due time regardless of insert order."""
    scheduler = Scheduler()
    scheduler.schedule_task(Task(id="t1", title="Evening", due_date=_at(18)))
    scheduler.schedule_task(Task(id="t2", title="Morning", due_date=_at(8)))
    scheduler.schedule_task(Task(id="t3", title="Noon", due_date=_at(12)))

    ordered = [t.title for t in scheduler.sort_by_time()]

    assert ordered == ["Morning", "Noon", "Evening"]


# --- Recurrence logic --------------------------------------------------------

def test_completing_daily_task_creates_next_day_instance():
    """Completing a daily task auto-schedules a new task for the following day."""
    scheduler = Scheduler()
    daily = Task(
        id="t1", title="Feeding", due_date=_at(8),
        recurrence=timedelta(days=1),
    )
    scheduler.schedule_task(daily)

    follow_up = scheduler.complete_task(daily)

    assert daily.completed is True
    assert follow_up is not None
    assert follow_up.completed is False
    assert follow_up.due_date == daily.due_date + timedelta(days=1)
    assert follow_up in scheduler.tasks


def test_completing_one_off_task_creates_no_follow_up():
    """A non-recurring task produces no follow-up when completed."""
    scheduler = Scheduler()
    task = Task(id="t1", title="Vet visit", due_date=_at(10))
    scheduler.schedule_task(task)

    follow_up = scheduler.complete_task(task)

    assert follow_up is None
    assert len(scheduler.tasks) == 1


# --- Conflict detection ------------------------------------------------------

def test_detect_conflicts_flags_duplicate_times():
    """Two tasks at the same time produce exactly one conflict warning."""
    scheduler = Scheduler()
    scheduler.schedule_task(Task(id="t1", title="Meds", due_date=_at(12)))
    scheduler.schedule_task(Task(id="t2", title="Cleanup", due_date=_at(12)))

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "12:00" in conflicts[0]


def test_no_conflicts_when_times_differ():
    """Tasks at different times produce no conflict warnings."""
    scheduler = Scheduler()
    scheduler.schedule_task(Task(id="t1", title="Meds", due_date=_at(12)))
    scheduler.schedule_task(Task(id="t2", title="Walk", due_date=_at(13)))

    assert scheduler.detect_conflicts() == []


# --- Edge case ---------------------------------------------------------------

def test_pet_with_no_tasks_has_empty_plan():
    """A pet with no tasks yields no upcoming tasks and an empty owner task list."""
    owner = Owner(id="o1", name="Alex")
    pet = Pet(id="p1", name="Ghost", species="Cat")
    owner.add_pet(pet)

    assert pet.get_upcoming_tasks() == []
    assert owner.get_all_tasks() == []
