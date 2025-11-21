// MiniAgent ACP VSCode Extension
const vscode = require('vscode');
const http = require('http');

function activate(context) {
    console.log('MiniAgent ACP Extension activated');
    
    // Register chat command
    let disposable = vscode.commands.registerCommand('minimax.chat', async function () {
        const message = await vscode.window.showInputBox({
            prompt: 'What would you like to ask MiniAgent?'
        });
        
        if (message) {
            try {
                const response = await callAgent(message);
                vscode.window.showInformationMessage(`MiniAgent: ${response}`);
            } catch (error) {
                vscode.window.showErrorMessage(`Agent Error: ${error.message}`);
            }
        }
    });
    
    // Create status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'minimax.chat';
    statusBarItem.text = '$(comment-discussion) MiniAgent';
    statusBarItem.tooltip = 'Chat with MiniAgent';
    statusBarItem.show();
    
    context.subscriptions.push(disposable, statusBarItem);
}

async function callAgent(message) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            message: message,
            session_id: 'vscode_extension'
        });
        
        const options = {
            hostname: 'localhost',
            port: 8000,
            path: '/chat',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };
        
        const req = http.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const response = JSON.parse(responseData);
                    resolve(response.message);
                } catch (error) {
                    reject(new Error('Invalid response from agent'));
                }
            });
        });
        
        req.on('error', (error) => {
            reject(new Error(`Connection failed: ${error.message}`));
        });
        
        req.write(data);
        req.end();
    });
}

function deactivate() {
    console.log('MiniAgent ACP Extension deactivated');
}

module.exports = {
    activate,
    deactivate
};
