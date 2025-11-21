"""Agent class for Mini-Agent"""
import asyncio
from typing import List, Any, Optional
from .schema import Message, LLMResponse
from .llm import LLMClient


class Agent:
    """Simple AI agent that uses LLM client"""
    
    def __init__(self, llm_client: LLMClient, system_prompt: str, tools: Optional[List] = None, max_steps: int = 10, workspace_dir: str = "."):
        """Initialize agent"""
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.max_steps = max_steps
        self.workspace_dir = workspace_dir
    
    async def run(self, messages: List[Message]) -> LLMResponse:
        """Run the agent with given messages"""
        # Add system prompt if not already present
        if not any(msg.role == "system" for msg in messages):
            messages = [Message(role="system", content=self.system_prompt)] + messages
        
        # For now, just use the LLM client directly
        if hasattr(self.llm_client, 'chat_async'):
            response = await self.llm_client.chat_async(messages)
        else:
            response = self.llm_client.chat(messages)
        
        return response
    
    def run_sync(self, messages: List[Message]) -> LLMResponse:
        """Synchronous version of run"""
        # Add system prompt if not already present
        if not any(msg.role == "system" for msg in messages):
            messages = [Message(role="system", content=self.system_prompt)] + messages
        
        return self.llm_client.chat(messages)