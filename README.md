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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
┌────────────────────────────────────────────────────────────────────────┐
│                    🐾 TODAY'S PET CARE PLAN: JORDAN                    │
└────────────────────────────────────────────────────────────────────────┘
  Time Limit: 60 mins | Scheduled: 55 mins (91.7% Used)
  Progress:   [██████████████████████████████████████████░░░░]
┌──────────────┬──────────────────────────────┬────────────┬─────────────┐
│ TIME SLOT    │ TASK DESCRIPTION             │ DURATION   │ PRIORITY    │
├──────────────┼──────────────────────────────┼────────────┼─────────────┤
│ 08:00 - 08:30│ 🦮 Biscuit Morning Walk      │ 30 min     │ HIGH        │
│ 08:30 - 08:45│ 🥣 Mochi Morning Feed        │ 15 min     │ HIGH        │
│ 13:00 - 13:10│ ✂️  Biscuit Grooming Session  │ 10 min     │ MEDIUM      │
└──────────────┴──────────────────────────────┴────────────┴─────────────┘
⚠️ SKIPPED TASKS (Exceeded Time Budget):
  • 🧸 Mochi Laser Playtime (15 min) [LOW]
    └─ Reason: Exceeded remaining care time limit by 10 mins.



## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

Our pet care scheduler incorporates advanced decision-making and logic to handle real-world scheduling needs:

### 1. Chronological & Priority Task Sorting
*   **Method**: `Scheduler.sort_tasks_by_time(tasks)`
*   **Behavior**: Sorts any list of tasks by prioritizing fixed-time tasks (those with specific `HH:MM` start times) chronologically first. Flexible tasks (without start times) are sorted next based on their preferred `TimeOfDay` window (`Morning` -> `Afternoon` -> `Evening` -> `Any`) and sub-sorted by Priority (High -> Medium -> Low).

### 2. Multi-Pet & Status Filtering
*   **Method**: `Scheduler.filter_tasks(pet_filter, status_filter, tasks)`
*   **Behavior**: Filters any list of tasks down by:
    *   **Pet Name**: Filters to a specific pet's tasks (e.g. `"Mochi"`) while retaining shared tasks owned by `"All"`.
    *   **Completion Status**: Filters to either `"Pending"` tasks or `"Completed"` tasks.

### 3. Basic Conflict Detection
*   **Method**: `Scheduler.detect_conflicts(tasks)`
*   **Behavior**: Scans the task pool for overlapping fixed start times (e.g., two tasks scheduled at `08:00` where the first task's duration overlaps the second's start). It returns warning objects with description messages that are displayed as warning alerts in the UI and skipped during schedule generation.

### 4. Recurring Task Auto-Generation
*   **Methods**: `Task.update_status(completed)` & `Scheduler.mark_task_complete(task)`
*   **Behavior**: When a task marked as `"daily"` or `"weekly"` is completed, the scheduler automatically calculates the next due date using Python's `timedelta` (e.g., today + 1 day for daily, today + 7 days for weekly) and generates a new, pending `Task` instance in the pool.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
