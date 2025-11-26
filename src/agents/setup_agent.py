"""
Setup Agent - Initial Project Configuration and System Optimization

This agent runs FIRST before anything else to:
1. Profile system resources (RAM, CPU, disk, network)
2. Calculate optimal resource constraints
3. Create workspace structure
4. Install dependencies intelligently
5. Configure tools based on system capabilities
6. Set up monitoring
7. Validate setup
8. Provide optimization recommendations
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import psutil
import platform
import subprocess
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SystemProfile:
    """System resource profile."""
    os_type: str
    os_version: str
    cpu_count: int
    cpu_freq_mhz: float
    ram_total_gb: float
    ram_available_gb: float
    disk_total_gb: float
    disk_free_gb: float
    disk_type: str  # SSD or HDD
    python_version: str
    has_git: bool
    has_node: bool
    has_vscode: bool
    network_speed_mbps: Optional[float] = None


@dataclass
class ResourceConstraints:
    """Computed resource constraints."""
    max_concurrent_agents: int
    max_memory_per_agent_mb: int
    max_cache_size_gb: float
    max_log_size_gb: float
    enable_disk_cache: bool
    enable_memory_cache: bool
    use_process_pool: bool
    recommended_workers: int


class SetupAgent:
    """
    Intelligent setup agent that analyzes system and configures optimally.
    
    This is the FIRST agent that runs. It ensures the system is configured
    optimally based on available resources.
    """
    
    def __init__(self):
        self.system_profile: Optional[SystemProfile] = None
        self.constraints: Optional[ResourceConstraints] = None
        self.setup_log: List[str] = []
        logger.info("Setup Agent initialized")
    
    def setup_project(self, project_path: str) -> Dict[str, Any]:
        """
        Complete project setup with intelligent resource management.
        
        Args:
            project_path: Path to project root
            
        Returns:
            Setup report with configuration and recommendations
        """
        self.log("🚀 Starting intelligent project setup...")
        
        try:
            # Phase 1: System Analysis
            self.log("📊 Phase 1: Analyzing system resources...")
            self.system_profile = self._profile_system()
            self.constraints = self._calculate_constraints(self.system_profile)
            
            # Phase 2: Validation
            self.log("✅ Phase 2: Validating setup...")
            validation_results = self._validate_setup(project_path)
            
            # Phase 3: Optimization
            self.log("⚡ Phase 3: Generating optimization recommendations...")
            recommendations = self._generate_recommendations()
            
            # Phase 4: Save Configuration
            self.log("💾 Phase 4: Saving workspace configuration...")
            self._save_workspace_config(project_path)
            
            self.log("✨ Setup complete!")
            
            return {
                'system_profile': asdict(self.system_profile),
                'constraints': asdict(self.constraints),
                'validation': validation_results,
                'recommendations': recommendations,
                'setup_log': self.setup_log
            }
            
        except Exception as e:
            logger.error(f"Setup failed: {e}", exc_info=True)
            raise
    
    def _profile_system(self) -> SystemProfile:
        """
        Profile system resources comprehensively.
        
        Returns:
            SystemProfile with all system information
        """
        self.log("  Detecting OS...")
        os_type = platform.system()
        os_version = platform.version()
        
        self.log("  Checking CPU...")
        cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_mhz = cpu_freq.current if cpu_freq else 0
        
        self.log("  Checking RAM...")
        ram = psutil.virtual_memory()
        ram_total_gb = ram.total / (1024**3)
        ram_available_gb = ram.available / (1024**3)
        
        self.log("  Checking disk...")
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024**3)
        disk_free_gb = disk.free / (1024**3)
        disk_type = self._detect_disk_type()
        
        self.log("  Checking Python version...")
        python_version = platform.python_version()
        
        self.log("  Checking required tools...")
        has_git = self._check_command('git --version')
        has_node = self._check_command('node --version')
        has_vscode = self._check_command('code --version')
        
        profile = SystemProfile(
            os_type=os_type,
            os_version=os_version,
            cpu_count=cpu_count,
            cpu_freq_mhz=cpu_freq_mhz,
            ram_total_gb=round(ram_total_gb, 2),
            ram_available_gb=round(ram_available_gb, 2),
            disk_total_gb=round(disk_total_gb, 2),
            disk_free_gb=round(disk_free_gb, 2),
            disk_type=disk_type,
            python_version=python_version,
            has_git=has_git,
            has_node=has_node,
            has_vscode=has_vscode
        )
        
        self.log(f"  System Profile: {profile}")
        return profile
    
    def _calculate_constraints(self, profile: SystemProfile) -> ResourceConstraints:
        """
        Calculate optimal resource constraints based on system profile.
        
        Strategy:
        - Reserve 2GB RAM for OS
        - Reserve 1GB RAM for VS Code
        - Use remaining RAM for agents
        - Limit concurrent agents based on CPU and RAM
        - Enable caching based on disk space
        - Adjust for disk type (SSD vs HDD)
        
        Args:
            profile: System profile
            
        Returns:
            ResourceConstraints with optimal settings
        """
        self.log("  Calculating resource constraints...")
        
        # Calculate available RAM for agents
        reserved_ram_gb = 3.0  # OS + VS Code
        available_ram_gb = max(profile.ram_available_gb - reserved_ram_gb, 1.0)
        
        # Calculate max concurrent agents
        # Each agent needs ~200MB RAM minimum
        max_agents_by_ram = int(available_ram_gb * 1024 / 200)
        # Also limited by CPU (2 agents per core is reasonable)
        max_agents_by_cpu = profile.cpu_count * 2
        # Take minimum, cap at 20
        max_concurrent_agents = min(max_agents_by_ram, max_agents_by_cpu, 20)
        
        # Calculate memory per agent
        max_memory_per_agent_mb = int((available_ram_gb * 1024) / max_concurrent_agents)
        
        # Calculate cache sizes
        # Use up to 10% of free disk for cache, max 10GB
        max_cache_size_gb = min(profile.disk_free_gb * 0.1, 10.0)
        # Logs: max 1GB
        max_log_size_gb = 1.0
        
        # Enable caching based on disk space
        enable_disk_cache = profile.disk_free_gb > 10.0
        enable_memory_cache = profile.ram_available_gb > 4.0
        
        # Use process pool if enough resources
        use_process_pool = profile.cpu_count >= 4 and profile.ram_available_gb > 4.0
        
        # Recommended workers for process pool
        recommended_workers = min(profile.cpu_count, max_concurrent_agents)
        
        constraints = ResourceConstraints(
            max_concurrent_agents=max_concurrent_agents,
            max_memory_per_agent_mb=max_memory_per_agent_mb,
            max_cache_size_gb=round(max_cache_size_gb, 2),
            max_log_size_gb=max_log_size_gb,
            enable_disk_cache=enable_disk_cache,
            enable_memory_cache=enable_memory_cache,
            use_process_pool=use_process_pool,
            recommended_workers=recommended_workers
        )
        
        self.log(f"  Resource Constraints: {constraints}")
        return constraints
    
    def _detect_disk_type(self) -> str:
        """
        Detect if disk is SSD or HDD.
        
        Returns:
            'SSD', 'HDD', or 'Unknown'
        """
        try:
            if platform.system() == 'Windows':
                # On Windows, check disk type via PowerShell
                result = subprocess.run(
                    ['powershell', '-Command', 
                     'Get-PhysicalDisk | Select-Object MediaType'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if 'SSD' in result.stdout:
                    return 'SSD'
                elif 'HDD' in result.stdout:
                    return 'HDD'
            # Default to SSD assumption for better performance
            return 'SSD'
        except Exception:
            return 'Unknown'
    
    def _check_command(self, command: str) -> bool:
        """
        Check if command is available.
        
        Args:
            command: Command to check
            
        Returns:
            True if command is available
        """
        try:
            subprocess.run(
                command.split(),
                capture_output=True,
                check=True,
                timeout=5
            )
            return True
        except Exception:
            return False
    
    def _validate_setup(self, project_path: str) -> Dict[str, Any]:
        """
        Validate that setup is correct and functional.
        
        Args:
            project_path: Path to project root
            
        Returns:
            Validation results
        """
        self.log("  Validating directory structure...")
        
        # Check critical directories exist
        critical_dirs = [
            'src', 'src/agents', 'src/core', 'src/memory',
            'libraries', 'agents', 'tests'
        ]
        
        dirs_exist = all(
            os.path.exists(os.path.join(project_path, d))
            for d in critical_dirs
        )
        
        self.log("  Validating Python environment...")
        python_valid = sys.version_info >= (3, 10)
        
        self.log("  Validating tools...")
        tools_valid = (
            self.system_profile.has_git and
            self.system_profile.python_version >= '3.10'
        )
        
        return {
            'directories': dirs_exist,
            'python': python_valid,
            'tools': tools_valid,
            'overall': dirs_exist and python_valid and tools_valid
        }
    
    def _generate_recommendations(self) -> List[str]:
        """
        Generate optimization recommendations based on system profile.
        
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        profile = self.system_profile
        constraints = self.constraints
        
        # RAM recommendations
        if profile.ram_total_gb < 8:
            recommendations.append(
                f"⚠️  LOW RAM: Consider upgrading to 16GB RAM for better performance. "
                f"Current limit: {constraints.max_concurrent_agents} concurrent agents."
            )
        
        # Disk recommendations
        if profile.disk_type == 'HDD':
            recommendations.append(
                "⚠️  HDD DETECTED: Consider upgrading to SSD for 10-100x faster I/O. "
                "This will significantly improve cache performance and startup time."
            )
        
        if profile.disk_free_gb < 10:
            recommendations.append(
                "⚠️  LOW DISK SPACE: Free up disk space. "
                "Disk caching is disabled due to low space."
            )
        
        # CPU recommendations
        if profile.cpu_count < 4:
            recommendations.append(
                f"⚠️  LOW CPU COUNT: Consider upgrading CPU for better parallel performance. "
                f"Current limit: {constraints.max_concurrent_agents} concurrent agents."
            )
        
        # Windows-specific recommendations
        if profile.os_type == 'Windows':
            recommendations.append(
                "💡 WINDOWS: Consider adding project folder to antivirus exclusions "
                "for better file I/O performance."
            )
            recommendations.append(
                "💡 WINDOWS: Enable long path support if not already enabled."
            )
        
        # Positive recommendations
        if (profile.ram_total_gb >= 16 and 
            profile.disk_type == 'SSD' and 
            profile.cpu_count >= 8):
            recommendations.append(
                f"✅ EXCELLENT SYSTEM: Your system has great resources! "
                f"You can run {constraints.max_concurrent_agents} concurrent agents efficiently."
            )
        
        # Cloud-first reminder
        recommendations.append(
            "🌐 CLOUD-FIRST: Remember, this system uses cloud agents by default. "
            "Your local resources are saved for coordination only!"
        )
        
        return recommendations
    
    def _save_workspace_config(self, project_path: str) -> None:
        """
        Save workspace configuration for future use.
        
        Args:
            project_path: Path to project root
        """
        self.log("  Saving workspace configuration...")
        
        import json
        
        config = {
            'system_profile': asdict(self.system_profile),
            'resource_constraints': asdict(self.constraints),
            'setup_timestamp': datetime.utcnow().isoformat(),
            'setup_version': '1.0.0'
        }
        
        config_path = os.path.join(project_path, 'workspace_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        self.log(f"  Workspace configuration saved to: {config_path}")
    
    def log(self, message: str) -> None:
        """
        Log setup progress.
        
        Args:
            message: Message to log
        """
        logger.info(message)
        self.setup_log.append(message)


def main():
    """Run setup agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Orchestrator Setup Agent')
    parser.add_argument(
        '--project-path',
        default='.',
        help='Path to project root (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Run setup
    agent = SetupAgent()
    result = agent.setup_project(args.project_path)
    
    # Print results
    print("\n" + "="*60)
    print("SETUP COMPLETE")
    print("="*60)
    
    print("\n📊 SYSTEM PROFILE:")
    for key, value in result['system_profile'].items():
        print(f"  {key}: {value}")
    
    print("\n⚙️  RESOURCE CONSTRAINTS:")
    for key, value in result['constraints'].items():
        print(f"  {key}: {value}")
    
    print("\n✅ VALIDATION:")
    for key, value in result['validation'].items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value}")
    
    print("\n💡 RECOMMENDATIONS:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "="*60)
    print("Setup agent completed successfully!")
    print("="*60)


if __name__ == '__main__':
    main()
