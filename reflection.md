# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
The three core actions a user should be able to perform are:
1. Configure constraints and profiles for the pet
2. Define a list of tasks with durations and priorities
3. Have the system generate a schedule that meets the constraints and priorities    

- Briefly describe your initial UML design.
1. Core Entities
Pet: A simple data class holding the pet's profile information (name, species, age).

Task: Represents a single care activity (id, name, duration, priority). It implements Python's __lt__ (less than) magic method so tasks can automatically be sorted by priority and duration.

Constraints: Manages the user's daily reality. It holds the total available time and provides methods to check and deduct minutes as tasks are scheduled.

2. The Orchestrator
Schedule: The central hub and "smart container." It stores the Pet it belongs to and maintains the lists of tasks (the initial pool, what was scheduled, what was deferred, and the reasoning log). Its generate() method acts as the core engine, evaluating the task pool against the constraints.

3. Class Relationships
Association: Schedule is associated with one Pet.

Aggregation: Schedule aggregates Task objects, taking ownership of organizing them from a general pool into specific outcome lists (scheduled vs. deferred).

Dependency: Schedule depends on Constraints. The generate() method requires a Constraints object to be passed in so it can execute the time-checking logic.

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
