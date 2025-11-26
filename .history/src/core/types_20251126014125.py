"""
Core Type Definitions for AI Orchestrator

This module defines all the core types, enums, and data structures
used throughout the system. Following world-class standards with
comprehensive type hints and documentation.
"""

from typing import Dict, List, Optional, Any, Union, Callable, TypeVar, Generic
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# ============================================
# Enums
# ============================================

class AgentType(Enum):
    """Types of agents in the system."""
    PROMETHEUS = "prometheus"  # Master orchestrator
    DOUBTFUL_THOMAS = "doubtful_thomas"  # QC agent
    RESEARCH_TEAM = "research_team"  # Research agents
    AI_SCIENTIST = "ai_scientist"  # Lead researcher
    ENVIRONMENT_TECH = "environment_tech"  # Environment manager
    SKILLS_AGENT = "skills_agent"  # Skills library manager
    TOOLS_AGENT = "tools_agent"  # Tools library manager
    MCP_AGENT = "mcp_agent"  # MCP server manager
    ARCHITECT = "architect"  # Architecture agent
    BACKEND = "backend"  # Backend coding agent
    FRONTEND = "frontend"  # Frontend coding agent
    DEVOPS = "devops"  # DevOps agent
    TESTING = "testing"  # Testing agent
    DOCUMENTATION = "documentation"  # Documentation agent
    SETUP = "setup"  # Setup agent
    SUB_AGENT = "sub_agent"  # Generic sub-agent


class AgentStatus(Enum):
    """Agent operational status."""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    BLOCKED = "blocked"
    ERROR = "error"
    TERMINATED = "terminated"


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    SUBMITTED_QC = "submitted_qc"
    QC_APPROVED = "qc_approved"
    QC_REJECTED = "qc_rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    LOWEST = 1


class ToolType(Enum):
    """Types of tools available."""
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    COPILOT = "copilot"
    JULES_CLI = "jules_cli"
    VSCODE = "vscode"
    GITHUB = "github"
    BLACKBOX_CLOUD = "blackbox_cloud"
    CUSTOM = "custom"


class MessageType(Enum):
    """Types of inter-agent messages."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ERROR = "error"
    STATUS_UPDATE = "status_update"


class QCResult(Enum):
    """Quality control results."""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    PENDING = "pending"


# ============================================
# Data Classes
# ============================================

@dataclass
class AgentConfig:
    """Configuration for an agent."""
    agent_id: str
    agent_type: AgentType
    name: str
    role: str
    model: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 300
    retry_attempts: int = 3
    retry_delay: int = 5
    max_memory_mb: int = 200
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Represents a task in the system."""
    task_id: str
    title: str
    description: str
    task_type: str
    priority: TaskPriority
    status: TaskStatus
    assigned_agent: Optional[str] = None
    parent_task_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: Optional[int] = None  # seconds
    actual_duration: Optional[int] = None  # seconds
    progress: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class SubTask:
    """Represents a subtask within a task."""
    subtask_id: str
    parent_task_id: str
    title: str
    description: str
    status: TaskStatus
    assigned_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None


@dataclass
class AgentMessage:
    """Message between agents."""
    message_id: str
    from_agent: str
    to_agent: Union[str, List[str]]  # Single agent or list for broadcast
    message_type: MessageType
    priority: TaskPriority
    subject: str
    body: str
    context: Dict[str, Any] = field(default_factory=dict)
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    requires_response: bool = False
    response_to: Optional[str] = None


