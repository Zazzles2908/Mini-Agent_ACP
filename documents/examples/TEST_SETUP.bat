@echo off
echo ============================================
echo 🧪 TEST YOUR MINI-AGENT SETUP
echo ============================================
echo.
echo Testing your complete Mini-Agent ACP setup...
echo.
echo ============================================
echo 📋 TEST 1: Agent Basic Functionality
echo ============================================
cd C:\Users\Jazeel-Home\Mini-Agent
echo Testing agent startup...
mini-agent
if %ERRORLEVEL% EQU 0 (
    echo ✅ Agent loads successfully
) else (
    echo ❌ Agent failed to load
)
echo.
pause
echo.
echo ============================================
echo 📋 TEST 2: ACP Server
echo ============================================
echo Testing ACP server...
python -m mini_agent.acp
if %ERRORLEVEL% EQU 0 (
    echo ✅ ACP server starts successfully
) else (
    echo ❌ ACP server failed to start
)
echo.
pause
echo.
echo ============================================
echo 📋 TEST 3: VS Code Extension
echo ============================================
echo Checking VS Code extension installation...
echo 1. Open VS Code
echo 2. Press Ctrl+Shift+P and search "Mini-Agent"
echo 3. Look for robot icon in status bar
echo 4. Check Extensions panel for Mini-Agent
echo.
echo If all tests pass, you're ready to go! 🚀
echo.
pause