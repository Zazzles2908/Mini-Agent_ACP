"""
LLM client wrapper that supports multiple providers.

This module provides a unified interface for different AI models
(Anthropic and OpenAI) through a single LLMClient class.
"""

import logging
from typing import Any

from ..retry import RetryConfig
from ..schema import LLMProvider, LLMResponse, Message
from .anthropic_client import AnthropicClient
from .base import LLMClientBase
from .openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM Client wrapper supporting multiple providers.

    This class provides a unified interface for different AI models.
    It automatically instantiates the correct underlying client based on
    the provider parameter and appends the appropriate API endpoint suffix.

    Supported providers:
    - anthropic: Appends /anthropic to api_base
    - openai: Appends /v1 to api_base
    """

    def __init__(
        self,
        api_key: str,
        provider: str | LLMProvider,  # Accept both string and enum
        api_base: str = "https://api.minimax.io",
        model: str = "MiniMax-M2",
        retry_config: RetryConfig | None = None,
    ):
        """Initialize LLM client with specified provider.

        Args:
            api_key: API key for authentication
            provider: str  # OpenAI SDK format
            api_base: Base URL for the API (default: https://api.minimax.io)
                     Will be automatically suffixed with /anthropic or /v1 based on provider
            model: Model name to use
            retry_config: Optional retry configuration
        """
        # Normalize provider to string
        if isinstance(provider, LLMProvider):
            provider_str = provider.value  # Convert enum to string
        else:
            provider_str = str(provider)  # Ensure string
            
        self.provider = provider_str
        self.api_key = api_key
        self._model = model  # Store model temporarily
        self.retry_config = retry_config or RetryConfig()

        # for backward compatibility - remove any existing /anthropic or /v1
        api_base = api_base.replace("/anthropic", "")
        api_base = api_base.replace("/v1", "")

        # Append provider-specific suffix to api_base
        if provider_str == "anthropic":
            full_api_base = f"{api_base.rstrip('/')}/anthropic"
        elif provider_str == "openai":
            full_api_base = f"{api_base.rstrip('/')}/v1"
        else:
            raise ValueError(f"Unsupported provider: {provider_str}")

        self.api_base = full_api_base

        # Instantiate the appropriate client with correct API base
        self._client: LLMClientBase
        if provider_str == "anthropic":
            self._client = AnthropicClient(
                api_key=api_key,
                api_base=full_api_base,  # This should be {base}/anthropic
                model=self._model,
                retry_config=retry_config,
            )
        elif provider_str == "openai":
            self._client = OpenAIClient(
                api_key=api_key,
                api_base=full_api_base,  # This should be {base}/v1
                model=self._model,
                retry_config=retry_config,
            )
        else:
            raise ValueError(f"Unsupported provider: {provider_str}")

        logger.info("Initialized LLM client with provider: %s, api_base: %s", provider_str, full_api_base)

    @property
    def retry_callback(self):
        """Get retry callback."""
        return self._client.retry_callback

    @retry_callback.setter
    def retry_callback(self, value):
        """Set retry callback."""
        self._client.retry_callback = value

    @property
    def model(self):
        """Get model name."""
        return self._model

    @model.setter
    def model(self, value: str):
        """Set model name."""
        self._model = value
        if hasattr(self, '_client'):
            self._client.model = value

    async def generate(
        self,
        messages: list[Message],
        tools: list[Any] | None = None,
    ) -> LLMResponse:
        """Generate response from LLM.

        Args:
            messages: List of conversation messages
            tools: Optional list of available tools

        Returns:
            LLMResponse containing the generated content, thinking, and tool calls
        """
        return await self._client.generate(messages, tools)

    async def generate_stream(self, messages: list[Message], tools: list[Any] | None = None):
        """Generate streaming response from LLM.

        Args:
            messages: List of conversation messages
            tools: Optional list of available tools

        Yields:
            LLMResponse containing the generated content, thinking, and tool calls
        """
        if hasattr(self._client, 'generate_stream'):
            async for chunk in self._client.generate_stream(messages, tools):
                yield chunk
        else:
            # Fallback to regular generate for clients that don't support streaming
            response = await self.generate(messages, tools)
            yield response
