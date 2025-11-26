"""
Metrics Collection for AI Orchestrator

This module provides comprehensive metrics collection for:
- Agent performance
- Task execution
- Resource usage
- API calls and costs
- Library usage
- System improvements
- Quality metrics
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import threading
from enum import Enum


class MetricType(str, Enum):
    """Types of metrics."""
    COUNTER = "counter"  # Monotonically increasing
    GAUGE = "gauge"  # Can go up or down
    HISTOGRAM = "histogram"  # Distribution of values
    SUMMARY = "summary"  # Summary statistics


@dataclass
class MetricValue:
    """A single metric value."""
    value: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class AgentMetrics:
    """Metrics for a single agent."""
    agent_id: str
    agent_type: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    tokens_used: int = 0
    api_calls: int = 0
    cost_usd: float = 0.0
    quality_score: float = 0.0
    last_active: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskMetrics:
    """Metrics for task execution."""
    total_tasks: int = 0
    pending_tasks: int = 0
    in_progress_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0
    average_duration: float = 0.0
    total_duration: float = 0.0
    qc_approval_rate: float = 0.0
    qc_rejection_rate: float = 0.0


@dataclass
class ResourceMetrics:
    """System resource metrics."""
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0
    memory_available_mb: float = 0.0
    disk_usage_gb: float = 0.0
    disk_free_gb: float = 0.0
    cache_size_mb: float = 0.0
    cache_hit_rate: float = 0.0
    active_agents: int = 0
    max_concurrent_agents: int = 0


@dataclass
class LibraryMetrics:
    """Metrics for library usage and improvements."""
    tools_created: int = 0
    skills_created: int = 0
    mcps_created: int = 0
    tools_used: int = 0
    skills_used: int = 0
    mcps_used: int = 0
    tool_effectiveness: Dict[str, float] = field(default_factory=dict)
    skill_effectiveness: Dict[str, float] = field(default_factory=dict)
    mcp_effectiveness: Dict[str, float] = field(default_factory=dict)
    improvements_measured: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CostMetrics:
    """Cost tracking metrics."""
    total_cost_usd: float = 0.0
    daily_cost_usd: float = 0.0
    monthly_cost_usd: float = 0.0
    cost_by_agent: Dict[str, float] = field(default_factory=dict)
    cost_by_model: Dict[str, float] = field(default_factory=dict)
    tokens_used: int = 0
    api_calls: int = 0
    average_cost_per_task: float = 0.0


class MetricsCollector:
    """
    Central metrics collector for the orchestrator.
    
    Thread-safe metrics collection with aggregation and export capabilities.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self._lock = threading.Lock()
        self._agent_metrics: Dict[str, AgentMetrics] = {}
        self._task_metrics = TaskMetrics()
        self._resource_metrics = ResourceMetrics()
        self._library_metrics = LibraryMetrics()
        self._cost_metrics = CostMetrics()
        self._custom_metrics: Dict[str, List[MetricValue]] = defaultdict(list)
        self._start_time = datetime.utcnow()
    
    # ============================================
    # Agent Metrics
    # ============================================
    
    def record_agent_task_completion(
        self,
        agent_id: str,
        agent_type: str,
        execution_time: float,
        success: bool = True
    ) -> None:
        """
        Record agent task completion.
        
        Args:
            agent_id: Agent identifier
            agent_type: Type of agent
            execution_time: Task execution time in seconds
            success: Whether task succeeded
        """
        with self._lock:
            if agent_id not in self._agent_metrics:
                self._agent_metrics[agent_id] = AgentMetrics(
                    agent_id=agent_id,
                    agent_type=agent_type
                )
            
            metrics = self._agent_metrics[agent_id]
            
            if success:
                metrics.tasks_completed += 1
            else:
                metrics.tasks_failed += 1
            
            metrics.total_execution_time += execution_time
            total_tasks = metrics.tasks_completed + metrics.tasks_failed
            metrics.average_execution_time = (
                metrics.total_execution_time / total_tasks if total_tasks > 0 else 0.0
            )
            metrics.last_active = datetime.utcnow()
    
    def record_agent_tokens(
        self,
        agent_id: str,
        tokens: int,
        cost_usd: float = 0.0
    ) -> None:
        """
        Record token usage by agent.
        
        Args:
            agent_id: Agent identifier
            tokens: Number of tokens used
            cost_usd: Cost in USD
        """
        with self._lock:
            if agent_id in self._agent_metrics:
                self._agent_metrics[agent_id].tokens_used += tokens
                self._agent_metrics[agent_id].cost_usd += cost_usd
                self._agent_metrics[agent_id].api_calls += 1
    
    def record_agent_quality_score(
        self,
        agent_id: str,
        score: float
    ) -> None:
        """
        Record agent quality score.
        
        Args:
            agent_id: Agent identifier
            score: Quality score (0.0 to 1.0)
        """
        with self._lock:
            if agent_id in self._agent_metrics:
                self._agent_metrics[agent_id].quality_score = score
    
    def get_agent_metrics(self, agent_id: str) -> Optional[AgentMetrics]:
        """
        Get metrics for specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            AgentMetrics if found, None otherwise
        """
        with self._lock:
            return self._agent_metrics.get(agent_id)
    
    def get_all_agent_metrics(self) -> Dict[str, AgentMetrics]:
        """Get metrics for all agents."""
        with self._lock:
            return self._agent_metrics.copy()
    
    # ============================================
    # Task Metrics
    # ============================================
    
    def record_task_created(self) -> None:
        """Record task creation."""
        with self._lock:
            self._task_metrics.total_tasks += 1
            self._task_metrics.pending_tasks += 1
    
    def record_task_started(self) -> None:
        """Record task start."""
        with self._lock:
            self._task_metrics.pending_tasks -= 1
            self._task_metrics.in_progress_tasks += 1
    
    def record_task_completed(self, duration: float) -> None:
        """
        Record task completion.
        
        Args:
            duration: Task duration in seconds
        """
        with self._lock:
            self._task_metrics.in_progress_tasks -= 1
            self._task_metrics.completed_tasks += 1
            self._task_metrics.total_duration += duration
            
            if self._task_metrics.completed_tasks > 0:
                self._task_metrics.average_duration = (
                    self._task_metrics.total_duration / 
                    self._task_metrics.completed_tasks
                )
    
    def record_task_failed(self) -> None:
        """Record task failure."""
        with self._lock:
            self._task_metrics.in_progress_tasks -= 1
            self._task_metrics.failed_tasks += 1
    
    def record_task_cancelled(self) -> None:
        """Record task cancellation."""
        with self._lock:
            if self._task_metrics.in_progress_tasks > 0:
                self._task_metrics.in_progress_tasks -= 1
            elif self._task_metrics.pending_tasks > 0:
                self._task_metrics.pending_tasks -= 1
            self._task_metrics.cancelled_tasks += 1
    
    def record_qc_result(self, approved: bool) -> None:
        """
        Record QC result.
        
        Args:
            approved: Whether QC approved
        """
        with self._lock:
            total_qc = (
                self._task_metrics.completed_tasks + 
                self._task_metrics.failed_tasks
            )
            
            if total_qc > 0:
                if approved:
                    approvals = self._task_metrics.completed_tasks
                    self._task_metrics.qc_approval_rate = approvals / total_qc
                else:
                    rejections = self._task_metrics.failed_tasks
                    self._task_metrics.qc_rejection_rate = rejections / total_qc
    
    def get_task_metrics(self) -> TaskMetrics:
        """Get task metrics."""
        with self._lock:
            return self._task_metrics
    
    # ============================================
    # Resource Metrics
    # ============================================
    
    def update_resource_metrics(
        self,
        cpu_usage: Optional[float] = None,
        memory_usage_mb: Optional[float] = None,
        memory_available_mb: Optional[float] = None,
        disk_usage_gb: Optional[float] = None,
        disk_free_gb: Optional[float] = None,
        cache_size_mb: Optional[float] = None,
        cache_hit_rate: Optional[float] = None,
        active_agents: Optional[int] = None
    ) -> None:
        """
        Update resource metrics.
        
        Args:
            cpu_usage: CPU usage percentage
            memory_usage_mb: Memory usage in MB
            memory_available_mb: Available memory in MB
            disk_usage_gb: Disk usage in GB
            disk_free_gb: Free disk space in GB
            cache_size_mb: Cache size in MB
            cache_hit_rate: Cache hit rate (0.0 to 1.0)
            active_agents: Number of active agents
        """
        with self._lock:
            if cpu_usage is not None:
                self._resource_metrics.cpu_usage_percent = cpu_usage
            if memory_usage_mb is not None:
                self._resource_metrics.memory_usage_mb = memory_usage_mb
            if memory_available_mb is not None:
                self._resource_metrics.memory_available_mb = memory_available_mb
            if disk_usage_gb is not None:
                self._resource_metrics.disk_usage_gb = disk_usage_gb
            if disk_free_gb is not None:
                self._resource_metrics.disk_free_gb = disk_free_gb
            if cache_size_mb is not None:
                self._resource_metrics.cache_size_mb = cache_size_mb
            if cache_hit_rate is not None:
                self._resource_metrics.cache_hit_rate = cache_hit_rate
            if active_agents is not None:
                self._resource_metrics.active_agents = active_agents
    
    def get_resource_metrics(self) -> ResourceMetrics:
        """Get resource metrics."""
        with self._lock:
            return self._resource_metrics
    
    # ============================================
    # Library Metrics
    # ============================================
    
    def record_library_creation(
        self,
        library_type: str,  # 'tool', 'skill', 'mcp'
        item_id: str
    ) -> None:
        """
        Record library item creation.
        
        Args:
            library_type: Type of library item
            item_id: Item identifier
        """
        with self._lock:
            if library_type == 'tool':
                self._library_metrics.tools_created += 1
            elif library_type == 'skill':
                self._library_metrics.skills_created += 1
            elif library_type == 'mcp':
                self._library_metrics.mcps_created += 1
    
    def record_library_usage(
        self,
        library_type: str,
        item_id: str
    ) -> None:
        """
        Record library item usage.
        
        Args:
            library_type: Type of library item
            item_id: Item identifier
        """
        with self._lock:
            if library_type == 'tool':
                self._library_metrics.tools_used += 1
            elif library_type == 'skill':
                self._library_metrics.skills_used += 1
            elif library_type == 'mcp':
                self._library_metrics.mcps_used += 1
    
    def record_library_effectiveness(
        self,
        library_type: str,
        item_id: str,
        effectiveness: float
    ) -> None:
        """
        Record library item effectiveness.
        
        Args:
            library_type: Type of library item
            item_id: Item identifier
            effectiveness: Effectiveness score (0.0 to 1.0)
        """
        with self._lock:
            if library_type == 'tool':
                self._library_metrics.tool_effectiveness[item_id] = effectiveness
            elif library_type == 'skill':
                self._library_metrics.skill_effectiveness[item_id] = effectiveness
            elif library_type == 'mcp':
                self._library_metrics.mcp_effectiveness[item_id] = effectiveness
    
    def record_improvement(
        self,
        improvement_type: str,
        baseline: float,
        new_value: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record system improvement.
        
        Args:
            improvement_type: Type of improvement
            baseline: Baseline value
            new_value: New value after improvement
            metadata: Additional metadata
        """
        with self._lock:
            improvement = {
                'type': improvement_type,
                'baseline': baseline,
                'new_value': new_value,
                'improvement_percent': ((new_value - baseline) / baseline * 100) if baseline > 0 else 0,
                'timestamp': datetime.utcnow().isoformat(),
                'metadata': metadata or {}
            }
            self._library_metrics.improvements_measured.append(improvement)
    
    def get_library_metrics(self) -> LibraryMetrics:
        """Get library metrics."""
        with self._lock:
            return self._library_metrics
    
    # ============================================
    # Cost Metrics
    # ============================================
    
    def record_cost(
        self,
        cost_usd: float,
        agent_id: Optional[str] = None,
        model: Optional[str] = None,
        tokens: int = 0
    ) -> None:
        """
        Record cost.
        
        Args:
            cost_usd: Cost in USD
            agent_id: Agent identifier
            model: Model used
            tokens: Number of tokens
        """
        with self._lock:
            self._cost_metrics.total_cost_usd += cost_usd
            self._cost_metrics.tokens_used += tokens
            self._cost_metrics.api_calls += 1
            
            if agent_id:
                self._cost_metrics.cost_by_agent[agent_id] = (
                    self._cost_metrics.cost_by_agent.get(agent_id, 0.0) + cost_usd
                )
            
            if model:
                self._cost_metrics.cost_by_model[model] = (
                    self._cost_metrics.cost_by_model.get(model, 0.0) + cost_usd
                )
            
            # Update average cost per task
            if self._task_metrics.completed_tasks > 0:
                self._cost_metrics.average_cost_per_task = (
                    self._cost_metrics.total_cost_usd / 
                    self._task_metrics.completed_tasks
                )
    
    def get_cost_metrics(self) -> CostMetrics:
        """Get cost metrics."""
        with self._lock:
            return self._cost_metrics
    
    # ============================================
    # Custom Metrics
    # ============================================
    
    def record_metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Record custom metric.
        
        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
        """
        with self._lock:
            metric = MetricValue(
                value=value,
                labels=labels or {}
            )
            self._custom_metrics[name].append(metric)
    
    def get_metric(self, name: str) -> List[MetricValue]:
        """
        Get custom metric values.
        
        Args:
            name: Metric name
            
        Returns:
            List of metric values
        """
        with self._lock:
            return self._custom_metrics.get(name, []).copy()
    
    # ============================================
    # Export & Summary
    # ============================================
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get complete metrics summary.
        
        Returns:
            Dictionary with all metrics
        """
        with self._lock:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()
            
            return {
                'uptime_seconds': uptime,
                'timestamp': datetime.utcnow().isoformat(),
                'agents': {
                    agent_id: asdict(metrics)
                    for agent_id, metrics in self._agent_metrics.items()
                },
                'tasks': asdict(self._task_metrics),
                'resources': asdict(self._resource_metrics),
                'library': asdict(self._library_metrics),
                'costs': asdict(self._cost_metrics),
                'custom_metrics': {
                    name: [asdict(m) for m in values]
                    for name, values in self._custom_metrics.items()
                }
            }
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._agent_metrics.clear()
            self._task_metrics = TaskMetrics()
            self._resource_metrics = ResourceMetrics()
            self._library_metrics = LibraryMetrics()
            self._cost_metrics = CostMetrics()
            self._custom_metrics.clear()
            self._start_time = datetime.utcnow()


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """
    Get global metrics collector instance.
    
    Returns:
        MetricsCollector instance
    """
    global _metrics_collector
    
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    
    return _metrics_collector


# Convenience functions
def record_agent_task(
    agent_id: str,
    agent_type: str,
    execution_time: float,
    success: bool = True
) -> None:
    """Record agent task completion."""
    get_metrics_collector().record_agent_task_completion(
        agent_id, agent_type, execution_time, success
    )


def record_tokens(agent_id: str, tokens: int, cost_usd: float = 0.0) -> None:
    """Record token usage."""
    get_metrics_collector().record_agent_tokens(agent_id, tokens, cost_usd)


def get_summary() -> Dict[str, Any]:
    """Get metrics summary."""
    return get_metrics_collector().get_summary()
