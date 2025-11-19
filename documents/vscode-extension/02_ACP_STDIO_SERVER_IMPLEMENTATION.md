# Phase 1: ACP Stdio Server Implementation
## Building JSON-RPC 2.0 over Stdio for VS Code/Zed Integration

**Phase**: 1 of 5  
**Priority**: 🔥 **CRITICAL PATH**  
**Estimated Time**: 4-6 hours  
**Dependencies**: None (uses existing Mini-Agent core)

---

## 🎯 Objective

Transform Mini-Agent's WebSocket-based ACP server into a stdio-based JSON-RPC 2.0 server that complies with the official Agent Client Protocol specification and works with VS Code/Zed editors.

---

## 📋 Current State vs. Target State

### Current Implementation (`mini_agent/acp/enhanced_server.py`)
```python
# Uses WebSocket
async with websockets.serve(self.handle_websocket_connection, host, port):
    # WebSocket-based communication
```

**Issues**:
- ❌ Uses WebSocket (not compatible with VS Code/Zed stdio requirement)
- ❌ Custom message format (not standard JSON-RPC 2.0)
- ❌ Requires network port (complicates deployment)

### Target Implementation
```python
# Uses stdin/stdout
async def handle_stdio():
    # Read JSON-RPC requests from stdin
    # Send JSON-RPC responses to stdout
    # Follow official ACP specification
```

**Benefits**:
- ✅ Standard stdio transport (compatible with all editors)
- ✅ JSON-RPC 2.0 compliant
- ✅ No network configuration needed
- ✅ Matches Zed's external agent implementation

---

## 🏗️ Architecture Design

### File Structure
```
mini_agent/acp/
├── __init__.py                 # Package exports
├── protocol.py                 # NEW: JSON-RPC 2.0 protocol handlers
├── stdio_server.py             # NEW: Main stdio server implementation
├── session_manager.py          # NEW: Session lifecycle management
├── message_types.py            # NEW: ACP message type definitions
├── server.py                   # KEEP: Legacy entry point (points to stdio)
└── enhanced_server.py          # KEEP: Legacy WebSocket server (optional)
```

### Component Responsibilities

#### 1. `protocol.py` - JSON-RPC 2.0 Handler
**Purpose**: Pure protocol implementation (no I/O, no business logic)

```python
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
import json

@dataclass
class JSONRPCRequest:
    """JSON-RPC 2.0 Request"""
    jsonrpc: str = "2.0"
    method: str = ""
    params: Optional[Dict[str, Any]] = None
    id: Optional[Union[str, int]] = None
    
    @classmethod
    def from_json(cls, data: str) -> 'JSONRPCRequest':
        obj = json.loads(data)
        return cls(
            jsonrpc=obj.get("jsonrpc", "2.0"),
            method=obj["method"],
            params=obj.get("params"),
            id=obj.get("id")
        )
    
    def is_notification(self) -> bool:
        """Notifications don't have an 'id' field"""
        return self.id is None

@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 Response"""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[str, int]] = None
    
    def to_json(self) -> str:
        data = {"jsonrpc": self.jsonrpc}
        if self.error:
            data["error"] = self.error
        else:
            data["result"] = self.result
        if self.id is not None:
            data["id"] = self.id
        return json.dumps(data)

@dataclass
class JSONRPCNotification:
    """JSON-RPC 2.0 Notification (no id, no response expected)"""
    jsonrpc: str = "2.0"
    method: str = ""
    params: Optional[Dict[str, Any]] = None
    
    def to_json(self) -> str:
        data = {
            "jsonrpc": self.jsonrpc,
            "method": self.method
        }
        if self.params:
            data["params"] = self.params
        return json.dumps(data)

class JSONRPCError:
    """Standard JSON-RPC 2.0 error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    
    @staticmethod
    def create_error(code: int, message: str, data: Any = None) -> Dict[str, Any]:
        error = {"code": code, "message": message}
        if data:
            error["data"] = data
        return error
```

#### 2. `message_types.py` - ACP Message Type Definitions

