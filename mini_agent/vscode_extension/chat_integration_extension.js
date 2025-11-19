const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

class EnhancedMiniAgentExtension {
    constructor(context) {
        this.context = context;
        this.acpServer = null;
        this.stdioClient = null;
        this.panel = null;
        this.statusBarItem = null;
        this.activeSession = null;
        this.disposable = null;
        this.messageId = 0;
        this.responseCallbacks = new Map();
        this.pendingResponses = new Map();
        this.chatParticipant = null;
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

        // Register Chat participant for @mini-agent
        this.registerChatParticipant();

        // Auto-start ACP server if workspace is available
        if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
            await this.startACPServer();
        }
    }

    registerChatParticipant() {
        // Check if VS Code Chat API is available (VS Code 1.82+)
        if (!vscode.chat) {
            console.log('Chat API not available in this VS Code version');
            return;
        }

        try {
            this.chatParticipant = vscode.chat.createChatParticipant('mini-agent', async (request, context, stream, token) => {
                try {
                    console.log('Chat request received:', request.prompt);
                    
                    // Update status
                    this.updateStatus('$(sync~spin) Mini-Agent Processing...');
                    
                    // Start ACP server if not running
                    await this.startACPServer();
                    await this.connectToACPServer();
                    
                    // Create or get session
                    let sessionId = this.activeSession;
                    if (!sessionId) {
                        sessionId = await this.createSession();
                        this.activeSession = sessionId;
                    }
                    
                    // Send prompt to ACP server
                    const response = await this.sendACPMessage('prompt', {
                        sessionId: sessionId,
                        prompt: request.prompt
                    });
                    
                    // Stream response back to chat
                    if (response && response.content && response.content.length > 0) {
                        const contentText = response.content.map(block => 
                            block.type === 'text' ? block.text : ''
                        ).join('');
                        
                        stream.markdown(contentText);
                    } else {
                        stream.markdown('Sorry, I couldn\'t process that request.');
                    }
                    
                    this.updateStatus('$(check) Mini-Agent Ready');
                    
                } catch (error) {
                    console.error('Chat error:', error);
                    stream.markdown(`Error: ${error.message}`);
                    this.updateStatus('$(error) Mini-Agent Error');
                }
            });

            // Set participant properties
            this.chatParticipant.iconPath = vscode.Uri.joinPath(this.context.extensionUri, 'resources', 'icon.png');
            this.chatParticipant.description = 'AI coding assistant powered by Mini-Agent';

            this.context.subscriptions.push(this.chatParticipant);
            console.log('Chat participant registered: @mini-agent');

        } catch (error) {
            console.log('Failed to register chat participant:', error.message);
        }
    }

    async startACPServer() {
        if (this.acpServer && this.acpServer.exitCode === null) {
            console.log('ACP server already running');
            return;
        }

        try {
            console.log('Starting ACP stdio server...');
            
            // Use enhanced_server.py directly to avoid import conflicts
            const extensionPath = this.context.extensionPath;
            const serverScript = path.join(extensionPath, '..', 'mini_agent', 'acp', 'enhanced_server.py');
            
            this.acpServer = spawn('python', [
                serverScript
            ], {
                cwd: vscode.workspace.rootPath || process.cwd(),
                stdio: ['pipe', 'pipe', 'pipe']
            });

            // Handle server output
            this.acpServer.stdout.on('data', (data) => {
                const output = data.toString();
                console.log('ACP Server:', output);
            });

            this.acpServer.stderr.on('data', (data) => {
                const error = data.toString();
                console.error('ACP Server Error:', error);
            });

            this.acpServer.on('close', (code) => {
                console.log(`ACP Server exited with code ${code}`);
                this.acpServer = null;
            });

            // Wait a moment for server to start
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            console.log('ACP server started successfully');

        } catch (error) {
            console.error('Failed to start ACP server:', error);
            throw error;
        }
    }

    async connectToACPServer() {
        if (!this.acpServer) {
            throw new Error('ACP server not running');
        }

        this.stdioClient = {
            write: (message) => {
                if (!this.acpServer || !this.acpServer.stdin) {
                    throw new Error('ACP server stdin not available');
                }
                this.acpServer.stdin.write(JSON.stringify(message) + '\n');
            },
            on: (event, callback) => {
                if (event === 'data' && this.acpServer && this.acpServer.stdout) {
                    this.acpServer.stdout.on('data', callback);
                }
            }
        };
    }

    async createSession() {
        const sessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const message = {
            jsonrpc: "2.0",
            id: ++this.messageId,
            method: "newSession",
            params: {
                sessionId: sessionId,
                timestamp: new Date().toISOString()
            }
        };

        const response = await this.sendACPMessage('newSession', { sessionId });
        return sessionId;
    }

    async sendACPMessage(method, params) {
        return new Promise((resolve, reject) => {
            if (!this.stdioClient) {
                reject(new Error('ACP server not connected'));
                return;
            }

            const messageId = ++this.messageId;
            const message = {
                jsonrpc: "2.0",
                id: messageId,
                method: method,
                params: params
            };

            // Set up response handler
            const timeout = setTimeout(() => {
                this.responseCallbacks.delete(messageId);
                reject(new Error('Request timeout'));
            }, 30000); // 30 second timeout

            this.responseCallbacks.set(messageId, (response) => {
                clearTimeout(timeout);
                this.responseCallbacks.delete(messageId);
                resolve(response);
            });

            // Send message
            try {
                this.stdioClient.write(message);
            } catch (error) {
                clearTimeout(timeout);
                this.responseCallbacks.delete(messageId);
                reject(error);
            }
        });
    }

    // Handle incoming messages from ACP server
    handleACPMessage(data) {
        try {
            const messages = data.toString().trim().split('\n').filter(line => line.trim());
            
            for (const line of messages) {
                const message = JSON.parse(line);
                
                if (message.id && this.responseCallbacks.has(message.id)) {
                    const callback = this.responseCallbacks.get(message.id);
                    callback(message);
                }
            }
        } catch (error) {
            console.error('Error parsing ACP message:', error);
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

        // Set up webview content
        this.panel.webview.html = this.getWebviewContent();

        // Handle webview messages
        this.panel.webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
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
        }, undefined, this.context.subscriptions);

        // Clean up panel
        this.panel.onDidDispose(() => {
            this.panel = null;
        });
    }

    async askQuestion() {
        const question = await vscode.window.showInputBox({
            prompt: 'Ask Mini-Agent anything:',
            placeHolder: 'Type your question...'
        });

        if (question) {
            await this.startACPServer();
            await this.connectToACPServer();
            
            let sessionId = this.activeSession;
            if (!sessionId) {
                sessionId = await this.createSession();
                this.activeSession = sessionId;
            }

            const response = await this.sendACPMessage('prompt', {
                sessionId: sessionId,
                prompt: question
            });

            if (response && response.content) {
                const contentText = response.content.map(block => 
                    block.type === 'text' ? block.text : ''
                ).join('');
                
                vscode.window.showInformationMessage(`Mini-Agent: ${contentText}`);
            }
        }
    }

    explainCode() {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            if (selection) {
                this.sendPrompt(`Explain this code:\n\n${selection}`);
            } else {
                vscode.window.showInformationMessage('Please select code to explain');
            }
        }
    }

    generateCode() {
        const description = vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate:',
            placeHolder: 'e.g., create a function to sort an array'
        });

        if (description) {
            this.sendPrompt(`Generate code for: ${description}`);
        }
    }

    refactorCode() {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            if (selection) {
                const instruction = vscode.window.showInputBox({
                    prompt: 'How should I refactor this code?',
                    placeHolder: 'e.g., make it more efficient, add error handling'
                });

                if (instruction) {
                    this.sendPrompt(`Refactor this code with the following requirements: ${instruction}\n\n${selection}`);
                }
            } else {
                vscode.window.showInformationMessage('Please select code to refactor');
            }
        }
    }

    generateTests() {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            if (selection) {
                this.sendPrompt(`Generate unit tests for this code:\n\n${selection}`);
            } else {
                vscode.window.showInformationMessage('Please select code to generate tests for');
            }
        }
    }

    async resetSession() {
        this.activeSession = null;
        vscode.window.showInformationMessage('Mini-Agent session reset');
        this.updateStatus('$(robot) Mini-Agent Ready');
    }

    sendPrompt(prompt) {
        if (this.panel && this.panel.webview) {
            this.panel.webview.postMessage({ type: 'userMessage', text: prompt });
        }
    }

    updateStatus(text) {
        if (this.statusBarItem) {
            this.statusBarItem.text = text;
        }
    }

    getHoverInfo(word, range) {
        // Simple hover info - can be enhanced with ACP server
        const hoverContent = new vscode.MarkdownString();
        hoverContent.appendText(`Mini-Agent could help explain: ${word}`);
        hoverContent.appendCodeblock(`// Ask @mini-agent for details about: ${word}`, 'typescript');
        
        return new vscode.Hover(hoverContent, range);
    }

    getWebviewContent() {
        return `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 20px; }
        .chat-container { height: 400px; border: 1px solid #ccc; border-radius: 8px; padding: 10px; overflow-y: auto; }
        .message { margin: 10px 0; padding: 8px; border-radius: 4px; }
        .user { background: #e3f2fd; }
        .assistant { background: #f3e5f5; }
        .input-container { margin-top: 10px; display: flex; gap: 10px; }
        input { flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 16px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005999; }
    </style>
</head>
<body>
    <h3>Mini-Agent Assistant</h3>
    <div class="chat-container" id="chatContainer">
        <div class="message assistant">Hello! I'm Mini-Agent. How can I help you today?</div>
    </div>
    <div class="input-container">
        <input type="text" id="messageInput" placeholder="Ask me anything..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');

        function addMessage(text, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = \`message \${isUser ? 'user' : 'assistant'}\`;
            messageDiv.textContent = text;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendMessage() {
            const text = messageInput.value.trim();
            if (text) {
                addMessage(text, true);
                messageInput.value = '';
                vscode.postMessage({ type: 'ask', text: text });
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        window.addEventListener('message', (event) => {
            const message = event.data;
            if (message.type === 'userMessage') {
                // Handle user message
            } else if (message.type === 'assistantMessage') {
                // Handle assistant message
                addMessage(message.text, false);
            }
        });
    </script>
</body>
</html>`;
    }
}

function activate(context) {
    const extension = new EnhancedMiniAgentExtension(context);
    extension.activate();
}

function deactivate() {
    // Clean up resources
}

module.exports = {
    activate,
    deactivate
};