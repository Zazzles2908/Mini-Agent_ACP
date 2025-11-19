# VS Code Extension Quick Reference
## Developer Cheat Sheet for Implementation

**Purpose**: Quick lookup for common tasks during implementation  
**Use Case**: Have this open while coding

---

## 🔧 Common Commands

### ACP Server
```bash
# Start ACP server (stdio mode)
python -m mini_agent.acp.stdio_server

# Test with debug logging
python -m mini_agent.acp.stdio_server --log-level DEBUG

# Run unit tests
python -m pytest tests/test_acp_protocol.py -v

# Run integration tests
python -m pytest tests/test_acp_stdio_integration.py -v
```

### VS Code Extension
```bash
# Install dependencies
cd vscode-extension && npm install

# Compile TypeScript
npm run compile

# Watch mode (auto-compile on changes)
npm run watch

# Run tests
npm test

# Package extension
npm run package

# Install locally for testing
code --install-extension mini-agent-vscode-0.1.0.vsix
```

---

## 📡 ACP Protocol Cheat Sheet

### JSON-RPC 2.0 Message Format
```json
// Request (expects response)
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "agent/createSession",
  "params": { "workspaceDir": "/path" }
}

// Response (success)
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { "sessionId": "uuid" }
}

// Response (error)
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": { "details": "..." }
  }
}

// Notification (no response expected)
{
  "jsonrpc": "2.0",
  "method": "agent/update",
  "params": {
    "sessionId": "uuid",
    "updateType": "thinking",
    "content": "Processing..."
  }
}
```

### ACP Methods
| Method | Type | Purpose |
|--------|------|---------|
| `initialize` | Request | Initialize connection |
| `initialized` | Notification | Server ready |
| `agent/createSession` | Request | Create new session |
| `agent/prompt` | Request | Send user prompt |
| `agent/update` | Notification | Streaming update |
| `agent/cancelSession` | Request | Cancel operation |
| `shutdown` | Request | Stop server |

### Error Codes
| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | Invalid JSON-RPC |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Bad parameters |
| -32603 | Internal error | Server error |

---

## 💻 Code Snippets

### Python: ACP Server

#### Send JSON-RPC Response
```python
def send_response(request_id, result):
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()
```

#### Send Notification
```python
def send_notification(method, params):
    notification = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }
    sys.stdout.write(json.dumps(notification) + "\n")
    sys.stdout.flush()
```

#### Read Request from stdin
```python
async def read_request():
    line = await asyncio.get_event_loop().run_in_executor(
        None, sys.stdin.readline
    )
    return json.loads(line.strip())
```

### TypeScript: VS Code Extension

#### Spawn ACP Server
```typescript
const process = spawn('python', ['-m', 'mini_agent.acp.stdio_server'], {
  stdio: ['pipe', 'pipe', 'pipe']
});
```

#### Send JSON-RPC Request
```typescript
function sendRequest(method: string, params: any, id: number): void {
  const request = {
    jsonrpc: '2.0',
    id,
    method,
    params
  };
  process.stdin!.write(JSON.stringify(request) + '\n');
}
```

#### Read Response
```typescript
const rl = readline.createInterface({
  input: process.stdout,
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  const message = JSON.parse(line);
  if ('id' in message) {
    // Response
    handleResponse(message);
  } else {
    // Notification
    handleNotification(message);
  }
});
```

#### Register Chat Participant
```typescript
const participant = vscode.chat.createChatParticipant(
  'mini-agent',
  async (request, context, stream, token) => {
    // Get session
    const sessionId = await sessionManager.getOrCreateSession(request);
    
    // Send prompt
    const response = await acpClient.sendPrompt(sessionId, request.prompt);
    
    // Stream response
    stream.markdown(response);
  }
);
```

#### Stream Markdown Response
```typescript
function streamResponse(stream: vscode.ChatResponseStream, content: string) {
  // Split into chunks for streaming effect
  const chunks = content.split(' ');
  for (const chunk of chunks) {
    stream.markdown(chunk + ' ');
  }
}
```

---

## 🧪 Testing Patterns

### Python: Test ACP Protocol
```python
def test_jsonrpc_request():
    data = '{"jsonrpc": "2.0", "method": "initialize", "id": 1}'
    req = JSONRPCRequest.from_json(data)
    assert req.method == "initialize"
    assert req.id == 1
```

### Python: Test Stdio Communication
```python
async def test_stdio_echo():
    proc = await asyncio.create_subprocess_exec(
        "python", "-m", "mini_agent.acp.stdio_server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    
    # Send request
    request = {"jsonrpc": "2.0", "method": "initialize", "id": 1, "params": {}}
    proc.stdin.write((json.dumps(request) + "\n").encode())
    await proc.stdin.drain()
    
    # Read response
    line = await proc.stdout.readline()
    response = json.loads(line.decode())
    assert response["id"] == 1
```

### TypeScript: Test ACP Client
```typescript
describe('ACPClient', () => {
  let client: ACPClient;
  
  beforeEach(() => {
    client = new ACPClient('python', ['-m', 'mini_agent.acp.stdio_server']);
  });
  
  afterEach(async () => {
    await client.stop();
  });
  
  it('should initialize successfully', async () => {
    await client.start();
    const result = await client.initialize();
    expect(result.serverInfo.name).toBe('mini-agent');
  });
});
```

---

## 🐛 Debugging Tips

### ACP Server Issues

**Server not starting:**
```bash
# Check Python path
which python

# Test Mini-Agent imports
python -c "from mini_agent.config import Config; print('OK')"

# Run with debug logging
python -m mini_agent.acp.stdio_server --log-level DEBUG
```

