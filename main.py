"""CLI demo for PawPal+.

A temporary testing ground that builds an owner, pets, and tasks, then
exercises the scheduler's smart features (sorting, filtering, recurrence,
and conflict detection) from the terminal.
Run with:  python main.py
"""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task, TaskType


def _today_at(hour: int, minute: int = 0) -> datetime:
    """Return a datetime for today at the given time."""
    return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)


def build_demo() -> tuple[Owner, Scheduler]:
    """Create a sample owner, pets, and tasks, then load a scheduler."""
    owner = Owner(id="o1", name="Alex", email="alex@example.com")

    biscuit = Pet(id="p1", name="Biscuit", species="Dog", breed="Golden Retriever")
    mittens = Pet(id="p2", name="Mittens", species="Cat", breed="Tabby")
    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    # Added intentionally OUT OF ORDER to prove sort_by_time() works.
    biscuit.add_task(Task(
        id="t1", title="Evening walk", task_type=TaskType.WALK,
        duration=timedelta(minutes=30), priority=Priority.MEDIUM,
        due_date=_today_at(18, 0),
    ))
    biscuit.add_task(Task(
        id="t2", title="Morning feeding", task_type=TaskType.FEEDING,
        duration=timedelta(minutes=10), priority=Priority.HIGH,
        due_date=_today_at(8, 0), recurrence=timedelta(days=1),  # daily
    ))
    mittens.add_task(Task(
        id="t3", title="Litter cleanup", task_type=TaskType.GROOMING,
        duration=timedelta(minutes=15), priority=Priority.MEDIUM,
        due_date=_today_at(12, 0),
    ))
    # Deliberate conflict: same time (12:00) as Mittens' litter cleanup.
    biscuit.add_task(Task(
        id="t4", title="Midday meds", task_type=TaskType.MEDICATION,
        duration=timedelta(minutes=5), priority=Priority.HIGH,
        due_date=_today_at(12, 0),
    ))

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)
    return owner, scheduler


def main() -> None:
    """Build demo data and exercise the scheduler's smart features."""
    owner, scheduler = build_demo()
    today = datetime.now()

    print(f"Today's Schedule for {owner.name} - {today.strftime('%A, %b %d')}")
    print("=" * 52)
    print("\nSorted by time (Scheduler.sort_by_time):")
    for task in scheduler.sort_by_time():
        print(f"  {task}")

    print("\nFilter - only Biscuit's tasks (Scheduler.filter_by_pet):")
    for task in scheduler.filter_by_pet("Biscuit"):
        print(f"  {task}")

    print("\nConflict detection (Scheduler.detect_conflicts):")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts found.")

    print("\nRecurrence (complete daily 'Morning feeding'):")
    feeding = next(t for t in scheduler.tasks if t.title == "Morning feeding")
    follow_up = scheduler.complete_task(feeding)
    if follow_up:
        print(f"  Completed today's feeding; next one auto-scheduled for "
              f"{follow_up.due_date.strftime('%b %d %H:%M')}")

    print("\nRemaining incomplete tasks (Scheduler.filter_by_status):")
    for task in scheduler.filter_by_status(completed=False):
        print(f"  {task}")


if __name__ == "__main__":
    main()
