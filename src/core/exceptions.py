"""
Custom Exceptions for AI Orchestrator

This module defines all custom exceptions used throughout the system.
Following world-class standards with clear exception hierarchy and
comprehensive error information.
"""

from typing import Optional, Dict, Any


# ============================================
# Base Exception
# ============================================

class OrchestratorException(Exception):
    """
    Base exception for all orchestrator errors.
    
    All custom exceptions inherit from this to allow catching
    all orchestrator-specific errors.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            'error_type': self.__class__.__name__,
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details
        }


# ============================================
# Agent Exceptions
# ============================================

class AgentException(OrchestratorException):
    """Base exception for agent-related errors."""
    pass


class AgentNotFoundError(AgentException):
    """Raised when an agent cannot be found."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            f"Agent not found: {agent_id}",
            error_code="AGENT_NOT_FOUND",
            details={'agent_id': agent_id}
        )


class AgentInitializationError(AgentException):
    """Raised when agent initialization fails."""
    
    def __init__(self, agent_id: str, reason: str):
        super().__init__(
            f"Failed to initialize agent {agent_id}: {reason}",
            error_code="AGENT_INIT_FAILED",
            details={'agent_id': agent_id, 'reason': reason}
        )


class AgentBusyError(AgentException):
    """Raised when agent is busy and cannot accept new tasks."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            f"Agent {agent_id} is busy",
            error_code="AGENT_BUSY",
            details={'agent_id': agent_id}
        )


class AgentTerminatedError(AgentException):
    """Raised when trying to use a terminated agent."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            f"Agent {agent_id} has been terminated",
            error_code="AGENT_TERMINATED",
            details={'agent_id': agent_id}
        )


# ============================================
# Task Exceptions
# ============================================

class TaskException(OrchestratorException):
    """Base exception for task-related errors."""
    pass


class TaskNotFoundError(TaskException):
    """Raised when a task cannot be found."""
    
    def __init__(self, task_id: str):
        super().__init__(
            f"Task not found: {task_id}",
            error_code="TASK_NOT_FOUND",
            details={'task_id': task_id}
        )


class TaskValidationError(TaskException):
    """Raised when task validation fails."""
    
    def __init__(self, task_id: str, validation_errors: list):
        super().__init__(
            f"Task validation failed for {task_id}",
            error_code="TASK_VALIDATION_FAILED",
            details={'task_id': task_id, 'errors': validation_errors}
        )


class TaskExecutionError(TaskException):
    """Raised when task execution fails."""
    
    def __init__(self, task_id: str, reason: str):
        super().__init__(
            f"Task execution failed for {task_id}: {reason}",
            error_code="TASK_EXECUTION_FAILED",
            details={'task_id': task_id, 'reason': reason}
        )


class TaskTimeoutError(TaskException):
    """Raised when task execution times out."""
    
    def __init__(self, task_id: str, timeout: int):
        super().__init__(
            f"Task {task_id} timed out after {timeout} seconds",
            error_code="TASK_TIMEOUT",
            details={'task_id': task_id, 'timeout': timeout}
        )


class TaskDependencyError(TaskException):
    """Raised when task dependencies cannot be resolved."""
    
    def __init__(self, task_id: str, missing_dependencies: list):
        super().__init__(
            f"Task {task_id} has unresolved dependencies",
            error_code="TASK_DEPENDENCY_ERROR",
            details={'task_id': task_id, 'missing': missing_dependencies}
        )


class TaskCancelledError(TaskException):
    """Raised when a task is cancelled."""
    
    def __init__(self, task_id: str, reason: Optional[str] = None):
        super().__init__(
            f"Task {task_id} was cancelled" + (f": {reason}" if reason else ""),
            error_code="TASK_CANCELLED",
            details={'task_id': task_id, 'reason': reason}
        )


# ============================================
# Configuration Exceptions
# ============================================

class ConfigurationException(OrchestratorException):
    """Base exception for configuration errors."""
    pass


class ConfigurationNotFoundError(ConfigurationException):
    """Raised when configuration file is not found."""
    
    def __init__(self, config_path: str):
        super().__init__(
            f"Configuration file not found: {config_path}",
            error_code="CONFIG_NOT_FOUND",
            details={'config_path': config_path}
        )


