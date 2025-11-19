"""
Enhanced ACP (Agent Client Protocol) Server for Mini-Agent
This implements a proper ACP server following the protocol specifications
"""

import asyncio
import json
import logging
import os
import websockets
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

# Mini-Agent imports
from mini_agent.config import Config
from mini_agent.llm import LLMClient
from mini_agent.schema import LLMProvider
from mini_agent.agent import Agent

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """ACP Message Types"""
    INITIALIZE = "initialize"
    NEW_SESSION = "newSession"
    PROMPT = "prompt"
    CANCEL_SESSION = "cancelSession"
    CLEANUP = "cleanup"
    HEARTBEAT = "heartbeat"


@dataclass
class ACPMessage:
    """Standardized ACP Message Format"""
    id: str
    type: str
    timestamp: str
    session_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        # Remove None values for cleaner JSON
        return {k: v for k, v in result.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ACPMessage':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class SessionContext:
    """ACP Session Context"""
    session_id: str
    workspace_dir: Path
    created_at: datetime
    last_activity: datetime
    messages: List[Dict[str, Any]]
    agent: Optional[Agent] = None
    cancelled: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "sessionId": self.session_id,
            "workspaceDir": str(self.workspace_dir),
            "createdAt": self.created_at.isoformat(),
            "lastActivity": self.last_activity.isoformat(),
            "messageCount": len(self.messages),
            "cancelled": self.cancelled
        }


