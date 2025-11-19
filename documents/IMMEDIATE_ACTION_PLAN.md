# Immediate Action Plan - VS Code Extension Integration

**Generated**: 2025-11-20  
**Status**: Ready for Implementation

---

## 🎯 Current Reality Check

**GOOD NEWS**: Your Mini-Agent already has 70% of what's needed for VS Code integration!

**KEY FINDINGS**:
- ✅ ACP stdio server already implemented in `mini_agent/acp/__init__.py`
- ✅ VS Code extension already built in `mini_agent/vscode_extension/`
- ✅ Session management and tools fully functional
- ⚠️ Need to connect existing stdio server to Chat API instead of WebSocket

---

## 📋 Immediate Actions (This Week)

### Day 1-2: Validate Current Implementation
```bash
# Test existing stdio ACP server
python -m mini_agent.acp

# Test with simple JSON-RPC message
echo '{"jsonrpc":"2.0","method":"initialize","params":{}}' | python -m mini_agent.acp
```

**Expected**: Server should respond to stdio messages

### Day 3-4: Adapt Extension for stdio
**File**: `mini_agent/vscode_extension/enhanced_extension.js`

**Changes Needed**:
```javascript
// REMOVE WebSocket code
// const ws = new WebSocket(`ws://${host}:${port}`);

// ADD stdio spawn code
const { spawn } = require('child_process');
const server = spawn('python', ['-m', 'mini_agent.acp'], {
    stdio: ['pipe', 'pipe', 'inherit']
});
```

### Day 5-7: Add Chat API Integration
**Add to existing extension**:
```typescript
// Add Chat participant
const participant = vscode.chat.createChatParticipant('mini-agent', async (request, context, stream, token) => {
    // Use existing stdio communication
    const response = await sendViaStdio(request.prompt);
    stream.markdown(response.content);
});
```

---

## 🔄 Step-by-Step Implementation

### Phase 1: Quick Win (2-3 days)
**Goal**: Get basic Chat API working

1. **Test Current stdio Server**
   ```bash
   cd mini_agent
   python -m acp
   ```

2. **Modify Extension Transport**
   - Open `mini_agent/vscode_extension/enhanced_extension.js`
   - Replace WebSocket with stdio spawn
   - Use existing JSON-RPC message format

3. **Test Communication**
   - Send initialize message via stdio
   - Receive response
   - Verify session creation works

### Phase 2: Chat Integration (3-4 days)
**Goal**: `@mini-agent` works in VS Code chat

1. **Add Chat Participant**
   - Use VS Code Chat API
   - Register with `@mini-agent` handle
   - Connect to existing stdio server

2. **Handle Chat Requests**
   - Convert chat messages to ACP format
   - Send via stdio
   - Stream responses back to chat

3. **Test End-to-End**
   - Install extension in VS Code
   - Open chat: `@mini-agent hello`
   - Verify response appears

### Phase 3: Polish (1-2 weeks)
**Goal**: Production quality

1. **Tool Visualization**
   - Show tool execution in chat
   - Display file operations
   - Show web search results

2. **Error Handling**
   - Robust error messages
   - Connection recovery
   - User feedback

3. **Performance**
   - Optimize communication
   - Reduce latency
   - Handle large responses

---

## 🛠️ Specific Code Changes

### Change 1: Transport Layer
**File**: `mini_agent/vscode_extension/enhanced_extension.js`
**Lines**: ~100-150 (WebSocket section)

**Replace**:
```javascript
// OLD: WebSocket approach
const ws = new WebSocket(`ws://${host}:${port}`);
ws.on('open', () => {
    // Send initialize message
});
```

**With**:
```javascript
// NEW: stdio approach
const { spawn } = require('child_process');
const server = spawn('python', ['-m', 'mini_agent.acp'], {
    stdio: ['pipe', 'pipe', 'inherit']
});

let messageId = 1;

// Send message via stdio
function sendMessage(method, params) {
    const message = {
        jsonrpc: "2.0",
        id: messageId++,
        method: method,
        params: params
    };
    
    server.stdin.write(JSON.stringify(message) + '\n');
}
```

### Change 2: Chat API Integration
**File**: `mini_agent/vscode_extension/enhanced_extension.js`
**Add**: Chat participant registration

**Add**:
```typescript
// Chat participant for @mini-agent
const participant = vscode.chat.createChatParticipant('mini-agent', async (request, context, stream, token) => {
    try {
        // Create session if needed
        const sessionId = await createSession();
        
        // Send prompt
        const response = await sendPrompt(sessionId, request.prompt);
        
        // Stream response
        stream.markdown(response.content);
        
    } catch (error) {
        stream.markdown(`Error: ${error.message}`);
    }
});
```

---

## 🧪 Testing Strategy

### Test 1: ACP Server
```bash
# Manual test
echo '{"jsonrpc":"2.0","method":"initialize","params":{}}' | python -m mini_agent.acp

# Expected: JSON response
```

### Test 2: Extension Installation
1. Copy `mini_agent/vscode_extension/` to new folder
2. Run `vsce package` 
3. Install in VS Code: `code --install-extension *.vsix`
4. Verify extension appears

### Test 3: Chat Functionality
1. Open VS Code
2. Open Chat panel (Ctrl+Shift+P → "Chat: Open Chat")
3. Type: `@mini-agent hello`
4. Verify response appears

---

## 📊 Success Metrics

### Week 1 Goals
- [ ] stdio ACP server works independently
- [ ] Extension can spawn and communicate with server
- [ ] Basic `@mini-agent` responds to prompts

### Week 2 Goals
- [ ] Tool execution visible in chat
- [ ] Error handling works
- [ ] Session management functional

### Production Goals
- [ ] All Mini-Agent tools accessible
- [ ] Streaming responses work
- [ ] Performance acceptable
- [ ] Ready for marketplace

---

## 🚨 Key Risks & Mitigation

### Risk 1: VS Code API Compatibility
**Issue**: Chat API might have changed
**Mitigation**: Check VS Code API documentation and test with latest version

### Risk 2: stdio Communication Issues
**Issue**: JSON parsing or encoding problems
**Mitigation**: Use existing tested implementation, add comprehensive logging

### Risk 3: Performance Problems
**Issue**: Latency or response time issues
**Mitigation**: Optimize message handling, implement streaming if needed

---

## 💡 Pro Tips

1. **Use Existing Code**: Your current ACP stdio implementation is solid - use it!
2. **Incremental Testing**: Test each change before moving to next
3. **Keep Working Code**: Maintain existing WebSocket functionality while adding Chat API
4. **Leverage Documentation**: VS Code Chat API has good examples
5. **Start Simple**: Get basic chat working first, add features later

---

## 🎉 Conclusion

**You're much closer to success than you think!** 

The heavy lifting is done. You have:
- ✅ Working ACP protocol
- ✅ stdio transport ready
- ✅ VS Code extension foundation
- ✅ All tools and session management

**Just connect the dots** and you'll have a working VS Code extension in 1-2 weeks.

**Next Action**: Test the current stdio ACP server today!

```bash
cd mini_agent
python -m acp
```

If that works (and it should), you're 70% done!