class ConfigurationValidationError(ConfigurationException):
    """Raised when configuration validation fails."""
    
    def __init__(self, validation_errors: list):
        super().__init__(
            "Configuration validation failed",
            error_code="CONFIG_VALIDATION_FAILED",
            details={'errors': validation_errors}
        )


class InvalidConfigurationError(ConfigurationException):
    """Raised when configuration is invalid."""
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Invalid configuration for {field}: {reason}",
            error_code="INVALID_CONFIG",
            details={'field': field, 'reason': reason}
        )


# ============================================
# Memory Exceptions
# ============================================

class MemoryException(OrchestratorException):
    """Base exception for memory/context errors."""
    pass


class MemoryStorageError(MemoryException):
    """Raised when memory storage operation fails."""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"Memory storage {operation} failed: {reason}",
            error_code="MEMORY_STORAGE_ERROR",
            details={'operation': operation, 'reason': reason}
        )


class MemoryRetrievalError(MemoryException):
    """Raised when memory retrieval fails."""
    
    def __init__(self, query: str, reason: str):
        super().__init__(
            f"Memory retrieval failed for query '{query}': {reason}",
            error_code="MEMORY_RETRIEVAL_ERROR",
            details={'query': query, 'reason': reason}
        )


class ContextSizeExceededError(MemoryException):
    """Raised when context size exceeds limits."""
    
    def __init__(self, current_size: int, max_size: int):
        super().__init__(
            f"Context size {current_size} exceeds maximum {max_size}",
            error_code="CONTEXT_SIZE_EXCEEDED",
            details={'current_size': current_size, 'max_size': max_size}
        )


# ============================================
# Integration Exceptions
# ============================================

class IntegrationException(OrchestratorException):
    """Base exception for integration errors."""
    pass


class APIException(IntegrationException):
    """Raised when API call fails."""
    
    def __init__(self, api_name: str, status_code: Optional[int], reason: str):
        super().__init__(
            f"API call to {api_name} failed: {reason}",
            error_code="API_ERROR",
            details={'api': api_name, 'status_code': status_code, 'reason': reason}
        )


class RateLimitException(IntegrationException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, service: str, retry_after: Optional[int] = None):
        super().__init__(
            f"Rate limit exceeded for {service}",
            error_code="RATE_LIMIT_EXCEEDED",
            details={'service': service, 'retry_after': retry_after}
        )


class AuthenticationError(IntegrationException):
    """Raised when authentication fails."""
    
    def __init__(self, service: str, reason: str):
        super().__init__(
            f"Authentication failed for {service}: {reason}",
            error_code="AUTH_FAILED",
            details={'service': service, 'reason': reason}
        )


class ToolExecutionError(IntegrationException):
    """Raised when tool execution fails."""
    
    def __init__(self, tool_name: str, reason: str):
        super().__init__(
            f"Tool execution failed for {tool_name}: {reason}",
            error_code="TOOL_EXECUTION_FAILED",
            details={'tool': tool_name, 'reason': reason}
        )


# ============================================
# QC Exceptions
# ============================================

class QCException(OrchestratorException):
    """Base exception for QC errors."""
    pass


class QCRejectionError(QCException):
    """Raised when QC rejects work."""
    
    def __init__(self, task_id: str, issues: list):
        super().__init__(
            f"QC rejected task {task_id}",
            error_code="QC_REJECTED",
            details={'task_id': task_id, 'issues': issues}
        )


class QCValidationError(QCException):
    """Raised when QC validation fails."""
    
    def __init__(self, task_id: str, validation_errors: list):
        super().__init__(
            f"QC validation failed for task {task_id}",
            error_code="QC_VALIDATION_FAILED",
            details={'task_id': task_id, 'errors': validation_errors}
        )


# ============================================
# Resource Exceptions
# ============================================

class ResourceException(OrchestratorException):
    """Base exception for resource errors."""
    pass


class ResourceExhaustedError(ResourceException):
    """Raised when system resources are exhausted."""
    
    def __init__(self, resource_type: str, current: float, limit: float):
        super().__init__(
            f"Resource exhausted: {resource_type} ({current}/{limit})",
            error_code="RESOURCE_EXHAUSTED",
            details={'resource': resource_type, 'current': current, 'limit': limit}
        )


