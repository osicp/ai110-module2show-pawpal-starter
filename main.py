from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TimeOfDay

# Helper dictionary to get emojis for categories
CATEGORY_ICONS = {
    "walk": "🦮",
    "feeding": "🥣",
    "meds": "💊",
    "enrichment": "🧸",
    "grooming": "✂️",
    "other": "🐾"
}

def print_pretty_schedule(owner, plan, scheduler, total_time_limit):
    # Calculate utilization metrics
    total_scheduled_time = sum(item["duration_minutes"] for item in plan)
    utilization_pct = (total_scheduled_time / total_time_limit) * 100
    
    # Generate progress bar
    bar_width = 30
    filled_blocks = int(round((total_scheduled_time / total_time_limit) * bar_width))
    progress_bar = "█" * min(filled_blocks, bar_width) + "░" * (bar_width - min(filled_blocks, bar_width))

    print("\n┌" + "─" * 72 + "┐")
    print(f"│{'🐾 TODAY\'S PET CARE PLAN: ' + owner.name.upper():^72}│")
    print("└" + "─" * 72 + "┘")
    
    print(f"  Time Budget: {total_time_limit} mins | Scheduled: {total_scheduled_time} mins ({utilization_pct:.1f}% Used)")
    print(f"  Progress:    [{progress_bar}]\n")
    
    # Print schedule table
    print("┌──────────────┬──────────────────────────────┬────────────┬─────────────┐")
    print("│ TIME SLOT    │ TASK DESCRIPTION             │ DURATION   │ PRIORITY    │")
    print("├──────────────┼──────────────────────────────┼────────────┼─────────────┤")
    
    for item in plan:
        icon = CATEGORY_ICONS.get(item["category"].lower(), "🐾")
        desc = f"{icon} {item['title']}"
        time_slot = f"{item['start_time']} - {item['end_time']}"
        duration = f"{item['duration_minutes']} min"
        priority = item["priority"]
        
        print(f"│ {time_slot:<12} │ {desc:<28} │ {duration:<10} │ {priority:<11} │")
        
    print("└──────────────┴──────────────────────────────┴────────────┴─────────────┘")

    # Parse and print skipped tasks from reasoning log
    skipped = [line for line in scheduler.get_reasoning().split("\n") if "❌" in line]
    if skipped:
        print("\n⚠️  SKIPPED TASKS (Exceeded Time Budget):")
        for line in skipped:
            # Clean up log for terminal display
            cleaned_line = line.replace("❌ Skipped ", "").strip()
            print(f"  • {cleaned_line}")
    print()

def main():
    # 1. Create Owner with 60 minutes of available care time
    owner = Owner(name="Jordan", available_time_minutes=60)

    # 2. Create at least two Pets
    mochi = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2, owner=owner)
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3, owner=owner)

    # 3. Create at least three Tasks with different times (totaling 80 mins, which exceeds Jordan's 60 mins limit)
    tasks = [
        Task(title="Biscuit Morning Walk", duration_minutes=30, priority=Priority.HIGH, category="walk", time_of_day=TimeOfDay.MORNING),
        Task(title="Mochi Morning Feed", duration_minutes=15, priority=Priority.HIGH, category="feeding", time_of_day=TimeOfDay.MORNING),
        Task(title="Biscuit Grooming Session", duration_minutes=20, priority=Priority.MEDIUM, category="grooming", time_of_day=TimeOfDay.AFTERNOON),
        Task(title="Mochi Laser Playtime", duration_minutes=15, priority=Priority.LOW, category="enrichment", time_of_day=TimeOfDay.EVENING)
    ]

    # 4. Instantiate the Scheduler and generate the daily plan
    scheduler = Scheduler(pet=mochi, tasks=tasks)
    plan = scheduler.generate_plan()

    # 5. Print the pretty formatted schedule
    print_pretty_schedule(owner, plan, scheduler, owner.available_time_minutes)

if __name__ == "__main__":
    main()
