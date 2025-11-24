"""Configuration management for Mini Agent."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration management for Mini Agent."""
    
    # LLM Configuration
    api_key: str = ""
    api_base: str = "https://api.minimax.io"
    model: str = "MiniMax-M2"
    provider: str = "openai"
    
    # Retry Configuration
    retry: Dict[str, Any] = field(default_factory=dict)
    
    # Agent Configuration
    max_steps: int = 200
    workspace_dir: str = "./workspace"
    system_prompt_path: str = "system_prompt.md"
    
    # Tools Configuration
    tools: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, config_path: Union[str, Path]) -> 'Config':
        """Load configuration from YAML file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    @classmethod
    def find_config_file(cls, config_name: str) -> Optional[Path]:
        """Find configuration file in priority order."""
        search_paths = [
            Path("mini_agent") / "config" / config_name,  # Development: ./mini_agent/config/
            Path.home() / ".mini-agent" / "config" / config_name,  # User: ~/.mini-agent/config/
            Path(__file__).parent / config_name,  # Package: <package>/config/
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    
    @classmethod
    def get_default_config_path(cls) -> Optional[Path]:
        """Get the default configuration file path."""
        return cls.find_config_file("config.yaml")
    
    @classmethod
    def get_package_dir(cls) -> Path:
        """Get the package directory."""
        return Path(__file__).parent
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self
        
        for k in keys:
            if hasattr(value, k):
                value = getattr(value, k)
            elif isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def update(self, config_data: Dict[str, Any]):
        """Update configuration with new data."""
        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(api_key={'***' if self.api_key else 'empty'}, model={self.model}, provider={self.provider})"
    
    def __repr__(self) -> str:
        return self.__str__()
