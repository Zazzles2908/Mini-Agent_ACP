#!/usr/bin/env python3
"""
Production Configuration for Mini-Agent Observability System
Handles environment variables, API keys, and production settings
"""

import os
import json
from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class ObservabilityConfig:
    """Configuration class for observability system"""
    
    # Langfuse Configuration
    langfuse_secret_key: Optional[str] = None
    langfuse_public_key: Optional[str] = None
    langfuse_host: str = "http://localhost:3000"
    
    # Supabase Configuration  
    supabase_url: str = "https://mxaazuhlqewmkweewyaz.supabase.co"
    supabase_anon_key: Optional[str] = None
    supabase_service_key: Optional[str] = None
    supabase_access_token: Optional[str] = None
    
    # Production Settings
    production_mode: bool = False
    batch_size: int = 10
    max_retry_attempts: int = 3
    timeout_seconds: int = 30
    
    # Feature Flags
    enable_langfuse: bool = True
    enable_supabase: bool = True
    enable_performance_logging: bool = True
    enable_error_tracking: bool = True
    
    # Data Retention
    retention_days: int = 30
    max_sessions_per_hour: int = 100
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        
        # Langfuse
        self.langfuse_secret_key = os.getenv('LANGFUSE_SECRET_KEY', self.langfuse_secret_key)
        self.langfuse_public_key = os.getenv('LANGFUSE_PUBLIC_KEY', self.langfuse_public_key)
        
        # Supabase
        self.supabase_anon_key = os.getenv('SUPABASE_ANON_KEY', self.supabase_anon_key)
        self.supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', self.supabase_service_key)
        self.supabase_access_token = os.getenv('SUPABASE_ACCESS_TOKEN', self.supabase_access_token)
        
        # Production mode detection
        self.production_mode = os.getenv('ENVIRONMENT', 'development').lower() in ['production', 'prod']
        
        # Feature flags
        self.enable_langfuse = os.getenv('ENABLE_LANGFUSE', 'true').lower() == 'true'
        self.enable_supabase = os.getenv('ENABLE_SUPABASE', 'true').lower() == 'true'
        
    def validate(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'missing_keys': [],
            'ready_for_production': False
        }
        
        # Check Langfuse configuration
        if self.enable_langfuse:
            if not self.langfuse_secret_key or not self.langfuse_public_key:
                validation_results['missing_keys'].append('Langfuse API keys')
                validation_results['warnings'].append('Langfuse enabled but API keys missing')
        
        # Check Supabase configuration
        if self.enable_supabase:
            if not self.supabase_service_key:
                validation_results['missing_keys'].append('Supabase service role key')
                validation_results['warnings'].append('Supabase enabled but service key missing')
        
        # Check production readiness
        if self.production_mode:
            if validation_results['missing_keys']:
                validation_results['errors'].append('Production mode requires all API keys')
                validation_results['valid'] = False
            
            if not validation_results['errors']:
                validation_results['ready_for_production'] = True
        else:
            validation_results['ready_for_production'] = True  # Dev mode is OK with missing keys
        
        return validation_results
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for logging"""
        
        return {
            'langfuse_enabled': self.enable_langfuse,
            'supabase_enabled': self.enable_supabase,
            'production_mode': self.production_mode,
            'langfuse_configured': bool(self.langfuse_secret_key and self.langfuse_public_key),
            'supabase_configured': bool(self.supabase_service_key),
            'supabase_url': self.supabase_url,
            'batch_size': self.batch_size,
            'retention_days': self.retention_days
        }

class ConfigManager:
    """Manages observability configuration loading and validation"""
    
    CONFIG_FILE_PATH = "C:\\Users\\Jazeel-Home\\.mini-agent\\observability\\config.json"
    
    @classmethod
    def load_config(cls) -> ObservabilityConfig:
        """Load configuration from environment and config file"""
        
        config = ObservabilityConfig()
        
        # Try to load from config file
        if os.path.exists(cls.CONFIG_FILE_PATH):
            try:
                with open(cls.CONFIG_FILE_PATH, 'r') as f:
                    file_config = json.load(f)
                
                # Update config with file values
                for key, value in file_config.items():
                    if hasattr(config, key) and value is not None:
                        setattr(config, key, value)
                
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return config
    
    @classmethod
    def save_config(cls, config: ObservabilityConfig) -> bool:
        """Save configuration to file"""
        
        try:
            config_dict = {
                'langfuse_secret_key': config.langfuse_secret_key,
                'langfuse_public_key': config.langfuse_public_key,
                'supabase_anon_key': config.supabase_anon_key,
                'supabase_service_key': config.supabase_service_key,
                'production_mode': config.production_mode,
                'batch_size': config.batch_size,
                'enable_langfuse': config.enable_langfuse,
                'enable_supabase': config.enable_supabase
            }
            
            os.makedirs(os.path.dirname(cls.CONFIG_FILE_PATH), exist_ok=True)
            
            with open(cls.CONFIG_FILE_PATH, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            print(f"[OK] Configuration saved to {cls.CONFIG_FILE_PATH}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error saving configuration: {e}")
            return False

def create_production_setup_script():
    """Create a script to help set up production configuration"""
    
    script_content = '''#!/usr/bin/env python3
"""
Production Setup Helper for Mini-Agent Observability
Run this script to configure production settings
"""

import os
from config import ConfigManager, ObservabilityConfig

def setup_production():
    """Interactive setup for production configuration"""
    
    print("Mini-Agent Observability Production Setup")
    print("=" * 50)
    
    config = ObservabilityConfig(production_mode=True)
    
    # Langfuse setup
    print("\\n1. Langfuse Configuration")
    print("   Visit: http://localhost:3000 to create project")
    print("   Get your API keys from project settings")
    
    langfuse_secret = input("Langfuse Secret Key (sk-lf-...): ").strip()
    langfuse_public = input("Langfuse Public Key (pk-lf-...): ").strip()
    
    if langfuse_secret:
        config.langfuse_secret_key = langfuse_secret
    if langfuse_public:
        config.langfuse_public_key = langfuse_public
    
    # Supabase setup
    print("\\n2. Supabase Configuration")
    print("   Your Supabase URL:", config.supabase_url)
    
    service_key = input("Supabase Service Role Key: ").strip()
    if service_key:
        config.supabase_service_key = service_key
    
    # Save configuration
    print("\\n3. Saving Configuration...")
    if ConfigManager.save_config(config):
        print("[OK] Configuration saved successfully!")
    else:
        print("[ERROR] Failed to save configuration")
    
    # Validate configuration
    print("\\n4. Validating Configuration...")
    validation = config.validate()
    
    if validation['valid']:
        print("[OK] Configuration is valid")
        if validation['ready_for_production']:
            print("[OK] Ready for production deployment")
        else:
            print("[WARN] Some features may not work in production")
    else:
        print("[ERROR] Configuration has errors:")
        for error in validation['errors']:
            print(f"   - {error}")
    
    print("\\nConfiguration Summary:")
    summary = config.get_config_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    setup_production()
'''
    
    with open("setup_production.py", "w") as f:
        f.write(script_content)
    
    print("Production setup script created: setup_production.py")

if __name__ == "__main__":
    print("Mini-Agent Observability Production Configuration")
    print("=" * 55)
    
    # Load and validate current configuration
    config = ConfigManager.load_config()
    
    print("Current Configuration:")
    summary = config.get_config_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\\nValidating configuration...")
    validation = config.validate()
    
    if validation['valid']:
        print("✓ Configuration is valid")
    else:
        print("⚠ Configuration has issues:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
        for error in validation['errors']:
            print(f"  - {error}")
    
    print(f"\\nReady for production: {validation['ready_for_production']}")
    
    # Create setup helper script
    create_production_setup_script()