@dataclass
class QCReport:
    """Quality control report from Doubtful Thomas."""
    report_id: str
    task_id: str
    agent_id: str
    result: QCResult
    score: float  # 0.0 to 1.0
    issues: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    test_results: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    reviewed_by: str = "doubtful_thomas"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchFinding:
    """Research finding from Research Team."""
    finding_id: str
    researcher_id: str
    topic: str
    summary: str
    details: str
    sources: List[str] = field(default_factory=list)
    confidence: float = 0.0  # 0.0 to 1.0
    relevance: float = 0.0  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolDefinition:
    """Definition of a tool in the tools library."""
    tool_id: str
    name: str
    tool_type: ToolType
    description: str
    version: str
    category: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    usage_examples: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    usage_count: int = 0
    success_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillDefinition:
    """Definition of a skill in the skills library."""
    skill_id: str
    name: str
    category: str
    description: str
    difficulty: str  # beginner, intermediate, advanced, expert
    prerequisites: List[str] = field(default_factory=list)
    learning_path: List[str] = field(default_factory=list)
    mastery_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    usage_count: int = 0
    effectiveness: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPServerDefinition:
    """Definition of an MCP server."""
    server_id: str
    name: str
    description: str
    protocol_version: str
    endpoint: str
    capabilities: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    usage_count: int = 0
    performance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextEntry:
    """Entry in the context/memory system."""
    entry_id: str
    content: str
    entry_type: str  # conversation, code, decision, learning, etc.
    source: str  # agent_id or system
    importance: float = 0.5  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    accessed_at: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class SystemMetrics:
    """System-wide metrics."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    active_agents: int = 0
    tasks_pending: int = 0
    tasks_in_progress: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    qc_approval_rate: float = 0.0
    average_task_duration: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    cache_hit_rate: float = 0.0
    token_usage: int = 0
    api_calls: int = 0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkspaceConfig:
    """Workspace configuration."""
    workspace_path: Path
    max_concurrent_agents: int
    max_memory_per_agent_mb: int
    max_cache_size_gb: float
    max_log_size_gb: float
    enable_disk_cache: bool
    enable_memory_cache: bool
    use_process_pool: bool
    recommended_workers: int
    cloud_first_enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PromptTemplate:
    """Template for prompts."""
    template_id: str
    name: str
    category: str
    template: str
    variables: List[str] = field(default_factory=list)
    agent_type: Optional[AgentType] = None
    task_type: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    usage_count: int = 0
    effectiveness: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================
# Type Aliases
# ============================================

AgentID = str
TaskID = str
MessageID = str
ToolID = str
SkillID = str
MCPID = str
ContextID = str

# Generic type variable
T = TypeVar('T')


# ============================================
# Result Types
# ============================================

@dataclass
class Result(Generic[T]):
    """
    Generic result type for operations that can succeed or fail.
    
    This follows the Result pattern for explicit error handling.
    """
    success: bool
    value: Optional[T] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def ok(cls, value: T, metadata: Optional[Dict[str, Any]] = None) -> 'Result[T]':
        """Create a successful result."""
        return cls(success=True, value=value, metadata=metadata or {})
    
    @classmethod
    def err(cls, error: str, metadata: Optional[Dict[str, Any]] = None) -> 'Result[T]':
        """Create a failed result."""
        return cls(success=False, error=error, metadata=metadata or {})
    
    def unwrap(self) -> T:
        """
        Unwrap the result value.
        
        Raises:
            ValueError: If result is an error
        """
        if not self.success:
            raise ValueError(f"Cannot unwrap error result: {self.error}")
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        """Unwrap the result value or return default."""
        return self.value if self.success else default


# ============================================
# Callback Types
# ============================================

TaskCallback = Callable[[Task], None]
AgentCallback = Callable[[AgentMessage], None]
ErrorCallback = Callable[[Exception], None]
ProgressCallback = Callable[[float], None]


# ============================================
# Constants
# ============================================

# Maximum values
MAX_TASK_RETRIES = 3
MAX_MESSAGE_SIZE_KB = 1024
MAX_CONTEXT_SIZE_TOKENS = 100000
MAX_CACHE_SIZE_GB = 10.0

# Timeouts (seconds)
DEFAULT_TASK_TIMEOUT = 300
DEFAULT_AGENT_TIMEOUT = 60
DEFAULT_QC_TIMEOUT = 120

# Thresholds
QC_APPROVAL_THRESHOLD = 0.95  # 95% quality required
CACHE_HIT_RATE_TARGET = 0.80  # 80% cache hit rate target
TOKEN_EFFICIENCY_TARGET = 0.70  # 70% token efficiency target
