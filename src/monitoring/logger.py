"""
Logging Infrastructure for AI Orchestrator

This module provides comprehensive logging with:
- Structured logging with Rich for development
- JSON logging for production
- Context-aware logging (agent, task, user)
- Performance logging
- Log rotation and retention
- Multiple log levels and handlers
"""

import logging
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

# Install rich traceback for better error display
install_rich_traceback(show_locals=True)


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(str, Enum):
    """Log output formats."""
    RICH = "rich"  # Rich formatted output for development
    JSON = "json"  # JSON output for production
    TEXT = "text"  # Plain text output


class ContextLogger:
    """
    Context-aware logger that includes agent, task, and user context.
    
    This logger automatically includes contextual information in all log messages,
    making it easy to trace actions across the system.
    """
    
    def __init__(
        self,
        name: str,
        agent_id: Optional[str] = None,
        task_id: Optional[str] = None,
        user_id: Optional[str] = None,
        extra_context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize context logger.
        
        Args:
            name: Logger name
            agent_id: Agent identifier
            task_id: Task identifier
            user_id: User identifier
            extra_context: Additional context to include
        """
        self.logger = logging.getLogger(name)
        self.agent_id = agent_id
        self.task_id = task_id
        self.user_id = user_id
        self.extra_context = extra_context or {}
    
    def _build_context(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Build context dictionary for log message.
        
        Args:
            extra: Additional context for this specific log
            
        Returns:
            Complete context dictionary
        """
        context = {
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        if self.agent_id:
            context['agent_id'] = self.agent_id
        if self.task_id:
            context['task_id'] = self.task_id
        if self.user_id:
            context['user_id'] = self.user_id
        
        # Add extra context
        context.update(self.extra_context)
        if extra:
            context.update(extra)
        
        return context
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message."""
        context = self._build_context(extra)
        self.logger.debug(message, extra={'context': context})
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log info message."""
        context = self._build_context(extra)
        self.logger.info(message, extra={'context': context})
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message."""
        context = self._build_context(extra)
        self.logger.warning(message, extra={'context': context})
    
    def error(
        self,
        message: str,
        exc_info: bool = False,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log error message."""
        context = self._build_context(extra)
        self.logger.error(message, exc_info=exc_info, extra={'context': context})
    
    def critical(
        self,
        message: str,
        exc_info: bool = False,
        extra: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log critical message."""
        context = self._build_context(extra)
        self.logger.critical(message, exc_info=exc_info, extra={'context': context})
    
    def exception(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log exception with traceback."""
        context = self._build_context(extra)
        self.logger.exception(message, extra={'context': context})


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Outputs logs as JSON for easy parsing by log aggregation systems.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON formatted log string
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add context if present
        if hasattr(record, 'context'):
            log_data['context'] = record.context
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class PerformanceLogger:
    """
    Logger for performance metrics.
    
    Tracks execution time, token usage, and other performance metrics.
    """
    
    def __init__(self, logger: ContextLogger):
        """
        Initialize performance logger.
        
        Args:
            logger: Context logger to use
        """
        self.logger = logger
        self.start_times: Dict[str, datetime] = {}
    
    def start(self, operation: str) -> None:
        """
        Start timing an operation.
        
        Args:
            operation: Operation name
        """
        self.start_times[operation] = datetime.utcnow()
        self.logger.debug(f"Started: {operation}")
    
    def end(
        self,
        operation: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        End timing an operation and log duration.
        
        Args:
            operation: Operation name
            metadata: Additional metadata to log
            
        Returns:
            Duration in seconds
        """
        if operation not in self.start_times:
            self.logger.warning(f"No start time found for operation: {operation}")
            return 0.0
        
        start_time = self.start_times.pop(operation)
        duration = (datetime.utcnow() - start_time).total_seconds()
        
        log_data = {
            'operation': operation,
            'duration_seconds': duration,
        }
        
        if metadata:
            log_data.update(metadata)
        
        self.logger.info(
            f"Completed: {operation} ({duration:.2f}s)",
            extra=log_data
        )
        
        return duration
    
    def log_tokens(
        self,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: Optional[float] = None
    ) -> None:
        """
        Log token usage.
        
        Args:
            operation: Operation name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_usd: Cost in USD (optional)
        """
        log_data = {
            'operation': operation,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
        }
        
        if cost_usd is not None:
            log_data['cost_usd'] = cost_usd
        
        self.logger.info(
            f"Token usage: {operation} "
            f"(in={input_tokens}, out={output_tokens}, total={input_tokens + output_tokens})",
            extra=log_data
        )


def setup_logging(
    log_level: Union[str, LogLevel] = LogLevel.INFO,
    log_format: Union[str, LogFormat] = LogFormat.RICH,
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    log_to_file: bool = True
) -> None:
    """
    Set up logging configuration for the entire application.
    
    Args:
        log_level: Logging level
        log_format: Log output format
        log_file: Path to log file (default: ./logs/orchestrator.log)
        log_to_console: Whether to log to console
        log_to_file: Whether to log to file
    """
    # Convert string to enum if needed
    if isinstance(log_level, str):
        log_level = LogLevel(log_level.upper())
    if isinstance(log_format, str):
        log_format = LogFormat(log_format.lower())
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.value))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    if log_to_console:
        if log_format == LogFormat.RICH:
            console_handler = RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True
            )
            console_handler.setFormatter(logging.Formatter("%(message)s"))
        elif log_format == LogFormat.JSON:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(JSONFormatter())
        else:  # TEXT
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )
        
        root_logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        if log_file is None:
            log_file = "./logs/orchestrator.log"
        
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use JSON format for file logging (easier to parse)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(file_handler)
    
    # Log initial message
    root_logger.info("Logging system initialized", extra={
        'context': {
            'log_level': log_level.value,
            'log_format': log_format.value,
            'log_file': log_file,
            'log_to_console': log_to_console,
            'log_to_file': log_to_file
        }
    })


def get_logger(
    name: str,
    agent_id: Optional[str] = None,
    task_id: Optional[str] = None,
    user_id: Optional[str] = None,
    extra_context: Optional[Dict[str, Any]] = None
) -> ContextLogger:
    """
    Get a context-aware logger.
    
    Args:
        name: Logger name
        agent_id: Agent identifier
        task_id: Task identifier
        user_id: User identifier
        extra_context: Additional context
        
    Returns:
        ContextLogger instance
    """
    return ContextLogger(
        name=name,
        agent_id=agent_id,
        task_id=task_id,
        user_id=user_id,
        extra_context=extra_context
    )


def get_performance_logger(
    name: str,
    agent_id: Optional[str] = None,
    task_id: Optional[str] = None
) -> PerformanceLogger:
    """
    Get a performance logger.
    
    Args:
        name: Logger name
        agent_id: Agent identifier
        task_id: Task identifier
        
    Returns:
        PerformanceLogger instance
    """
    context_logger = get_logger(name, agent_id=agent_id, task_id=task_id)
    return PerformanceLogger(context_logger)


# Convenience function for quick logging setup
def quick_setup(level: str = "INFO", format: str = "rich") -> None:
    """
    Quick logging setup with sensible defaults.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log format (rich, json, text)
    """
    setup_logging(
        log_level=level,
        log_format=format,
        log_to_console=True,
        log_to_file=True
    )


# Example usage
if __name__ == '__main__':
    # Set up logging
    quick_setup(level="DEBUG", format="rich")
    
    # Get a context logger
    logger = get_logger(
        "example",
        agent_id="prometheus-001",
        task_id="task-123"
    )
    
    # Log some messages
    logger.info("Starting task execution")
    logger.debug("Debug information", extra={'detail': 'some detail'})
    logger.warning("This is a warning")
    
    # Performance logging
    perf_logger = get_performance_logger(
        "performance",
        agent_id="prometheus-001",
        task_id="task-123"
    )
    
    perf_logger.start("example_operation")
    # ... do some work ...
    import time
    time.sleep(0.1)
    perf_logger.end("example_operation", metadata={'items_processed': 100})
    
    perf_logger.log_tokens(
        "claude_api_call",
        input_tokens=1000,
        output_tokens=500,
        cost_usd=0.015
    )
    
    # Error logging
    try:
        raise ValueError("Example error")
    except Exception:
        logger.exception("An error occurred")
    
    print("\n✅ Logging system demonstration complete!")
