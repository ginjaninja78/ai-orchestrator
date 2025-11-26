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

## 🤖 AGENT ROSTER & RESPONSIBILITIES

### CORE ORCHESTRATION

#### PROMETHEUS (Master Orchestrator)
**Primary Functions:**
- Task decomposition and assignment
- Resource allocation
- Progress monitoring
- Dependency management
- Cross-agent coordination
- Status reporting to user

**Decision Authority:**
- Agent assignment
- Task prioritization
- Resource allocation
- Workflow optimization
- Sub-agent spawning approval

**Communication:**
- Receives from: User, all agents
- Sends to: All agents, user
- Frequency: Continuous
- Channel: Blackbox Cloud + direct

---

#### DOUBTFUL THOMAS (QC Gatekeeper)
**Primary Functions:**
- Code validation (99.999999999% standard)
- Test execution and verification
- Logic verification
- Security auditing
- Performance validation
- Requirement compliance checking

**Decision Authority:**
- APPROVE or REJECT all outputs
- Cannot be overridden by other agents
- Can request additional testing
- Can escalate to user
- Can request Research Team investigation

**Validation Checklist:**
```markdown
## QC VALIDATION CHECKLIST

### Code Quality
- [ ] Syntax correct
- [ ] Logic sound
- [ ] No code smells
- [ ] Follows patterns
- [ ] Properly commented
- [ ] Type hints present

### Testing
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Integration tested

### Requirements
- [ ] Meets all requirements
- [ ] No scope creep
- [ ] User stories satisfied
- [ ] Acceptance criteria met

### Security
- [ ] No vulnerabilities
- [ ] Input validated
- [ ] Secrets protected
- [ ] Auth/authz correct

### Performance
- [ ] Meets performance targets
- [ ] No memory leaks
- [ ] Efficient algorithms
- [ ] Optimized queries

### Documentation
- [ ] Code documented
- [ ] API documented
- [ ] README updated
- [ ] TODO updated

### Integration
- [ ] No breaking changes
- [ ] Dependencies satisfied
- [ ] Backward compatible
- [ ] Migration path clear
```

**Communication:**
- Receives from: All agents (work submissions)
- Sends to: Prometheus (approvals/rejections), submitting agent (feedback)
- Frequency: Per submission
- Channel: Blackbox Cloud

---

### RESEARCH & INTELLIGENCE

#### RESEARCH TEAM (Always-On Intelligence)

##### AI SCIENTIST (Lead Researcher)
**Primary Functions:**
- Continuous research on project domain
- Technology evaluation
- Best practice identification
- Innovation discovery
- Hypothesis formation and testing
- Knowledge synthesis

**Research Methodology:**
1. **PLAN**: Define research questions
2. **RESEARCH**: Gather information from multiple sources
3. **HYPOTHESIZE**: Form theories and approaches
4. **TEST**: Validate hypotheses through experimentation
5. **THEORIZE**: Develop comprehensive solutions
6. **DOCUMENT**: Capture learnings
7. **SHARE**: Distribute knowledge
8. **ITERATE**: Continuous improvement

**Research Areas:**
- Current project technologies
- Alternative approaches
- Performance optimization
- Security best practices
- Architecture patterns
- Tool capabilities
- Industry trends
- Cutting-edge innovations

**Communication:**
- Receives from: Any agent (research requests)
- Sends to: All agents (proactive findings), requesting agent (specific answers)
- Frequency: Continuous + on-demand
- Channel: Blackbox Cloud + Knowledge Base

##### RESEARCH SUB-AGENTS (Spawned as needed)
- **Technology Researcher**: Deep dives on specific technologies
- **Pattern Researcher**: Code patterns and anti-patterns
- **Performance Researcher**: Optimization strategies
- **Security Researcher**: Security best practices
- **Architecture Researcher**: System design patterns
- **Tool Researcher**: Tool capabilities and integrations
- **Innovation Researcher**: Cutting-edge techniques

---

### LIBRARY MANAGEMENT & CREATION

#### SKILLS AGENT (Skills Library Manager & Creator)
**Primary Functions:**
- Manages skills library
- Creates new skills on-the-fly
- Identifies skill gaps
- Develops training materials
- Tracks skill effectiveness
- Evolves existing skills

