"""
Enhanced utilities using new dependencies
"""
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

try:
    from pydantic import BaseModel, ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


class SystemMonitor:
    """Enhanced system monitoring using psutil."""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get current memory usage."""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil not available"}
        
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free
        }
    
    @staticmethod
    def get_cpu_usage() -> Dict[str, Any]:
        """Get current CPU usage."""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil not available"}
        
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        }
    
    @staticmethod
    def get_disk_usage(path: str = ".") -> Dict[str, Any]:
        """Get disk usage for given path."""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil not available"}
        
        usage = psutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": (usage.used / usage.total) * 100
        }


class SecurityHelper:
    """Security utilities using bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        if not BCRYPT_AVAILABLE:
            raise ImportError("bcrypt not available")
        
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        if not BCRYPT_AVAILABLE:
            raise ImportError("bcrypt not available")
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class DisplayHelper:
    """Enhanced display utilities using rich."""
    
    @staticmethod
    def show_system_status():
        """Display system status in a nice table."""
        if not RICH_AVAILABLE:
            print("System status (basic):")
            monitor = SystemMonitor()
            print(f"Memory: {monitor.get_memory_usage()}")
            print(f"CPU: {monitor.get_cpu_usage()}")
            print(f"Disk: {monitor.get_disk_usage()}")
            return
        
        console = Console()
        monitor = SystemMonitor()
        
        table = Table(title="System Status")
        table.add_column("Component", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Details", style="yellow")
        
        # Memory info
        memory = monitor.get_memory_usage()
        if "error" not in memory:
            table.add_row(
                "Memory",
                f"{memory['percent']:.1f}%",
                f"{memory['used']/1024**3:.1f}GB / {memory['total']/1024**3:.1f}GB"
            )
        
        # CPU info
        cpu = monitor.get_cpu_usage()
        if "error" not in cpu:
            table.add_row(
                "CPU",
                f"{cpu['percent']:.1f}%",
                f"{cpu['count']} cores"
            )
        
        # Disk info
        disk = monitor.get_disk_usage()
        if "error" not in disk:
            table.add_row(
                "Disk",
                f"{disk['percent']:.1f}%",
                f"{disk['used']/1024**3:.1f}GB / {disk['total']/1024**3:.1f}GB"
            )
        
        console.print(table)
    
    @staticmethod
    def show_progress_demo():
        """Demonstrate rich progress bars."""
        if not RICH_AVAILABLE:
            print("Progress demo (basic):")
            for i in range(10):
                print(f"Step {i+1}/10")
            return
        
        console = Console()
        console.print("📊 [bold blue]Progress Demo[/bold blue]")
        
        for step in track(range(10), description="Processing..."):
            import time
            time.sleep(0.1)
        
        console.print("✅ [green]Complete![/green]")


if PYDANTIC_AVAILABLE:
    class WebStoreConfig(BaseModel):
        """Configuration model using Pydantic for validation."""
        app_name: str = "WebStore"
        app_version: str = "1.0.0"
        debug_mode: bool = False
        log_level: str = "INFO"
        max_memory_mb: int = 512
        enable_monitoring: bool = True
        database_url: str = "sqlite:///webstore.db"
        secret_key: str = "change-me"
        
        class Config:
            env_prefix = "WEBSTORE_"


def get_config_from_env() -> Optional[Dict[str, Any]]:
    """Get configuration from environment variables with validation."""
    if not PYDANTIC_AVAILABLE:
        return None
    
    try:
        config = WebStoreConfig()
        return config.dict()
    except ValidationError as e:
        if LOGURU_AVAILABLE:
            logger.error(f"Configuration validation error: {e}")
        else:
            print(f"Configuration validation error: {e}")
        return None


def demo_all_features():
    """Demonstrate all enhanced features."""
    print("🚀 WebStore Enhanced Features Demo")
    print("=" * 50)
    
    # Display helper demo
    print("\n1. System Status Display:")
    DisplayHelper.show_system_status()
    
    print("\n2. Progress Bar Demo:")
    DisplayHelper.show_progress_demo()
    
    # Security demo (if available)
    if BCRYPT_AVAILABLE:
        print("\n3. Security Features:")
        password = "test123"
        hashed = SecurityHelper.hash_password(password)
        is_valid = SecurityHelper.verify_password(password, hashed)
        print(f"Password hashing: {'✅ Working' if is_valid else '❌ Failed'}")
    
    # Configuration demo
    if PYDANTIC_AVAILABLE:
        print("\n4. Configuration Validation:")
        config = get_config_from_env()
        if config:
            print(f"Configuration loaded: {config.get('app_name')} v{config.get('app_version')}")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    demo_all_features()