```python
"""
ACP Protocol Message Types
Based on: https://agentclientprotocol.com/protocol/overview
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

class ACPMethod(Enum):
    """Official ACP Methods"""
    # Lifecycle
    INITIALIZE = "initialize"
    SHUTDOWN = "shutdown"
    
    # Session Management
    CREATE_SESSION = "agent/createSession"
    CANCEL_SESSION = "agent/cancelSession"
    
    # Prompting
    PROMPT = "agent/prompt"
    
    # Notifications (no response expected)
    INITIALIZED = "initialized"
    AGENT_UPDATE = "agent/update"
    TOOL_CALL = "agent/toolCall"
    TOOL_RESULT = "agent/toolResult"

@dataclass
class InitializeParams:
    """Parameters for initialize request"""
    protocolVersion: str
    capabilities: Dict[str, Any]
    clientInfo: Dict[str, str]

@dataclass
class InitializeResult:
    """Result for initialize request"""
    protocolVersion: str
    capabilities: Dict[str, Any]
    serverInfo: Dict[str, str]

@dataclass
class CreateSessionParams:
    """Parameters for agent/createSession"""
    workspaceDir: str
    environmentVars: Optional[Dict[str, str]] = None

@dataclass
class CreateSessionResult:
    """Result for agent/createSession"""
    sessionId: str

@dataclass
class PromptParams:
    """Parameters for agent/prompt"""
    sessionId: str
    prompt: str

@dataclass
class PromptResult:
    """Result for agent/prompt (final response)"""
    content: str
    
@dataclass
class AgentUpdateParams:
    """Parameters for agent/update notification"""
    sessionId: str
    updateType: str  # "thinking", "tool_call", "tool_result", "response"
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
```

#### 3. `session_manager.py` - Session Lifecycle

```python
"""
ACP Session Manager
Manages agent sessions and their lifecycle
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

from mini_agent.agent import Agent
from mini_agent.llm import LLMClient
from mini_agent.config import Config

@dataclass
class SessionContext:
    """Context for an ACP session"""
    session_id: str
    workspace_dir: Path
    created_at: datetime
    agent: Agent
    cancelled: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "sessionId": self.session_id,
            "workspaceDir": str(self.workspace_dir),
            "createdAt": self.created_at.isoformat(),
            "cancelled": self.cancelled
        }

class SessionManager:
    """Manages ACP sessions"""
    
    def __init__(self, config: Config, llm_client: LLMClient):
        self.config = config
        self.llm_client = llm_client
        self.sessions: Dict[str, SessionContext] = {}
        self.base_tools = []
    
    def initialize_tools(self):
        """Initialize base tools for sessions"""
        from mini_agent.tools.bash_tool import BashTool
        from mini_agent.tools.file_tools import ReadTool, WriteTool, EditTool
        from mini_agent.tools.note_tool import RecordNoteTool
        
        # Initialize with dummy workspace (will be overridden per session)
        self.base_tools = [
            BashTool(),
            ReadTool(workspace_dir="./"),
            WriteTool(workspace_dir="./"),
            EditTool(workspace_dir="./"),
            RecordNoteTool()
        ]
    
    def create_session(self, workspace_dir: str) -> str:
        """Create new session with agent"""
        session_id = str(uuid.uuid4())
        workspace_path = Path(workspace_dir).expanduser().resolve()
        
        # Create workspace if doesn't exist
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create agent for session
        system_prompt = self._get_system_prompt()
        agent = Agent(
            llm_client=self.llm_client,
            system_prompt=system_prompt,
            tools=self.base_tools,
            max_steps=self.config.agent.max_steps,
            workspace_dir=str(workspace_path)
        )
        
        # Store session
        session = SessionContext(
            session_id=session_id,
            workspace_dir=workspace_path,
            created_at=datetime.now(),
            agent=agent
        )
        self.sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def cancel_session(self, session_id: str) -> bool:
        """Cancel session"""
        if session_id in self.sessions:
            self.sessions[session_id].cancelled = True
            return True
        return False
    
    def close_session(self, session_id: str):
        """Close and remove session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for agent"""
        return """You are Mini-Agent, an AI coding assistant integrated with VS Code.

You have access to:
- File operations (read, write, edit)
- Bash commands
- Web search (Z.AI)
- Session notes for memory
- Advanced skills system

Always:
- Be concise and helpful
- Show your work (explain tool usage)
- Provide code examples when relevant
- Ask clarifying questions if needed"""
```

