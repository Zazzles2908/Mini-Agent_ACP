# Phase 2: VS Code Extension Development
## Building the Chat Participant with ACP Client Integration

**Phase**: 2 of 5  
**Priority**: 🔥 **CRITICAL PATH**  
**Estimated Time**: 6-8 hours  
**Dependencies**: Phase 1 (ACP Stdio Server)

---

## 🎯 Objective

Create a professional VS Code extension that integrates Mini-Agent through the Chat API, providing users with an `@mini-agent` chat participant that communicates via the ACP protocol.

---

## 📋 Architecture Overview

### Extension Components

```
vscode-extension/
├── package.json                    # Extension manifest
├── tsconfig.json                   # TypeScript configuration
├── .vscodeignore                   # Files to exclude from package
├── README.md                       # User documentation
├── CHANGELOG.md                    # Version history
├── src/
│   ├── extension.ts                # Main entry point
│   ├── chatParticipant.ts          # Chat participant handler
│   ├── acpClient.ts                # ACP protocol client
│   ├── sessionManager.ts           # Session lifecycle management
│   ├── responseRenderer.ts         # Response formatting/display
│   ├── configManager.ts            # Extension configuration
│   └── types.ts                    # TypeScript type definitions
└── test/
    ├── suite/
    │   ├── extension.test.ts       # Extension tests
    │   └── acpClient.test.ts       # ACP client tests
    └── runTest.ts                  # Test runner
```

---

## 🏗️ Implementation Plan

### Step 1: Project Setup

#### Create Extension Directory
```bash
cd Mini-Agent
mkdir -p vscode-extension/src
cd vscode-extension
```

#### Initialize npm Project
```bash
npm init -y
```

#### Install Dependencies
```bash
# Core dependencies
npm install --save-dev @types/vscode @types/node typescript

# Development tools
npm install --save-dev @vscode/test-electron mocha @types/mocha

# Extension utilities
npm install uuid
npm install --save-dev @types/uuid
```

#### Configure TypeScript (`tsconfig.json`)
```json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "lib": ["ES2020"],
    "sourceMap": true,
    "rootDir": "src",
    "outDir": "out",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", ".vscode-test"]
}
```

---

### Step 2: Extension Manifest (`package.json`)

```json
{
  "name": "mini-agent-vscode",
  "displayName": "Mini-Agent",
  "description": "AI coding assistant powered by Mini-Agent",
  "version": "0.1.0",
  "publisher": "mini-agent",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": [
    "AI",
    "Chat Participants"
  ],
  "activationEvents": [
    "onStartupFinished"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "chatParticipants": [
      {
        "id": "mini-agent.chat",
        "name": "mini-agent",
        "description": "AI coding assistant with file operations, web search, and skills",
        "isSticky": true,
        "commands": [
          {
            "name": "help",
            "description": "Show available commands"
          },
          {
            "name": "reset",
            "description": "Reset the current session"
          }
        ]
      }
    ],
    "commands": [
      {
        "command": "mini-agent.startServer",
        "title": "Mini-Agent: Start Server"
      },
      {
        "command": "mini-agent.stopServer",
        "title": "Mini-Agent: Stop Server"
      },
      {
        "command": "mini-agent.restartServer",
        "title": "Mini-Agent: Restart Server"
      }
    ],
    "configuration": {
      "title": "Mini-Agent",
      "properties": {
        "miniAgent.serverPath": {
          "type": "string",
          "default": "python",
          "description": "Path to Python executable"
        },
        "miniAgent.serverArgs": {
          "type": "array",
          "default": ["-m", "mini_agent.acp.stdio_server"],
          "description": "Arguments to start ACP server"
        },
        "miniAgent.workspaceDir": {
          "type": "string",
          "default": "${workspaceFolder}",
          "description": "Workspace directory for Mini-Agent"
        },
        "miniAgent.autoStart": {
          "type": "boolean",
          "default": true,
          "description": "Automatically start server on activation"
        },
        "miniAgent.logLevel": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
          "default": "INFO",
          "description": "Log level for Mini-Agent server"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile",
    "test": "node ./out/test/runTest.js",
    "lint": "eslint src --ext ts",
    "package": "vsce package"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "^20.x",
    "@types/mocha": "^10.0.6",
    "@types/uuid": "^9.0.7",
    "@vscode/test-electron": "^2.3.8",
    "typescript": "^5.3.3",
    "mocha": "^10.2.0"
  },
  "dependencies": {
    "uuid": "^9.0.1"
  }
}
```

