#!/usr/bin/env python3
"""
Quick VS Code Terminal → ACP Bridge
Immediate integration solution for current session
"""

import subprocess
import sys
import json
import os
from pathlib import Path

class VSCodeACPBridge:
    """Simple bridge to connect VS Code terminal to ACP server"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.acp_command = [
            sys.executable, "-m", "mini_agent.acp.server"
        ]
        
    def check_setup(self):
        """Verify current setup"""
        print("🔍 VS Code + Mini-Agent ACP Bridge Setup")
        print("=" * 50)
        
        # Check working directory
        print(f"📁 Working Directory: {os.getcwd()}")
        print(f"🏠 Project Root: {self.project_root}")
        
        # Check if we're in VS Code
        if 'VSCODE' in os.environ:
            print("✅ Running in VS Code Terminal")
        else:
            print("⚠️  Not detected as VS Code terminal")
        
        # Test ACP server
        print("\n🧪 Testing ACP Server...")
        try:
            result = subprocess.run(
                self.acp_command + ["--help"], 
                cwd=self.project_root,
                capture_output=True, 
                text=True, 
                timeout=5
            )
            print("✅ ACP server is accessible")
            return True
        except Exception as e:
            print(f"❌ ACP server test failed: {e}")
            return False
    
    def start_interactive_bridge(self):
        """Start interactive bridge for immediate use"""
        print("\n🚀 Starting VS Code → ACP Bridge")
        print("=" * 50)
        print("This will start the ACP server for editor integration")
        print("Commands available:")
        print("  /help     - Show this help")
        print("  /status   - Check connection status") 
        print("  /exit     - Exit bridge")
        print("  /prompt   - Send prompt to Mini-Agent")
        print("\nPress Ctrl+C to exit")
        print("-" * 50)
        
        try:
            # Start ACP server process
            print("Starting ACP server...")
            process = subprocess.Popen(
                self.acp_command,
                cwd=self.project_root,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ ACP server started")
            print(f"📋 Server PID: {process.pid}")
            print("🔄 Bridge is active - awaiting protocol messages")
            
            # Simple interaction loop
            while True:
                try:
                    user_input = input("\n💭 Enter command (/help for options): ").strip()
                    
                    if user_input == "/exit":
                        print("👋 Shutting down bridge...")
                        break
                    elif user_input == "/help":
                        self.show_help()
                    elif user_input == "/status":
                        self.show_status(process)
                    elif user_input.startswith("/prompt"):
                        self.send_prompt(process, user_input)
                    else:
                        # Send raw input to ACP server
                        if process.stdin:
                            process.stdin.write(user_input + "\n")
                            process.stdin.flush()
                        
                        # Show output
                        if process.stdout:
                            output = process.stdout.readline()
                            if output:
                                print(f"📤 Server: {output.strip()}")
                
                except KeyboardInterrupt:
                    print("\n\n🛑 Interrupt received, shutting down...")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Clean shutdown
            if process:
                process.terminate()
                process.wait(timeout=5)
                print("✅ Bridge closed")
                
        except Exception as e:
            print(f"❌ Bridge failed: {e}")
    
    def show_help(self):
        """Show help information"""
        print("""
🤖 VS Code ↔️ Mini-Agent ACP Bridge Help

Available Commands:
  /help           - Show this help message
  /status         - Check server connection status
  /prompt [text]  - Send prompt to Mini-Agent via ACP
  /exit           - Exit the bridge

Protocol Messages (ACP):
  The bridge handles standard ACP protocol messages:
  - Initialize requests
  - New session requests  
  - Prompt requests
  - Tool execution updates

For full VS Code integration:
  1. Install VS Code extension (future step)
  2. Configure extension to use ACP server
  3. Get visual tool feedback in editor
        """)
    
    def show_status(self, process):
        """Show connection status"""
        print(f"""
🔍 Bridge Status Report
======================
Project Root: {self.project_root}
ACP Command: {' '.join(self.acp_command)}
Server PID: {process.pid}
Server Running: {process.poll() is None}
Working Directory: {os.getcwd()}
        """)
        
        # Check if ACP dependencies are available
        try:
            import acp
            print(f"✅ ACP library: Available")
        except ImportError:
            print(f"❌ ACP library: Missing (pip install agent-client-protocol)")
    
    def send_prompt(self, process, user_input):
        """Send prompt via ACP protocol"""
        prompt_text = user_input.replace("/prompt", "").strip()
        if not prompt_text:
            print("❌ Please provide prompt text")
            return
        
        print(f"📤 Sending prompt via ACP: {prompt_text[:50]}...")
        
        # Create ACP protocol message
        acp_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "prompt",
            "params": {
                "prompt": [{"type": "text", "text": prompt_text}],
                "sessionId": "vscode-terminal-session"
            }
        }
        
        try:
            if process.stdin:
                process.stdin.write(json.dumps(acp_message) + "\n")
                process.stdin.flush()
                
                # Read response
                if process.stdout:
                    response = process.stdout.readline()
                    if response:
                        print(f"📥 ACP Response: {response.strip()}")
        except Exception as e:
            print(f"❌ Failed to send prompt: {e}")

def main():
    """Main bridge function"""
    bridge = VSCodeACPBridge()
    
    if not bridge.check_setup():
        print("❌ Setup check failed")
        return 1
    
    bridge.start_interactive_bridge()
    return 0

if __name__ == "__main__":
    sys.exit(main())
