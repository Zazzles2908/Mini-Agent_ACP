#!/usr/bin/env python3
"""
MCP Configuration Fact-Checker
Validate the restored MCP configuration and test connectivity
"""

import json
import asyncio
import aiohttp
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPFactChecker:
    """Fact-check MCP configuration and dependencies"""
    
    def __init__(self):
        self.config_path = "mini_agent/config/.mcp.json"
        self.config = {}
        self.results = {}
    
    async def load_configuration(self) -> Dict[str, Any]:
        """Load and validate the MCP configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            
            self.results["config_loading"] = {
                "success": True,
                "message": "Configuration loaded successfully",
                "servers_found": len(self.config.get("mcpServers", {}))
            }
            return self.config
            
        except FileNotFoundError:
            self.results["config_loading"] = {
                "success": False,
                "message": f"Configuration file not found: {self.config_path}",
                "servers_found": 0
            }
        except json.JSONDecodeError as e:
            self.results["config_loading"] = {
                "success": False,
                "message": f"Invalid JSON in configuration: {e}",
                "servers_found": 0
            }
        except Exception as e:
            self.results["config_loading"] = {
                "success": False,
                "message": f"Error loading configuration: {e}",
                "servers_found": 0
            }
        
        return {}
    
    def validate_server_configurations(self) -> Dict[str, Any]:
        """Validate each server configuration"""
        servers = self.config.get("mcpServers", {})
        validation_results = {}
        
        for server_name, server_config in servers.items():
            validation = {
                "exists": True,
                "valid": True,
                "issues": [],
                "score": 100
            }
            
            # Check required fields
            command = server_config.get("command")
            if not command:
                validation["valid"] = False
                validation["issues"].append("Missing 'command' field")
                validation["score"] -= 30
            
            # Check URL validity for remote servers
            if command == "remote":
                url = server_config.get("url")
                if not url:
                    validation["valid"] = False
                    validation["issues"].append("Missing 'url' field for remote server")
                    validation["score"] -= 40
                elif not url.startswith("http"):
                    validation["valid"] = False
                    validation["issues"].append("Invalid URL format")
                    validation["score"] -= 20
            
            # Check headers for remote servers
            if command == "remote":
                headers = server_config.get("headers", {})
                if not headers.get("Authorization"):
                    validation["issues"].append("Missing Authorization header")
                    validation["score"] -= 10
            
            # Check timeout settings
            timeout = server_config.get("timeout")
            if timeout and (timeout < 5 or timeout > 300):
                validation["issues"].append(f"Unusual timeout value: {timeout} (should be 5-300)")
                validation["score"] -= 5
            
            # Check disabled status
            disabled = server_config.get("disabled", False)
            if disabled:
                validation["issues"].append("Server is disabled")
                validation["score"] -= 10
            
            validation_results[server_name] = validation
        
        return validation_results
    
    async def check_remote_endpoints(self) -> Dict[str, Any]:
        """Check connectivity to remote MCP endpoints"""
        remote_results = {}
        servers = self.config.get("mcpServers", {})
        
        for server_name, server_config in servers.items():
            if server_config.get("command") == "remote":
                url = server_config.get("url")
                headers = server_config.get("headers", {})
                
                # Skip Z.AI servers if no API key
                if "z.ai" in url and not os.getenv('ZAI_API_KEY'):
                    remote_results[server_name] = {
                        "accessible": False,
                        "reason": "ZAI_API_KEY not configured",
                        "tested": False
                    }
                    continue
                
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            url,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            remote_results[server_name] = {
                                "accessible": True,
                                "status_code": response.status,
                                "response_time_ms": "< 10s",
                                "tested": True
                            }
                except asyncio.TimeoutError:
                    remote_results[server_name] = {
                        "accessible": False,
                        "reason": "Connection timeout",
                        "tested": True
                    }
                except Exception as e:
                    remote_results[server_name] = {
                        "accessible": False,
                        "reason": str(e),
                        "tested": True
                    }
            else:
                remote_results[server_name] = {
                    "accessible": "not_applicable",
                    "reason": "Local server, not remote",
                    "tested": False
                }
        
        return remote_results
    
    def check_local_dependencies(self) -> Dict[str, Any]:
        """Check dependencies for local MCP servers"""
        dependency_results = {}
        servers = self.config.get("mcpServers", {})
        
        for server_name, server_config in servers.items():
            command = server_config.get("command")
            args = server_config.get("args", [])
            
            if command == "npx":
                # Check if npx is available
                try:
                    result = subprocess.run(['npx', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        dependency_results[server_name] = {
                            "available": True,
                            "command": command,
                            "version": result.stdout.strip(),
                            "package": args[1] if len(args) > 1 else "unknown"
                        }
                    else:
                        dependency_results[server_name] = {
                            "available": False,
                            "command": command,
                            "error": "npx command failed"
                        }
                except Exception as e:
                    dependency_results[server_name] = {
                        "available": False,
                        "command": command,
                        "error": str(e)
                    }
            
            elif command == "python":
                # Check Python module availability
                try:
                    module_name = args[1] if len(args) > 1 else args[0] if args else ""
                    if module_name.startswith('-m '):
                        module_name = module_name[3:]
                    
                    import_result = subprocess.run([sys.executable, '-c', f'import {module_name}'], 
                                                 capture_output=True, timeout=5)
                    
                    if import_result.returncode == 0:
                        dependency_results[server_name] = {
                            "available": True,
                            "command": command,
                            "module": module_name
                        }
                    else:
                        dependency_results[server_name] = {
                            "available": False,
                            "command": command,
                            "module": module_name,
                            "error": "Python module not available"
                        }
                except Exception as e:
                    dependency_results[server_name] = {
                        "available": False,
                        "command": command,
                        "error": str(e)
                    }
            
            else:
                dependency_results[server_name] = {
                    "available": "not_checked",
                    "command": command,
                    "reason": "Unknown command type"
                }
        
        return dependency_results
    
    def calculate_overall_score(self) -> int:
        """Calculate overall configuration score"""
        total_score = 0
        count = 0
        
        # Configuration loading score
        config_score = 80 if self.results.get("config_loading", {}).get("success") else 0
        total_score += config_score
        count += 1
        
        # Server validation scores
        server_validations = self.results.get("server_validations", {})
        for server_name, validation in server_validations.items():
            total_score += validation.get("score", 0)
            count += 1
        
        # Connectivity scores
        connectivity_results = self.results.get("connectivity", {})
        for server_name, result in connectivity_results.items():
            if result.get("accessible") == True:
                total_score += 100
            elif result.get("accessible") == False:
                total_score += 30
            else:
                total_score += 50  # Not applicable
            count += 1
        
        # Dependency scores
        dependency_results = self.results.get("dependencies", {})
        for server_name, result in dependency_results.items():
            if result.get("available") == True:
                total_score += 100
            elif result.get("available") == False:
                total_score += 20
            else:
                total_score += 50  # Not checked or not applicable
            count += 1
        
        return int(total_score / count) if count > 0 else 0
    
    async def run_fact_check(self) -> Dict[str, Any]:
        """Run complete fact-check"""
        logger.info("Starting MCP configuration fact-check...")
        
        # Load configuration
        await self.load_configuration()
        
        # Validate server configurations
        self.results["server_validations"] = self.validate_server_configurations()
        
        # Check remote endpoints
        self.results["connectivity"] = await self.check_remote_endpoints()
        
        # Check local dependencies
        self.results["dependencies"] = self.check_local_dependencies()
        
        # Calculate overall score
        self.results["overall_score"] = self.calculate_overall_score()
        
        # Add timestamp
        from datetime import datetime
        self.results["timestamp"] = datetime.now().isoformat()
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate fact-check report"""
        report = [
            "# MCP Configuration Fact-Check Report",
            "",
            f"**Overall Score:** {self.results.get('overall_score', 0)}/100",
            f"**Generated:** {self.results.get('timestamp', 'Unknown')}",
            "",
            "## Configuration Loading",
            ""
        ]
        
        config_result = self.results.get("config_loading", {})
        status = "✅" if config_result.get("success") else "❌"
        report.extend([
            f"{status} **Status:** {config_result.get('success', False)}",
            f"**Servers Found:** {config_result.get('servers_found', 0)}",
            f"**Message:** {config_result.get('message', 'Unknown error')}",
            ""
        ])
        
        # Server validations
        report.extend(["## Server Validations", ""])
        server_validations = self.results.get("server_validations", {})
        for server_name, validation in server_validations.items():
            status = "✅" if validation.get("valid") else "❌"
            score = validation.get("score", 0)
            report.extend([
                f"### {status} {server_name} (Score: {score}/100)",
                ""
            ])
            
            if validation.get("issues"):
                report.extend(["**Issues:**", ""])
                for issue in validation["issues"]:
                    report.append(f"- {issue}")
                report.append("")
        
        # Connectivity results
        report.extend(["## Connectivity Results", ""])
        connectivity_results = self.results.get("connectivity", {})
        for server_name, result in connectivity_results.items():
            accessible = result.get("accessible")
            if accessible == True:
                status = "✅"
                details = f"HTTP {result.get('status_code', 'unknown')}"
            elif accessible == False:
                status = "❌"
                details = result.get("reason", "Unknown error")
            else:
                status = "ℹ️"
                details = result.get("reason", "Not tested")
            
            report.extend([
                f"{status} **{server_name}:** {details}",
                ""
            ])
        
        # Dependency results
        report.extend(["## Dependency Check", ""])
        dependency_results = self.results.get("dependencies", {})
        for server_name, result in dependency_results.items():
            available = result.get("available")
            if available == True:
                status = "✅"
                details = f"Available ({result.get('command', 'unknown')})"
            elif available == False:
                status = "❌"
                details = f"Unavailable: {result.get('error', 'Unknown error')}"
            else:
                status = "ℹ️"
                details = result.get("reason", "Not checked")
            
            report.extend([
                f"{status} **{server_name}:** {details}",
                ""
            ])
        
        # Recommendations
        report.extend(["## Recommendations", ""])
        
        overall_score = self.results.get("overall_score", 0)
        if overall_score >= 90:
            report.extend(["✅ **Configuration looks excellent!**", ""])
        elif overall_score >= 70:
            report.extend(["⚠️ **Configuration is good but has some issues to address.**", ""])
        else:
            report.extend(["❌ **Configuration needs significant fixes before use.**", ""])
        
        report.extend([
            "",
            "**Next Steps:**",
            "1. Address any issues listed above",
            "2. Test MCP loading with the actual system",
            "3. Verify real MCP responses work correctly",
            "4. Monitor for any runtime errors"
        ])
        
        return "\n".join(report)


async def main():
    """Main fact-check execution"""
    fact_checker = MCPFactChecker()
    
    # Run fact-check
    results = await fact_checker.run_fact_check()
    
    # Generate and display report
    report = fact_checker.generate_report()
    print(report)
    
    # Save report to file
    report_file = f"mcp_fact_check_{results.get('timestamp', 'unknown').replace(':', '-').replace('.', '-')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {report_file}")
    
    # Return overall score for exit code
    return results.get("overall_score", 0)


if __name__ == "__main__":
    score = asyncio.run(main())
    exit(0 if score >= 70 else 1)