**JSON-RPC errors:**
```python
# Add debug logging to stdio_server.py
logger.debug(f"Received: {message_str}")
logger.debug(f"Parsed: {request}")
logger.debug(f"Sending: {response}")
```

**Stdin/stdout issues:**
```python
# Verify streams are line-buffered
sys.stdin.reconfigure(encoding='utf-8', newline='\n')
sys.stdout.reconfigure(encoding='utf-8', newline='\n')

# Always flush after write
sys.stdout.write(message + "\n")
sys.stdout.flush()
```

### VS Code Extension Issues

**Extension not activating:**
```typescript
// Check activation events in package.json
"activationEvents": ["onStartupFinished"]

// Add logging to activate()
export function activate(context: vscode.ExtensionContext) {
  console.log('Mini-Agent extension activating...');
  // ...
}
```

**ACP client not connecting:**
```typescript
// Check process spawn
client.on('started', () => console.log('Server started'));
client.on('error', (error) => console.error('Server error:', error));
client.on('log', (line) => console.log('Server log:', line));
```

**Chat participant not showing:**
```typescript
// Verify registration
const participant = vscode.chat.createChatParticipant('mini-agent', handler);
context.subscriptions.push(participant);

// Check in VS Code
// Open chat and type @ - should see @mini-agent
```

---

## 📋 File Checklist

### Phase 1: ACP Server
- [ ] `mini_agent/acp/protocol.py`
- [ ] `mini_agent/acp/message_types.py`
- [ ] `mini_agent/acp/session_manager.py`
- [ ] `mini_agent/acp/stdio_server.py`
- [ ] `mini_agent/acp/__init__.py`
- [ ] `tests/test_acp_protocol.py`
- [ ] `tests/test_acp_stdio_integration.py`

### Phase 2: VS Code Extension
- [ ] `vscode-extension/package.json`
- [ ] `vscode-extension/tsconfig.json`
- [ ] `vscode-extension/src/types.ts`
- [ ] `vscode-extension/src/acpClient.ts`
- [ ] `vscode-extension/src/sessionManager.ts`
- [ ] `vscode-extension/src/configManager.ts`
- [ ] `vscode-extension/src/chatParticipant.ts`
- [ ] `vscode-extension/src/responseRenderer.ts`
- [ ] `vscode-extension/src/extension.ts`
- [ ] `vscode-extension/test/suite/extension.test.ts`

---

## 🎨 UI/UX Patterns

### Progress Indicators
```typescript
// Show thinking indicator
stream.progress('Analyzing your request...');

// Show tool execution
stream.progress('🔧 Running bash command...');
stream.progress('📝 Writing file...');
stream.progress('🌐 Searching web...');

// Final response
stream.markdown('Here is your result:\n\n');
```

### Markdown Formatting
```typescript
// Code blocks
stream.markdown('```python\n' + code + '\n```');

// Lists
stream.markdown('- Item 1\n- Item 2\n- Item 3');

// Bold/Italic
stream.markdown('**Important:** This is *emphasized*');

// Links
stream.markdown('[Documentation](https://example.com)');
```

### Error Handling
```typescript
try {
  const response = await acpClient.sendPrompt(sessionId, prompt);
  stream.markdown(response);
} catch (error) {
  stream.markdown('⚠️ **Error:** ' + error.message);
  stream.markdown('\n\nPlease try again or check your configuration.');
}
```

---

## ⚡ Performance Tips

### ACP Server
```python
# Use async/await for I/O
async def handle_prompt(request):
    result = await session.agent.run(prompt)
    return result

# Batch notifications
updates = []
# ... collect updates ...
for update in updates:
    send_notification('agent/update', update)
```

### VS Code Extension
```typescript
// Cache sessions
private sessionCache = new Map<string, string>();

// Debounce rapid requests
private debounce(func: Function, wait: number) {
  let timeout: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Stream responses in chunks
async function* streamResponse(text: string) {
  const chunks = text.match(/.{1,100}/g) || [];
  for (const chunk of chunks) {
    yield chunk;
    await new Promise(resolve => setTimeout(resolve, 50));
  }
}
```

---

## 🔍 Troubleshooting Decision Tree

```
Problem: Extension not working
├─ Extension not activating?
│  ├─ Check activation events in package.json
│  └─ Check VS Code developer console for errors
├─ Server not starting?
│  ├─ Verify Python path in settings
│  ├─ Check server args are correct
│  └─ Test server manually: python -m mini_agent.acp.stdio_server
├─ Communication failing?
│  ├─ Check JSON-RPC format
│  ├─ Verify stdin/stdout not mixed with logging
│  └─ Test with simple echo client
└─ Chat not responding?
   ├─ Verify session created successfully
   ├─ Check ACP client event listeners
   └─ Look for errors in stderr output
```

---

## 📚 Quick Links

- [Full Overview](./01_ACP_VS_CODE_INTEGRATION_OVERVIEW.md)
- [Phase 1: ACP Server](./02_ACP_STDIO_SERVER_IMPLEMENTATION.md)
- [Phase 2: Extension](./03_VSCODE_EXTENSION_DEVELOPMENT.md)
- [ACP Protocol Spec](https://agentclientprotocol.com/)
- [VS Code Chat API](https://code.visualstudio.com/api/extension-guides/ai/chat)

---

**Last Updated**: 2025-11-20  
**Version**: 1.0  
**Status**: Ready for use during implementation
