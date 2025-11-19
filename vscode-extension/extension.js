const vscode = require('vscode');

function activate(context) {
    console.log('Mini-Agent ACP integration activated');

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
