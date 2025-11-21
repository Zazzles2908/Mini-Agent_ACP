"""Configuration management for Mini-Agent"""
import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class LLMConfig:
    """LLM configuration"""
    api_key: Optional[str] = None
    api_base: str = "https://api.minimax.io/v1/chat/completions"
    model: str = "MiniMax-M2"
    provider: str = "anthropic"
    max_tokens: int = 4000
    temperature: float = 0.7


@dataclass 
class AgentConfig:
    """Agent configuration"""
    max_steps: int = 10
    system_prompt: str = "You are a helpful AI assistant."


@dataclass
class Config:
    """Main configuration class"""
    llm: LLMConfig = field(default_factory=LLMConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment and files"""
        config = cls()
        
        # Load from environment variables
        config.llm.api_key = os.getenv("MINIMAX_API_KEY") or os.getenv("ZAI_API_KEY")
        config.llm.api_base = os.getenv("API_BASE", "https://api.minimax.io")
        config.llm.model = os.getenv("MODEL", "MiniMax-M2")
        config.llm.provider = os.getenv("PROVIDER", "anthropic")
        
        # Also load from .env file if it exists
        env_file = Path.cwd() / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        
        # Update config from environment
        config.llm.api_key = os.getenv("MINIMAX_API_KEY") or os.getenv("ZAI_API_KEY")
        config.llm.api_base = os.getenv("API_BASE", "https://api.minimax.io")
        config.llm.model = os.getenv("MODEL", "MiniMax-M2")
        config.llm.provider = os.getenv("PROVIDER", "anthropic")
        
        return config