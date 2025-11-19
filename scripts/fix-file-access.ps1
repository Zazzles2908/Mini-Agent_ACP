# Quick Fix Script for Mini-Agent File Access Issues
# Run this script to add Mini-Agent ACP server to Claude Desktop config

$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"

Write-Host "=== Mini-Agent Quick Fix Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if Claude Desktop config exists
if (-not (Test-Path $configPath)) {
    Write-Host "❌ Claude Desktop config not found at: $configPath" -ForegroundColor Red
    Write-Host "Please install Claude Desktop first." -ForegroundColor Yellow
    exit 1
}

# Backup existing config
$backupPath = "$configPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $configPath $backupPath
Write-Host "✅ Backed up config to: $backupPath" -ForegroundColor Green

# Read existing config
$config = Get-Content $configPath -Raw | ConvertFrom-Json

# Add agentServers section if it doesn't exist
if (-not $config.PSObject.Properties['agentServers']) {
    $config | Add-Member -NotePropertyName 'agentServers' -NotePropertyValue @{} -Force
    Write-Host "➕ Added agentServers section" -ForegroundColor Yellow
}

# Add mini-agent configuration
$miniAgentPath = $PSScriptRoot
if (-not $miniAgentPath) {
    $miniAgentPath = "C:\Users\Jazeel-Home\Mini-Agent"
}

$config.agentServers | Add-Member -NotePropertyName 'mini-agent' -NotePropertyValue @{
    command = "uv"
    args = @("run", "mini-agent-acp")
    cwd = $miniAgentPath
    allowedDirectories = @(
        "C:\Users\Jazeel-Home",
        "C:\Project",
        "C:\tmp",
        $miniAgentPath
    )
    env = @{
        PYTHONIOENCODING = "utf-8"
        PYTHONUNBUFFERED = "1"
    }
} -Force

# Save updated config
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8

Write-Host ""
Write-Host "✅ Successfully updated Claude Desktop config!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Changes made:" -ForegroundColor Cyan
Write-Host "  • Added agentServers section" -ForegroundColor White
Write-Host "  • Configured mini-agent ACP server" -ForegroundColor White
Write-Host "  • Set allowed directories:" -ForegroundColor White
Write-Host "    - C:\Users\Jazeel-Home" -ForegroundColor Gray
Write-Host "    - C:\Project" -ForegroundColor Gray
Write-Host "    - C:\tmp" -ForegroundColor Gray
Write-Host "    - $miniAgentPath" -ForegroundColor Gray
Write-Host ""
Write-Host "🔄 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Close Claude Desktop completely" -ForegroundColor White
Write-Host "  2. Restart Claude Desktop" -ForegroundColor White
Write-Host "  3. Create a new conversation" -ForegroundColor White
Write-Host "  4. Select 'mini-agent' from the agent dropdown" -ForegroundColor White
Write-Host ""
Write-Host "📂 Backup saved at:" -ForegroundColor Gray
Write-Host "  $backupPath" -ForegroundColor Gray
Write-Host ""
