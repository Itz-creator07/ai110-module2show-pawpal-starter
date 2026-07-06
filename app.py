"""PawPal+ Streamlit UI.

This is the presentation layer. All real logic lives in pawpal_system.py;
this file imports those classes and wires the UI buttons to their methods.
Because Streamlit re-runs top-to-bottom on every interaction, the Owner and
Scheduler are kept in st.session_state so data persists across reruns.
"""

from datetime import datetime, timedelta

import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task, TaskType

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant.")

# --- Application memory ------------------------------------------------------
# Streamlit is stateless, so create the Owner/Scheduler once and reuse them.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(id="o1", name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

PRIORITIES = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

# --- Owner -------------------------------------------------------------------
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a pet ---------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name", value="")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    new_pet_breed = st.text_input("Breed (optional)", value="")
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet and new_pet_name.strip():
    pet_id = f"p{len(owner.pets) + 1}"
    owner.add_pet(Pet(
        id=pet_id, name=new_pet_name.strip(),
        species=new_pet_species, breed=new_pet_breed.strip(),
    ))
    st.success(f"Added {new_pet_name.strip()} to {owner.name}'s pets.")

if owner.pets:
    st.write("Your pets:", ", ".join(str(p) for p in owner.list_pets()))
else:
    st.info("No pets yet. Add one above to get started.")

st.divider()

# --- Add a task --------------------------------------------------------------
st.subheader("Schedule a Task")
if not owner.pets:
    st.caption("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_choice = st.selectbox(
            "Pet", owner.list_pets(), format_func=lambda p: p.name
        )
        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox("Type", [t.value for t in TaskType])
        task_time = st.time_input("Time", value=datetime.now().time())
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", list(PRIORITIES), index=2)
        submitted_task = st.form_submit_button("Add task")

    if submitted_task and task_title.strip():
        due = datetime.now().replace(
            hour=task_time.hour, minute=task_time.minute, second=0, microsecond=0
        )
        task = Task(
            id=f"t{len(scheduler.tasks) + 1}",
            title=task_title.strip(),
            task_type=TaskType(task_type),
            duration=timedelta(minutes=int(duration)),
            priority=PRIORITIES[priority],
            due_date=due,
        )
        pet_choice.add_task(task)
        scheduler.schedule_task(task)
        st.success(f"Scheduled '{task.title}' for {pet_choice.name}.")

st.divider()

# --- Today's schedule --------------------------------------------------------
st.subheader("Today's Schedule")

show_completed = st.checkbox("Show completed tasks", value=False)

if st.button("Generate schedule"):
    # Surface any scheduling conflicts before showing the plan.
    for warning in scheduler.detect_conflicts():
        st.warning(f"⚠️ {warning}")

    tasks = scheduler.sort_by_time()
    if not show_completed:
        tasks = [t for t in tasks if not t.completed]
    # Keep only today's tasks.
    today = datetime.now().date()
    tasks = [t for t in tasks if t.due_date and t.due_date.date() == today]

    if not tasks:
        st.info("No tasks scheduled for today yet.")
    else:
        rows = [
            {
                "Time": t.time_label(),
                "Pet": t.pet.name if t.pet else "-",
                "Task": t.title,
                "Duration (min)": int(t.duration.total_seconds() // 60),
                "Priority": t.priority.name.lower(),
                "Done": "✅" if t.completed else "",
            }
            for t in tasks
        ]
        st.success(f"Planned {len(rows)} task(s) for today.")
        st.table(rows)
