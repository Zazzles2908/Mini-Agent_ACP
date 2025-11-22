#!/usr/bin/env python3
"""
Comprehensive ACP Protocol Integration Test
Tests the full Mini-Agent ACP implementation including WebSocket communication
"""

import asyncio
import json
import time
import websockets
import uuid
from pathlib import Path
import subprocess
import sys

class ACPIntegrationTest:
    def __init__(self):
        self.acp_server_process = None
        self.test_results = []
        
    async def run_all_tests(self):
        """Run all ACP integration tests"""
        print("=" * 80)
        print("🧪 Mini-Agent ACP Protocol Integration Test Suite")
        print("=" * 80)
        
        tests = [
            ("Environment Setup", self.test_environment_setup),
            ("ACP Server Startup", self.test_acp_server_startup),
            ("WebSocket Connection", self.test_websocket_connection),
            ("ACP Protocol Handshake", self.test_acp_handshake),
            ("Session Management", self.test_session_management),
            ("Prompt Processing", self.test_prompt_processing),
            ("Error Handling", self.test_error_handling),
            ("Cleanup", self.test_cleanup)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                result = await test_func()
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status} {test_name}")
                self.test_results.append((test_name, result))
            except Exception as e:
                print(f"   ❌ FAIL {test_name}: {e}")
                self.test_results.append((test_name, False))
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 Test Results Summary")
        print("=" * 80)
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All ACP integration tests passed!")
            print("✅ Mini-Agent is fully operational with ACP protocol")
            print("🚀 VS Code extension should work correctly")
            return 0
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check logs above.")
            return 1

    async def test_environment_setup(self):
        """Test environment setup and dependencies"""
        try:
            # Check if required packages are available
            import websockets
            print("   ✅ websockets library available")
            
            from mini_agent.config import Config
            config = Config.load()
            print("   ✅ Mini-Agent configuration loads successfully")
            print(f"      - API Base: {config.llm.api_base}")
            print(f"      - Model: {config.llm.model}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Environment setup failed: {e}")
            return False

    async def test_acp_server_startup(self):
        """Test ACP server startup"""
        try:
            print("   🚀 Starting ACP server...")
            
            # Start the enhanced ACP server
            script_path = Path(__file__).parent.parent / "mini_agent" / "acp" / "enhanced_server.py"
            
            if not script_path.exists():
                print(f"   ❌ ACP server script not found: {script_path}")
                return False
            
            self.acp_server_process = subprocess.Popen([
                sys.executable, str(script_path),
                "--host", "127.0.0.1",
                "--port", "8765",
                "--log-level", "WARNING"  # Reduce noise during testing
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for server to start
            await asyncio.sleep(3)
            
            if self.acp_server_process.poll() is not None:
                stdout, stderr = self.acp_server_process.communicate()
                print(f"   ❌ Server failed to start: {stderr}")
                return False
            
            print("   ✅ ACP server started successfully")
            return True
            
        except Exception as e:
            print(f"   ❌ ACP server startup failed: {e}")
            return False

    async def test_websocket_connection(self):
        """Test WebSocket connection to ACP server"""
        try:
            print("   📡 Testing WebSocket connection...")
            
            uri = "ws://127.0.0.1:8765"
            
            # Test connection with timeout
            async with websockets.connect(uri, timeout=5) as websocket:
                print("   ✅ WebSocket connection established")
                
                # Test basic connection message
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2)
                    message = json.loads(response)
                    print(f"   ✅ Received connection message: {message.get('type', 'unknown')}")
                    return True
                except asyncio.TimeoutError:
                    print("   ⚠️  No immediate response from server (this may be normal)")
                    return True
                
        except Exception as e:
            print(f"   ❌ WebSocket connection failed: {e}")
            return False

    async def test_acp_handshake(self):
        """Test ACP protocol handshake"""
        try:
            print("   🤝 Testing ACP protocol handshake...")
            
            uri = "ws://127.0.0.1:8765"
            
            async with websockets.connect(uri, timeout=5) as websocket:
                # Send initialize message
                init_message = {
                    "id": str(uuid.uuid4()),
                    "type": "initialize",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "data": {}
                }
                
                await websocket.send(json.dumps(init_message))
                print("   📤 Sent initialization message")
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                response_message = json.loads(response)
                
                if response_message.get("type") == "initialize_response":
                    print("   ✅ ACP handshake successful")
                    print(f"      Protocol version: {response_message.get('data', {}).get('protocol_version', 'unknown')}")
                    return True
                else:
                    print(f"   ❌ Unexpected response type: {response_message.get('type')}")
                    return False
                
        except Exception as e:
            print(f"   ❌ ACP handshake failed: {e}")
            return False

    async def test_session_management(self):
        """Test session creation and management"""
        try:
            print("   📝 Testing session management...")
            
            uri = "ws://127.0.0.1:8765"
            session_id = None
            
            async with websockets.connect(uri, timeout=5) as websocket:
                # Create session
                session_message = {
                    "id": str(uuid.uuid4()),
                    "type": "newSession",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "data": {
                        "workspaceDir": "."
                    }
                }
                
                await websocket.send(json.dumps(session_message))
                print("   📤 Sent session creation request")
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                response_message = json.loads(response)
                
                if response_message.get("type") == "new_session_response":
                    session_id = response_message.get("data", {}).get("sessionId")
                    print(f"   ✅ Session created: {session_id}")
                    return True
                else:
                    print(f"   ❌ Session creation failed: {response_message}")
                    return False
                
        except Exception as e:
            print(f"   ❌ Session management test failed: {e}")
            return False

    async def test_prompt_processing(self):
        """Test prompt processing through ACP"""
        try:
            print("   🧠 Testing prompt processing...")
            
            uri = "ws://127.0.0.1:8765"
            
            async with websockets.connect(uri, timeout=5) as websocket:
                # First create a session
                session_message = {
                    "id": str(uuid.uuid4()),
                    "type": "newSession",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "data": {"workspaceDir": "."}
                }
                
                await websocket.send(json.dumps(session_message))
                session_response = await asyncio.wait_for(websocket.recv(), timeout=5)
                session_data = json.loads(session_response)
                session_id = session_data.get("data", {}).get("sessionId")
                
                if not session_id:
                    print("   ❌ Failed to create session for prompt test")
                    return False
                
                print("   📤 Sending test prompt...")
                
                # Send prompt
                prompt_message = {
                    "id": str(uuid.uuid4()),
                    "type": "prompt",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "sessionId": session_id,
                    "data": {
                        "prompt": "Hello! Please respond with 'Hello from Mini-Agent via ACP!'"
                    }
                }
                
                await websocket.send(json.dumps(prompt_message))
                
                # Wait for processing status
                status_response = await asyncio.wait_for(websocket.recv(), timeout=5)
                status_data = json.loads(status_response)
                
                if status_data.get("type") == "status_update" and status_data.get("data", {}).get("status") == "processing":
                    print("   ✅ Processing started")
                    
                    # Wait for response
                    response = await asyncio.wait_for(websocket.recv(), timeout=30)  # Longer timeout for AI processing
                    response_data = json.loads(response)
                    
                    if response_data.get("type") == "prompt_response":
                        content = response_data.get("data", {}).get("content", "")
                        print("   ✅ Prompt processed successfully")
                        print(f"      Response preview: {content[:100]}...")
                        return True
                    else:
                        print(f"   ❌ Unexpected response type: {response_data.get('type')}")
                        return False
                else:
                    print("   ❌ No processing status received")
                    return False
                
        except asyncio.TimeoutError:
            print("   ⚠️  Prompt processing timeout (this is expected with slow AI responses)")
            return False
        except Exception as e:
            print(f"   ❌ Prompt processing test failed: {e}")
            return False

    async def test_error_handling(self):
        """Test error handling"""
        try:
            print("   🛡️  Testing error handling...")
            
            uri = "ws://127.0.0.1:8765"
            
            async with websockets.connect(uri, timeout=5) as websocket:
                # Test invalid session ID
                invalid_message = {
                    "id": str(uuid.uuid4()),
                    "type": "prompt",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "sessionId": "invalid-session-id",
                    "data": {"prompt": "This should fail"}
                }
                
                await websocket.send(json.dumps(invalid_message))
                
                # Should receive error message
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                response_data = json.loads(response)
                
                if response_data.get("type") == "error":
                    print("   ✅ Error handling working correctly")
                    return True
                else:
                    print("   ❌ Error handling not working as expected")
                    return False
                
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            return False

    async def test_cleanup(self):
        """Test cleanup and server shutdown"""
        try:
            print("   🧹 Testing cleanup...")
            
            if self.acp_server_process:
                self.acp_server_process.terminate()
                await asyncio.sleep(2)
                
                if self.acp_server_process.poll() is None:
                    self.acp_server_process.kill()
                
                self.acp_server_process = None
                print("   ✅ Cleanup completed")
                return True
            else:
                print("   ⚠️  No server process to cleanup")
                return True
                
        except Exception as e:
            print(f"   ❌ Cleanup failed: {e}")
            return False

    def cleanup(self):
        """Cleanup any remaining processes"""
        if self.acp_server_process:
            try:
                self.acp_server_process.terminate()
                self.acp_server_process.wait(timeout=5)
            except:
                self.acp_server_process.kill()


async def main():
    """Main test execution"""
    test_suite = ACPIntegrationTest()
    
    try:
        result = await test_suite.run_all_tests()
        return result
    finally:
        test_suite.cleanup()


if __name__ == "__main__":
    import sys
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        sys.exit(1)
