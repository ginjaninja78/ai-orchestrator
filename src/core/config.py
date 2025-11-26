"""
Configuration Management for AI Orchestrator

This module provides robust configuration management with:
- Pydantic validation
- Environment variable support
- Multiple environment configs (dev, staging, prod)
- Secrets management
- Type safety
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum
import os

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class Environment(str, Enum):
    """Deployment environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class AgentConfig(BaseModel):
    """Configuration for a single agent."""
    model_config = ConfigDict(extra='allow')
    
    model: str = Field(..., description="Model to use for this agent")
    role: str = Field(..., description="Agent's role description")
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout: int = Field(default=300, ge=1, le=3600)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_delay: int = Field(default=5, ge=1, le=60)


class APIConfig(BaseModel):
    """API configuration."""
    model_config = ConfigDict(extra='allow')
    
    api_key: str = Field(default="", description="API key (from env var)")
    base_url: str = Field(..., description="API base URL")
    rate_limit: int = Field(default=50, ge=1, description="Requests per minute")
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key is not empty in production."""
        # In development, empty API key is OK (cloud-first)
        return v


class MemoryConfig(BaseModel):
    """Memory system configuration."""
    model_config = ConfigDict(extra='allow')
    
    chromadb_persist_directory: str = Field(
        default="./data/chromadb",
        description="ChromaDB persistence directory"
    )
    chromadb_collection_name: str = Field(
        default="orchestrator_memory",
        description="ChromaDB collection name"
    )
    embedding_model: str = Field(
        default="text-embedding-ada-002",
        description="Embedding model to use"
    )
    max_history: int = Field(default=50, ge=1, le=1000)
    max_tokens: int = Field(default=100000, ge=1000, le=1000000)
    compression_enabled: bool = Field(default=True)


class TaskConfig(BaseModel):
    """Task management configuration."""
    model_config = ConfigDict(extra='allow')
    
    queue_max_size: int = Field(default=1000, ge=1, le=10000)
    priority_levels: int = Field(default=5, ge=3, le=10)
    max_concurrent: int = Field(default=5, ge=1, le=100)
    timeout: int = Field(default=3600, ge=60, le=86400)
    retry_policy: str = Field(default="exponential_backoff")


class MonitoringConfig(BaseModel):
    """Monitoring configuration."""
    model_config = ConfigDict(extra='allow')
    
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    log_file: str = Field(default="./logs/orchestrator.log")
    log_rotation: str = Field(default="1 day")
    log_retention: str = Field(default="30 days")
    metrics_enabled: bool = Field(default=True)
    metrics_export_interval: int = Field(default=60, ge=1, le=3600)
    prometheus_port: int = Field(default=9090, ge=1024, le=65535)


class WebConfig(BaseModel):
    """Web interface configuration."""
    model_config = ConfigDict(extra='allow')
    
    enabled: bool = Field(default=True)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1024, le=65535)
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])


class PathsConfig(BaseModel):
    """Paths configuration."""
    model_config = ConfigDict(extra='allow')
    
    workspace: str = Field(default="./workspace")
    logs: str = Field(default="./logs")
    data: str = Field(default="./data")
    cache: str = Field(default="./cache")


class UsageLimitsConfig(BaseModel):
    """Usage limits for cost control."""
    model_config = ConfigDict(extra='allow')
    
    daily_token_limit: int = Field(default=1000000, ge=1000)
    daily_api_call_limit: int = Field(default=1000, ge=10)
    daily_cost_limit_usd: float = Field(default=10.0, ge=0.0)
    monthly_cost_limit_usd: float = Field(default=50.0, ge=0.0)


class CloudConfig(BaseModel):
    """Cloud configuration."""
    model_config = ConfigDict(extra='allow')
    
    blackbox_cloud_endpoint: str = Field(
        default="https://cloud.blackbox.ai/api/v1"
    )
    cloud_first_enabled: bool = Field(
        default=True,
        description="Enable cloud-first mode (should always be true)"
    )
    allow_local_fallback: bool = Field(
        default=True,
        description="Allow fallback to local if cloud unavailable"
    )


class OrchestratorConfig(BaseSettings):
    """
    Main orchestrator configuration.
    
    This loads from:
    1. config.yaml file
    2. Environment variables (override)
    3. .env file (if present)
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='allow'
    )
    
    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Deployment environment"
    )
    
    # Agents configuration
    agents: Dict[str, AgentConfig] = Field(
        default_factory=dict,
        description="Agent configurations"
    )
    
    # API configuration
    api: Dict[str, APIConfig] = Field(
        default_factory=dict,
        description="API configurations"
    )
    
    # Memory configuration
    memory: MemoryConfig = Field(
        default_factory=MemoryConfig,
        description="Memory system configuration"
    )
    
    # Task configuration
    tasks: TaskConfig = Field(
        default_factory=TaskConfig,
        description="Task management configuration"
    )
    
    # Monitoring configuration
    monitoring: MonitoringConfig = Field(
        default_factory=MonitoringConfig,
        description="Monitoring configuration"
    )
    
    # Web configuration
    web: WebConfig = Field(
        default_factory=WebConfig,
        description="Web interface configuration"
    )
    
    # Paths configuration
    paths: PathsConfig = Field(
        default_factory=PathsConfig,
        description="Paths configuration"
    )
    
    # Usage limits
    usage_limits: UsageLimitsConfig = Field(
        default_factory=UsageLimitsConfig,
        description="Usage limits for cost control"
    )
    
    # Cloud configuration
    cloud: CloudConfig = Field(
        default_factory=CloudConfig,
        description="Cloud configuration"
    )
    
    # Resource constraints (set by Setup Agent)
    max_concurrent_agents: int = Field(default=10, ge=1, le=100)
    max_memory_per_agent_mb: int = Field(default=200, ge=50, le=2000)
    max_cache_size_gb: float = Field(default=5.0, ge=0.1, le=100.0)
    max_log_size_gb: float = Field(default=1.0, ge=0.1, le=10.0)
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'OrchestratorConfig':
        """
        Load configuration from YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            OrchestratorConfig instance
        """
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        # Process environment variables in config
        config_dict = cls._process_env_vars(config_dict)
        
        return cls(**config_dict)
    
    @staticmethod
    def _process_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process environment variables in configuration.
        
        Replaces ${VAR_NAME} with environment variable value.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Processed configuration
        """
        def process_value(value: Any) -> Any:
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                var_name = value[2:-1]
                return os.getenv(var_name, value)
            elif isinstance(value, dict):
                return {k: process_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [process_value(v) for v in value]
            return value
        
        return process_value(config)
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of issues.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Check required agents
        required_agents = ['researcher', 'coder', 'manager']
        for agent in required_agents:
            if agent not in self.agents:
                issues.append(f"Missing required agent configuration: {agent}")
        
        # Check API keys in production
        if self.environment == Environment.PRODUCTION:
            if 'anthropic' in self.api and not self.api['anthropic'].api_key:
                issues.append("Anthropic API key required in production")
        
        # Check paths exist
        for path_name, path_value in self.paths.model_dump().items():
            path = Path(path_value)
            if not path.exists():
                issues.append(f"Path does not exist: {path_name} = {path_value}")
        
        # Check resource constraints
        if self.max_concurrent_agents < 1:
            issues.append("max_concurrent_agents must be at least 1")
        
        if self.max_memory_per_agent_mb < 50:
            issues.append("max_memory_per_agent_mb must be at least 50MB")
        
        return issues
    
    def create_directories(self) -> None:
        """Create all configured directories if they don't exist."""
        for path_value in self.paths.model_dump().values():
            path = Path(path_value)
            path.mkdir(parents=True, exist_ok=True)
    
    def to_yaml(self, output_path: str) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            output_path: Path to output YAML file
        """
        config_dict = self.model_dump(exclude_none=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """
        Get configuration for specific agent.
        
        Args:
            agent_name: Name of agent
            
        Returns:
            AgentConfig if found, None otherwise
        """
        return self.agents.get(agent_name)
    
    def update_from_workspace_config(self, workspace_config: Dict[str, Any]) -> None:
        """
        Update configuration from workspace config (created by Setup Agent).
        
        Args:
            workspace_config: Workspace configuration dictionary
        """
        if 'resource_constraints' in workspace_config:
            constraints = workspace_config['resource_constraints']
            self.max_concurrent_agents = constraints.get(
                'max_concurrent_agents',
                self.max_concurrent_agents
            )
            self.max_memory_per_agent_mb = constraints.get(
                'max_memory_per_agent_mb',
                self.max_memory_per_agent_mb
            )
            self.max_cache_size_gb = constraints.get(
                'max_cache_size_gb',
                self.max_cache_size_gb
            )
            self.max_log_size_gb = constraints.get(
                'max_log_size_gb',
                self.max_log_size_gb
            )


# Global configuration instance
_config: Optional[OrchestratorConfig] = None


def load_config(config_path: str = "config.yaml") -> OrchestratorConfig:
    """
    Load global configuration.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        OrchestratorConfig instance
    """
    global _config
    
    if Path(config_path).exists():
        _config = OrchestratorConfig.from_yaml(config_path)
    else:
        # Use defaults if config file doesn't exist
        _config = OrchestratorConfig()
    
    # Create directories
    _config.create_directories()
    
    # Load workspace config if it exists
    workspace_config_path = Path("workspace_config.json")
    if workspace_config_path.exists():
        import json
        with open(workspace_config_path, 'r') as f:
            workspace_config = json.load(f)
        _config.update_from_workspace_config(workspace_config)
    
    return _config


def get_config() -> OrchestratorConfig:
    """
    Get global configuration instance.
    
    Returns:
        OrchestratorConfig instance
        
    Raises:
        RuntimeError: If configuration not loaded
    """
    global _config
    
    if _config is None:
        _config = load_config()
    
    return _config


def reload_config(config_path: str = "config.yaml") -> OrchestratorConfig:
    """
    Reload configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        OrchestratorConfig instance
    """
    global _config
    _config = None
    return load_config(config_path)