**Skills Library Structure:**
```
libraries/skills/
├── coding/
│   ├── languages/
│   ├── frameworks/
│   ├── patterns/
│   └── best_practices/
├── architecture/
├── testing/
├── devops/
├── problem_solving/
└── meta_skills/
    ├── learning/
    ├── collaboration/
    └── adaptation/
```

**Skill Creation Process:**
1. **IDENTIFY NEED**: Gap in current capabilities
2. **RESEARCH**: Best practices and approaches
3. **DESIGN**: Skill structure and components
4. **IMPLEMENT**: Create skill materials
5. **TEST**: Validate with real tasks
6. **DOCUMENT**: Comprehensive documentation
7. **DEPLOY**: Add to library
8. **MEASURE**: Track effectiveness
9. **REFINE**: Continuous improvement

**Skill Format:**
```markdown
# SKILL: [Name]

## Category: [Category]
## Difficulty: [Beginner/Intermediate/Advanced/Expert]
## Prerequisites: [List]

## Description
[What this skill enables]

## Components
1. **Knowledge**: [What you need to know]
2. **Techniques**: [How to apply]
3. **Tools**: [What tools to use]
4. **Patterns**: [Common patterns]

## Learning Path
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Practice Exercises
- [Exercise 1]
- [Exercise 2]

## Mastery Criteria
- [ ] Can explain concept
- [ ] Can apply in simple cases
- [ ] Can apply in complex cases
- [ ] Can teach others
- [ ] Can innovate

## Examples
[Real-world examples]

## Common Pitfalls
- [Pitfall 1]
- [Pitfall 2]

## Related Skills
- [Skill 1]
- [Skill 2]

## Resources
- [Resource 1]
- [Resource 2]
```

**Communication:**
- Receives from: Any agent (skill requests), Prometheus (skill gaps)
- Sends to: All agents (new skills), Knowledge Base
- Frequency: Continuous monitoring + on-demand creation
- Channel: Blackbox Cloud + Skills Library

**Improvement Mandate:**
- Every new skill MUST improve system capabilities
- Track skill usage and effectiveness
- Retire obsolete skills
- Merge similar skills
- Evolve based on feedback

---

#### TOOLS AGENT (Tools Library Manager & Creator)
**Primary Functions:**
- Manages tools library
- Creates new tools on-the-fly
- Integrates external tools
- Develops tool wrappers
- Tracks tool effectiveness
- Optimizes tool usage

**Tools Library Structure:**
```
libraries/tools/
├── claude_code/
│   ├── prompts/
│   ├── workflows/
│   ├── automation/
│   └── examples/
├── codex/
├── copilot/
├── jules_cli/
├── vscode/
├── github/
├── custom_tools/
│   ├── code_analysis/
│   ├── refactoring/
│   ├── testing/
│   └── deployment/
└── tool_chains/
    ├── development/
    ├── testing/
    └── deployment/
```

**Tool Creation Process:**
1. **IDENTIFY NEED**: Task that lacks appropriate tool
2. **RESEARCH**: Existing solutions and approaches
3. **DESIGN**: Tool interface and functionality
4. **IMPLEMENT**: Build the tool
5. **TEST**: Validate with real scenarios
6. **DOCUMENT**: Usage guide and API
7. **INTEGRATE**: Add to orchestrator
8. **DEPLOY**: Make available to agents
9. **MEASURE**: Track usage and effectiveness
10. **REFINE**: Continuous improvement

**Tool Format:**
```markdown
# TOOL: [Name]

## Category: [Category]
## Purpose: [What it does]
## Input: [What it takes]
## Output: [What it produces]

## Description
[Detailed description]

## Usage
```python
from tools import ToolName

