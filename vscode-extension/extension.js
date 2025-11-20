const vscode = require('vscode');
const { spawn } = require('child_process');

function activate(context) {
    console.log('Mini-Agent ACP integration activated');

    // Register Chat Participant
    const miniAgentChat = vscode.chat.createChatParticipant('mini-agent', async (request, context, stream, cancellationToken) => {
        try {
            const acpServer = spawn('python', ['-m', 'mini_agent.acp.server'], {
                stdio: ['pipe', 'pipe', 'inherit']
            });

            // Send prompt to ACP server
            const prompt = {
                jsonrpc: "2.0",
                id: Date.now(),
                method: "prompt",
                params: { text: request.prompt }
            };

            acpServer.stdin.write(JSON.stringify(prompt) + '\n');
            
            acpServer.stdout.on('data', (data) => {
                try {
                    const response = JSON.parse(data.toString());
                    if (response.result) {
                        stream.markdown(response.result.text);
                    }
                } catch (e) {
                    console.error('Parse error:', e);
                }
            });

            // Clean up after timeout
            setTimeout(() => {
                acpServer.kill();
            }, 30000);

        } catch (error) {
            stream.markdown('Error connecting to Mini-Agent ACP server. Make sure Mini-Agent is installed and accessible.');
        }
    });

    context.subscriptions.push(miniAgentChat);

    // Start ACP session command
    let startCommand = vscode.commands.registerCommand('miniAgent.start', function () {
        const terminal = vscode.window.createTerminal('Mini-Agent ACP');
        terminal.sendText('python -m mini_agent.acp.server');
        terminal.show();
        
        vscode.window.showInformationMessage('Mini-Agent ACP server started in terminal');
    });

    // Send prompt command
    let promptCommand = vscode.commands.registerCommand('miniAgent.prompt', async function () {
        const prompt = await vscode.window.showInputBox({
            prompt: 'Enter your prompt for Mini-Agent'
        });
        
        if (prompt) {
            vscode.window.showInformationMessage(`Prompt sent: ${prompt.substring(0, 50)}...`);
            // Here you would implement actual ACP protocol communication
        }
    });

    context.subscriptions.push(startCommand);
    context.subscriptions.push(promptCommand);
}

function deactivate() {
    console.log('Mini-Agent ACP integration deactivated');
}

module.exports = {
    activate,
    deactivate
};
