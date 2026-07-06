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
    # 1. Create Owner with 120 minutes of available care time
    owner = Owner(name="Jordan", available_time_minutes=120)

    # 2. Create at least two Pets
    mochi = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2, owner=owner)
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3, owner=owner)

    # 3. Create Tasks WITH A TIME CONFLICT (Mochi Morning Feed and Biscuit Morning Walk both at 08:00)
    tasks = [
        Task(title="Mochi Evening Brush", duration_minutes=15, priority=Priority.LOW, category="grooming", time_of_day=TimeOfDay.EVENING, pet_name="Mochi"),
        Task(title="Biscuit Afternoon Walk", duration_minutes=30, priority=Priority.HIGH, category="walk", time_of_day=TimeOfDay.AFTERNOON, pet_name="Biscuit"),
        Task(title="Mochi Morning Feed", duration_minutes=15, priority=Priority.HIGH, category="feeding", specific_time="08:00", pet_name="Mochi"), # Conflict
        Task(title="Biscuit Morning Walk", duration_minutes=25, priority=Priority.HIGH, category="walk", specific_time="08:00", pet_name="Biscuit"), # Conflict
        Task(title="Shared Playtime", duration_minutes=20, priority=Priority.MEDIUM, category="enrichment", time_of_day=TimeOfDay.AFTERNOON, pet_name="All"),
    ]

    # 4. Instantiate the Scheduler
    scheduler = Scheduler(pet=mochi, tasks=tasks)

    print("=== 1. ALL POOL TASKS (AS ADDED - OUT OF ORDER) ===")
    for t in scheduler.tasks:
        time_info = f"at {t.specific_time}" if t.specific_time else f"in {t.time_of_day.value}"
        print(f"  • [{t.pet_name}] {t.title} ({t.duration_minutes}m) {time_info} [Priority: {t.priority.name}]")

    # Run conflict detection on all tasks in the pool
    print("\n=== RUNNING POOL CONFLICT DETECTION ===")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("⚠️  Warning: Detected schedule time conflicts in the task pool!")
        for c in conflicts:
            print(f"  - {c['message']}")
    else:
        print("✅ No conflicts detected in the task pool.")

    # 5. Filter by Pet: Mochi (includes tasks specific to Mochi and 'All' shared tasks)
    print("\n=== 2. FILTERED TASKS (PET: MOCHI + SHARED) ===")
    mochi_tasks = scheduler.filter_tasks(pet_filter="Mochi")
    for t in mochi_tasks:
        time_info = f"at {t.specific_time}" if t.specific_time else f"in {t.time_of_day.value}"
        print(f"  • [{t.pet_name}] {t.title} ({t.duration_minutes}m) {time_info} [Priority: {t.priority.name}]")

    # 6. Sort the Mochi tasks using the new sort method
    print("\n=== 3. FILTERED & CHRONOLOGICALLY SORTED TASKS (PET: MOCHI) ===")
    sorted_mochi_tasks = scheduler.sort_tasks_by_time(mochi_tasks)
    for t in sorted_mochi_tasks:
        time_info = f"at {t.specific_time}" if t.specific_time else f"in {t.time_of_day.value}"
        print(f"  • [{t.pet_name}] {t.title} ({t.duration_minutes}m) {time_info} [Priority: {t.priority.name}]")

    # 7. Generate and display the plan to see how the Scheduler structures it (since we filter by Mochi, Biscuit's walk is ignored)
    print("\n=== 4. GENERATED PLAN FOR MOCHI (FILTERED & CONSTRAINED) ===")
    plan = scheduler.generate_plan(pet_filter="Mochi")
    print_pretty_schedule(owner, plan, scheduler, owner.available_time_minutes)

    # Let's generate a plan for ALL pets, which will trigger conflict resolution (skipping the lower priority/later fixed task)
    print("\n=== 5. GENERATED PLAN FOR ALL PETS (WITH CONFLICT TRIGGERED) ===")
    scheduler_all = Scheduler(pet=mochi, tasks=tasks)
    plan_all = scheduler_all.generate_plan(pet_filter="All")
    print_pretty_schedule(owner, plan_all, scheduler_all, owner.available_time_minutes)

if __name__ == "__main__":
    main()