tool = ToolName(config)
result = tool.execute(input_data)
```

## Parameters
- `param1`: [Description]
- `param2`: [Description]

## Examples
### Example 1: [Scenario]
```python
# Code example
```

### Example 2: [Scenario]
```python
# Code example
```

## Error Handling
- `ErrorType1`: [How to handle]
- `ErrorType2`: [How to handle]

## Performance
- Time Complexity: [O(n)]
- Space Complexity: [O(n)]
- Typical Runtime: [X seconds]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Integration Points
- Works with: [Tool 1, Tool 2]
- Used by: [Agent 1, Agent 2]

## Metrics
- Usage count: [Tracked]
- Success rate: [Tracked]
- Average runtime: [Tracked]

## Changelog
- v1.0: Initial release
- v1.1: [Changes]
```

**Communication:**
- Receives from: Any agent (tool requests), Engineering agents
- Sends to: All agents (new tools), Tools Library
- Frequency: Continuous monitoring + on-demand creation
- Channel: Blackbox Cloud + Tools Library

**Improvement Mandate:**
- Every new tool MUST improve efficiency or capability
- Track tool usage metrics
- Deprecate unused tools
- Optimize frequently-used tools
- Create tool chains for common workflows

---

#### MCP SERVER AGENT (MCP Integration & Creation)
**Primary Functions:**
- Manages MCP (Model Context Protocol) servers
- Creates new MCP servers on-the-fly
- Integrates external MCP servers
- Optimizes context sharing
- Tracks MCP effectiveness
- Evolves MCP capabilities

**MCP Library Structure:**
```
libraries/mcp/
├── servers/
│   ├── code_context/
│   ├── project_context/
│   ├── knowledge_base/
│   ├── tool_registry/
│   └── custom/
├── clients/
│   ├── claude_code/
│   ├── codex/
│   └── custom/
├── protocols/
│   ├── context_sharing/
│   ├── tool_invocation/
│   └── state_management/
└── integrations/
    ├── vscode/
    ├── github/
    └── blackbox_cloud/
```

**MCP Server Creation Process:**
1. **IDENTIFY NEED**: Context or capability gap
2. **DESIGN PROTOCOL**: Define MCP interface
3. **IMPLEMENT SERVER**: Build MCP server
4. **CREATE CLIENT**: Build client integrations
5. **TEST**: Validate with real scenarios
6. **DOCUMENT**: Protocol and usage
7. **DEPLOY**: Make available to agents
8. **INTEGRATE**: Connect to orchestrator
9. **MEASURE**: Track effectiveness
10. **REFINE**: Continuous improvement

**MCP Server Format:**
```python
"""
MCP Server: [Name]

Purpose: [What context/capability it provides]
Protocol Version: [Version]
"""

from mcp import Server, Context, Tool

class CustomMCPServer(Server):
    """
    [Description of what this MCP server does]
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.context_store = {}
        self.tools = []
    
    async def get_context(self, query: str) -> Context:
        """
        Retrieve relevant context based on query.
        
        Args:
            query: Context query
            
        Returns:
            Context object with relevant information
        """
        pass
    
    async def register_tool(self, tool: Tool):
        """
        Register a new tool with the MCP server.
        
        Args:
            tool: Tool to register
        """
        pass
    
    async def invoke_tool(self, tool_name: str, params: dict):
        """
        Invoke a registered tool.
        
        Args:
            tool_name: Name of tool to invoke
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        pass
```

**Communication:**
- Receives from: Any agent (MCP requests), Engineering agents
- Sends to: All agents (new MCPs), MCP Library
- Frequency: Continuous + on-demand
- Channel: MCP Protocol + Blackbox Cloud

**Improvement Mandate:**
- Every new MCP MUST improve context sharing or tool access
- Track MCP usage and performance
- Optimize slow MCPs
- Create MCP chains for complex workflows
- Ensure backward compatibility

---

### ENGINEERING & CREATION COLLABORATION

#### Engineering Team Collaboration Protocol

**When New Tool/Skill/MCP Needed:**

1. **IDENTIFICATION** (Any Agent)
   ```
   Agent identifies need → Reports to Prometheus → 
   Prometheus evaluates → Assigns to appropriate library agent
   ```

2. **RESEARCH** (Library Agent + Research Team)
   ```
   Library agent requests research → Research Team investigates →
   Findings shared → Best approach identified
   ```

3. **DESIGN** (Library Agent + Engineering Agents)
   ```
   Library agent creates design → Engineering agents review →
   Feedback incorporated → Design finalized
   ```

