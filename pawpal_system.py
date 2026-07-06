"""PawPal+ logic layer.

Implements the four core classes designed in diagrams/uml.mmd:
Owner, Pet, Task, and Scheduler. This is the backend "brain" that is
verified from the terminal (main.py) before being wired to Streamlit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class Priority(Enum):
    """How important a task is when the scheduler must make trade-offs."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TaskType(Enum):
    """The kind of care a task represents."""

    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    GROOMING = "grooming"
    ENRICHMENT = "enrichment"
    OTHER = "other"


@dataclass
class Task:
    """A single pet-care activity (description, time, frequency, status)."""

    id: str
    title: str
    task_type: TaskType = TaskType.OTHER
    duration: timedelta = timedelta(minutes=30)
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None
    recurrence: timedelta | None = None
    completed: bool = False
    description: str = ""
    pet: "Pet | None" = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def reschedule(self, new_date: datetime) -> None:
        """Move this task to a new due date and reopen it."""
        self.due_date = new_date
        self.completed = False

    def is_overdue(self) -> bool:
        """Return True if the task is past its due date and not completed."""
        if self.completed or self.due_date is None:
            return False
        return self.due_date < datetime.now()

    def next_occurrence(self) -> "Task | None":
        """Return a fresh copy of this task for its next recurrence, or None.

        Uses timedelta to shift the due date forward (e.g., +1 day for a
        daily task). Returns None if the task is not recurring.
        """
        if self.recurrence is None or self.due_date is None:
            return None
        new_due = self.due_date + self.recurrence
        return Task(
            id=f"{self.id}@{new_due.strftime('%Y%m%d%H%M')}",
            title=self.title,
            task_type=self.task_type,
            duration=self.duration,
            priority=self.priority,
            due_date=new_due,
            recurrence=self.recurrence,
            completed=False,
            description=self.description,
            pet=self.pet,
        )

    def time_label(self) -> str:
        """Return a short HH:MM label for the task's due time, or '--:--'."""
        return self.due_date.strftime("%H:%M") if self.due_date else "--:--"

    def __str__(self) -> str:
        """Return a human-readable one-line summary of the task."""
        mins = int(self.duration.total_seconds() // 60)
        status = "done" if self.completed else "todo"
        return (
            f"{self.time_label()}  {self.title} "
            f"({mins} min) [priority: {self.priority.name.lower()}] [{status}]"
        )


@dataclass
class Pet:
    """An animal being cared for, holding its own list of care tasks."""

    id: str
    name: str
    species: str
    breed: str = ""
    age: int = 0
    owner: "Owner | None" = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet and back-link the task to it."""
        task.pet = self
        self.tasks.append(task)

    def get_upcoming_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not yet completed, sorted by time."""
        upcoming = [t for t in self.tasks if not t.completed]
        return sorted(upcoming, key=_task_sort_key)

    def __str__(self) -> str:
        """Return a short description of the pet."""
        breed = f" ({self.breed})" if self.breed else ""
        return f"{self.name}{breed} - {self.species}"


@dataclass
class Owner:
    """A pet owner who manages one or more pets and their care tasks."""

    id: str
    name: str
    email: str = ""
    phone: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner and back-link it."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by its id."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def list_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across pets."""

    id: str = "default"
    tasks: list[Task] = field(default_factory=list)

    def schedule_task(self, task: Task) -> None:
        """Add a task to the scheduler's queue if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def cancel_task(self, task_id: str) -> None:
        """Remove a task from the scheduler by its id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def load_from_owner(self, owner: Owner) -> None:
        """Pull every task from the owner's pets into the scheduler."""
        for task in owner.get_all_tasks():
            self.schedule_task(task)

    def sort_by_time(self) -> list[Task]:
        """Return all scheduled tasks ordered chronologically by due time.

        Uses sorted() with a lambda key so timeless tasks sort to the end.
        """
        return sorted(self.tasks, key=lambda t: t.due_date or datetime.max)

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return scheduled tasks matching the given completion status."""
        return [t for t in self.tasks if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return scheduled tasks whose pet name matches (case-insensitive)."""
        name = pet_name.lower()
        return [t for t in self.tasks if t.pet and t.pet.name.lower() == name]

    def complete_task(self, task: Task) -> "Task | None":
        """Mark a task complete; if it recurs, schedule its next occurrence.

        Returns the newly created follow-up task, or None for one-off tasks.
        """
        task.mark_complete()
        follow_up = task.next_occurrence()
        if follow_up is not None:
            self.schedule_task(follow_up)
            if follow_up.pet is not None:
                follow_up.pet.tasks.append(follow_up)
        return follow_up

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time.

        Lightweight check: flags exact due-time matches rather than raising,
        so the caller can surface a warning without crashing.
        """
        warnings: list[str] = []
        by_time: dict[datetime, list[Task]] = {}
        for task in self.tasks:
            if task.due_date is None:
                continue
            by_time.setdefault(task.due_date, []).append(task)

        for when, clashing in by_time.items():
            if len(clashing) > 1:
                titles = ", ".join(
                    f"{t.title} ({t.pet.name if t.pet else '?'})" for t in clashing
                )
                warnings.append(
                    f"Conflict at {when.strftime('%H:%M')}: {titles}"
                )
        return warnings

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return all scheduled tasks belonging to a given pet."""
        return [t for t in self.tasks if t.pet is pet]

    def get_tasks_for_date(self, date: datetime) -> list[Task]:
        """Return all scheduled tasks due on a given calendar date."""
        due = [
            t for t in self.tasks
            if t.due_date is not None and t.due_date.date() == date.date()
        ]
        return sorted(due, key=_task_sort_key)

    def get_overdue_tasks(self) -> list[Task]:
        """Return all scheduled tasks that are past due and not completed."""
        return [t for t in self.tasks if t.is_overdue()]

    def generate_daily_plan(
        self, date: datetime, available_time: timedelta | None = None
    ) -> list[Task]:
        """Return the day's incomplete tasks ordered by priority then time.

        If ``available_time`` is given, only include tasks that fit within
        that time budget (highest priority first).
        """
        candidates = [t for t in self.get_tasks_for_date(date) if not t.completed]
        candidates.sort(key=lambda t: (-t.priority.value, _task_sort_key(t)))

        if available_time is None:
            return candidates

        plan: list[Task] = []
        remaining = available_time
        for task in candidates:
            if task.duration <= remaining:
                plan.append(task)
                remaining -= task.duration
        return plan

    def send_reminders(self) -> list[str]:
        """Return reminder messages for every overdue task."""
        return [
            f"Reminder: '{t.title}' for "
            f"{t.pet.name if t.pet else 'a pet'} is overdue."
            for t in self.get_overdue_tasks()
        ]


def _task_sort_key(task: Task) -> datetime:
    """Sort helper: order tasks by due time, pushing timeless tasks last."""
    return task.due_date or datetime.max
