"""Initial automated tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Task


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