4. **IMPLEMENTATION** (Engineering Agents + Library Agent)
   ```
   Engineering agents build → Library agent guides →
   Iterative development → Testing throughout
   ```

5. **VALIDATION** (Doubtful Thomas + Library Agent)
   ```
   Implementation complete → Submit to QC →
   Doubtful Thomas validates → Approve or reject
   ```

6. **DEPLOYMENT** (Library Agent)
   ```
   QC approved → Add to library → Document →
   Announce to all agents → Track usage
   ```

7. **MEASUREMENT** (Library Agent + Prometheus)
   ```
   Track usage → Measure effectiveness →
   Gather feedback → Identify improvements
   ```

8. **EVOLUTION** (Library Agent + Engineering Agents)
   ```
   Analyze metrics → Identify improvements →
   Implement enhancements → Redeploy →
   System improves!
   ```

**Collaboration Channels:**
- **Blackbox Cloud**: Real-time communication
- **Shared Context**: Design docs, specs, feedback
- **Code Repository**: Version control
- **Knowledge Base**: Documentation and learnings

---

### ENVIRONMENT & OPERATIONS

#### ENVIRONMENT TECH (Error Resolution & System Management)
**Primary Functions:**
- Monitors system health
- Detects and fixes errors
- Manages dependencies
- Handles environment issues
- Debugs problems
- Prevents future issues

**Error Resolution Process:**
1. **DETECT**: Monitor for errors
2. **ANALYZE**: Identify root cause
3. **RESEARCH**: Check knowledge base + Research Team
4. **FIX**: Implement solution
5. **TEST**: Verify fix works
6. **DOCUMENT**: Add to knowledge base
7. **PREVENT**: Implement safeguards

**Capabilities:**
- Direct VS Code control
- Terminal access
- File system operations
- Package management
- Environment variables
- Process management
- Log analysis
- Automated debugging

**Communication:**
- Receives from: All agents (error reports), system monitors
- Sends to: Prometheus (status), affected agents (resolutions)
- Frequency: Continuous monitoring + on-demand
- Channel: Blackbox Cloud + direct system access

---

#### SPECIALIZED CODING AGENTS

##### ARCHITECT AGENT
- System design
- Technology selection
- Scalability planning
- Integration architecture
- Works with: Skills Agent, Tools Agent, MCP Agent

##### BACKEND AGENT
- Server-side logic
- API development
- Database design
- Business logic
- Works with: Tools Agent for backend tools

##### FRONTEND AGENT
- UI/UX implementation
- Component development
- State management
- Responsive design
- Works with: Tools Agent for frontend tools

##### DEVOPS AGENT
- CI/CD pipelines
- Deployment automation
- Infrastructure as code
- Monitoring setup
- Works with: Tools Agent, MCP Agent

##### TESTING AGENT
- Test strategy
- Test creation
- Test automation
- Quality metrics
- Works with: Doubtful Thomas, Tools Agent

##### DOCUMENTATION AGENT
- Code documentation
- API documentation
- User guides
- Architecture docs
- Works with: Skills Agent, all other agents

**All Coding Agents:**
- Can spawn sub-agents
- Submit work to Doubtful Thomas
- Request Research Team help
- Use library agents for new tools/skills/MCPs
- Report to Prometheus

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
6. Check if new tools/skills/MCPs needed
7. Create initial task breakdown
8. Present plan to user for approval

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
- Identify tool/skill/MCP needs

**Output:**
- Updated PROJECT_TODO.md
- Created TASK_TYPE_TODO.md files
- Agent assignments made
- Dependencies mapped
- Tool/skill/MCP creation tasks if needed

---

#### 3. TOOL/SKILL/MCP CREATION (If Needed)
```
Need identified → Library agent assigned → 
Engineering collaboration → Creation → Deployment
```

**Priority:** HIGH (blocks other work)

**Process:**
1. Library agent (Skills/Tools/MCP) receives assignment
2. Research Team investigates best approaches
3. Library agent designs solution
4. Engineering agents implement
5. Doubtful Thomas validates
6. Library agent deploys
7. All agents notified
8. Original task can proceed