---

### Step 3: Type Definitions (`src/types.ts`)

```typescript
/**
 * Type definitions for Mini-Agent VS Code extension
 */

// JSON-RPC 2.0 types
export interface JSONRPCRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: any;
}

export interface JSONRPCResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: any;
  error?: JSONRPCError;
}

export interface JSONRPCNotification {
  jsonrpc: '2.0';
  method: string;
  params?: any;
}

export interface JSONRPCError {
  code: number;
  message: string;
  data?: any;
}

// ACP Protocol types
export enum ACPMethod {
  Initialize = 'initialize',
  Shutdown = 'shutdown',
  CreateSession = 'agent/createSession',
  CancelSession = 'agent/cancelSession',
  Prompt = 'agent/prompt',
  AgentUpdate = 'agent/update',
  ToolCall = 'agent/toolCall',
  ToolResult = 'agent/toolResult',
}

export interface InitializeParams {
  protocolVersion: string;
  capabilities: {
    [key: string]: any;
  };
  clientInfo: {
    name: string;
    version: string;
  };
}

export interface InitializeResult {
  protocolVersion: string;
  capabilities: {
    [key: string]: any;
  };
  serverInfo: {
    name: string;
    version: string;
  };
}

export interface CreateSessionParams {
  workspaceDir: string;
  environmentVars?: { [key: string]: string };
}

export interface CreateSessionResult {
  sessionId: string;
}

export interface PromptParams {
  sessionId: string;
  prompt: string;
}

export interface PromptResult {
  content: string;
}

export interface AgentUpdateParams {
  sessionId: string;
  updateType: 'thinking' | 'tool_call' | 'tool_result' | 'response';
  content?: string;
  data?: any;
}

// Extension types
export interface ServerConfig {
  pythonPath: string;
  serverArgs: string[];
  workspaceDir: string;
  autoStart: boolean;
  logLevel: string;
}

export interface SessionInfo {
  sessionId: string;
  workspaceDir: string;
  createdAt: Date;
}
```

---

### Step 4: ACP Client Implementation (`src/acpClient.ts`)

