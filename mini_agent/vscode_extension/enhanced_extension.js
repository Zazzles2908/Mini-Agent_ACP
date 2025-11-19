const vscode = require('vscode');
const WebSocket = require('ws');
const path = require('path');

class EnhancedMiniAgentExtension {
    constructor(context) {
        this.context = context;
        this.acpServer = null;
        this.wsClient = null;
        this.panel = null;
        this.statusBarItem = null;
        this.activeSession = null;
        this.disposable = null;
        this.messageId = 0;
    }

    async activate() {
        console.log('Enhanced Mini-Agent VS Code extension activated');

        // Create status bar item
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        this.statusBarItem.command = 'miniAgent.activate';
        this.statusBarItem.text = '$(robot) Mini-Agent';
        this.statusBarItem.tooltip = 'Click to activate Mini-Agent';
        this.statusBarItem.show();
        this.context.subscriptions.push(this.statusBarItem);

        // Register commands
        const commands = [
            vscode.commands.registerCommand('miniAgent.activate', () => this.activateMiniAgent()),
            vscode.commands.registerCommand('miniAgent.ask', () => this.askQuestion()),
            vscode.commands.registerCommand('miniAgent.explain', () => this.explainCode()),
            vscode.commands.registerCommand('miniAgent.generate', () => this.generateCode()),
            vscode.commands.registerCommand('miniAgent.refactor', () => this.refactorCode()),
            vscode.commands.registerCommand('miniAgent.test', () => this.generateTests()),
            vscode.commands.registerCommand('miniAgent.reset', () => this.resetSession())
        ];

        commands.forEach(cmd => this.context.subscriptions.push(cmd));

        // Register hover provider
        this.disposable = vscode.languages.registerHoverProvider(['typescript', 'javascript', 'python', 'markdown'], {
            provideHover: (document, position, token) => {
                const range = document.getWordRangeAtPosition(position);
                const word = document.getText(range);
                return this.getHoverInfo(word, range);
            }
        });

        this.context.subscriptions.push(this.disposable);

        // Auto-start ACP server if workspace is available
        if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
            await this.startACPServer();
        }
    }

    async activateMiniAgent() {
        if (this.panel) {
            this.panel.reveal(vscode.ViewColumn.Beside);
            return;
        }

        // Create webview panel
        this.panel = vscode.window.createWebviewPanel(
            'miniAgentPanel',
            'Mini-Agent Assistant',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                localResourceRoots: [this.context.extensionUri],
                retainContextWhenHidden: true
            }
        );

        // Start ACP server if not running
        await this.startACPServer();
        await this.connectToACPServer();

        // Set webview content
        this.panel.webview.html = this.getWebviewHTML();

        // Handle messages from webview
        this.panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'ask':
                        this.sendPrompt(message.text);
                        return;
                    case 'explain':
                        this.explainCode();
                        return;
                    case 'reset':
                        this.resetSession();
                        return;
                }
            },
            undefined,
            this.context.subscriptions
        );

        // Clean up panel
        this.panel.onDidDispose(() => {
            this.panel = null;
        });
    }

    async startACPServer() {
        if (this.acpServer && this.acpServer.exitCode === null) {
            console.log('ACP server already running');
            return;
        }

        try {
            console.log('Starting enhanced ACP server...');
            
            const { spawn } = require('child_process');
            
            // Start the enhanced ACP server
            this.acpServer = spawn('python', [
                path.join(__dirname, '../../mini_agent/acp/enhanced_server.py'),
                '--host', '127.0.0.1',
                '--port', '8765',
                '--log-level', 'INFO'
            ], {
                cwd: vscode.workspace.rootPath || process.cwd(),
                stdio: ['pipe', 'pipe', 'pipe']
            });

            // Handle server output
            this.acpServer.stdout.on('data', (data) => {
                const output = data.toString();
                console.log('ACP Server:', output);
                
                if (output.includes('ACP server started successfully')) {
                    this.updateStatus('$(check) Mini-Agent Ready');
                }
            });

            this.acpServer.stderr.on('data', (data) => {
                console.error('ACP Server Error:', data.toString());
            });

            this.acpServer.on('close', (code) => {
                console.log(`ACP Server process exited with code ${code}`);
                this.updateStatus('$(robot) Mini-Agent Stopped');
                this.wsClient = null;
            });

            // Wait for server to start
            await new Promise(resolve => setTimeout(resolve, 3000));
            console.log('ACP server started');

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to start Mini-Agent: ${error.message}`);
            this.updateStatus('$(error) Mini-Agent Error');
        }
    }

    async connectToACPServer() {
        if (this.wsClient && this.wsClient.readyState === WebSocket.OPEN) {
            console.log('Already connected to ACP server');
            return;
        }

        try {
            console.log('Connecting to ACP server...');
            
            // Use native WebSocket if available in Node.js context
            const WebSocketClient = WebSocket || require('ws');
            
            this.wsClient = new WebSocketClient('ws://127.0.0.1:8765');

            this.wsClient.on('open', () => {
                console.log('✅ Connected to ACP server');
                this.updateStatus('$(check) Connected');
                
                // Send initialization message
                this.sendACPMessage('initialize', {});
            });

            this.wsClient.on('message', (data) => {
                try {
                    const message = JSON.parse(data.toString());
                    this.handleACPMessage(message);
                } catch (error) {
                    console.error('Error parsing ACP message:', error);
                }
            });

            this.wsClient.on('close', () => {
                console.log('🔌 Disconnected from ACP server');
                this.updateStatus('$(robot) Disconnected');
                this.activeSession = null;
            });

            this.wsClient.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.updateStatus('$(error) Connection Error');
            });

            // Wait for connection
            await new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Connection timeout'));
                }, 5000);

                this.wsClient.once('open', () => {
                    clearTimeout(timeout);
                    resolve();
                });

                this.wsClient.once('error', (error) => {
                    clearTimeout(timeout);
                    reject(error);
                });
            });

        } catch (error) {
            console.error('Failed to connect to ACP server:', error);
            this.updateStatus('$(error) Connection Failed');
        }
    }

    sendACPMessage(type, data, sessionId = null) {
        if (!this.wsClient || this.wsClient.readyState !== WebSocket.OPEN) {
            console.error('Not connected to ACP server');
            return;
        }

        const message = {
            id: `msg-${++this.messageId}`,
            type: type,
            timestamp: new Date().toISOString(),
            sessionId: sessionId,
            data: data
        };

        this.wsClient.send(JSON.stringify(message));
        return message.id;
    }

    async handleACPMessage(message) {
        console.log('Received ACP message:', message.type);

        switch (message.type) {
            case 'initialize_response':
                await this.createNewSession();
                break;
                
            case 'new_session_response':
                this.activeSession = message.data.sessionId;
                console.log('Created new session:', this.activeSession);
                this.updateStatus('$(check) Session Ready');
                break;
                
            case 'prompt_response':
                if (this.panel) {
                    this.panel.webview.postMessage({
                        command: 'response',
                        text: message.data.content,
                        messageId: message.data.messageId,
                        timestamp: message.timestamp
                    });
                }
                this.updateStatus('$(check) Ready');
                break;
                
            case 'status_update':
                if (message.data.status === 'processing') {
                    this.updateStatus('$(loading~spin) Thinking...');
                }
                break;
                
            case 'error':
                console.error('ACP Error:', message.error);
                this.updateStatus('$(error) Error');
                if (this.panel) {
                    this.panel.webview.postMessage({
                        command: 'error',
                        text: message.error,
                        timestamp: message.timestamp
                    });
                }
                break;
        }
    }

    async createNewSession() {
        try {
            const workspaceDir = vscode.workspace.rootPath || './';
            this.sendACPMessage('newSession', {
                workspaceDir: workspaceDir
            });
        } catch (error) {
            console.error('Error creating session:', error);
        }
    }

    async sendPrompt(prompt) {
        if (!this.activeSession) {
            vscode.window.showWarningMessage('No active session. Please activate Mini-Agent first.');
            return;
        }

        this.updateStatus('$(loading~spin) Processing...');
        
        try {
            this.sendACPMessage('prompt', {
                prompt: prompt
            }, this.activeSession);
        } catch (error) {
            vscode.window.showErrorMessage(`Mini-Agent Error: ${error.message}`);
            this.updateStatus('$(error) Error');
        }
    }

    async resetSession() {
        if (this.wsClient) {
            this.sendACPMessage('cleanup', {});
            this.activeSession = null;
            this.updateStatus('$(check) Reset Complete');
            
            // Recreate session after cleanup
            setTimeout(() => {
                this.createNewSession();
            }, 1000);
        }
    }

    async askQuestion() {
        const prompt = await vscode.window.showInputBox({
            prompt: 'Ask Mini-Agent a question',
            placeHolder: 'What would you like to know?'
        });

        if (prompt) {
            await this.sendPrompt(prompt);
        }
    }

    async explainCode() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection) || 
                         editor.document.getText(new vscode.Range(0, 0, editor.selection.start.line, editor.selection.start.character));

        if (!selection.trim()) {
            vscode.window.showWarningMessage('No code selected');
            return;
        }

        await this.sendPrompt(`Please explain this code:\n\n\`\`\`\n${selection}\n\`\`\``);
    }

    async generateCode() {
        const prompt = await vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate',
            placeHolder: 'e.g., Create a Python function to sort a list'
        });

        if (prompt) {
            await this.sendPrompt(`Please generate code for: ${prompt}`);
        }
    }

    async refactorCode() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection);
        if (!selection.trim()) {
            vscode.window.showWarningMessage('No code selected');
            return;
        }

        const refactorType = await vscode.window.showQuickPick([
            'Improve readability',
            'Optimize performance',
            'Add error handling',
            'Make more concise',
            'Add documentation'
        ], {
            placeHolder: 'How would you like to refactor the code?'
        });

        if (refactorType) {
            await this.sendPrompt(`Please refactor this code to ${refactorType}:\n\n\`\`\`\n${selection}\n\`\`\``);
        }
    }

    async generateTests() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection);
        if (!selection.trim()) {
            vscode.window.showWarningMessage('No code selected');
            return;
        }

        await this.sendPrompt(`Please generate unit tests for this code:\n\n\`\`\`\n${selection}\n\`\`\``);
    }

    async getHoverInfo(word, range) {
        const hoverContent = new vscode.MarkdownString();
        hoverContent.appendText(`Mini-Agent: ${word}`);
        hoverContent.appendText('\n\n');
        hoverContent.appendText('$(robot) Ask Mini-Agent for more info');
        hoverContent.appendCodeblock(word);
        
        return new vscode.Hover(hoverContent, range);
    }

    updateStatus(text) {
        if (this.statusBarItem) {
            this.statusBarItem.text = text;
        }
    }

    getWebviewHTML() {
        return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: #f8f9fa;
                }
                .header { 
                    border-bottom: 2px solid #e0e0e0; 
                    padding-bottom: 15px; 
                    margin-bottom: 20px; 
                }
                .header h2 {
                    margin: 0;
                    color: #2c3e50;
                }
                .header p {
                    margin: 5px 0 0 0;
                    color: #6c757d;
                    font-size: 14px;
                }
                .input-area { 
                    display: flex; 
                    gap: 10px; 
                    margin-bottom: 20px; 
                }
                #promptInput { 
                    flex: 1; 
                    padding: 12px; 
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    font-size: 14px;
                    outline: none;
                }
                #promptInput:focus {
                    border-color: #007acc;
                }
                .send-btn { 
                    padding: 12px 24px; 
                    background: #007acc; 
                    color: white; 
                    border: none; 
                    border-radius: 8px; 
                    cursor: pointer; 
                    font-weight: 500;
                }
                .send-btn:hover {
                    background: #0056b3;
                }
                .response-area { 
                    border: 2px solid #e9ecef;
                    border-radius: 8px; 
                    padding: 20px; 
                    min-height: 400px; 
                    background: white;
                    max-height: 600px;
                    overflow-y: auto;
                }
                .loading { 
                    color: #6c757d; 
                    font-style: italic; 
                    text-align: center;
                    padding: 40px;
                }
                .response-item {
                    margin-bottom: 20px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 6px;
                    border-left: 4px solid #007acc;
                }
                .prompt-text {
                    font-weight: 500;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .response-text {
                    color: #495057;
                    line-height: 1.6;
                    white-space: pre-wrap;
                }
                .error-text {
                    color: #dc3545;
                    background: #f8d7da;
                    border-color: #dc3545;
                }
                .controls {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                }
                .control-btn {
                    padding: 8px 16px;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    background: white;
                    cursor: pointer;
                    font-size: 12px;
                }
                .control-btn:hover {
                    background: #f8f9fa;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🤖 Mini-Agent Assistant</h2>
                <p>Your AI coding companion with full ACP protocol support</p>
            </div>
            
            <div class="controls">
                <button class="control-btn" onclick="resetSession()">🔄 Reset</button>
                <button class="control-btn" onclick="clearHistory()">🗑️ Clear</button>
            </div>
            
            <div class="input-area">
                <input type="text" id="promptInput" placeholder="Ask Mini-Agent anything about your code...">
                <button class="send-btn" onclick="sendPrompt()">Send</button>
            </div>
            
            <div class="response-area" id="responseArea">
                <div class="loading">Welcome to Mini-Agent! Ask me anything about your code or development.</div>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                let messageHistory = [];
                
                function sendPrompt() {
                    const input = document.getElementById('promptInput');
                    const prompt = input.value.trim();
                    
                    if (prompt) {
                        const responseArea = document.getElementById('responseArea');
                        
                        // Add user message to history
                        const userMessage = {
                            type: 'user',
                            content: prompt,
                            timestamp: new Date().toISOString()
                        };
                        messageHistory.push(userMessage);
                        
                        // Show loading state
                        const loadingDiv = document.createElement('div');
                        loadingDiv.className = 'response-item';
                        loadingDiv.innerHTML = '<div class="loading">🤔 Mini-Agent is thinking...</div>';
                        responseArea.appendChild(loadingDiv);
                        
                        // Send to extension
                        vscode.postMessage({
                            command: 'ask',
                            text: prompt
                        });
                        
                        input.value = '';
                        
                        // Scroll to bottom
                        responseArea.scrollTop = responseArea.scrollHeight;
                    }
                }
                
                function resetSession() {
                    messageHistory = [];
                    const responseArea = document.getElementById('responseArea');
                    responseArea.innerHTML = '<div class="loading">Resetting session...</div>';
                    
                    vscode.postMessage({
                        command: 'reset'
                    });
                }
                
                function clearHistory() {
                    messageHistory = [];
                    document.getElementById('responseArea').innerHTML = '<div class="loading">History cleared. Ask me anything!</div>';
                }
                
                document.getElementById('promptInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        sendPrompt();
                    }
                });
                
                window.addEventListener('message', (event) => {
                    const message = event.data;
                    
                    if (message.command === 'response') {
                        // Remove loading state and add response
                        const responseArea = document.getElementById('responseArea');
                        responseArea.removeChild(responseArea.lastChild);
                        
                        const responseDiv = document.createElement('div');
                        responseDiv.className = 'response-item';
                        responseDiv.innerHTML = \`
                            <div class="prompt-text">You:</div>
                            <div class="response-text">\${message.text}</div>
                            <div style="font-size: 12px; color: #6c757d; margin-top: 10px;">
                                \${new Date(message.timestamp).toLocaleTimeString()}
                            </div>
                        \`;
                        responseArea.appendChild(responseDiv);
                        
                        // Scroll to bottom
                        responseArea.scrollTop = responseArea.scrollHeight;
                    }
                    
                    if (message.command === 'error') {
                        // Remove loading state and show error
                        const responseArea = document.getElementById('responseArea');
                        responseArea.removeChild(responseArea.lastChild);
                        
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'response-item error-text';
                        errorDiv.innerHTML = \`
                            <div class="response-text">❌ \${message.text}</div>
                            <div style="font-size: 12px; margin-top: 10px;">
                                \${new Date(message.timestamp).toLocaleTimeString()}
                            </div>
                        \`;
                        responseArea.appendChild(errorDiv);
                        
                        // Scroll to bottom
                        responseArea.scrollTop = responseArea.scrollHeight;
                    }
                });
            </script>
        </body>
        </html>
        `;
    }

    dispose() {
        // Stop ACP server
        if (this.acpServer) {
            this.acpServer.kill();
            this.acpServer = null;
        }
        
        // Close WebSocket connection
        if (this.wsClient) {
            this.wsClient.close();
            this.wsClient = null;
        }
        
        // Clean up panel
        if (this.panel) {
            this.panel.dispose();
        }
        
        if (this.disposable) {
            this.disposable.dispose();
        }
        
        if (this.statusBarItem) {
            this.statusBarItem.dispose();
        }
    }
}

// Activation function
function activate(context) {
    const extension = new EnhancedMiniAgentExtension(context);
    extension.activate();
    
    // Store extension instance for disposal
    context.subscriptions.push({
        dispose: () => extension.dispose()
    });
}

// Deactivation function
function deactivate() {
    console.log('Enhanced Mini-Agent VS Code extension deactivated');
}

module.exports = {
    activate,
    deactivate
};
