"""CLI demo for PawPal+.

A temporary testing ground that builds an owner, some pets and tasks,
then prints today's schedule to verify the logic layer works end to end.
Run with:  python main.py
"""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task, TaskType


def _today_at(hour: int, minute: int = 0) -> datetime:
    """Return a datetime for today at the given time."""
    now = datetime.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def build_demo() -> tuple[Owner, Scheduler]:
    """Create a sample owner, pets, and tasks, then load a scheduler."""
    owner = Owner(id="o1", name="Alex", email="alex@example.com")

    biscuit = Pet(id="p1", name="Biscuit", species="Dog", breed="Golden Retriever")
    mittens = Pet(id="p2", name="Mittens", species="Cat", breed="Tabby")
    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    biscuit.add_task(Task(
        id="t1", title="Morning walk", task_type=TaskType.WALK,
        duration=timedelta(minutes=30), priority=Priority.HIGH,
        due_date=_today_at(8, 0),
    ))
    biscuit.add_task(Task(
        id="t2", title="Feeding", task_type=TaskType.FEEDING,
        duration=timedelta(minutes=10), priority=Priority.HIGH,
        due_date=_today_at(9, 0),
    ))
    mittens.add_task(Task(
        id="t3", title="Litter cleanup", task_type=TaskType.GROOMING,
        duration=timedelta(minutes=15), priority=Priority.MEDIUM,
        due_date=_today_at(18, 30),
    ))

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)
    return owner, scheduler


def print_todays_schedule(owner: Owner, scheduler: Scheduler) -> None:
    """Print a readable 'Today's Schedule' grouped by pet."""
    today = datetime.now()
    print(f"Today's Schedule for {owner.name} - {today.strftime('%A, %b %d')}")
    print("=" * 48)

    plan = scheduler.generate_daily_plan(today)
    if not plan:
        print("  (no tasks scheduled for today)")
        return

    for pet in owner.list_pets():
        pet_tasks = [t for t in plan if t.pet is pet]
        if not pet_tasks:
            continue
        print(f"\n{pet}")
        for task in pet_tasks:
            print(f"  {task}")


def main() -> None:
    """Build the demo data and print today's schedule."""
    owner, scheduler = build_demo()
    print_todays_schedule(owner, scheduler)


if __name__ == "__main__":
    main()