```typescript
/**
 * ACP Protocol Client
 * Manages communication with Mini-Agent ACP server via stdio
 */

import { ChildProcess, spawn } from 'child_process';
import { EventEmitter } from 'events';
import * as readline from 'readline';
import { v4 as uuidv4 } from 'uuid';
import {
  JSONRPCRequest,
  JSONRPCResponse,
  JSONRPCNotification,
  ACPMethod,
  InitializeParams,
  CreateSessionParams,
  PromptParams,
  AgentUpdateParams,
} from './types';

export class ACPClient extends EventEmitter {
  private process: ChildProcess | null = null;
  private requestId = 0;
  private pendingRequests = new Map<string | number, {
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }>();
  private initialized = false;

  constructor(
    private pythonPath: string,
    private serverArgs: string[]
  ) {
    super();
  }

  /**
   * Start the ACP server process
   */
  async start(): Promise<void> {
    if (this.process) {
      throw new Error('Server already running');
    }

    return new Promise((resolve, reject) => {
      this.process = spawn(this.pythonPath, this.serverArgs, {
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      if (!this.process.stdin || !this.process.stdout || !this.process.stderr) {
        reject(new Error('Failed to create process stdio streams'));
        return;
      }

      // Setup stdout reader (protocol messages)
      const rl = readline.createInterface({
        input: this.process.stdout,
        crlfDelay: Infinity,
      });

      rl.on('line', (line) => {
        this.handleMessage(line);
      });

      // Setup stderr reader (server logs)
      const errRl = readline.createInterface({
        input: this.process.stderr!,
        crlfDelay: Infinity,
      });

      errRl.on('line', (line) => {
        this.emit('log', line);
      });

      // Handle process events
      this.process.on('error', (error) => {
        this.emit('error', error);
        reject(error);
      });

      this.process.on('exit', (code, signal) => {
        this.emit('exit', { code, signal });
        this.cleanup();
      });

      // Server started successfully
      this.emit('started');
      resolve();
    });
  }

  /**
   * Stop the ACP server
   */
  async stop(): Promise<void> {
    if (!this.process) {
      return;
    }

    // Send shutdown request
    if (this.initialized) {
      try {
        await this.sendRequest(ACPMethod.Shutdown, {});
      } catch (error) {
        // Ignore shutdown errors
      }
    }

    // Kill process
    this.process.kill('SIGTERM');
    
    // Wait for exit
    await new Promise<void>((resolve) => {
      const timeout = setTimeout(() => {
        if (this.process) {
          this.process.kill('SIGKILL');
        }
        resolve();
      }, 5000);

      this.once('exit', () => {
        clearTimeout(timeout);
        resolve();
      });
    });

    this.cleanup();
  }

  /**
   * Initialize the ACP server
   */
  async initialize(): Promise<any> {
    const params: InitializeParams = {
      protocolVersion: '1.0',
      capabilities: {
        streaming: true,
        toolExecution: true,
      },
      clientInfo: {
        name: 'vscode-mini-agent',
        version: '0.1.0',
      },
    };

    const result = await this.sendRequest(ACPMethod.Initialize, params);
    this.initialized = true;
    this.emit('initialized', result);
    return result;
  }

  /**
   * Create a new session
   */
  async createSession(workspaceDir: string): Promise<string> {
    const params: CreateSessionParams = { workspaceDir };
    const result = await this.sendRequest(ACPMethod.CreateSession, params);
    return result.sessionId;
  }

  /**
   * Send a prompt to a session
   */
  async sendPrompt(sessionId: string, prompt: string): Promise<string> {
    const params: PromptParams = { sessionId, prompt };
    const result = await this.sendRequest(ACPMethod.Prompt, params);
    return result.content;
  }

  /**
   * Cancel a session
   */
  async cancelSession(sessionId: string): Promise<void> {
    await this.sendRequest(ACPMethod.CancelSession, { sessionId });
  }

  /**
   * Send a JSON-RPC request and wait for response
   */
  private async sendRequest(method: string, params: any): Promise<any> {
    if (!this.process || !this.process.stdin) {
      throw new Error('Server not running');
    }

    const id = ++this.requestId;
    const request: JSONRPCRequest = {
      jsonrpc: '2.0',
      id,
      method,
      params,
    };

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(id, { resolve, reject });

      const message = JSON.stringify(request) + '\n';
      this.process!.stdin!.write(message, (error) => {
        if (error) {
          this.pendingRequests.delete(id);
          reject(error);
        }
      });

      // Timeout after 30 seconds
      setTimeout(() => {
        if (this.pendingRequests.has(id)) {
          this.pendingRequests.delete(id);
          reject(new Error('Request timeout'));
        }
      }, 30000);
    });
  }

  /**
   * Handle incoming message from server
   */
  private handleMessage(line: string): void {
    try {
      const message = JSON.parse(line);

      // Check if it's a response or notification
      if ('id' in message) {
        // Response
        const response = message as JSONRPCResponse;
        this.handleResponse(response);
      } else {
        // Notification
        const notification = message as JSONRPCNotification;
        this.handleNotification(notification);
      }
    } catch (error) {
      this.emit('error', new Error(`Failed to parse message: ${error}`));
    }
  }

  /**
   * Handle JSON-RPC response
   */
  private handleResponse(response: JSONRPCResponse): void {
    const pending = this.pendingRequests.get(response.id);
    if (!pending) {
      return;
    }

    this.pendingRequests.delete(response.id);

    if (response.error) {
      pending.reject(new Error(response.error.message));
    } else {
      pending.resolve(response.result);
    }
  }

  /**
   * Handle JSON-RPC notification
   */
  private handleNotification(notification: JSONRPCNotification): void {
    switch (notification.method) {
      case ACPMethod.AgentUpdate:
        this.emit('agentUpdate', notification.params as AgentUpdateParams);
        break;
      case ACPMethod.ToolCall:
        this.emit('toolCall', notification.params);
        break;
      case ACPMethod.ToolResult:
        this.emit('toolResult', notification.params);
        break;
      default:
        this.emit('notification', notification);
    }
  }

  /**
   * Cleanup resources
   */
  private cleanup(): void {
    this.process = null;
    this.initialized = false;
    
    // Reject all pending requests
    for (const [id, pending] of this.pendingRequests) {
      pending.reject(new Error('Server stopped'));
    }
    this.pendingRequests.clear();
  }

  /**
   * Check if server is running
   */
  isRunning(): boolean {
    return this.process !== null && !this.process.killed;
  }

  /**
   * Check if server is initialized
   */
  isInitialized(): boolean {
    return this.initialized;
  }
}
```

