@echo off
echo ============================================
echo 🤖 INSTALL THE CORRECT VS CODE EXTENSION
echo ============================================
echo.
echo Installing the ENHANCED extension (with ACP in the name)
echo This is the one that WORKS! 
echo.
cd C:\Users\Jazeel-Home\Mini-Agent\mini_agent\vscode_extension
echo Current extension directory: %CD%
echo.
echo Installing Mini-Agent Enhanced VS Code Extension...
code --install-extension . --force
echo.
echo ✅ Extension installed! 
echo.
echo Now you MUST restart VS Code:
echo 1. Close all VS Code windows
echo 2. Reopen VS Code 
echo 3. Press Ctrl+Shift+P and search for "Mini-Agent"
echo.
echo 📋 Available Commands After Install:
echo - Ctrl+Shift+A → Ask Mini-Agent
echo - Ctrl+Shift+E → Explain Code  
echo - Ctrl+Shift+G → Generate Code
echo - Ctrl+Shift+R → Refactor Selection
echo - Ctrl+Shift+T → Generate Tests
echo.
echo 📊 Status Bar: Look for robot icon "🤖 Mini-Agent"
echo.
pause