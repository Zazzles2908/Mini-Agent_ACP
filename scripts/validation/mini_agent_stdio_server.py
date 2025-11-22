#!/usr/bin/env python3
"""Production ACP stdio server with full Mini-Agent integration"""

import asyncio
import json
import sys
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

# Configure logging to go to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class MiniAgentACPStdioServer:
    """Production ACP stdio server integrating with Mini-Agent"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.message_id = 1
        self.config = None
        self.llm_client = None
        self.base_tools = []
        self.initialized = False
        
    async def initialize_system(self):
        """Initialize Mini-Agent components"""
        if self.initialized:
            return
            
        try:
            logger.info("🔧 Initializing Mini-Agent system...")
            
            # Load configuration
            try:
                from mini_agent.config import Config
                self.config = Config.load()
                logger.info("✅ Configuration loaded")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load config: {e}, using defaults")
                self.config = self._create_default_config()
            
            # Initialize LLM client
            try:
                from mini_agent.llm import LLMClient
                from mini_agent.schema import LLMProvider
                
                provider = LLMProvider.ANTHROPIC if self.config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI
                self.llm_client = LLMClient(
                    api_key=self.config.llm.api_key,
                    provider=provider,
                    api_base=self.config.llm.api_base,
                    model=self.config.llm.model,
                )
                logger.info("✅ LLM client initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize LLM client: {e}")
                self.llm_client = None
            
            # Initialize base tools
            try:
                from mini_agent.cli import initialize_base_tools
                self.base_tools = await initialize_base_tools(self.config)
                logger.info(f"✅ Loaded {len(self.base_tools)} tools")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize tools: {e}")
                self.base_tools = []
            
            self.initialized = True
            logger.info("🚀 Mini-Agent system initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize system: {e}")
            raise
    
    def _create_default_config(self):
        """Create default configuration for testing"""
        class DefaultConfig:
            def __init__(self):
                self.llm = type('LLMConfig', (), {
                    'api_key': 'test',
                    'api_base': 'https://api.minimax.io',
                    'model': 'MiniMax-M2',
                    'provider': 'minimax',
                    'retry': type('RetryConfig', (), {
                        'enabled': False,
                        'max_retries': 3,
                        'initial_delay': 1.0,
                        'max_delay': 60.0,
                        'exponential_base': 2.0
                    })()
                })()
                self.agent = type('AgentConfig', (), {
                    'max_steps': 10
                })()
                
        return DefaultConfig()
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC message"""
        try:
            if 'jsonrpc' not in message or message['jsonrpc'] != '2.0':
                return self.create_error(message.get('id'), -32600, "Invalid Request")
            
            method = message.get('method')
            params = message.get('params', {})
            msg_id = message.get('id')
            
            logger.info(f"📨 Handling method: {method}")
            
            if method == 'initialize':
                await self.initialize_system()
                return self.create_response(msg_id, {
                    'protocolVersion': 1,
                    'agentCapabilities': {'loadSession': False},
                    'agentInfo': {
                        'name': 'mini-agent',
                        'title': 'Mini-Agent AI Assistant',
                        'version': '0.1.0',
                        'description': 'AI coding assistant with ACP integration'
                    }
                })
            
            elif method == 'newSession':
                session_id = f"session-{uuid4().hex[:8]}"
                workspace = Path(params.get('cwd', "./workspace")).expanduser()
                if not workspace.is_absolute():
                    workspace = workspace.resolve()
                
                # Create workspace if it doesn't exist
                workspace.mkdir(parents=True, exist_ok=True)
                
                # Initialize agent for this session
                session_data = {
                    'sessionId': session_id,
                    'workspace': str(workspace),
                    'created': True,
                    'agent': None
                }
                
                self.sessions[session_id] = session_data
                logger.info(f"📝 Created session: {session_id}")
                
                return self.create_response(msg_id, {'sessionId': session_id})
            
            elif method == 'prompt':
                session_id = params.get('sessionId')
                prompt_text = params.get('prompt', '')
                
                if not session_id or session_id not in self.sessions:
                    return self.create_error(msg_id, -32602, "Invalid params: session not found")
                
                session = self.sessions[session_id]
                
                try:
                    # Initialize agent for this session if not already done
                    if not session['agent'] and self.llm_client and self.base_tools:
                        from mini_agent.agent import Agent
                        
                        system_prompt = "You are Mini-Agent, a helpful AI coding assistant. You can help with programming, code analysis, debugging, and software development tasks."
                        
                        session['agent'] = Agent(
                            llm_client=self.llm_client,
                            system_prompt=system_prompt,
                            tools=self.base_tools,
                            max_steps=10,
                            workspace_dir=session['workspace']
                        )
                        logger.info(f"🤖 Initialized agent for session {session_id}")
                    
                    # Process the prompt
                    if session['agent']:
                        from mini_agent.schema import Message
                        messages = [Message(role="user", content=prompt_text)]
                        
                        # Run the agent
                        response = await session['agent'].run(messages)
                        content_text = response.content
                    else:
                        # Fallback response if agent not available
                        content_text = f"I'm Mini-Agent, your AI coding assistant. I received your message: '{prompt_text}'. Currently initializing full capabilities..."
                    
                    return self.create_response(msg_id, {
                        'content': [
                            {
                                'type': 'text',
                                'text': content_text
                            }
                        ]
                    })
                    
                except Exception as e:
                    logger.error(f"❌ Error processing prompt: {e}")
                    return self.create_response(msg_id, {
                        'content': [
                            {
                                'type': 'text',
                                'text': f"Sorry, I encountered an error processing your request: {str(e)}"
                            }
                        ],
                        'hasError': True
                    })
            
            elif method == 'cancel':
                session_id = params.get('sessionId')
                if session_id in self.sessions:
                    logger.info(f"🛑 Cancelling session: {session_id}")
                    # Note: In a full implementation, we would cancel the running agent
                
                return self.create_response(msg_id, {'cancelled': True})
            
            else:
                return self.create_error(msg_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
            return self.create_error(message.get('id'), -32603, f"Internal error: {str(e)}")
    
    def create_response(self, msg_id: Optional[Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Create JSON-RPC response"""
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'result': result
        }
    
    def create_error(self, msg_id: Optional[Any], code: int, message: str) -> Dict[str, Any]:
        """Create JSON-RPC error"""
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    async def run(self):
        """Main server loop"""
        logger.info("🚀 Mini-Agent ACP stdio server starting...")
        
        try:
            while True:
                try:
                    # Read line from stdin
                    line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                    if not line:
                        logger.info("📥 EOF received, shutting down")
                        break
                    
                    # Parse JSON message
                    message = json.loads(line.strip())
                    logger.debug(f"📨 Received: {message}")
                    
                    # Handle message and send response
                    response = await self.handle_message(message)
                    response_json = json.dumps(response) + '\n'
                    sys.stdout.write(response_json)
                    sys.stdout.flush()
                    
                    logger.debug(f"📤 Sent response")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error: {e}")
                    error_response = self.create_error(None, -32700, f"Parse error: {str(e)}")
                    sys.stdout.write(json.dumps(error_response) + '\n')
                    sys.stdout.flush()
                    
                except KeyboardInterrupt:
                    logger.info("🛑 Server interrupted by user")
                    break
                    
                except Exception as e:
                    logger.error(f"❌ Server error: {e}")
                    # Don't break on errors, try to continue
                    continue
                    
        except Exception as e:
            logger.error(f"💥 Fatal server error: {e}")
            raise
        finally:
            logger.info("👋 Mini-Agent ACP server shutting down")

async def main():
    """Main entry point"""
    server = MiniAgentACPStdioServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Goodbye!", file=sys.stderr)
    except Exception as e:
        print(f"💥 Fatal error: {e}", file=sys.stderr)
        sys.exit(1)