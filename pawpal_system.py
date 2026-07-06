from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: Dict[str, Any] = field(default_factory=dict)

    def get_owner_details(self) -> str:
        """Returns a string summary of the owner's profile and constraints."""
        pass

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    owner: Owner

    def get_profile(self) -> str:
        """Returns a string profile of the pet."""
        pass

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # 'low', 'medium', 'high'
    category: str
    is_completed: bool = False

    def update_status(self, completed: bool) -> None:
        """Updates the completion status of the task."""
        pass

class Scheduler:
    def __init__(self, pet: Pet, owner: Owner, tasks: List[Task]):
        self.pet: Pet = pet
        self.owner: Owner = owner
        self.tasks: List[Task] = tasks
        self.plan: List[Dict[str, Any]] = []
        self.reasoning: str = ""

    def generate_plan(self) -> List[Dict[str, Any]]:
        """Generates a daily schedule based on priority and owner's time constraints."""
        pass

    def get_reasoning(self) -> str:
        """Returns the explanation of how and why the schedule was generated."""
        pass