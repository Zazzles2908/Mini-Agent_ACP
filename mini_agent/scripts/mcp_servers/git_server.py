#!/usr/bin/env python3
"""
Git MCP Server - Basic Git operations implementation
Provides essential Git functionality for repository management.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

# Configure logging (redirect to stderr to avoid MCP protocol interference)
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("git-mcp-server")

class GitMCPServer:
    """Simple Git MCP Server using system git commands."""
    
    def __init__(self):
        # Check if git is available
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
            self.git_available = result.returncode == 0
            self.git_version = result.stdout.strip() if self.git_available else None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.git_available = False
            self.git_version = None
        
        self.tools = {
            "git_status": {
                "name": "git_status",
                "description": "Get the current git repository status showing modified, staged, and untracked files.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "git_log": {
                "name": "git_log", 
                "description": "Show git commit history with optional limit on number of commits.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of commits to show (default: 10)",
                            "default": 10
                        }
                    },
                    "required": []
                }
            },
            "git_branch": {
                "name": "git_branch",
                "description": "Show current git branch and list all available branches.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "all": {
                            "type": "boolean",
                            "description": "Show all branches including remote (default: false)",
                            "default": False
                        }
                    },
                    "required": []
                }
            },
            "git_add": {
                "name": "git_add",
                "description": "Add files to git staging area.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of files to add (use '.' to add all changes)"
                        }
                    },
                    "required": ["files"]
                }
            },
            "git_commit": {
                "name": "git_commit",
                "description": "Commit staged changes with a message.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Commit message"
                        }
                    },
                    "required": ["message"]
                }
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol requests."""
        
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return {
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "git-mcp-server",
                    "version": "1.0.0"
                }
            }
        
        elif method == "tools/list":
            return {
                "tools": list(self.tools.values())
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "git_status":
                return await self._handle_git_status(arguments)
            elif tool_name == "git_log":
                return await self._handle_git_log(arguments)
            elif tool_name == "git_branch":
                return await self._handle_git_branch(arguments)
            elif tool_name == "git_add":
                return await self._handle_git_add(arguments)
            elif tool_name == "git_commit":
                return await self._handle_git_commit(arguments)
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unknown tool: {tool_name}"
                        }
                    ],
                    "isError": True
                }
        
        else:
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Unknown method: {method}"
                    }
                ],
                "isError": True
            }
    
    async def _run_git_command(self, args: List[str]) -> tuple[bool, str, str]:
        """Run a git command and return success, stdout, stderr"""
        try:
            result = subprocess.run(
                ['git'] + args, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return False, "", str(e)
    
    async def _handle_git_status(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git status request"""
        if not self.git_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Git is not available on this system"
                    }
                ],
                "isError": True
            }
        
        # Check if we're in a git repository
        success, stdout, stderr = await self._run_git_command(['status', '--porcelain'])
        
        if not success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Not a git repository or git error: {stderr}"
                    }
                ],
                "isError": True
            }
        
        # Parse git status output
        lines = stdout.strip().split('\n') if stdout.strip() else []
        
        modified = []
        staged = []
        untracked = []
        
        for line in lines:
            if line:
                status = line[:2]
                filename = line[3:]
                
                if status[0] == 'M' or status[1] == 'M':
                    if status[0] == 'M':
                        staged.append(f"{filename} (staged)")
                    if status[1] == 'M':
                        modified.append(filename)
                elif status == '??':
                    untracked.append(filename)
        
        # Get current branch
        success, branch_stdout, _ = await self._run_git_command(['branch', '--show-current'])
        current_branch = branch_stdout.strip() if success else "unknown"
        
        # Get remote status
        success, remote_stdout, _ = await self._run_git_command(['status', '-uno', '--porcelain=v3'])
        ahead_behind = ""
        if success and remote_stdout:
            for line in remote_stdout.strip().split('\n'):
                if line.startswith('# branch.upstream'):
                    ahead_behind = line.split('...')[1] if '...' in line else ""
        
        result_parts = [
            f"**📁 Git Repository Status**",
            f"**Branch:** {current_branch}",
            "",
        ]
        
        if ahead_behind:
            result_parts.append(f"**Remote Status:** {ahead_behind}")
        
        if staged:
            result_parts.extend([
                "**Staged Changes:**",
                *[f"  • {file}" for file in staged],
                ""
            ])
        
        if modified:
            result_parts.extend([
                "**Modified Files:**",
                *[f"  • {file}" for file in modified],
                ""
            ])
        
        if untracked:
            result_parts.extend([
                "**Untracked Files:**",
                *[f"  • {file}" for file in untracked],
                ""
            ])
        
        if not staged and not modified and not untracked:
            result_parts.append("**✅ Working tree clean**")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n".join(result_parts)
                }
            ]
        }
    
    async def _handle_git_log(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git log request"""
        if not self.git_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Git is not available on this system"
                    }
                ],
                "isError": True
            }
        
        limit = arguments.get("limit", 10)
        success, stdout, stderr = await self._run_git_command([
            'log', 
            '--oneline', 
            '--decorate',
            '-n', str(limit)
        ])
        
        if not success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Git log error: {stderr}"
                    }
                ],
                "isError": True
            }
        
        commits = stdout.strip().split('\n') if stdout.strip() else []
        
        result_parts = [
            f"**📜 Git Commit History (last {limit} commits)**",
            ""
        ]
        
        for commit in commits:
            if commit:
                result_parts.append(f"• {commit}")
        
        if not commits:
            result_parts.append("No commits found")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n".join(result_parts)
                }
            ]
        }
    
    async def _handle_git_branch(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git branch request"""
        if not self.git_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Git is not available on this system"
                    }
                ],
                "isError": True
            }
        
        show_all = arguments.get("all", False)
        args = ['branch', '--list']
        if show_all:
            args.append('-a')
        
        success, stdout, stderr = await self._run_git_command(args)
        
        if not success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Git branch error: {stderr}"
                    }
                ],
                "isError": True
            }
        
        branches = stdout.strip().split('\n') if stdout.strip() else []
        
        # Get current branch
        success, current_stdout, _ = await self._run_git_command(['branch', '--show-current'])
        current_branch = current_stdout.strip() if success else None
        
        result_parts = [
            "**🌿 Git Branches**",
            ""
        ]
        
        for branch in branches:
            if branch:
                # Remove leading '* ' for current branch
                branch_name = branch[2:] if branch.startswith('* ') else branch
                if branch_name == current_branch:
                    result_parts.append(f"• **{branch_name}** (current)")
                else:
                    result_parts.append(f"• {branch_name}")
        
        if not branches:
            result_parts.append("No branches found")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n".join(result_parts)
                }
            ]
        }
    
    async def _handle_git_add(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git add request"""
        if not self.git_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Git is not available on this system"
                    }
                ],
                "isError": True
            }
        
        files = arguments.get("files", [])
        if not files:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No files specified to add"
                    }
                ],
                "isError": True
            }
        
        # Handle special case of adding all files
        if files == ["."]:
            success, stdout, stderr = await self._run_git_command(['add', '.'])
        else:
            success, stdout, stderr = await self._run_git_command(['add'] + files)
        
        if not success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Git add error: {stderr}"
                    }
                ],
                "isError": True
            }
        
        files_str = ", ".join(files)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"**✅ Added to staging:** {files_str}"
                }
            ]
        }
    
    async def _handle_git_commit(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git commit request"""
        if not self.git_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Git is not available on this system"
                    }
                ],
                "isError": True
            }
        
        message = arguments.get("message", "")
        if not message:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No commit message provided"
                    }
                ],
                "isError": True
            }
        
        success, stdout, stderr = await self._run_git_command(['commit', '-m', message])
        
        if not success:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Git commit error: {stderr}"
                    }
                ],
                "isError": True
            }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"**✅ Committed:** {message}"
                }
            ]
        }

async def main():
    """Main MCP server loop."""
    
    server = GitMCPServer()
    
    # Check git availability on startup
    if not server.git_available:
        # Exit silently if git is not available
        sys.exit(1)
    
    # MCP server communication over stdin/stdout
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            
            # Handle request
            response_content = await server.handle_request(request)
            
            # Get the request ID
            request_id = request.get("id")
            if request_id is None:
                request_id = 1
            
            # Format as proper JSON-RPC response
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": response_content
            }
            
            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            # Send JSON-RPC parse error
            error_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
            continue
        except Exception as e:
            # Send proper JSON-RPC error response
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())