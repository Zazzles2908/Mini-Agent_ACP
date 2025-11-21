"""LLM Client for Mini-Agent"""
import json
import httpx
from typing import List, Dict, Any
from .schema import LLMProvider, Message, LLMResponse


class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self, api_key: str, provider: LLMProvider, api_base: str = "https://api.minimax.io", model: str = "MiniMax-M2"):
        """Initialize LLM client"""
        self.api_key = api_key
        self.provider = provider
        self.api_base = api_base.rstrip("/")
        self.model = model
        
        # Set up headers based on provider
        if provider == LLMProvider.ANTHROPIC:
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            # Only append endpoint path if not already included
            if "/v1/" not in api_base:
                self.chat_endpoint = f"{api_base}/v1/messages"
            else:
                self.chat_endpoint = api_base
        else:
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # Only append endpoint path if not already included
            if "/v1/" not in api_base:
                self.chat_endpoint = f"{api_base}/v1/chat/completions"
            else:
                self.chat_endpoint = api_base
    
    async def chat(self, messages: List[Message]) -> LLMResponse:
        """Send chat messages and get response"""
        # Convert messages to the appropriate format
        if self.provider == LLMProvider.ANTHROPIC:
            # Anthropic format
            payload = {
                "model": self.model,
                "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                "max_tokens": 4000,
                "temperature": 0.7
            }
        else:
            # OpenAI format
            payload = {
                "model": self.model,
                "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                "max_tokens": 4000,
                "temperature": 0.7
            }
        
        # Make the API call
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.chat_endpoint,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract content based on provider
                if self.provider == LLMProvider.ANTHROPIC:
                    content = result.get("content", [])
                    if content and isinstance(content, list) and len(content) > 0:
                        text_content = content[0].get("text", "")
                    else:
                        text_content = str(result)
                else:
                    text_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Extract usage and other metadata
                usage = result.get("usage", {})
                finish_reason = result.get("choices", [{}])[0].get("finish_reason", "unknown")
                
                return LLMResponse(
                    content=text_content,
                    finish_reason=finish_reason
                )
                
        except Exception as e:
            return LLMResponse(
                content=f"Error: {str(e)}",
                finish_reason="error"
            )