**Timeline:** Must be completed before dependent tasks

---

#### 4. TASK ASSIGNMENT
```
Subtasks created → Agents assigned → AGENT_TODO.md created
```

**Assignment Criteria:**
- Agent specialization match
- Agent current workload
- Task priority
- Dependencies ready
- Resources available
- Tools/skills/MCPs available

---

#### 5. TASK EXECUTION
```
Agent works → Updates TODO → Uses tools/skills/MCPs →
Submits to QC → Prometheus monitors
```

**Execution Rules:**
- Update AGENT_TODO.md every 30 minutes
- Report blockers immediately
- Request help when stuck >1 hour
- Use appropriate tools from library
- Apply relevant skills
- Leverage MCPs for context
- Test continuously
- Document decisions

---

#### 6. QUALITY CONTROL
```
Work complete → Submit to Doubtful Thomas → Validation → Approve/Reject
```

**Doubtful Thomas Process:**
1. Initial review
2. Testing
3. Integration check
4. Decision: APPROVE or REJECT

**If REJECT:**
- Detailed feedback to agent
- Agent fixes issues
- Resubmit to QC
- Repeat until approved

---

#### 7. TASK COMPLETION
```
QC approved → Prometheus verifies → Updates TODO →
Notifies user → Captures learnings
```

**Completion Actions:**
1. Mark task complete in all TODO levels
2. Update project progress
3. Notify dependent tasks
4. Capture learnings
5. Update metrics
6. Report to user

**Learning Capture:**
- What worked well
- What didn't work
- New tools/skills/MCPs created
- Improvements identified
- Add to knowledge base

---

## 🔄 CONTINUOUS IMPROVEMENT MANDATE

### System Evolution Rules

#### EVERY Addition MUST Improve System

**When New Tool Created:**
- [ ] Solves a real problem
- [ ] More efficient than alternatives
- [ ] Well documented
- [ ] Tested thoroughly
- [ ] Integrated properly
- [ ] Metrics tracked
- [ ] System capability increased

**When New Skill Created:**
- [ ] Fills a capability gap
- [ ] Teachable and learnable
- [ ] Measurable mastery
- [ ] Practical applications
- [ ] Well documented
- [ ] Agents can apply it
- [ ] System capability increased

**When New MCP Created:**
- [ ] Improves context sharing
- [ ] Enables new capabilities
- [ ] Efficient protocol
- [ ] Well documented
- [ ] Properly integrated
- [ ] Metrics tracked
- [ ] System capability increased

#### Improvement Metrics

**Track for Every Addition:**
```python
class ImprovementMetrics:
    # Before addition
    baseline_capability: float
    baseline_efficiency: float
    baseline_quality: float
    
    # After addition
    new_capability: float
    new_efficiency: float
    new_quality: float
    
    # Improvement
    capability_increase: float  # Must be > 0
    efficiency_increase: float  # Must be > 0
    quality_increase: float     # Must be > 0
    
    # Usage
    usage_count: int
    success_rate: float
    user_satisfaction: float
```

**Minimum Improvement Thresholds:**
- Capability: +5% or new capability unlocked
- Efficiency: +10% faster or easier
- Quality: +5% better outcomes

**If Improvement Not Met:**
- Reject addition
- Refine and retry
- Or abandon if not viable

---

### Knowledge Accumulation

**Every Task Adds to Knowledge Base:**

1. **Technical Knowledge**
   - Code patterns discovered
   - Solutions to problems
   - Best practices identified
   - Anti-patterns to avoid

2. **Process Knowledge**
   - Workflow optimizations
   - Collaboration patterns
   - Communication improvements
   - Efficiency gains

3. **Domain Knowledge**
   - Project-specific learnings
   - Industry insights
   - User preferences
   - Business logic

4. **Meta Knowledge**
   - How agents learn
   - What works best
   - Common pitfalls
   - Success patterns

**Knowledge Sharing:**
- Automatic: All learnings to knowledge base
- Proactive: Research Team shares findings
- On-demand: Agents query knowledge base
- Continuous: Knowledge base always growing

---

### Adaptation Mechanisms

#### Agent Specialization
```
Agent performs task → Measures performance →
Identifies strengths → Specializes further →
Becomes expert in domain
```

