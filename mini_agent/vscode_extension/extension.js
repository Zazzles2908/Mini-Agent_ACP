const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

class MiniAgentExtension {
    constructor(context) {
        this.context = context;
        this.acpProcess = null;
        this.panel = null;
        this.statusBarItem = null;
        this.disposable = null;
    }

    async activate() {
        console.log('Mini-Agent VS Code extension activated');

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
            vscode.commands.registerCommand('miniAgent.test', () => this.generateTests())
        ];

        commands.forEach(cmd => this.context.subscriptions.push(cmd));

        // Register document selector
        this.disposable = vscode.languages.registerHoverProvider(['typescript', 'javascript', 'python', 'markdown'], {
            provideHover: (document, position, token) => {
                const range = document.getWordRangeAtPosition(position);
                const word = document.getText(range);
                return this.getHoverInfo(word, range);
            }
        });

        this.context.subscriptions.push(this.disposable);
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
                localResourceRoots: [this.context.extensionUri]
            }
        );

        // Start ACP server
        await this.startACPServer();

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
                }
            },
            undefined,
            this.context.subscriptions
        );

        // Clean up panel
        this.panel.onDidDispose(() => {
            this.panel = null;
            this.stopACPServer();
        });
    }

    async startACPServer() {
        try {
            // Start the ACP server process
            this.acpProcess = spawn('python', [
                '-m', 
                'mini_agent.acp'
            ], {
                cwd: vscode.workspace.rootPath,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            this.acpProcess.stdout.on('data', (data) => {
                console.log('ACP Server:', data.toString());
                this.updateStatus('$(loading~spin) Mini-Agent Active');
            });

            this.acpProcess.stderr.on('data', (data) => {
                console.error('ACP Server Error:', data.toString());
            });

            this.acpProcess.on('close', (code) => {
                console.log(`ACP Server process exited with code ${code}`);
                this.updateStatus('$(robot) Mini-Agent Ready');
            });

            // Wait for server to start
            await new Promise(resolve => setTimeout(resolve, 2000));
            this.updateStatus('$(check) Mini-Agent Ready');

        } catch (error) {
            vscode.window.showErrorMessage(`Failed to start Mini-Agent: ${error.message}`);
            this.updateStatus('$(error) Mini-Agent Error');
        }
    }

    stopACPServer() {
        if (this.acpProcess) {
            this.acpProcess.kill();
            this.acpProcess = null;
        }
        this.updateStatus('$(robot) Mini-Agent Ready');
    }

    async sendPrompt(prompt) {
        this.updateStatus('$(loading~spin) Mini-Agent Thinking...');
        
        try {
            // Send prompt to ACP server
            const response = await this.callACPServer('prompt', {
                sessionId: 'vscode-session',
                prompt: prompt,
                cwd: vscode.workspace.rootPath
            });

            // Display response in webview
            if (this.panel) {
                this.panel.webview.postMessage({
                    command: 'response',
                    text: response.content,
                    timestamp: new Date().toISOString()
                });
            }

            this.updateStatus('$(check) Mini-Agent Ready');

        } catch (error) {
            vscode.window.showErrorMessage(`Mini-Agent Error: ${error.message}`);
            this.updateStatus('$(error) Mini-Agent Error');
        }
    }

    async callACPServer(method, params) {
        return new Promise((resolve, reject) => {
            if (!this.acpProcess) {
                reject(new Error('ACP Server not running'));
                return;
            }

            const message = JSON.stringify({
                jsonrpc: '2.0',
                id: Date.now(),
                method: method,
                params: params
            }) + '\n';

            const timeout = setTimeout(() => {
                reject(new Error('Request timeout'));
            }, 30000);

            this.acpProcess.stdout.once('data', (data) => {
                clearTimeout(timeout);
                try {
                    const response = JSON.parse(data.toString());
                    resolve(response.result || response);
                } catch (error) {
                    reject(error);
                }
            });

            this.acpProcess.stdin.write(message);
        });
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
        // Provide hover information for code
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
                }
                .header { 
                    border-bottom: 1px solid #e0e0e0; 
                    padding-bottom: 10px; 
                    margin-bottom: 20px; 
                }
                .input-area { 
                    display: flex; 
                    gap: 10px; 
                    margin-bottom: 20px; 
                }
                #promptInput { 
                    flex: 1; 
                    padding: 10px; 
                    border: 1px solid #ccc; 
                    border-radius: 5px; 
                }
                .send-btn { 
                    padding: 10px 20px; 
                    background: #007acc; 
                    color: white; 
                    border: none; 
                    border-radius: 5px; 
                    cursor: pointer; 
                }
                .response-area { 
                    border: 1px solid #e0e0e0; 
                    border-radius: 5px; 
                    padding: 15px; 
                    min-height: 300px; 
                    background: #f9f9f9; 
                }
                .loading { 
                    color: #666; 
                    font-style: italic; 
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>$(robot) Mini-Agent Assistant</h2>
                <p>Your AI coding companion integrated with VS Code</p>
            </div>
            
            <div class="input-area">
                <input type="text" id="promptInput" placeholder="Ask Mini-Agent anything...">
                <button class="send-btn" onclick="sendPrompt()">Send</button>
            </div>
            
            <div class="response-area" id="responseArea">
                <p>Ask me anything about your code or development!</p>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                
                function sendPrompt() {
                    const input = document.getElementById('promptInput');
                    const prompt = input.value.trim();
                    
                    if (prompt) {
                        const responseArea = document.getElementById('responseArea');
                        responseArea.innerHTML = '<p class="loading">Mini-Agent is thinking...</p>';
                        
                        vscode.postMessage({
                            command: 'ask',
                            text: prompt
                        });
                        
                        input.value = '';
                    }
                }
                
                document.getElementById('promptInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        sendPrompt();
                    }
                });
                
                window.addEventListener('message', (event) => {
                    const message = event.data;
                    
                    if (message.command === 'response') {
                        const responseArea = document.getElementById('responseArea');
                        responseArea.innerHTML = '<pre>' + message.text + '</pre>';
                    }
                });
            </script>
        </body>
        </html>
        `;
    }

    dispose() {
        this.stopACPServer();
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
    const extension = new MiniAgentExtension(context);
    extension.activate();
    
    // Store extension instance for disposal
    context.subscriptions.push({
        dispose: () => extension.dispose()
    });
}

// Deactivation function
function deactivate() {
    console.log('Mini-Agent VS Code extension deactivated');
}

module.exports = {
    activate,
    deactivate
};
