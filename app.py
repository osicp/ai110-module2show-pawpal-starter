import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TimeOfDay

# Set page config
st.set_page_config(page_title="PawPal+ — Smart Pet Care Planner", page_icon="🐾", layout="wide")

# Custom CSS for premium aesthetics
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background-color: #F8F9FD;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #4D96FF 0%, #6BCB77 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .stSubheader {
        font-weight: 600;
        color: #1A1A2E;
    }
    
    /* Cards and Containers */
    .plan-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
        border: 1px solid #EAECEF;
        transition: transform 0.2s ease;
    }
    
    .plan-card:hover {
        transform: translateY(-2px);
    }
    
    /* Custom Timeline Item styling */
    .timeline-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-top: 15px;
    }
    
    .timeline-item {
        display: flex;
        align-items: center;
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        border: 1px solid #F1F3F5;
        border-left-width: 6px;
        border-left-style: solid;
    }
    
    .timeline-item.morning { border-left-color: #4D96FF; }
    .timeline-item.afternoon { border-left-color: #FFB319; }
    .timeline-item.evening { border-left-color: #9B72AA; }
    .timeline-item.any { border-left-color: #6BCB77; }
    
    .time-slot {
        font-weight: 700;
        color: #1A1A2E;
        min-width: 110px;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .task-details {
        flex-grow: 1;
        padding-left: 15px;
    }
    
    .task-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #2D3748;
        margin: 0;
    }
    
    .task-meta {
        font-size: 0.85rem;
        color: #718096;
        margin-top: 4px;
        display: flex;
        gap: 12px;
    }
    
    .badge {
        padding: 2px 8px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
    }
    
    .badge-high { background-color: #FFF5F5; color: #E53E3E; }
    .badge-medium { background-color: #FFFDF0; color: #D69E2E; }
    .badge-low { background-color: #F0FFF4; color: #38A169; }
    
    /* Styled buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4D96FF 0%, #6BCB77 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(77, 150, 255, 0.2);
        transition: all 0.2s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(77, 150, 255, 0.3);
    }
    
    .reason-box {
        background-color: #F7FAFC;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #CBD5E0;
        font-family: monospace;
        font-size: 0.9rem;
        color: #4A5568;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- SESSION STATE INITIALIZATION (Pattern A) -----------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time_minutes=60)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="Mochi", species="Cat", breed="Ragdoll", age=2, owner=st.session_state.owner)

if "scheduler" not in st.session_state:
    # Seed default tasks inside our Task class instances
    default_tasks = [
        Task(title="Morning Walk", duration_minutes=30, priority=Priority.HIGH, category="walk", time_of_day=TimeOfDay.MORNING),
        Task(title="Breakfast Feed", duration_minutes=15, priority=Priority.HIGH, category="feeding", time_of_day=TimeOfDay.MORNING),
        Task(title="Teeth Grooming", duration_minutes=10, priority=Priority.MEDIUM, category="grooming", time_of_day=TimeOfDay.AFTERNOON),
        Task(title="Fetch Playtime", duration_minutes=25, priority=Priority.MEDIUM, category="enrichment", time_of_day=TimeOfDay.ANY),
        Task(title="Brush Fur", duration_minutes=15, priority=Priority.LOW, category="grooming", time_of_day=TimeOfDay.EVENING)
    ]
    st.session_state.scheduler = Scheduler(pet=st.session_state.pet, tasks=default_tasks)

# Render main header with nice emojis
st.markdown('<h1 class="app-header">🐾 PawPal+ Care Assistant</h1>', unsafe_allow_html=True)
st.markdown("##### *Helping busy pet owners maintain consistent, optimized care for their companions.*")
st.divider()

# Layout split into two columns: Left for Inputs, Right for Generated Schedule
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.subheader("👤 Profiles & Constraints")
    
    # Grid for Owner & Pet info (updating the session state objects directly)
    c1, c2 = st.columns(2)
    with c1:
        owner_name = st.text_input("Owner Name", value=st.session_state.owner.name)
        available_time = st.number_input("Available Time (min/day)", min_value=10, max_value=1440, value=st.session_state.owner.available_time_minutes, step=10)
    with c2:
        pet_name = st.text_input("Pet Name", value=st.session_state.pet.name)
        
        # Selectbox mapping index to preserve current species selection
        species_options = ["Dog", "Cat", "Bird", "Rabbit", "Reptile", "Other"]
        species_index = species_options.index(st.session_state.pet.species) if st.session_state.pet.species in species_options else 1
        species = st.selectbox("Species", species_options, index=species_index)
        
    c3, c4 = st.columns(2)
    with c3:
        breed = st.text_input("Breed", value=st.session_state.pet.breed)
    with c4:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=st.session_state.pet.age, step=1)
    
    # Keep attributes in session state synced with UI inputs
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time_minutes = available_time
    st.session_state.pet.name = pet_name
    st.session_state.pet.species = species
    st.session_state.pet.breed = breed
    st.session_state.pet.age = age
    
    st.divider()
    
    st.subheader("📝 Add Pet Care Task")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        task_title = st.text_input("Task Title", placeholder="e.g. Give Medication")
        category = st.selectbox("Category", ["walk", "feeding", "meds", "enrichment", "grooming", "other"])
    with t_col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15, step=5)
        priority = st.selectbox("Priority Level", ["low", "medium", "high"], index=1)
        
    time_of_day = st.selectbox("Preferred Time of Day", ["any", "morning", "afternoon", "evening"], index=0)
    
    # Task actions (Add and Clear)
    act_col1, act_col2 = st.columns([1, 1])
    with act_col1:
        # Add Task via Scheduler method
        if st.button("➕ Add Task"):
            if task_title.strip():
                new_task = Task(
                    title=task_title.strip(),
                    duration_minutes=int(duration),
                    priority=Priority.from_str(priority),
                    category=category,
                    time_of_day=TimeOfDay.from_str(time_of_day)
                )
                # Calling our actual Scheduler.add_task method
                st.session_state.scheduler.add_task(new_task)
                st.success(f"Added task: '{task_title}'!")
                st.rerun()
            else:
                st.error("Task title cannot be empty!")
    with act_col2:
        if st.button("🗑️ Clear All Tasks"):
            st.session_state.scheduler.tasks = []
            st.info("Cleared all tasks.")
            st.rerun()
            
    # List Current Tasks from Scheduler's internal list
    st.markdown("### Current Task List Pool")
    if st.session_state.scheduler.tasks:
        task_df = []
        for i, t in enumerate(st.session_state.scheduler.tasks):
            task_df.append({
                "Index": i + 1,
                "Title": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority.name,
                "Time Preference": t.time_of_day.value.capitalize(),
                "Category": t.category.capitalize()
            })
        st.table(task_df)
    else:
        st.info("No tasks in the pool. Add some tasks above to begin planning.")

with col_right:
    st.subheader("📅 Daily Schedule & Planner")
    
    # Build schedule button
    if st.button("⚡ Generate Daily Schedule"):
        if not st.session_state.scheduler.tasks:
            st.warning("Please add some tasks to the pool before generating the schedule.")
        else:
            # Solve schedule and retrieve reasoning using methods we wrote
            plan = st.session_state.scheduler.generate_plan()
            reasoning = st.session_state.scheduler.get_reasoning()
            
            # Summarize metrics
            total_scheduled_time = sum(item["duration_minutes"] for item in plan)
            utilization = (total_scheduled_time / st.session_state.owner.available_time_minutes) * 100
            
            st.markdown(f"#### Generated Schedule for **{st.session_state.pet.name}**")
            st.markdown(f"*{st.session_state.pet.get_profile()}*")
            
            # Metrics Row
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Scheduled Tasks", f"{len(plan)} / {len(st.session_state.scheduler.tasks)}")
            m_col2.metric("Scheduled Duration", f"{total_scheduled_time} mins")
            m_col3.metric("Available Time Limit", f"{st.session_state.owner.available_time_minutes} mins")
            
            # Progress bar for time utilization
            st.progress(min(utilization / 100.0, 1.0))
            st.caption(f"Time utilization: {total_scheduled_time} / {st.session_state.owner.available_time_minutes} minutes ({utilization:.1f}%)")
            
            # Display Plan Timeline
            if plan:
                st.markdown("### ⏰ Daily Timeline")
                st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
                for item in plan:
                    # Select icons based on category
                    category_icons = {
                        "walk": "🦮",
                        "feeding": "🥣",
                        "meds": "💊",
                        "enrichment": "🧸",
                        "grooming": "✂️",
                        "other": "🐾"
                    }
                    icon = category_icons.get(item["category"].lower(), "🐾")
                    
                    time_class = item["time_of_day"].lower()
                    p_name = item["priority"].lower()
                    
                    st.markdown(
                        f"""
                        <div class="timeline-item {time_class}">
                            <div class="time-slot">
                                ⏱️ {item["start_time"]} - {item["end_time"]}
                            </div>
                            <div class="task-details">
                                <p class="task-title">{icon} {item["title"]}</p>
                                <div class="task-meta">
                                    <span>⏳ {item["duration_minutes"]} mins</span>
                                    <span>📂 {item["category"].capitalize()}</span>
                                    <span class="badge badge-{p_name}">{item["priority"]} Priority</span>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No tasks could be scheduled within your available time limit!")
            
            # Display Reasoning
            st.markdown("### 🧠 Scheduling Engine Reasoning")
            st.markdown(f'<div class="reason-box">{reasoning}</div>', unsafe_allow_html=True)
    else:
        # Initial call-to-action placeholder
        st.info(f"Click the 'Generate Daily Schedule' button above to plan {st.session_state.pet.name}'s day based on your available time constraints.")
