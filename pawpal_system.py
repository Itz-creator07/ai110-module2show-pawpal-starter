"""PawPal+ logic layer.

Class skeletons generated from the UML draft in diagrams/uml.mmd.
These are stubs only — attributes and empty method bodies. Scheduling
logic is implemented in a later phase.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class Priority(Enum):
    """How important a task is when the scheduler has to make trade-offs."""

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
class Owner:
    """A pet owner who manages one or more pets and their care tasks."""

    id: str
    name: str
    email: str = ""
    phone: str = ""
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Register a new pet under this owner."""
        raise NotImplementedError

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by its id."""
        raise NotImplementedError

    def list_pets(self) -> list["Pet"]:
        """Return all pets belonging to this owner."""
        raise NotImplementedError


@dataclass
class Pet:
    """An animal being cared for, with its own set of care tasks."""

    id: str
    name: str
    species: str
    breed: str = ""
    age: int = 0
    owner: "Owner | None" = None
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Attach a care task to this pet."""
        raise NotImplementedError

    def get_upcoming_tasks(self) -> list["Task"]:
        """Return this pet's tasks that are not yet completed."""
        raise NotImplementedError


@dataclass
class Task:
    """A single unit of pet care (e.g., a walk or a feeding)."""

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
        raise NotImplementedError

    def reschedule(self, new_date: datetime) -> None:
        """Move this task to a new due date."""
        raise NotImplementedError

    def is_overdue(self) -> bool:
        """Return True if the task is past its due date and not completed."""
        raise NotImplementedError


@dataclass
class Scheduler:
    """Organizes tasks into a daily plan based on time and priority."""

    id: str = "default"
    tasks: list["Task"] = field(default_factory=list)

    def schedule_task(self, task: "Task") -> None:
        """Add a task to the scheduler's queue."""
        raise NotImplementedError

    def cancel_task(self, task_id: str) -> None:
        """Remove a task from the scheduler by its id."""
        raise NotImplementedError

    def get_tasks_for_pet(self, pet: "Pet") -> list["Task"]:
        """Return all scheduled tasks belonging to a given pet."""
        raise NotImplementedError

    def get_tasks_for_date(self, date: datetime) -> list["Task"]:
        """Return all tasks due on a given date."""
        raise NotImplementedError

    def get_overdue_tasks(self) -> list["Task"]:
        """Return all tasks that are past due and not completed."""
        raise NotImplementedError

    def generate_daily_plan(
        self, date: datetime, available_time: timedelta
    ) -> list["Task"]:
        """Build an ordered plan for the day within the available time budget."""
        raise NotImplementedError

    def send_reminders(self) -> None:
        """Notify the owner of upcoming or overdue tasks."""
        raise NotImplementedError