#### Tool Optimization
```
Tool used → Metrics collected → Performance analyzed →
Bottlenecks identified → Optimizations implemented →
Tool improves
```

#### Workflow Refinement
```
Workflow executed → Efficiency measured →
Bottlenecks identified → Process improved →
Workflow optimized
```

#### Prompt Evolution
```
Prompt used → Results measured → Effectiveness analyzed →
Prompt refined → A/B tested → Best version kept
```

---

## 🎯 AGENT COMMUNICATION PROTOCOLS

### Communication Channels

#### 1. BLACKBOX CLOUD (Primary)
**URL:** https://cloud.blackbox.ai/

**Usage:**
- Cross-agent messaging
- Shared context storage
- Real-time collaboration
- Knowledge sharing
- Status broadcasting

**Message Format:**
```json
{
  "from": "agent_name",
  "to": "agent_name|all|team_name",
  "type": "request|response|notification|broadcast",
  "priority": "low|medium|high|critical",
  "subject": "Brief subject",
  "body": "Detailed message",
  "context": {
    "task_id": "task_123",
    "project_id": "project_456",
    "related_agents": ["agent1", "agent2"]
  },
  "attachments": [
    {"type": "code", "content": "..."},
    {"type": "document", "url": "..."}
  ],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### 2. TODO SYSTEM (Status)
**Usage:**
- Task status updates
- Progress tracking
- Blocker reporting
- Completion notifications

**Update Frequency:**
- Every 30 minutes during active work
- Immediately on status change
- Immediately on blocker
- Immediately on completion

#### 3. KNOWLEDGE BASE (Persistent)
**Usage:**
- Store learnings
- Share discoveries
- Document decisions
- Archive solutions

**Structure:**
```
knowledge_base/
├── technical/
│   ├── code_patterns/
│   ├── solutions/
│   └── best_practices/
├── process/
│   ├── workflows/
│   ├── collaboration/
│   └── optimizations/
├── domain/
│   ├── project_specific/
│   ├── industry/
│   └── business_logic/
└── meta/
    ├── learning/
    ├── success_patterns/
    └── pitfalls/
```

#### 4. DIRECT (Urgent)
**Usage:**
- Critical errors
- Urgent blockers
- Emergency escalation
- Immediate coordination

**When to Use:**
- System failure
- Security issue
- Data loss risk
- User-blocking issue

---

### Communication Rules

#### Request for Help
```markdown
## HELP REQUEST

**From:** [Agent Name]
**To:** [Target Agent/Team]
**Priority:** [Low/Medium/High/Critical]
**Task:** [Task ID and description]

**Problem:**
[Clear description of the problem]

**What I've Tried:**
1. [Attempt 1]
2. [Attempt 2]
3. [Attempt 3]

**What I Need:**
[Specific help needed]

