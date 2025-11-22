#!/usr/bin/env python3
"""Create a simple stdio-based ACP server without external dependencies"""

import asyncio
import json
import sys
import logging
from pathlib import Path

# Simple JSON-RPC 2.0 over stdio implementation
class SimpleStdioACPServer:
    """Simple ACP server that speaks JSON-RPC 2.0 over stdio"""
    
    def __init__(self):
        self.sessions = {}
        self.message_id = 1
        
    async def handle_message(self, message):
        """Handle incoming JSON-RPC message"""
        try:
            if 'jsonrpc' not in message or message['jsonrpc'] != '2.0':
                return self.create_error(message.get('id'), -32600, "Invalid Request")
            
            method = message.get('method')
            params = message.get('params', {})
            msg_id = message.get('id')
            
            if method == 'initialize':
                return self.create_response(msg_id, {
                    'protocolVersion': 1,
                    'agentCapabilities': {'loadSession': False},
                    'agentInfo': {
                        'name': 'mini-agent',
                        'title': 'Mini-Agent',
                        'version': '0.1.0'
                    }
                })
            
            elif method == 'newSession':
                session_id = f"session-{self.message_id}"
                self.message_id += 1
                self.sessions[session_id] = {'created': True}
                return self.create_response(msg_id, {'sessionId': session_id})
            
            elif method == 'prompt':
                session_id = params.get('sessionId')
                prompt_text = params.get('prompt', '')
                
                if session_id not in self.sessions:
                    return self.create_error(msg_id, -32602, "Invalid params: session not found")
                
                # Simple echo response
                response_text = f"Hello! You said: '{prompt_text}'. I'm Mini-Agent, your AI coding assistant."
                
                return self.create_response(msg_id, {
                    'content': [
                        {
                            'type': 'text',
                            'text': response_text
                        }
                    ]
                })
            
            elif method == 'cancel':
                return self.create_response(msg_id, {'cancelled': True})
            
            else:
                return self.create_error(msg_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            return self.create_error(message.get('id'), -32603, f"Internal error: {str(e)}")
    
    def create_response(self, msg_id, result):
        """Create JSON-RPC response"""
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'result': result
        }
    
    def create_error(self, msg_id, code, message):
        """Create JSON-RPC error"""
        return {
            'jsonrpc': '2.0',
            'id': msg_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    async def run(self):
        """Main server loop"""
        print("🚀 Simple ACP Server starting on stdio...", file=sys.stderr)
        
        while True:
            try:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                # Parse JSON message
                message = json.loads(line.strip())
                print(f"📨 Received: {message}", file=sys.stderr)
                
                # Handle message and send response
                response = await self.handle_message(message)
                response_json = json.dumps(response) + '\n'
                sys.stdout.write(response_json)
                sys.stdout.flush()
                
                print(f"📤 Sent: {response}", file=sys.stderr)
                
            except json.JSONDecodeError as e:
                error_response = self.create_error(None, -32700, f"Parse error: {str(e)}")
                sys.stdout.write(json.dumps(error_response) + '\n')
                sys.stdout.flush()
                
            except KeyboardInterrupt:
                print("🛑 Server interrupted", file=sys.stderr)
                break
                
            except Exception as e:
                print(f"❌ Server error: {e}", file=sys.stderr)
                break

async def main():
    """Main entry point"""
    server = SimpleStdioACPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())