#### 4. `stdio_server.py` - Main Server Implementation

```python
"""
ACP Stdio Server
JSON-RPC 2.0 over stdin/stdout for VS Code/Zed integration
"""

import asyncio
import sys
import logging
from typing import Optional

from mini_agent.config import Config
from mini_agent.llm import LLMClient
from mini_agent.schema import LLMProvider

from .protocol import (
    JSONRPCRequest, 
    JSONRPCResponse, 
    JSONRPCNotification,
    JSONRPCError
)
from .message_types import (
    ACPMethod,
    InitializeParams,
    CreateSessionParams,
    PromptParams,
    AgentUpdateParams
)
from .session_manager import SessionManager

logger = logging.getLogger(__name__)

class ACPStdioServer:
    """ACP Server using stdio transport"""
    
    def __init__(self):
        self.config: Optional[Config] = None
        self.llm_client: Optional[LLMClient] = None
        self.session_manager: Optional[SessionManager] = None
        self.initialized = False
        self.shutdown_requested = False
    
    async def start(self):
        """Start stdio server"""
        logger.info("🚀 Starting Mini-Agent ACP Server (stdio mode)")
        
        # Setup stdin/stdout as line-buffered
        sys.stdin.reconfigure(encoding='utf-8', newline='\n')
        sys.stdout.reconfigure(encoding='utf-8', newline='\n')
        
        # Main message loop
        try:
            while not self.shutdown_requested:
                # Read one line from stdin (blocking)
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:  # EOF
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Process message
                await self.handle_message(line)
                
        except KeyboardInterrupt:
            logger.info("Server interrupted")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
        finally:
            logger.info("🛑 ACP Server stopped")
    
    async def handle_message(self, message_str: str):
        """Handle incoming JSON-RPC message"""
        try:
            # Parse JSON-RPC request
            request = JSONRPCRequest.from_json(message_str)
            logger.debug(f"📨 Received: {request.method}")
            
            # Route to handler
            if request.method == ACPMethod.INITIALIZE.value:
                await self.handle_initialize(request)
            elif request.method == ACPMethod.SHUTDOWN.value:
                await self.handle_shutdown(request)
            elif request.method == ACPMethod.CREATE_SESSION.value:
                await self.handle_create_session(request)
            elif request.method == ACPMethod.PROMPT.value:
                await self.handle_prompt(request)
            elif request.method == ACPMethod.CANCEL_SESSION.value:
                await self.handle_cancel_session(request)
            else:
                # Unknown method
                self.send_error_response(
                    request.id,
                    JSONRPCError.METHOD_NOT_FOUND,
                    f"Unknown method: {request.method}"
                )
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            self.send_error_response(
                None,
                JSONRPCError.PARSE_ERROR,
                "Invalid JSON"
            )
        except Exception as e:
            logger.error(f"Message handling error: {e}", exc_info=True)
            self.send_error_response(
                None,
                JSONRPCError.INTERNAL_ERROR,
                str(e)
            )
    
    async def handle_initialize(self, request: JSONRPCRequest):
        """Handle initialize request"""
        try:
            # Load config and initialize components
            self.config = Config.load()
            
            # Initialize LLM client
            provider = (LLMProvider.ANTHROPIC 
                       if self.config.llm.provider.lower() == "anthropic"
                       else LLMProvider.OPENAI)
            
            self.llm_client = LLMClient(
                api_key=self.config.llm.api_key,
                provider=provider,
                api_base=self.config.llm.api_base,
                model=self.config.llm.model
            )
            
            # Initialize session manager
            self.session_manager = SessionManager(self.config, self.llm_client)
            self.session_manager.initialize_tools()
            
            self.initialized = True
            
            # Send response
            result = {
                "protocolVersion": "1.0",
                "capabilities": {
                    "sessionManagement": True,
                    "streaming": True,
                    "toolExecution": True,
                    "fileOperations": True,
                    "webSearch": True
                },
                "serverInfo": {
                    "name": "mini-agent",
                    "version": "0.1.0"
                }
            }
            
            self.send_response(request.id, result)
            
            # Send initialized notification
            self.send_notification(ACPMethod.INITIALIZED.value, {})
            
            logger.info("✅ Server initialized")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}", exc_info=True)
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                f"Initialization failed: {str(e)}"
            )
    
    async def handle_create_session(self, request: JSONRPCRequest):
        """Handle agent/createSession"""
        if not self.initialized:
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                "Server not initialized"
            )
            return
        
        try:
            params = request.params
            workspace_dir = params.get("workspaceDir", "./workspace")
            
            # Create session
            session_id = self.session_manager.create_session(workspace_dir)
            
            logger.info(f"📝 Created session: {session_id}")
            
            # Send response
            result = {"sessionId": session_id}
            self.send_response(request.id, result)
            
        except Exception as e:
            logger.error(f"Session creation error: {e}", exc_info=True)
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                f"Session creation failed: {str(e)}"
            )
    
    async def handle_prompt(self, request: JSONRPCRequest):
        """Handle agent/prompt with streaming"""
        if not self.initialized:
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                "Server not initialized"
            )
            return
        
        try:
            params = request.params
            session_id = params.get("sessionId")
            prompt = params.get("prompt")
            
            if not session_id or not prompt:
                self.send_error_response(
                    request.id,
                    JSONRPCError.INVALID_PARAMS,
                    "Missing sessionId or prompt"
                )
                return
            
            session = self.session_manager.get_session(session_id)
            if not session:
                self.send_error_response(
                    request.id,
                    JSONRPCError.INVALID_PARAMS,
                    f"Invalid session: {session_id}"
                )
                return
            
            logger.info(f"🧠 Processing prompt for session {session_id}")
            
            # Send thinking notification
            self.send_notification(
                ACPMethod.AGENT_UPDATE.value,
                {
                    "sessionId": session_id,
                    "updateType": "thinking",
                    "content": "Processing your request..."
                }
            )
            
            # Run agent
            from mini_agent.schema import Message
            response = await session.agent.run([Message(role="user", content=prompt)])
            
            # Send final response
            result = {"content": response.content}
            self.send_response(request.id, result)
            
            logger.info(f"✅ Completed prompt for session {session_id}")
            
        except Exception as e:
            logger.error(f"Prompt processing error: {e}", exc_info=True)
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                f"Prompt processing failed: {str(e)}"
            )
    
    async def handle_cancel_session(self, request: JSONRPCRequest):
        """Handle agent/cancelSession"""
        try:
            params = request.params
            session_id = params.get("sessionId")
            
            if self.session_manager.cancel_session(session_id):
                result = {"cancelled": True}
            else:
                result = {"cancelled": False}
            
            self.send_response(request.id, result)
            
        except Exception as e:
            logger.error(f"Cancel error: {e}", exc_info=True)
            self.send_error_response(
                request.id,
                JSONRPCError.INTERNAL_ERROR,
                str(e)
            )
    
    async def handle_shutdown(self, request: JSONRPCRequest):
        """Handle shutdown request"""
        self.shutdown_requested = True
        self.send_response(request.id, {})
        logger.info("Shutdown requested")
    
    def send_response(self, request_id, result):
        """Send JSON-RPC response"""
        response = JSONRPCResponse(id=request_id, result=result)
        self._write_message(response.to_json())
    
    def send_error_response(self, request_id, code: int, message: str):
        """Send JSON-RPC error response"""
        error = JSONRPCError.create_error(code, message)
        response = JSONRPCResponse(id=request_id, error=error)
        self._write_message(response.to_json())
    
    def send_notification(self, method: str, params: dict):
        """Send JSON-RPC notification"""
        notification = JSONRPCNotification(method=method, params=params)
        self._write_message(notification.to_json())
    
    def _write_message(self, message: str):
        """Write message to stdout"""
        sys.stdout.write(message + "\n")
        sys.stdout.flush()


async def main():
    """Main entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr  # Log to stderr, keep stdout for protocol
    )
    
    server = ACPStdioServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧪 Testing Strategy

### 1. Unit Tests for Protocol Layer

```python
# tests/test_acp_protocol.py
import json
from mini_agent.acp.protocol import JSONRPCRequest, JSONRPCResponse, JSONRPCError

