from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def from_str(cls, val: str) -> "Priority":
        val_upper = val.strip().upper()
        if val_upper == "LOW":
            return cls.LOW
        elif val_upper == "MEDIUM":
            return cls.MEDIUM
        elif val_upper == "HIGH":
            return cls.HIGH
        raise ValueError(f"Invalid priority: {val}. Must be 'low', 'medium', or 'high'.")

class TimeOfDay(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    ANY = "any"

    @classmethod
    def from_str(cls, val: str) -> "TimeOfDay":
        val_lower = val.strip().lower()
        for member in cls:
            if member.value == val_lower:
                return member
        raise ValueError(f"Invalid time of day: {val}. Must be 'morning', 'afternoon', 'evening', or 'any'.")

@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: Dict[str, Any] = field(default_factory=dict)

    def get_owner_details(self) -> str:
        """Returns a string summary of the owner's profile and constraints."""
        pref_str = ", ".join(f"{k}: {v}" for k, v in self.preferences.items()) if self.preferences else "None"
        return f"Owner: {self.name} | Available Time: {self.available_time_minutes} mins | Preferences: {pref_str}"

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    owner: Owner

    def get_profile(self) -> str:
        """Returns a string profile of the pet."""
        return f"{self.name} ({self.age}yo {self.breed} {self.species}) - Owned by {self.owner.name}"

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: str
    time_of_day: TimeOfDay = TimeOfDay.ANY
    is_completed: bool = False

    def update_status(self, completed: bool) -> None:
        """Updates the completion status of the task."""
        self.is_completed = completed

class Scheduler:
    def __init__(self, pet: Pet, tasks: List[Task]):
        self.pet: Pet = pet
        self.owner: Owner = pet.owner
        self.tasks: List[Task] = tasks
        self.plan: List[Dict[str, Any]] = []
        self.reasoning: str = ""

    def add_task(self, task: Task) -> None:
        """Adds a task to the scheduler's list of tasks."""
        self.tasks.append(task)


    def _format_time(self, minutes: int) -> str:
        hrs = (minutes // 60) % 24
        mins = minutes % 60
        return f"{hrs:02d}:{mins:02d}"

    def generate_plan(self) -> List[Dict[str, Any]]:
        """Generates a daily schedule based on priority and owner's time constraints."""
        self.plan = []
        reason_steps = []

        total_time_limit = self.owner.available_time_minutes
        current_used_time = 0

        # Sort tasks: Priority descending (HIGH -> MEDIUM -> LOW). 
        # Secondary sort: time of day ordering (morning -> afternoon -> evening -> any)
        def get_time_of_day_order(t: Task) -> int:
            order = {
                TimeOfDay.MORNING: 0,
                TimeOfDay.AFTERNOON: 1,
                TimeOfDay.EVENING: 2,
                TimeOfDay.ANY: 3
            }
            return order.get(t.time_of_day, 4)

        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (t.priority.value, -get_time_of_day_order(t)),
            reverse=True
        )

        # Time markers for scheduling slots (in minutes from midnight)
        morning_marker = 8 * 60      # 08:00
        afternoon_marker = 13 * 60   # 13:00
        evening_marker = 18 * 60     # 18:00

        reason_steps.append(f"Starting schedule generation for {self.pet.name}.")
        reason_steps.append(f"Owner {self.owner.name} has {total_time_limit} minutes available.")
        reason_steps.append(f"Analyzing {len(self.tasks)} total tasks, sorted by priority and preferred time of day.")

        for task in sorted_tasks:
            # Check if task duration fits within remaining time
            remaining_time = total_time_limit - current_used_time
            if task.duration_minutes > remaining_time:
                reason_steps.append(
                    f"❌ Skipped '{task.title}' (Priority: {task.priority.name}, Duration: {task.duration_minutes} min) "
                    f"because it exceeds the remaining available care time of {remaining_time} minutes."
                )
                continue

            # Determine start time slot
            start_minutes = 0
            if task.time_of_day == TimeOfDay.MORNING:
                start_minutes = morning_marker
                morning_marker += task.duration_minutes
            elif task.time_of_day == TimeOfDay.AFTERNOON:
                start_minutes = afternoon_marker
                afternoon_marker += task.duration_minutes
            elif task.time_of_day == TimeOfDay.EVENING:
                start_minutes = evening_marker
                evening_marker += task.duration_minutes
            else:  # TimeOfDay.ANY
                # Put it in the slot with the earliest running marker
                min_marker = min(morning_marker, afternoon_marker, evening_marker)
                if min_marker == morning_marker:
                    start_minutes = morning_marker
                    morning_marker += task.duration_minutes
                elif min_marker == afternoon_marker:
                    start_minutes = afternoon_marker
                    afternoon_marker += task.duration_minutes
                else:
                    start_minutes = evening_marker
                    evening_marker += task.duration_minutes

            end_minutes = start_minutes + task.duration_minutes
            current_used_time += task.duration_minutes

            self.plan.append({
                "title": task.title,
                "category": task.category,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority.name,
                "time_of_day": task.time_of_day.value,
                "start_time": self._format_time(start_minutes),
                "end_time": self._format_time(end_minutes),
                "start_minutes": start_minutes
            })

            reason_steps.append(
                f"✅ Scheduled '{task.title}' (Priority: {task.priority.name}, Duration: {task.duration_minutes} min) "
                f"at {self._format_time(start_minutes)} - {self._format_time(end_minutes)}."
            )

        # Sort the final plan chronologically for display
        self.plan.sort(key=lambda item: item["start_minutes"])

        reason_steps.append(
            f"Schedule generation complete. Scheduled {len(self.plan)} tasks, "
            f"utilizing {current_used_time} / {total_time_limit} available minutes."
        )

        self.reasoning = "\n".join(reason_steps)
        return self.plan

    def get_reasoning(self) -> str:
        """Returns the explanation of how and why the schedule was generated."""
        return self.reasoning