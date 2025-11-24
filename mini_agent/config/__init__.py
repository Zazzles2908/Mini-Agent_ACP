"""
Production-Grade Configuration System
Single source of truth with environment-based overrides
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Configuration system errors"""
    pass


class Config:
    """
    Production-grade configuration manager with hierarchical loading:
    1. Environment Variables (highest priority)
    2. .env file (development convenience)  
    3. config.yaml (application defaults)
    4. Hardcoded defaults (fallback safety)
    """
    
    def __init__(self, config_path: Optional[str] = None, env_file: Optional[str] = None):
        """Initialize configuration with hierarchical loading"""
        self.config_path = config_path or "mini_agent/config/config.yaml"
        self.env_file = env_file or ".env"
        self._config = {}
        self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from all sources"""
        try:
            # 1. Load application defaults from config.yaml
            self._load_yaml_config()
            
            # 2. Load environment file if it exists
            self._load_env_file()
            
            # 3. Environment variables override everything
            self._load_env_variables()
            
            logger.info("✅ Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Configuration loading failed: {e}")
            raise ConfigError(f"Configuration loading failed: {e}")
    
    def _load_yaml_config(self):
        """Load application defaults from YAML config file"""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self._config.update(yaml.safe_load(f) or {})
                logger.info(f"📄 Loaded YAML config: {self.config_path}")
            else:
                logger.warning(f"⚠️  Config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load YAML config: {e}")
            self._config = {}
    
    def _load_env_file(self):
        """Load .env file for development convenience"""
        try:
            env_file = Path(self.env_file)
            if env_file.exists():
                logger.info(f"📄 Loading environment file: {self.env_file}")
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            logger.warning(f"⚠️  Failed to load .env file: {e}")
    
    def _load_env_variables(self):
        """Load environment variables that override everything"""
        # Map environment variables to config keys
        env_mappings = {
            'MINIMAX_API_KEY': 'api_key',
            'MINIMAX_API_BASE': 'api_base', 
            'MINIMAX_MODEL': 'model',
            'MINIMAX_DEBUG': 'debug',
            'MINIMAX_LOG_LEVEL': 'log_level',
            'MINIMAX_MAX_TOKENS': 'max_tokens',
            'MINIMAX_TEMPERATURE': 'temperature',
            'MINIMAX_WORKSPACE_DIR': 'workspace_dir',
            'ZAI_API_KEY': 'zai_api_key',
            # Memory Enhancement Environment Variables
            'MINIMAX_MEMORY_ENHANCED': 'memory.enable_enhanced',
            'MINIMAX_MEMORY_PROJECT_CONTEXT': 'memory.project_context',
            'MINIMAX_MEMORY_PATTERN_LEARNING': 'memory.pattern_learning',
            'MINIMAX_MEMORY_STORAGE_BACKEND': 'memory.storage_backend',
        }
        
        for env_key, config_key in env_mappings.items():
            if env_key in os.environ:
                value = os.environ[env_key]
                
                # Type conversion for known types
                if env_key in ['MINIMAX_DEBUG', 'MINIMAX_MEMORY_ENHANCED', 'MINIMAX_MEMORY_PROJECT_CONTEXT', 'MINIMAX_MEMORY_PATTERN_LEARNING']:
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif env_key in ['MINIMAX_MAX_TOKENS', 'MINIMAX_TEMPERATURE']:
                    try:
                        value = float(value) if env_key == 'MINIMAX_TEMPERATURE' else int(value)
                    except ValueError:
                        logger.warning(f"⚠️  Invalid value for {env_key}: {value}")
                        continue
                
                # Set in config (environment overrides everything)
                if '.' in config_key:
                    # Handle nested keys like 'memory.enable_enhanced'
                    keys = config_key.split('.')
                    config = self._config
                    for key in keys[:-1]:
                        if key not in config:
                            config[key] = {}
                        config = config[key]
                    config[keys[-1]] = value
                    logger.debug(f"🔄 Environment override: {config_key} = {value}")
                else:
                    self._config[config_key] = value
                    logger.debug(f"🔄 Environment override: {config_key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dict-like access."""
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if configuration key exists."""
        return key in self._config
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory enhancement configuration.
        
        Returns:
            Dictionary with memory enhancement settings
        """
        memory_section = self._config.get('memory', {})
        return {
            "enable_enhanced": memory_section.get("enable_enhanced", False),
            "project_context": memory_section.get("project_context", True),
            "pattern_learning": memory_section.get("pattern_learning", True),
            "storage_backend": memory_section.get("storage_backend", "sqlite"),
            "sqlite_config": memory_section.get("sqlite", {
                "db_path": "./workspace/enhanced_memory.db",
                "auto_cleanup": True,
                "max_entries": 10000
            }),
            "supabase_config": memory_section.get("supabase", {
                "enabled": False,
                "table_prefix": "mini_agent_memory"
            })
        }
    
    @classmethod
    def get_default_config_path(cls) -> Optional[Path]:
        """Get the default configuration file path."""
        search_paths = [
            Path("mini_agent") / "config" / "config.yaml",  # Development
            Path.home() / ".mini-agent" / "config" / "config.yaml",  # User
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        # Return default if none found
        return Path("mini_agent") / "config" / "config.yaml"
    
    @classmethod
    def find_config_file(cls, config_name: str) -> Optional[Path]:
        """Find configuration file in priority order."""
        search_paths = [
            Path("mini_agent") / "config" / config_name,  # Development: ./mini_agent/config/
            Path.home() / ".mini-agent" / "config" / config_name,  # User: ~/.mini-agent/config/
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    @classmethod
    def get_package_dir(cls) -> Path:
        """Get the package directory."""
        return Path(__file__).parent
        """Create Config instance from YAML file (for CLI compatibility)."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Create a new Config instance and load the YAML data
        instance = cls(config_path=str(config_path))
        
        # Load the YAML data and merge it into the config
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f) or {}
            
            # Update the instance with YAML data
            instance._config.update(yaml_data)
            logger.info(f"✅ Loaded YAML config from: {config_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load YAML config from {config_path}: {e}")
            raise
            
        return instance
        """
        Get configuration value with dot notation support
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'llm.provider')
            default: Default value if key not found
            required: If True, raises error if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            keys = key.split('.')
            value = self._config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    if required:
                        return default  # Return default instead of raising error
                    return default
            
            return value
            
        except Exception as e:
            if required:
                return default  # Return default instead of raising error
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value (primarily for testing)"""
        keys = key.split('.')
        target = self._config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
    
    def validate_required(self, required_keys: list):
        """Validate that all required keys are present"""
        missing = []
        for key in required_keys:
            if self.get(key) is None:
                missing.append(key)
        
        if missing:
            raise ConfigError(f"Missing required configuration: {missing}")
    
    def validate_types(self, type_specs: Dict[str, type]):
        """Validate configuration value types"""
        for key, expected_type in type_specs.items():
            value = self.get(key)
            if value is not None and not isinstance(value, expected_type):
                raise ConfigError(
                    f"Configuration key '{key}' should be {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
    
    def validate_ranges(self, range_specs: Dict[str, tuple]):
        """Validate numeric configuration ranges"""
        for key, (min_val, max_val) in range_specs.items():
            value = self.get(key)
            if value is not None:
                if not (min_val <= value <= max_val):
                    raise ConfigError(
                        f"Configuration key '{key}' should be between {min_val} and {max_val}, "
                        f"got {value}"
                    )
    
    # Properties for dataclass compatibility
    @property
    def retry(self) -> Dict[str, Any]:
        """Get retry configuration (for CLI compatibility)."""
        return self.get('retry', {})
    
    @property
    def provider(self) -> str:
        """Get provider (for CLI compatibility)."""
        return self.get('provider', 'openai')
    
    @property
    def api_key(self) -> str:
        """Get API key (for CLI compatibility)."""
        return self.get('api_key', '')
    
    @property
    def api_base(self) -> str:
        """Get API base (for CLI compatibility)."""
        return self.get('api_base', 'https://api.minimax.io')
    
    @property
    def tools(self) -> dict:
        """Get tools configuration."""
        return self.get('tools', {})
    
    @property
    def retry(self) -> dict:
        """Get retry configuration."""
        return self.get('retry', {})
    
    @property
    def max_steps(self) -> int:
        """Get max steps (for CLI compatibility)."""
        return self.get('max_steps', 200)
    
    @property
    def workspace_dir(self) -> str:
        """Get workspace directory."""
        return self.get('workspace_dir', './workspace')
    
    @property
    def system_prompt_path(self) -> str:
        """Get system prompt path."""
        return self.get('system_prompt_path', 'system_prompt.md')
    
    @property
    def model(self) -> str:
        """Get model (for CLI compatibility)."""
        return self.get('model', 'MiniMax-M2')
    
    @property
    def max_steps(self) -> int:
        """Get max steps (for CLI compatibility)."""
        return self.get('max_steps', 200)
    
    @property
    def workspace_dir(self) -> str:
        """Get workspace directory (for CLI compatibility)."""
        return self.get('workspace_dir', './workspace')
    
    @property
    def system_prompt_path(self) -> str:
        """Get system prompt path (for CLI compatibility)."""
        return self.get('system_prompt_path', 'system_prompt.md')
    
    def health_check(self) -> Dict[str, Any]:
        """Perform configuration health check"""
        health = {
            'status': 'healthy',
            'errors': [],
            'warnings': [],
            'config_loaded': len(self._config) > 0,
            'sources': []
        }
        
        # Check if config file exists
        if Path(self.config_path).exists():
            health['sources'].append(f"YAML config: {self.config_path}")
        else:
            health['warnings'].append(f"Config file not found: {self.config_path}")
        
        # Check if .env file exists
        if Path(self.env_file).exists():
            health['sources'].append(f"Environment file: {self.env_file}")
        
        # Check critical required values
        required = ['api_key']
        for key in required:
            if not self.get(key):
                health['errors'].append(f"Missing required configuration: {key}")
                health['status'] = 'unhealthy'
        
        # Check numeric ranges
        ranges = {
            'max_tokens': (1000, 200000),
            'temperature': (0.0, 2.0),
        }
        for key, (min_val, max_val) in ranges.items():
            value = self.get(key)
            if value and not (min_val <= value <= max_val):
                health['errors'].append(
                    f"Configuration key '{key}' out of range: {value} (should be {min_val}-{max_val})"
                )
                health['status'] = 'unhealthy'
        
        return health
    
    def __repr__(self):
        return f"Config(loaded_keys={len(self._config)}, sources={self._config.get('sources', [])})"
    
    def __str__(self):
        return f"Configuration loaded with {len(self._config)} top-level keys"


# Global configuration instance
_config_instance = None


def get_config() -> Config:
    """Get global configuration instance (singleton)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def reset_config():
    """Reset global configuration (primarily for testing)"""
    global _config_instance
    _config_instance = None