def test_parse_request():
    data = '{"jsonrpc": "2.0", "method": "initialize", "id": 1}'
    req = JSONRPCRequest.from_json(data)
    assert req.method == "initialize"
    assert req.id == 1
    assert not req.is_notification()

def test_notification_no_id():
    data = '{"jsonrpc": "2.0", "method": "agent/update", "params": {}}'
    req = JSONRPCRequest.from_json(data)
    assert req.is_notification()

def test_response_serialization():
    resp = JSONRPCResponse(id=1, result={"status": "ok"})
    data = json.loads(resp.to_json())
    assert data["id"] == 1
    assert data["result"]["status"] == "ok"
```

### 2. Integration Test with Stdio

```python
# tests/test_acp_stdio_integration.py
import asyncio
import subprocess
import json

async def test_stdio_server():
    """Test ACP server via stdio"""
    
    # Start server
    proc = await asyncio.create_subprocess_exec(
        "python", "-m", "mini_agent.acp.stdio_server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Send initialize
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": 1,
        "params": {
            "protocolVersion": "1.0",
            "capabilities": {},
            "clientInfo": {"name": "test"}
        }
    }
    
    proc.stdin.write((json.dumps(init_request) + "\n").encode())
    await proc.stdin.drain()
    
    # Read response
    line = await proc.stdout.readline()
    response = json.loads(line.decode())
    
    assert response["id"] == 1
    assert "result" in response
    assert response["result"]["serverInfo"]["name"] == "mini-agent"
    
    # Cleanup
    proc.terminate()
    await proc.wait()
