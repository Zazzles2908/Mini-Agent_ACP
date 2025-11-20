@echo off
echo ============================================
echo 🚀 PUSH YOUR LOCAL CHANGES TO GITHUB
echo ============================================
echo.
cd C:\Users\Jazeel-Home\Mini-Agent
echo Current directory: %CD%
echo.
echo Checking git status...
git status
echo.
echo Staging all changes...
git add .
echo.
echo Committing changes...
git commit -m "QA fixes and VS Code extension improvements"
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo ✅ Push complete! Check your repository at:
echo https://github.com/Zazzles2908/Mini-Agent_ACP
echo.
pause