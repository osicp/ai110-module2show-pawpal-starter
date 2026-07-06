import pytest
from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TimeOfDay

def test_owner_pet_creation():
    owner = Owner(name="Alice", available_time_minutes=60, preferences={"outdoor_only": True})
    pet = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3, owner=owner)

    assert pet.name == "Biscuit"
    assert pet.owner.name == "Alice"
    assert "Alice" in owner.get_owner_details()
    assert "Biscuit" in pet.get_profile()

def test_priority_timeofday_from_str():
    assert Priority.from_str("high") == Priority.HIGH
    assert Priority.from_str(" MEDIUM ") == Priority.MEDIUM
    assert Priority.from_str("low") == Priority.LOW
    with pytest.raises(ValueError):
        Priority.from_str("invalid")

    assert TimeOfDay.from_str("morning") == TimeOfDay.MORNING
    assert TimeOfDay.from_str(" afternoon ") == TimeOfDay.AFTERNOON
    assert TimeOfDay.from_str("evening") == TimeOfDay.EVENING
    assert TimeOfDay.from_str("any") == TimeOfDay.ANY
    with pytest.raises(ValueError):
        TimeOfDay.from_str("invalid")

def test_task_status_update():
    task = Task(title="Morning feeding", duration_minutes=10, priority=Priority.HIGH, category="Feeding")
    assert not task.is_completed
    task.update_status(True)
    assert task.is_completed

def test_scheduler_task_addition():
    owner = Owner(name="Charlie", available_time_minutes=60)
    pet = Pet(name="Biscuit", species="Dog", breed="Poodle", age=4, owner=owner)
    scheduler = Scheduler(pet=pet, tasks=[])
    
    assert len(scheduler.tasks) == 0
    new_task = Task(title="Walk", duration_minutes=20, priority=Priority.HIGH, category="walk")
    scheduler.add_task(new_task)
    assert len(scheduler.tasks) == 1
    assert scheduler.tasks[0] == new_task

def test_scheduler_greedy_time_constraint():

    # Owner has 60 minutes available
    owner = Owner(name="Bob", available_time_minutes=60)
    pet = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2, owner=owner)

    # 4 tasks totaling 100 minutes. 
    # High Priority: Walk (30 min)
    # High Priority: Feed (15 min)
    # Medium Priority: Grooming (30 min) -> should be skipped because 30+15+30 = 75 > 60
    # Low Priority: Play (25 min) -> should also be skipped
    tasks = [
        Task(title="Grooming", duration_minutes=30, priority=Priority.MEDIUM, category="grooming", time_of_day=TimeOfDay.AFTERNOON),
        Task(title="Walk", duration_minutes=30, priority=Priority.HIGH, category="walk", time_of_day=TimeOfDay.MORNING),
        Task(title="Feed", duration_minutes=15, priority=Priority.HIGH, category="feeding", time_of_day=TimeOfDay.MORNING),
        Task(title="Play", duration_minutes=25, priority=Priority.LOW, category="enrichment", time_of_day=TimeOfDay.ANY),
    ]

    scheduler = Scheduler(pet=pet, tasks=tasks)
    plan = scheduler.generate_plan()

    # The scheduled tasks should be Walk and Feed (total 45 mins).
    scheduled_titles = [item["title"] for item in plan]
    assert "Walk" in scheduled_titles
    assert "Feed" in scheduled_titles
    assert "Grooming" not in scheduled_titles
    assert "Play" not in scheduled_titles

    # Verify times assigned
    # Walk starts at 8:00 AM (480 mins) and ends at 8:30 (510 mins)
    # Feed starts at 8:30 AM (510 mins) and ends at 8:45 (525 mins)
    walk_item = next(item for item in plan if item["title"] == "Walk")
    feed_item = next(item for item in plan if item["title"] == "Feed")
    
    assert walk_item["start_time"] == "08:00"
    assert walk_item["end_time"] == "08:30"
    assert feed_item["start_time"] == "08:30"
    assert feed_item["end_time"] == "08:45"

    # Verify reasoning contains explanations for scheduled and skipped tasks
    reasoning = scheduler.get_reasoning()
    assert "Scheduled 'Walk'" in reasoning
    assert "Scheduled 'Feed'" in reasoning
    assert "Skipped 'Grooming'" in reasoning
    assert "Skipped 'Play'" in reasoning
    assert "45 / 60 available minutes" in reasoning