```

### 3. Manual Testing with CLI Client

```bash
# Create simple test client
cat > test_client.py << 'EOF'
import sys
import json

def send_request(method, params, req_id):
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": req_id
    }
    print(json.dumps(request), flush=True)

def read_response():
    line = sys.stdin.readline()
    return json.loads(line)

# Test sequence
send_request("initialize", {"protocolVersion": "1.0", "capabilities": {}, "clientInfo": {"name": "test"}}, 1)
response = read_response()
print(f"Initialize: {response}", file=sys.stderr)

send_request("agent/createSession", {"workspaceDir": "./test_workspace"}, 2)
response = read_response()
session_id = response["result"]["sessionId"]
print(f"Session: {session_id}", file=sys.stderr)

send_request("agent/prompt", {"sessionId": session_id, "prompt": "Hello!"}, 3)
response = read_response()
print(f"Response: {response['result']['content']}", file=sys.stderr)
EOF

# Test the server
python -m mini_agent.acp.stdio_server < test_client.py
```

---

## ✅ Acceptance Criteria

- [ ] Server starts and accepts JSON-RPC messages on stdin
- [ ] Server sends JSON-RPC responses/notifications on stdout
- [ ] Initialize handshake works correctly
- [ ] Session creation returns valid session ID
- [ ] Prompt processing executes agent and returns response
- [ ] Error handling returns proper JSON-RPC error objects
- [ ] Logging goes to stderr (not stdout)
- [ ] All unit tests pass
- [ ] Integration test with stdio passes
- [ ] Manual CLI client test succeeds

---

## 📦 Deliverables

1. ✅ `mini_agent/acp/protocol.py` - JSON-RPC 2.0 implementation
2. ✅ `mini_agent/acp/message_types.py` - ACP message definitions
3. ✅ `mini_agent/acp/session_manager.py` - Session lifecycle
4. ✅ `mini_agent/acp/stdio_server.py` - Main server
5. ✅ `mini_agent/acp/__init__.py` - Updated exports
6. ✅ `tests/test_acp_protocol.py` - Protocol tests
7. ✅ `tests/test_acp_stdio_integration.py` - Integration tests
8. ✅ `scripts/test_acp_client.py` - Manual testing client

---

**Next Phase**: [03_VSCODE_EXTENSION_DEVELOPMENT.md](./03_VSCODE_EXTENSION_DEVELOPMENT.md)
