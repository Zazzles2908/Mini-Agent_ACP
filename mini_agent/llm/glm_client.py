"""GLM LLM client implementation for primary reasoning.

This client provides GLM-4.6 and other GLM models for general LLM reasoning
tasks, complementing the Z.AI web search capabilities.
"""

import json
import logging
from typing import Any

from ..llm.zai_client import ZAIClient
from ..retry import RetryConfig, async_retry
from ..schema import FunctionCall, LLMResponse, Message, ToolCall, LLMProvider
from .base import LLMClientBase

logger = logging.getLogger(__name__)


class GLMClient(LLMClientBase):
    """LLM client using GLM models via Z.AI API.
    
    This client provides access to GLM-4.6 and other GLM models for
    primary reasoning tasks, while Z.AI web search remains separate.
    """

    def __init__(
        self,
        api_key: str,
        api_base: str = "https://api.z.ai/api/coding/paas/v4",
        model: str = "glm-4.6",
        retry_config: RetryConfig | None = None,
    ):
        """Initialize GLM client.
        
        Args:
            api_key: Z.AI API key for GLM access
            api_base: Z.AI API base URL
            model: GLM model name (glm-4.6, glm-4.5, etc.)
            retry_config: Optional retry configuration
        """
        super().__init__(api_key, api_base, model, retry_config)
        
        # Initialize Z.AI client for GLM
        self.client = ZAIClient(api_key, use_coding_plan=True)
        
        # Map model names
        self.model_mapping = {
            "glm-4.6": "glm-4.6",
            "glm-4.5": "glm-4.5", 
            "glm-4.5-air": "glm-4.5-air",
        }
        
        # Set the actual model name
        self.model = self.model_mapping.get(model, model)

    def _convert_messages(self, messages: list[Message]) -> tuple[str | None, list[dict[str, Any]]]:
        """Convert messages to GLM API format.
        
        Args:
            messages: List of Message objects
            
        Returns:
            Tuple of (system_message, api_messages)
        """
        system_messages = []
        api_messages = []
        
        for message in messages:
            if message.role == "system":
                system_messages.append(str(message.content))
            elif message.role == "user":
                if isinstance(message.content, list):
                    content = message.content
                else:
                    content = str(message.content)
                api_messages.append({
                    "role": "user", 
                    "content": content
                })
            elif message.role == "assistant":
                content_parts = []
                if message.content:
                    content_parts.append(str(message.content))
                if message.thinking:
                    content_parts.append(f"<thinking>{message.thinking}</thinking>")
                
                api_messages.append({
                    "role": "assistant",
                    "content": "\n".join(content_parts)
                })
            elif message.role == "tool":
                api_messages.append({
                    "role": "user",
                    "content": f"Tool result: {message.content}"
                })
        
        system_message = "\n\n".join(system_messages) if system_messages else None
        return system_message, api_messages

    def _prepare_request(
        self,
        messages: list[Message],
        tools: list[Any] | None = None,
    ) -> dict[str, Any]:
        """Prepare request payload for GLM API.
        
        Args:
            messages: List of conversation messages
            tools: Optional tools to enable
            
        Returns:
            Dictionary containing the request payload
        """
        system_message, api_messages = self._convert_messages(messages)
        
        payload = {
            "model": self.model,
            "messages": api_messages,
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        
        if system_message:
            payload["system"] = system_message
        
        # Add tools if provided
        if tools:
            # Note: This is a simplified tool handling
            # In production, this would properly format tools for GLM API
            pass
        
        return payload

    async def generate(
        self,
        messages: list[Message],
        tools: list[Any] | None = None,
    ) -> LLMResponse:
        """Generate response using GLM model.
        
        Args:
            messages: List of conversation messages
            tools: Optional tools to enable
            
        Returns:
            LLMResponse containing the generated content
        """
        try:
            # Convert messages to Z.AI format
            system_message, api_messages = self._convert_messages(messages)
            
            # Prepare messages for GLM API
            glm_messages = []
            if system_message:
                glm_messages.append({
                    "role": "system",
                    "content": system_message
                })
            glm_messages.extend(api_messages)
            
            logger.info(f"GLM-4.6 request with {len(glm_messages)} messages")
            
            # Make actual API call using ZAIClient
            result = await self.client.chat_completion(
                messages=glm_messages,
                model=self.model,
                temperature=0.7,
                max_tokens=2048
            )
            
            if result["success"]:
                content = result.get("content", "")
                usage = result.get("usage", {})
                
                return LLMResponse(
                    content=content,
                    thinking=None,
                    tool_calls=None,
                    finish_reason="stop"
                )
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"GLM-4.6 API request failed: {error_msg}")
                return LLMResponse(
                    content=f"Error: Unable to generate response - {error_msg}",
                    thinking=None,
                    tool_calls=None,
                    finish_reason="error"
                )
                
        except Exception as e:
            logger.error(f"GLM-4.6 API request failed: {e}")
            return LLMResponse(
                content=f"Error: Unable to generate response - {str(e)}",
                thinking=None,
                tool_calls=None,
                finish_reason="error"
            )


class GLMLLMClient(GLMClient):
    """Alias for GLMClient to maintain compatibility."""
    pass