"""
MiniMax Client Implementation
Production-grade client for MiniMax API
"""

import json
import logging
from typing import Optional, AsyncGenerator, Any, List, Dict

from .base import LLMClientBase
from ..retry import RetryConfig
from ..schema import Message, LLMResponse

logger = logging.getLogger(__name__)


class MinimaxClient(LLMClientBase):
    """
    Production-grade client for MiniMax API.
    
    This client provides a clean interface to MiniMax's AI models with
    proper error handling, retry logic, and streaming support.
    """
    
    def __init__(
        self,
        api_key: str,
        api_base: str = "https://api.minimax.io",
        model: str = "MiniMax-M2",
        max_tokens: int = 200000,
        temperature: float = 0.7,
        timeout: int = 120,
        retry_config: Optional[RetryConfig] = None,
    ):
        """Initialize MiniMax client"""
        super().__init__(api_key, api_base, model, retry_config)
        
        self.api_base = api_base.rstrip('/')
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        
        logger.info(f"Initialized MiniMax client: model={model}, api_base={api_base}")
    
    def _convert_messages(self, messages: List[Message]) -> tuple[str | None, list[dict[str, Any]]]:
        """Convert messages to MiniMax API format"""
        system_message = None
        api_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = str(msg.content)
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": str(msg.content)
                })
        
        return system_message, api_messages
    
    def _prepare_request(self, messages: List[Message], tools: List[Any] | None = None) -> dict[str, Any]:
        """Prepare request payload for MiniMax API"""
        system_message, api_messages = self._convert_messages(messages)
        
        payload = {
            "model": self.model,
            "messages": api_messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        
        if system_message:
            # MiniMax API supports system messages through the messages array
            api_messages.insert(0, {
                "role": "system", 
                "content": system_message
            })
        
        return payload
    
    async def generate(self, messages: List[Message]) -> LLMResponse:
        """Generate response from MiniMax API"""
        import httpx
        
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": self._format_messages(messages),
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": False,
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "MiniAgent/1.0.0"
            }
            
            # Make the API request with retry logic
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await self._retry_request(
                    client.post,
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    headers=headers
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Parse MiniMax response format
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                content = choice.get("message", {}).get("content", "")
                usage = data.get("usage", {})
                
                return LLMResponse(
                    content=content,
                    total_tokens=usage.get("total_tokens", 0),
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    model=self.model,
                    finish_reason=choice.get("finish_reason", "stop")
                )
            else:
                raise ValueError("Unexpected response format from MiniMax API")
                
        except httpx.HTTPError as e:
            logger.error(f"MiniMax API HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"MiniMax API error: {e}")
            raise
    
    async def generate_stream(self, messages: List[Message]) -> AsyncGenerator[LLMResponse, None]:
        """Generate streaming response from MiniMax API"""
        import httpx
        
        try:
            # Prepare the request payload for streaming
            payload = {
                "model": self.model,
                "messages": self._format_messages(messages),
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": True,  # Enable streaming
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "MiniAgent/1.0.0"
            }
            
            # Make streaming API request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    response.raise_for_status()
                    
                    content_chunks = []
                    total_tokens = 0
                    
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                            
                        # MiniMax uses server-sent events format
                        if line.startswith("data: "):
                            data_str = line[6:]  # Remove "data: " prefix
                            
                            if data_str.strip() == "[DONE]":
                                break
                                
                            try:
                                chunk_data = json.loads(data_str)
                                
                                if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                    delta = chunk_data["choices"][0].get("delta", {})
                                    chunk_content = delta.get("content", "")
                                    
                                    if chunk_content:
                                        content_chunks.append(chunk_content)
                                        
                                        # Yield incremental response
                                        partial_content = "".join(content_chunks)
                                        yield LLMResponse(
                                            content=partial_content,
                                            total_tokens=0,  # Streaming doesn't provide token counts
                                            prompt_tokens=0,
                                            completion_tokens=0,
                                            model=self.model,
                                            finish_reason="partial"
                                        )
                                        
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse streaming data: {data_str}")
                                continue
                    
                    # Yield final response
                    final_content = "".join(content_chunks)
                    if final_content:
                        yield LLMResponse(
                            content=final_content,
                            total_tokens=0,
                            prompt_tokens=0,
                            completion_tokens=0,
                            model=self.model,
                            finish_reason="stop"
                        )
                        
        except httpx.HTTPError as e:
            logger.error(f"MiniMax streaming API HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"MiniMax streaming API error: {e}")
            raise
    
    def _format_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Format messages for MiniMax API"""
        formatted = []
        
        for msg in messages:
            role = msg.role
            content = msg.content
            
            # Handle content blocks (text, tool calls, etc.)
            if isinstance(content, list):
                # MiniMax supports both simple string content and content blocks
                content_blocks = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            content_blocks.append(block["text"])
                        elif block.get("type") == "image_url":
                            content_blocks.append({
                                "type": "image_url",
                                "image_url": {"url": block["image_url"]["url"]}
                            })
                    else:
                        content_blocks.append(str(block))
                
                content = "\n".join(content_blocks) if content_blocks else str(content)
            
            formatted.append({
                "role": role,
                "content": str(content)
            })
        
        return formatted
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on MiniMax client"""
        import httpx
        
        health = {
            "status": "healthy",
            "provider": "minimax",
            "model": self.model,
            "api_base": self.api_base,
            "api_key_configured": bool(self.api_key),
            "configuration": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "timeout": self.timeout,
            },
            "errors": [],
            "warnings": [],
        }
        
        try:
            # Test API connectivity
            async def test_connection():
                async with httpx.AsyncClient(timeout=10) as client:
                    # Simple test to check if API is reachable
                    # We use a minimal request to test connectivity
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    }
                    
                    test_payload = {
                        "model": self.model,
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 1,
                    }
                    
                    response = await client.post(
                        f"{self.api_base}/chat/completions",
                        json=test_payload,
                        headers=headers
                    )
                    
                    return response.status_code == 200
            
            # Note: We don't actually test this in health_check to avoid API costs
            # In a real implementation, you might want to test with a cached response
            # or use a different endpoint for health checks
            
        except Exception as e:
            health["status"] = "unhealthy"
            health["errors"].append(f"Health check failed: {e}")
        
        return health
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "provider": "minimax",
            "model": self.model,
            "api_base": self.api_base,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
        }
    
    def __repr__(self) -> str:
        return f"MinimaxClient(model={self.model}, api_base={self.api_base})"
