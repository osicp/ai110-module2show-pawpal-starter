# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
The three core actions a user should be able to perform are:
1. Configure constraints and profiles for the pet
2. Define a list of tasks with durations and priorities
3. Have the system generate a schedule that meets the constraints and priorities    

- Briefly describe your initial UML design.
Domain Models (Owner, Pet, Task):
Owner: Encapsulates the user profile, storing constraints (such as available_time_minutes) and customized preferences.
Pet: Represents the animal receiving care and has a one-to-one relationship with its Owner.
Task: Represents specific care items (e.g., feeding, walk) with a specified duration_minutes and priority level.
Controller (Scheduler):
Acts as the core engine. It associates a Pet, an Owner, and a list of Task objects.
It filters and prioritizes the list of tasks against the owner's constraints (available_time_minutes) to construct the final daily plan and explain the selection reasoning.

- What classes did you include, and what responsibilities did you assign to each?
1 Task class, stores task id, name, duration, and priority
2 Schedule class, runs sorting logic and produces a schedule based on constraints and tasks
3 Constraints class, tracks the boundary conditions the algorithm must operate within
4 Pet class, stores pet information such as name, type, and size

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