---

### Step 5: Session Manager (`src/sessionManager.ts`)

```typescript
/**
 * Session Manager
 * Manages ACP sessions for chat participants
 */

import * as vscode from 'vscode';
import { ACPClient } from './acpClient';
import { SessionInfo } from './types';

export class SessionManager {
  private sessions = new Map<string, SessionInfo>();
  private chatToSession = new Map<vscode.ChatParticipantRequest, string>();

  constructor(private acpClient: ACPClient) {}

  /**
   * Get or create session for chat request
   */
  async getOrCreateSession(
    request: vscode.ChatParticipantRequest
  ): Promise<string> {
    // Check if we have existing session for this chat
    let sessionId = this.chatToSession.get(request);
    if (sessionId && this.sessions.has(sessionId)) {
      return sessionId;
    }

    // Create new session
    const workspaceDir = this.getWorkspaceDir();
    sessionId = await this.acpClient.createSession(workspaceDir);

    const sessionInfo: SessionInfo = {
      sessionId,
      workspaceDir,
      createdAt: new Date(),
    };

    this.sessions.set(sessionId, sessionInfo);
    this.chatToSession.set(request, sessionId);

    return sessionId;
  }

  /**
   * Cancel session
   */
  async cancelSession(sessionId: string): Promise<void> {
    if (!this.sessions.has(sessionId)) {
      return;
    }

    await this.acpClient.cancelSession(sessionId);
    this.sessions.delete(sessionId);

    // Remove from chat mapping
    for (const [chat, sid] of this.chatToSession) {
      if (sid === sessionId) {
        this.chatToSession.delete(chat);
      }
    }
  }

  /**
   * Get session info
   */
  getSessionInfo(sessionId: string): SessionInfo | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * Clear all sessions
   */
  async clearAll(): Promise<void> {
    const promises = Array.from(this.sessions.keys()).map(id =>
      this.cancelSession(id)
    );
    await Promise.all(promises);
  }

  /**
   * Get workspace directory for sessions
   */
  private getWorkspaceDir(): string {
    const config = vscode.workspace.getConfiguration('miniAgent');
    let workspaceDir = config.get<string>('workspaceDir', '${workspaceFolder}');

    // Resolve ${workspaceFolder}
    if (workspaceDir.includes('${workspaceFolder}')) {
      const wsFolder = vscode.workspace.workspaceFolders?.[0];
      if (wsFolder) {
        workspaceDir = workspaceDir.replace('${workspaceFolder}', wsFolder.uri.fsPath);
      } else {
        workspaceDir = process.cwd();
      }
    }

    return workspaceDir;
  }
}
```

---

## ✅ Acceptance Criteria (Step 2)

- [ ] TypeScript compiles without errors
- [ ] Extension manifest is valid
- [ ] ACP client can spawn server process
- [ ] ACP client can send/receive JSON-RPC messages
- [ ] Session manager creates and tracks sessions
- [ ] Configuration system works
- [ ] All type definitions are correct

---

**Next Sections**:
- Step 6: Chat Participant Implementation
- Step 7: Response Renderer
- Step 8: Main Extension Entry Point
- Step 9: Testing
- Step 10: Packaging

**Continued in**: Part 2 of this document (due to length)

**Next Phase**: [04_STREAMING_AND_VISUALIZATION.md](./04_STREAMING_AND_VISUALIZATION.md)