**Blocker:** [Yes/No]
**Impact:** [What's blocked]
**Urgency:** [Timeline]
```

#### Status Update
```markdown
## STATUS UPDATE

**Agent:** [Name]
**Task:** [ID and description]
**Status:** [In Progress/Blocked/Complete]
**Progress:** [X%]

**Completed:**
- [Item 1]
- [Item 2]

**In Progress:**
- [Item 3] (60% done)

**Upcoming:**
- [Item 4]

**Blockers:**
- [None or description]

**ETA:** [Timestamp]
**Next Update:** [Timestamp]
```

#### Knowledge Share
```markdown
## KNOWLEDGE SHARE

**From:** [Agent Name]
**Category:** [Technical/Process/Domain/Meta]
**Relevance:** [Who should know this]

**Discovery:**
[What was learned]

**Context:**
[When/how it was discovered]

**Application:**
[How to use this knowledge]

**Examples:**
[Concrete examples]

**Added to KB:** [Location in knowledge base]
```

---

## 🔐 SECURITY & SAFETY PROTOCOLS

### Access Control

#### Agent Permissions

**PROMETHEUS:**
- Full system access
- Can spawn/terminate agents
- Can modify workflows
- Can access all data
- Cannot override QC rejections

**DOUBTFUL THOMAS:**
- Read access to all code
- Execute tests
- Cannot modify production code
- Can reject any submission
- Cannot be overridden

**RESEARCH TEAM:**
- Read access to all data
- Write access to knowledge base
- Cannot modify production code
- Can access external resources

**LIBRARY AGENTS (Skills/Tools/MCP):**
- Full access to respective libraries
- Can create new items
- Can modify existing items
- Submit to QC for validation
- Cannot deploy without QC approval

**ENVIRONMENT TECH:**
- Full system access
- Can modify environment
- Can install packages
- Can fix errors
- All changes logged

**CODING AGENTS:**
- Read/write in assigned areas
- Cannot modify other agents' code
- Submit all work to QC
- Can request library additions

**SUB-AGENTS:**
- Limited to parent's permissions
- Cannot access outside scope
- Inherit parent context
- Report only to parent

---

### Safety Rules

#### Code Execution
- All code reviewed by Doubtful Thomas
- No direct production deployment
- Sandbox testing first
- Rollback plan required
- User approval for major changes

#### Data Handling
- No hardcoded secrets
- Encrypt sensitive data
- Validate all inputs
- Sanitize all outputs
- Log all access

#### Error Handling
- Graceful degradation
- No silent failures
- Comprehensive logging
- Automatic recovery attempts
- Escalate if can't resolve

#### Resource Management
- Monitor resource usage
- Prevent resource exhaustion
- Clean up after tasks
- Optimize continuously
- Alert on anomalies

---

## 📊 METRICS & MONITORING

### System Metrics

#### Performance Metrics
```python
class SystemMetrics:
    # Task Metrics
    tasks_completed: int
    tasks_in_progress: int
    tasks_blocked: int
    average_completion_time: float
    task_success_rate: float
    
    # Agent Metrics
    agent_utilization: Dict[str, float]
    agent_efficiency: Dict[str, float]
    agent_quality_score: Dict[str, float]
    
    # Quality Metrics
    qc_approval_rate: float
    qc_rejection_rate: float
    bug_rate: float
    test_coverage: float
    
    # Library Metrics
    tools_created: int
    skills_created: int
    mcps_created: int
    library_usage: Dict[str, int]
    
    # Improvement Metrics
    capability_growth: float
    efficiency_growth: float
    quality_growth: float
    knowledge_base_size: int
```

#### Monitoring Dashboard

**Real-Time View:**
```
┌─────────────────────────────────────────┐
│ AI ORCHESTRATOR - SYSTEM STATUS         │
├─────────────────────────────────────────┤
│ Active Agents: 12/15                    │
│ Tasks In Progress: 8                    │
│ Tasks Completed Today: 24               │
│ QC Approval Rate: 94%                   │
│ System Health: ████████░░ 85%           │
├─────────────────────────────────────────┤
│ AGENT STATUS                            │
│ ├─ Prometheus: Active (Orchestrating)   │
│ ├─ Doubtful Thomas: Active (Reviewing)  │
│ ├─ Research Team: Active (3 sub-agents) │
│ ├─ Skills Agent: Active (Creating)      │
│ ├─ Tools Agent: Active (Optimizing)     │
│ ├─ MCP Agent: Idle                      │
│ ├─ Environment Tech: Monitoring         │
│ └─ Coding Agents: 5 Active, 1 Idle      │
├─────────────────────────────────────────┤
│ RECENT IMPROVEMENTS                     │
│ ├─ New Tool: Code Analyzer (+15% speed) │
│ ├─ New Skill: Advanced Debugging        │
│ ├─ MCP Optimized: Context Server (-30%) │
│ └─ Workflow Refined: Testing (+20%)     │
├─────────────────────────────────────────┤
│ ALERTS                                  │
│ └─ None                                 │
└─────────────────────────────────────────┘
```

---

## 🎓 LEARNING & EVOLUTION

### Learning Loop

```
Execute → Measure → Analyze → Learn → Improve → Execute
```

#### 1. EXECUTE
- Agents perform tasks
- Use tools, skills, MCPs
- Follow workflows
- Collaborate

#### 2. MEASURE
- Collect metrics
- Track performance
- Monitor quality
- Record outcomes