class MiniAgentACPServer:
    """Enhanced ACP Server implementing the full protocol"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.sessions: Dict[str, SessionContext] = {}
        self.config: Optional[Config] = None
        self.llm_client: Optional[LLMClient] = None
        self.base_tools: List = []
        self.running = False
        
    async def initialize(self):
        """Initialize the ACP server components"""
        logger.info("Initializing Mini-Agent ACP Server...")
        
        try:
            # Load configuration with environment variables
            self.config = Config.load()
            logger.info("✅ Configuration loaded")
            
            # Initialize LLM client
            provider = LLMProvider.ANTHROPIC if self.config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI
            self.llm_client = LLMClient(
                api_key=self.config.llm.api_key,
                provider=provider,
                api_base=self.config.llm.api_base,
                model=self.config.llm.model,
            )
            logger.info("✅ LLM client initialized")
            
            # Initialize base tools (simplified)
            from mini_agent.tools.bash_tool import BashTool
            from mini_agent.tools.file_tools import ReadTool, WriteTool, EditTool
            
            self.base_tools = [
                BashTool(),
                ReadTool(workspace_dir="./"),
                WriteTool(workspace_dir="./"),
                EditTool(workspace_dir="./")
            ]
            logger.info("✅ Base tools initialized")
            
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            raise
    
    async def handle_websocket_connection(self, websocket, path):
        """Handle WebSocket connection"""
        client_id = str(uuid.uuid4())
        logger.info(f"📡 New WebSocket connection from {client_id}")
        
        try:
            # Send initialization acknowledgment
            await websocket.send(json.dumps({
                "type": "connection_established",
                "clientId": client_id,
                "timestamp": datetime.now().isoformat(),
                "protocol": "acp",
                "version": "1.0"
            }))
            
            async for message_data in websocket:
                try:
                    await self.process_message(websocket, client_id, message_data)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await self.send_error(websocket, f"Message processing error: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"📡 Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"WebSocket error for client {client_id}: {e}")
    
    async def process_message(self, websocket, client_id: str, message_data: str):
        """Process incoming ACP message"""
        try:
            message = ACPMessage.from_dict(json.loads(message_data))
            logger.info(f"📨 Processing message {message.id} of type {message.type}")
            
            # Update session activity
            if message.session_id and message.session_id in self.sessions:
                self.sessions[message.session_id].last_activity = datetime.now()
            
            # Route to appropriate handler
            if message.type == MessageType.INITIALIZE.value:
                await self.handle_initialize(websocket, message)
            elif message.type == MessageType.NEW_SESSION.value:
                await self.handle_new_session(websocket, message)
            elif message.type == MessageType.PROMPT.value:
                await self.handle_prompt(websocket, message)
            elif message.type == MessageType.CANCEL_SESSION.value:
                await self.handle_cancel_session(websocket, message)
            elif message.type == MessageType.HEARTBEAT.value:
                await self.handle_heartbeat(websocket, message)
            elif message.type == MessageType.CLEANUP.value:
                await self.handle_cleanup(websocket, message)
            else:
                await self.send_error(websocket, f"Unknown message type: {message.type}")
                
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON in message")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_error(websocket, f"Internal server error: {str(e)}")
    
    async def handle_initialize(self, websocket, message: ACPMessage):
        """Handle initialize message"""
        capabilities = {
            "protocol_version": "1.0",
            "features": [
                "real_time_communication",
                "session_management", 
                "tool_integration",
                "file_operations",
                "web_search",
                "code_generation"
            ],
            "agent_info": {
                "name": "mini-agent",
                "version": "0.1.0",
                "description": "Mini-Agent AI assistant with ACP integration"
            }
        }
        
        response = ACPMessage(
            id=str(uuid.uuid4()),
            type="initialize_response",
            timestamp=datetime.now().isoformat(),
            data=capabilities
        )
        
        await self.send_message(websocket, response)
    
    async def handle_new_session(self, websocket, message: ACPMessage):
        """Handle new session creation"""
        try:
            workspace_dir = Path(message.data.get("workspaceDir", "./workspace")).expanduser()
            if not workspace_dir.is_absolute():
                workspace_dir = workspace_dir.resolve()
            
            # Create workspace if it doesn't exist
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
            # Create new session
            session_id = str(uuid.uuid4())
            session = SessionContext(
                session_id=session_id,
                workspace_dir=workspace_dir,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                messages=[]
            )
            
            # Initialize agent for this session
            system_prompt = "You are a helpful AI coding assistant integrated with VS Code through the Agent Client Protocol."
            
            session.agent = Agent(
                llm_client=self.llm_client,
                system_prompt=system_prompt,
                tools=self.base_tools,
                max_steps=self.config.agent.max_steps,
                workspace_dir=str(workspace_dir)
            )
            
            self.sessions[session_id] = session
            
            logger.info(f"📝 Created new session: {session_id}")
            
            response = ACPMessage(
                id=str(uuid.uuid4()),
                type="new_session_response",
                timestamp=datetime.now().isoformat(),
                session_id=session_id,
                data={
                    "sessionId": session_id,
                    "workspaceDir": str(workspace_dir),
                    "createdAt": session.created_at.isoformat()
                }
            )
            
            await self.send_message(websocket, response)
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            await self.send_error(websocket, f"Session creation failed: {str(e)}")
    
    async def handle_prompt(self, websocket, message: ACPMessage):
        """Handle prompt processing"""
        try:
            session_id = message.session_id
            if not session_id or session_id not in self.sessions:
                await self.send_error(websocket, "Invalid session ID")
                return
            
            session = self.sessions[session_id]
            if session.cancelled:
                await self.send_error(websocket, "Session has been cancelled")
                return
            
            prompt_text = message.data.get("prompt", "")
            if not prompt_text:
                await self.send_error(websocket, "Empty prompt")
                return
            
            # Log the prompt
            prompt_entry = {
                "type": "user_prompt",
                "content": prompt_text,
                "timestamp": datetime.now().isoformat()
            }
            session.messages.append(prompt_entry)
            
            logger.info(f"🧠 Processing prompt for session {session_id}")
            
            # Send processing started notification
            await websocket.send(json.dumps({
                "type": "status_update",
                "sessionId": session_id,
                "status": "processing",
                "timestamp": datetime.now().isoformat()
            }))
            
            try:
                # Process with agent
                from mini_agent.schema import Message
                response = await session.agent.run([Message(role="user", content=prompt_text)])
                
                # Log the response
                response_entry = {
                    "type": "agent_response",
                    "content": response.content,
                    "timestamp": datetime.now().isoformat()
                }
                session.messages.append(response_entry)
                
                # Send response
                response_message = ACPMessage(
                    id=str(uuid.uuid4()),
                    type="prompt_response",
                    timestamp=datetime.now().isoformat(),
                    session_id=session_id,
                    data={
                        "content": response.content,
                        "messageId": str(uuid.uuid4()),
                        "status": "completed"
                    }
                )
                
                await self.send_message(websocket, response_message)
                
            except Exception as e:
                logger.error(f"Agent processing error: {e}")
                error_entry = {
                    "type": "error",
                    "content": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                session.messages.append(error_entry)
                
                await self.send_error(websocket, f"Agent processing failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error handling prompt: {e}")
            await self.send_error(websocket, f"Prompt processing failed: {str(e)}")
    
    async def handle_cancel_session(self, websocket, message: ACPMessage):
        """Handle session cancellation"""
        try:
            session_id = message.session_id
            if session_id and session_id in self.sessions:
                self.sessions[session_id].cancelled = True
                logger.info(f"🛑 Cancelled session: {session_id}")
                
                response = ACPMessage(
                    id=str(uuid.uuid4()),
                    type="cancel_session_response",
                    timestamp=datetime.now().isoformat(),
                    session_id=session_id,
                    data={"status": "cancelled"}
                )
                
                await self.send_message(websocket, response)
            else:
                await self.send_error(websocket, "Invalid session ID")
                
        except Exception as e:
            logger.error(f"Error cancelling session: {e}")
            await self.send_error(websocket, f"Session cancellation failed: {str(e)}")
    
    async def handle_heartbeat(self, websocket, message: ACPMessage):
        """Handle heartbeat to keep connection alive"""
        response = ACPMessage(
            id=str(uuid.uuid4()),
            type="heartbeat_response",
            timestamp=datetime.now().isoformat(),
            data={"status": "alive", "active_sessions": len(self.sessions)}
        )
        await self.send_message(websocket, response)
    
    async def handle_cleanup(self, websocket, message: ACPMessage):
        """Handle cleanup request"""
        try:
            # Cancel all sessions
            for session in self.sessions.values():
                session.cancelled = True
            
            # Clear sessions
            self.sessions.clear()
            
            response = ACPMessage(
                id=str(uuid.uuid4()),
                type="cleanup_response",
                timestamp=datetime.now().isoformat(),
                data={"status": "cleaned"}
            )
            
            await self.send_message(websocket, response)
            logger.info("🧹 Cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            await self.send_error(websocket, f"Cleanup failed: {str(e)}")
    
    async def send_message(self, websocket, message: ACPMessage):
        """Send ACP message to client"""
        try:
            await websocket.send(json.dumps(message.to_dict()))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def send_error(self, websocket, error_message: str):
        """Send error message to client"""
        try:
            error_response = ACPMessage(
                id=str(uuid.uuid4()),
                type="error",
                timestamp=datetime.now().isoformat(),
                error=error_message
            )
            await self.send_message(websocket, error_response)
        except Exception as e:
            logger.error(f"Error sending error message: {e}")
    
    async def start_server(self):
        """Start the WebSocket ACP server"""
        if not self.llm_client:
            await self.initialize()
        
        self.running = True
        logger.info(f"🚀 Starting ACP server on ws://{self.host}:{self.port}")
        
        try:
            async with websockets.serve(self.handle_websocket_connection, self.host, self.port):
                logger.info("✅ ACP server started successfully")
                logger.info(f"📡 WebSocket endpoint: ws://{self.host}:{self.port}")
                logger.info("🎯 Ready for VS Code extension connections")
                
                # Keep server running
                while self.running:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Failed to start ACP server: {e}")
            raise
        finally:
            await self.stop_server()
    
    async def stop_server(self):
        """Stop the ACP server"""
        self.running = False
        
        # Cleanup all sessions
        for session in self.sessions.values():
            session.cancelled = True
        self.sessions.clear()
        
        logger.info("🛑 ACP server stopped")


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mini-Agent ACP Server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Server port (default: 8765)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start server
    server = MiniAgentACPServer(host=args.host, port=args.port)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
