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
            console.log('Starting ACP stdio server...');
            
            // Start the ACP stdio server using the module entry point
            this.acpServer = spawn('python', [
                '-m', 'mini_agent.acp'
            ], {
                cwd: vscode.workspace.rootPath || process.cwd(),
                stdio: ['pipe', 'pipe', 'pipe']
            });

            // Handle server output
            this.acpServer.stdout.on('data', (data) => {
                const output = data.toString();
                console.log('ACP Server:', output);
                
                if (output.includes('ACP server') || output.includes('agent')) {
                    this.updateStatus('$(check) Mini-Agent Ready');
                }
            });

            this.acpServer.stderr.on('data', (data) => {
                const error = data.toString();
                console.error('ACP Server Error:', error);
                
                // Don't show errors if they're just warnings
                if (!error.includes('DeprecationWarning') && !error.includes('FutureWarning')) {
                    this.updateStatus('$(error) Mini-Agent Warning');
                }
            });

            this.acpServer.on('close', (code) => {
                console.log(`ACP Server process exited with code ${code}`);
                this.updateStatus('$(robot) Mini-Agent Stopped');
                this.stdioClient = null;
            });

            this.acpServer.on('error', (error) => {
                console.error('Failed to start ACP server:', error);
                this.updateStatus('$(error) Mini-Agent Failed');
            });

            // Wait for server to initialize
            await new Promise(resolve => setTimeout(resolve, 2000));
            console.log('ACP server started');

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to start Mini-Agent: ${error.message}`);
            this.updateStatus('$(error) Mini-Agent Error');
        }
    }

    async connectToACPServer() {
        if (this.stdioClient && this.acpServer && this.acpServer.exitCode === null) {
            console.log('Already connected to ACP server');
            return;
        }

        try {
            console.log('Connecting to ACP stdio server...');
            
            // Send initialization message
            await this.sendACPMessage('initialize', {});
            
            console.log('✅ Connected to ACP stdio server');
            this.updateStatus('$(check) Connected');

        } catch (error) {
            console.error('Failed to connect to ACP server:', error);
            this.updateStatus('$(error) Connection Error');
        }
    }

    async sendACPMessage(method, params) {
        return new Promise((resolve, reject) => {
            if (!this.acpServer || this.acpServer.exitCode !== null) {
                reject(new Error('ACP server not running'));
                return;
            }

            const messageId = ++this.messageId;
            const message = {
                jsonrpc: "2.0",
                id: messageId,
                method: method,
                params: params
            };

            console.log('Sending ACP message:', message);

            // Set up response handler
            const timeout = setTimeout(() => {
                this.responseCallbacks.delete(messageId);
                reject(new Error(`Timeout waiting for response to ${method}`));
            }, 30000); // 30 second timeout

            this.responseCallbacks.set(messageId, (response) => {
                clearTimeout(timeout);
                if (response.error) {
                    reject(new Error(response.error.message || 'ACP error'));
                } else {
                    resolve(response.result);
                }
                this.responseCallbacks.delete(messageId);
            });

            // Send message
            const messageStr = JSON.stringify(message) + '\n';
            this.acpServer.stdin.write(messageStr);
        });
    }

    handleACPMessage(message) {
        console.log('Received ACP message:', message);

        // Handle response messages
        if (message.id && this.responseCallbacks.has(message.id)) {
            const callback = this.responseCallbacks.get(message.id);
            callback(message);
            return;
        }

        // Handle notifications
        if (message.method) {
            this.handleACPNotification(message);
        }
    }

    handleACPNotification(message) {
        console.log('ACP notification:', message);
        // Handle streaming responses, status updates, etc.
    }

    async createSession() {
        try {
            const response = await this.sendACPMessage('newSession', {
                cwd: vscode.workspace.rootPath || process.cwd()
            });
            
            console.log('Created session:', response.sessionId);
            return response.sessionId;
            
        } catch (error) {
            console.error('Failed to create session:', error);
            throw error;
        }
    }

    async sendPrompt(prompt) {
        try {
            if (!this.activeSession) {
                this.activeSession = await this.createSession();
            }

            const response = await this.sendACPMessage('prompt', {
                sessionId: this.activeSession,
                prompt: prompt
            });

            this.displayResponse(response);

        } catch (error) {
            console.error('Failed to send prompt:', error);
            this.displayError(error.message);
        }
    }

    displayResponse(response) {
        if (!this.panel) {
            return;
        }

        const content = response.content || [];
        const contentText = content.map(block => 
            block.type === 'text' ? block.text : ''
        ).join('');

        this.panel.webview.postMessage({
            command: 'displayResponse',
            content: contentText
        });
    }

    displayError(error) {
        if (!this.panel) {
            return;
        }

        this.panel.webview.postMessage({
            command: 'displayError',
            content: error
        });
    }

    updateStatus(text) {
        if (this.statusBarItem) {
            this.statusBarItem.text = text;
        }
    }

    async askQuestion() {
        const question = await vscode.window.showInputBox({
            prompt: 'Ask Mini-Agent a question:'
        });

        if (question) {
            await this.sendPrompt(question);
        }
    }

    async explainCode() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection) || 
                         editor.document.getText(new vscode.Range(0, 0, editor.document.lineCount, 0));

        const prompt = `Please explain this code:\n\n${selection}`;
        await this.sendPrompt(prompt);
    }

    async generateCode() {
        const description = await vscode.window.showInputBox({
            prompt: 'Describe the code you want to generate:'
        });

        if (description) {
            const prompt = `Please generate code for: ${description}`;
            await this.sendPrompt(prompt);
        }
    }

    async refactorCode() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection);

        const prompt = `Please refactor this code to improve it:\n\n${selection}`;
        await this.sendPrompt(prompt);
    }

    async generateTests() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection);

        const prompt = `Please generate unit tests for this code:\n\n${selection}`;
        await this.sendPrompt(prompt);
    }

    async resetSession() {
        this.activeSession = null;
        this.updateStatus('$(robot) Session Reset');
        
        vscode.window.showInformationMessage('Mini-Agent session reset');
    }

    getHoverInfo(word, range) {
        return new vscode.Hover({
            contents: [
                `**${word}**`,
                '',
                `Ask Mini-Agent about: "${word}"`,
                '',
                `Click to ask Mini-Agent about this code`
            ]
        }, range);
    }

    getWebviewHTML() {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini-Agent Assistant</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
        .header { background: #007ACC; color: white; padding: 15px; margin: -20px -20px 20px -20px; }
        .chat-container { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; }
        .message { margin-bottom: 15px; padding: 10px; border-radius: 5px; }
        .user-message { background: #f0f0f0; }
        .agent-message { background: #e3f2fd; }
        .input-container { display: flex; gap: 10px; }
        #promptInput { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #007ACC; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #005a9e; }
        .error { background: #ffebee; color: #c62828; }
    </style>
</head>
<body>
    <div class="header">
        <h2>🤖 Mini-Agent Assistant</h2>
        <p>Your AI coding companion</p>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message agent-message">
            <strong>Mini-Agent:</strong> Hello! I'm here to help you with coding. Ask me anything!
        </div>
    </div>
    
    <div class="input-container">
        <input type="text" id="promptInput" placeholder="Ask Mini-Agent..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        function sendMessage() {
            const input = document.getElementById('promptInput');
            const message = input.value.trim();
            
            if (message) {
                addMessage(message, 'user');
                vscode.postMessage({ command: 'ask', text: message });
                input.value = '';
            }
        }
        
        function addMessage(content, sender) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender + '-message';
            messageDiv.innerHTML = '<strong>' + (sender === 'user' ? 'You' : 'Mini-Agent') + ':</strong> ' + content;
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'displayResponse':
                    addMessage(message.content, 'agent');
                    break;
                case 'displayError':
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message error';
                    errorDiv.innerHTML = '<strong>Error:</strong> ' + message.content;
                    document.getElementById('chatContainer').appendChild(errorDiv);
                    break;
            }
        });
        
        // Handle Enter key
        document.getElementById('promptInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
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
    
    context.subscriptions.push({
        dispose: () => {
            if (extension.acpServer) {
                extension.acpServer.kill();
            }
        }
    });
}

function deactivate() {
    console.log('Mini-Agent extension deactivated');
}

module.exports = {
    activate,
    deactivate
};