# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design focuses on three main actions a pet owner should be able to perform:

1. A pet owner can add and manage information about themselves and their pets.
2. A pet owner can create, edit, and prioritize pet care tasks such as feeding, walking, grooming, and medication.
3. A pet owner can generate and view a daily schedule that organizes tasks based on available time and priority.

The main classes I plan to include are Owner, Pet, Task, and Scheduler.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. When I translated the UML into the `pawpal_system.py` skeleton, I made a few changes:

1. **Added a `Priority` enum and explicit `duration`/`priority` fields to `Task`.** My first UML only had a `TaskType`, but the README says the scheduler must plan by time available and priority. Those two values are the core inputs to scheduling, so they needed to be first-class fields on `Task` rather than an afterthought.

2. **Added `generate_daily_plan(date, available_time)` to `Scheduler`.** The original UML described the scheduler in vague terms. The app's whole purpose is to produce a daily plan within a time budget, so I gave the class a method that names that responsibility directly.

3. **Kept the `Pet.tasks` ↔ `Task.pet` link but flagged the risk.** These two references point at each other, which is convenient but can drift out of sync if I update one side and not the other. I left it in for now because it keeps navigation simple, but I noted that the logic layer will need to keep both sides consistent (or make one the single source of truth) when I implement it.

I also used Python dataclasses for `Owner`, `Pet`, `Task`, and `Scheduler` to keep the skeleton clean and avoid writing boilerplate `__init__` methods.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers three constraints: the **time** a task is due, its **priority** (low/medium/high), and the **duration** it takes. Time matters most for ordering the day, so `sort_by_time()` sorts everything chronologically. When there is a limited time budget, `generate_daily_plan()` uses priority as the tiebreaker so the most important tasks (like medication) are kept first and low-priority tasks are dropped if the day runs out of time. I decided time and priority mattered most because a pet owner's real question is "what do I do next, and what can't I skip?"

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict detector (`detect_conflicts()`) only flags tasks that share the **exact same start time**, not tasks whose durations *overlap*. For example, a 30-minute walk at 08:00 and a feeding at 08:15 would not be flagged, even though they overlap in real life. I chose exact-time matching because it is simple, fast, and easy to reason about, and it catches the most common mistake (double-booking the same slot) without the added complexity of interval math. For a lightweight pet-care helper this is a reasonable tradeoff: it warns the owner about obvious clashes and returns a friendly message instead of crashing, and true interval-overlap detection can be added later if needed.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
