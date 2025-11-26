# AI ORCHESTRATOR - MANAGEMENT RULES

## 🎯 PURPOSE
This document defines the rules and protocols for MANAGING the AI Orchestrator system once it's operational. These rules govern how agents interact, how tasks are orchestrated, and how the system evolves.

---

## 🏛️ GOVERNANCE STRUCTURE

### Decision Hierarchy

#### Level 1: USER (Ultimate Authority)
- Final decision on all major changes
- Can override any agent decision
- Sets project goals and priorities
- Approves/rejects deliverables
- Controls system behavior

#### Level 2: PROMETHEUS (Orchestrator)
- Decomposes user tasks
- Assigns work to agents
- Manages resources
- Coordinates dependencies
- Reports to user

#### Level 3: DOUBTFUL THOMAS (QC Gatekeeper)
- Validates all outputs
- Can reject work
- Enforces quality standards
- Cannot be overridden by other agents
- Reports to Prometheus and User

#### Level 4: SPECIALIZED AGENTS
- Execute assigned tasks
- Report to Prometheus
- Submit work to Doubtful Thomas
- Can request Research Team help
- Can spawn sub-agents

#### Level 5: SUB-AGENTS
- Execute specific subtasks
- Report to parent agent
- Limited scope and lifetime
- Inherit parent context

---

## 📋 TASK MANAGEMENT PROTOCOLS

### Task Lifecycle

#### 1. TASK SUBMISSION
```
User submits task → Prometheus receives → Logs to PROJECT_TODO.md
```

**Prometheus Actions:**
1. Acknowledge receipt
2. Analyze task complexity
3. Estimate effort and time
4. Identify required agents
5. Check for dependencies
6. Create initial task breakdown
7. Present plan to user for approval

**User Response Required:**
- Approve plan
- Request modifications
- Provide additional context
- Set priority level

---

#### 2. TASK DECOMPOSITION
```
Approved task → Prometheus decomposes → Creates task hierarchy
```

**Decomposition Rules:**
- Break into atomic, testable units
- Each subtask assigned to ONE agent
- Dependencies clearly identified
- Estimated completion time for each
- Success criteria defined
- Rollback plan included

**Output:**
- Updated PROJECT_TODO.md
- Created TASK_TYPE_TODO.md files
- Agent assignments made
- Dependencies mapped

---

#### 3. TASK ASSIGNMENT
```
Subtasks created → Agents assigned → AGENT_TODO.md created
```

**Assignment Criteria:**
- Agent specialization match
- Agent current workload
- Task priority
- Dependencies ready
- Resources available

**Agent Responsibilities:**
1. Acknowledge assignment
2. Review task requirements
3. Request clarification if needed
4. Create execution plan
5. Estimate completion time
6. Begin work

---

#### 4. TASK EXECUTION
```
Agent works → Updates TODO → Submits to QC → Prometheus monitors
```

**Execution Rules:**
- Update AGENT_TODO.md every 30 minutes
- Report blockers immediately
- Request help when stuck >1 hour
- Test continuously
- Document decisions
- Maintain context

**Progress Reporting:**
```markdown
## PROGRESS UPDATE
**Agent:** [Name]
**Task:** [Description]
**Status:** [In Progress]
**Progress:** [X%]
**Time Spent:** [Hours]
**ETA:** [Timestamp]
**Blockers:** [None/Description]
**Next Steps:** [What's next]
```

---

#### 5. QUALITY CONTROL
```
Work complete → Submit to Doubtful Thomas → Validation → Approve/Reject
```

**Doubtful Thomas Validation Process:**

**Step 1: Initial Review**
- Code syntax check
- Logic verification
- Requirement matching
- Test coverage check

**Step 2: Testing**
- Run all tests
- Check edge cases
- Verify error handling
- Performance check
- Security audit

**Step 3: Integration Check**
- Dependencies verified
- No breaking changes
- Documentation updated
- TODO updated

**Step 4: Decision**
- **APPROVE**: Forward to Prometheus, mark complete
- **REJECT**: Return to agent with detailed feedback

**Rejection Format:**
```markdown
## QC REJECTION

**Task:** [Description]
**Agent:** [Name]
**Rejection Reason:** [Category]

**Issues Found:**
1. [Issue 1 with location and description]
2. [Issue 2 with location and description]
3. [Issue 3 with location and description]

**Required Fixes:**
1. [Fix 1 with acceptance criteria]
2. [Fix 2 with acceptance criteria]
3. [Fix 3 with acceptance criteria]

**Resubmit When:**
- All issues resolved
- All tests passing
- Documentation updated

**Estimated Fix Time:** [Hours]
```

---

#### 6. TASK COMPLETION
```
