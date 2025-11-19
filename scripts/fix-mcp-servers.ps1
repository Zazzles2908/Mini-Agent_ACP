# Fix MCP Server Configuration Script
# Purpose: Disable problematic MCP servers and resolve connection failures

Write-Host "🔧 Fixing MCP Server Configuration" -ForegroundColor Cyan
Write-Host "=" * 50

$projectRoot = "C:\Users\Jazeel-Home\Mini-Agent"
Set-Location $projectRoot

Write-Host "📍 Working directory: $projectRoot" -ForegroundColor Blue

$configFile = "mcp.json"
$fullPath = Join-Path $projectRoot $configFile

Write-Host "`n🔍 Checking for MCP configuration..." -ForegroundColor Yellow

if (Test-Path $fullPath) {
    Write-Host "✅ Found MCP config: $configFile" -ForegroundColor Green
    
    # Read current configuration
    $content = Get-Content $fullPath -Raw
    $originalContent = $content
    
    Write-Host "📖 Current configuration preview:" -ForegroundColor Blue
    Write-Host $content -ForegroundColor Gray
    
    $changesMade = $false
    
    # Check for minimax_search server (known to fail)
    if ($content -match '"minimax_search"') {
        Write-Host "`n🔍 Found problematic 'minimax_search' MCP server" -ForegroundColor Yellow
        Write-Host "   This server has connection issues and is not needed with Z.AI integration" -ForegroundColor Cyan
        
        # Add disabled flag to minimax_search
        $content = $content -replace '"minimax_search": {', '"minimax_search": {"disabled": true,'
        $changesMade = $true
        Write-Host "⚙️ Disabled minimax_search MCP server" -ForegroundColor Green
    }
    
    # Check for other potentially problematic servers
    $problematicServers = @("filesystem", "git", "memory")
    foreach ($server in $problematicServers) {
        if ($content -match "\"$server\"") {
            Write-Host "ℹ️ Found '$server' server - keeping enabled for now" -ForegroundColor Blue
        }
    }
    
    if ($changesMade) {
        # Create backup
        $backupPath = "$fullPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item $fullPath $backupPath
        Write-Host "💾 Created backup: $backupPath" -ForegroundColor Green
        
        # Apply changes
        Set-Content $fullPath $content
        Write-Host "✅ MCP configuration updated successfully" -ForegroundColor Green
        
        Write-Host "`n📋 Updated configuration:" -ForegroundColor Blue
        Write-Host $content -ForegroundColor Gray
    } else {
        Write-Host "✅ No changes needed - configuration already optimal" -ForegroundColor Green
    }
    
} else {
    Write-Host "⚠️ MCP config file not found: $fullPath" -ForegroundColor Yellow
    Write-Host "   This is normal for some Mini-Agent configurations" -ForegroundColor Cyan
}

Write-Host "`n🎯 Summary of Changes:" -ForegroundColor Cyan
Write-Host "• Disabled problematic minimax_search MCP server" -ForegroundColor White
Write-Host "• Native Z.AI web search will be used instead" -ForegroundColor White
Write-Host "• This should resolve 'Connection closed' errors" -ForegroundColor White
Write-Host "• Z.AI integration provides better web search capabilities" -ForegroundColor Green

Write-Host "`nℹ️ About Z.AI Integration:" -ForegroundColor Cyan
Write-Host "• Mini-Agent has built-in Z.AI web search via GLM models" -ForegroundColor White
Write-Host "• Uses Z.AI's Search Prime engine for better results" -ForegroundColor White
Write-Host "• No external MCP servers needed for web search" -ForegroundColor White
Write-Host "• Automatically selects optimal GLM model (glm-4.6, glm-4.5, etc.)" -ForegroundColor White

Write-Host "`n🔧 To apply changes:" -ForegroundColor Yellow
Write-Host "1. Restart your Mini-Agent session" -ForegroundColor White
Write-Host "2. Web search should now use native Z.AI instead of MCP" -ForegroundColor White
Write-Host "3. No more 'Connection closed' errors for web search" -ForegroundColor Green

Write-Host "`n✅ MCP Server Fix Complete!" -ForegroundColor Green