class MemoryLimitExceededError(ResourceException):
    """Raised when memory limit is exceeded."""
    
    def __init__(self, current_mb: float, limit_mb: float):
        super().__init__(
            f"Memory limit exceeded: {current_mb}MB / {limit_mb}MB",
            error_code="MEMORY_LIMIT_EXCEEDED",
            details={'current_mb': current_mb, 'limit_mb': limit_mb}
        )


class DiskSpaceError(ResourceException):
    """Raised when disk space is insufficient."""
    
    def __init__(self, required_gb: float, available_gb: float):
        super().__init__(
            f"Insufficient disk space: need {required_gb}GB, have {available_gb}GB",
            error_code="DISK_SPACE_ERROR",
            details={'required_gb': required_gb, 'available_gb': available_gb}
        )


class ConcurrencyLimitError(ResourceException):
    """Raised when concurrency limit is reached."""
    
    def __init__(self, current: int, limit: int):
        super().__init__(
            f"Concurrency limit reached: {current}/{limit}",
            error_code="CONCURRENCY_LIMIT",
            details={'current': current, 'limit': limit}
        )


# ============================================
# Library Exceptions
# ============================================

class LibraryException(OrchestratorException):
    """Base exception for library errors."""
    pass


class ToolNotFoundError(LibraryException):
    """Raised when tool is not found in library."""
    
    def __init__(self, tool_id: str):
        super().__init__(
            f"Tool not found: {tool_id}",
            error_code="TOOL_NOT_FOUND",
            details={'tool_id': tool_id}
        )


class SkillNotFoundError(LibraryException):
    """Raised when skill is not found in library."""
    
    def __init__(self, skill_id: str):
        super().__init__(
            f"Skill not found: {skill_id}",
            error_code="SKILL_NOT_FOUND",
            details={'skill_id': skill_id}
        )


class MCPNotFoundError(LibraryException):
    """Raised when MCP server is not found."""
    
    def __init__(self, mcp_id: str):
        super().__init__(
            f"MCP server not found: {mcp_id}",
            error_code="MCP_NOT_FOUND",
            details={'mcp_id': mcp_id}
        )


# ============================================
# Validation Exceptions
# ============================================

class ValidationException(OrchestratorException):
    """Base exception for validation errors."""
    pass


class InvalidInputError(ValidationException):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, value: Any, reason: str):
        super().__init__(
            f"Invalid input for {field}: {reason}",
            error_code="INVALID_INPUT",
            details={'field': field, 'value': str(value), 'reason': reason}
        )


class SchemaValidationError(ValidationException):
    """Raised when schema validation fails."""
    
    def __init__(self, schema: str, errors: list):
        super().__init__(
            f"Schema validation failed for {schema}",
            error_code="SCHEMA_VALIDATION_FAILED",
            details={'schema': schema, 'errors': errors}
        )


# ============================================
# Communication Exceptions
# ============================================

class CommunicationException(OrchestratorException):
    """Base exception for communication errors."""
    pass


class MessageDeliveryError(CommunicationException):
    """Raised when message delivery fails."""
    
    def __init__(self, message_id: str, recipient: str, reason: str):
        super().__init__(
            f"Failed to deliver message {message_id} to {recipient}: {reason}",
            error_code="MESSAGE_DELIVERY_FAILED",
            details={'message_id': message_id, 'recipient': recipient, 'reason': reason}
        )


class BlackboxCloudError(CommunicationException):
    """Raised when Blackbox Cloud communication fails."""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"Blackbox Cloud {operation} failed: {reason}",
            error_code="BLACKBOX_CLOUD_ERROR",
            details={'operation': operation, 'reason': reason}
        )


# ============================================
# Utility Functions
# ============================================

def handle_exception(exc: Exception) -> Dict[str, Any]:
    """
    Convert any exception to a standardized error dictionary.
    
    Args:
        exc: Exception to handle
        
    Returns:
        Standardized error dictionary
    """
    if isinstance(exc, OrchestratorException):
        return exc.to_dict()
    
    return {
        'error_type': exc.__class__.__name__,
        'error_code': 'UNKNOWN_ERROR',
        'message': str(exc),
        'details': {}
    }
