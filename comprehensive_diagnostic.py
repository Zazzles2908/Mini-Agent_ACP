#!/usr/bin/env python3
"""
Comprehensive Diagnostic Script for Mini-Agent_ACP Issues

This script performs systematic diagnostics to identify configuration,
environment, and API connectivity issues that cause CLI and VSCode extension failures.

Usage:
    python3 comprehensive_diagnostic.py

The script will:
1. Check environment variable configuration
2. Validate all configuration files
3. Test API connectivity 
4. Diagnose LLM client initialization
5. Identify file structure issues
6. Provide specific fix recommendations
"""

import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Any
import yaml

# ANSI color codes for terminal output
class Colors:
    """Terminal color definitions"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"

class DiagnosticReport:
    """Accumulates diagnostic results"""
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        
    def add_issue(self, message: str):
        self.issues.append(message)
        
    def add_warning(self, message: str):
        self.warnings.append(message)
        
    def add_success(self, message: str):
        self.successes.append(message)
        
    def print_summary(self):
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}=== DIAGNOSTIC SUMMARY ==={Colors.RESET}")
        
        if self.issues:
            print(f"\n{Colors.BRIGHT_RED}🔴 ISSUES FOUND ({len(self.issues)}):{Colors.RESET}")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {Colors.RED}{issue}{Colors.RESET}")
        
        if self.warnings:
            print(f"\n{Colors.BRIGHT_YELLOW}🟡 WARNINGS ({len(self.warnings)}):{Colors.RESET}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {Colors.YELLOW}{warning}{Colors.RESET}")
                
        if self.successes:
            print(f"\n{Colors.BRIGHT_GREEN}✅ SUCCESSES ({len(self.successes)}):{Colors.RESET}")
            for i, success in enumerate(self.successes, 1):
                print(f"  {i}. {Colors.GREEN}{success}{Colors.RESET}")
                
        print(f"\n{Colors.BOLD}Total checks: {len(self.issues) + len(self.warnings) + len(self.successes)}{Colors.RESET}")

def check_environment_variables(report: DiagnosticReport):
    """Check environment variable configuration"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}1. ENVIRONMENT VARIABLES{Colors.RESET}")
    
    # Check for required environment variables
    required_vars = ['MINIMAX_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'ZAI_API_KEY']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show first few characters for security
            display_value = value[:8] + "..." if len(value) > 8 else value
            report.add_success(f"{var} is set (starts with: {display_value})")
        else:
            report.add_warning(f"{var} is not set")
    
    # Check .env file existence
    env_file = Path('.env')
    if env_file.exists():
        report.add_success(f".env file exists at {env_file.absolute()}")
        try:
            with open(env_file) as f:
                content = f.read()
                print(f"  {Colors.GREEN}.env file contents (API keys masked):{Colors.RESET}")
                for line in content.split('\n'):
                    if '=' in line and any(key in line.upper() for key in ['KEY', 'TOKEN', 'SECRET']):
                        key, val = line.split('=', 1)
                        masked_val = val[:4] + "..." + val[-4:] if len(val) > 8 else "***"
                        print(f"    {key}={masked_val}")
                    elif line.strip():
                        print(f"    {line}")
        except Exception as e:
            report.add_issue(f"Error reading .env file: {e}")
    else:
        report.add_warning(".env file not found in current directory")

def check_configuration_files(report: DiagnosticReport):
    """Check configuration file consistency"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}2. CONFIGURATION FILES{Colors.RESET}")
    
    config_files = [
        'local_config.yaml',
        'test_config.yaml', 
        'mini_agent/config/config.yaml',
        'mini_agent/config/config-example.yaml'
    ]
    
    configs = {}
    
    for config_file in config_files:
        path = Path(config_file)
        if path.exists():
            try:
                with open(path) as f:
                    content = f.read()
                    # Check for environment variable substitution
                    if '${' in content:
                        report.add_warning(f"{config_file} contains unresolved environment variables")
                    
                    config_data = yaml.safe_load(content)
                    configs[config_file] = config_data
                    
                    provider = config_data.get('provider', 'not specified')
                    api_base = config_data.get('api_base', 'not specified')
                    
                    print(f"  {Colors.GREEN}✓{Colors.RESET} {config_file}: provider='{provider}', api_base='{api_base}'")
                    
            except yaml.YAMLError as e:
                report.add_issue(f"{config_file} has invalid YAML: {e}")
            except Exception as e:
                report.add_issue(f"Error reading {config_file}: {e}")
        else:
            print(f"  {Colors.YELLOW}⚠{Colors.RESET} {config_file}: not found")
    
    # Check for provider consistency
    providers = [cfg.get('provider') for cfg in configs.values() if cfg and 'provider' in cfg]
    if len(set(providers)) > 1:
        report.add_issue(f"Inconsistent providers across config files: {set(providers)}")
    elif providers:
        report.add_success(f"Consistent provider across files: {providers[0]}")
    
    # Check API base URLs
    api_bases = [cfg.get('api_base') for cfg in configs.values() if cfg and 'api_base' in cfg]
    if len(set(api_bases)) > 1:
        report.add_warning(f"Different API base URLs: {set(api_bases)}")

def check_repository_structure(report: DiagnosticReport):
    """Check repository structure and file presence"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}3. REPOSITORY STRUCTURE{Colors.RESET}")
    
    required_files = [
        'mini_agent/__init__.py',
        'mini_agent/cli.py',
        'mini_agent/agent.py',
        'mini_agent/config.py',
        'mini_agent/llm/__init__.py',
        'mini_agent/llm/openai_client.py',
        'mini_agent/llm/anthropic_client.py',
        'vscode-extension/extension.js',
        'vscode-extension/package.json'
    ]
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            report.add_success(f"{file_path} exists ({size} bytes)")
        else:
            report.add_issue(f"Missing required file: {file_path}")
    
    # Check ACP folder
    acp_path = Path('mini_agent/acp')
    if acp_path.exists():
        files = list(acp_path.glob('*.py'))
        report.add_success(f"ACP folder found with {len(files)} Python files")
        for py_file in files:
            print(f"    {Colors.CYAN}ACP:{Colors.RESET} {py_file.name}")
    else:
        report.add_warning("ACP folder not found")

def check_python_dependencies(report: DiagnosticReport):
    """Check Python dependencies"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}4. PYTHON DEPENDENCIES{Colors.RESET}")
    
    required_packages = [
        'anthropic',
        'openai',
        'prompt_toolkit',
        'pyyaml',
        'tiktoken',
        'aiohttp'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            report.add_success(f"{package} is installed")
        except ImportError:
            report.add_issue(f"Missing package: {package}")

async def test_llm_client_initialization(report: DiagnosticReport):
    """Test LLM client initialization"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}5. LLM CLIENT INITIALIZATION{Colors.RESET}")
    
    try:
        # Test importing mini_agent components
        sys.path.insert(0, '.')
        from mini_agent.config import Config
        from mini_agent.llm import LLMClient
        from mini_agent.schema import LLMProvider
        
        report.add_success("Successfully imported mini_agent components")
        
        # Try to load configuration
        config_files = [
            'mini_agent/config/config.yaml',
            'local_config.yaml'
        ]
        
        config = None
        config_file_used = None
        
        for config_file in config_files:
            try:
                config = Config.from_yaml(config_file)
                config_file_used = config_file
                break
            except Exception as e:
                continue
        
        if config:
            report.add_success(f"Loaded configuration from {config_file_used}")
            print(f"  {Colors.GREEN}Provider:{Colors.RESET} {config.llm.provider}")
            print(f"  {Colors.GREEN}API Base:{Colors.RESET} {config.llm.api_base}")
            print(f"  {Colors.GREEN}Model:{Colors.RESET} {config.llm.model}")
            print(f"  {Colors.GREEN}API Key:{Colors.RESET} {'***' + config.llm.api_key[-4:] if config.llm.api_key else 'NOT SET'}")
            
            # Test provider conversion
            provider_enum = LLMProvider.ANTHROPIC if config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI
            report.add_success(f"Provider enum conversion: {provider_enum}")
            
            # Try to initialize LLM client
            try:
                from mini_agent.retry import RetryConfig
                
                retry_config = RetryConfig(
                    enabled=config.llm.retry.enabled,
                    max_retries=config.llm.retry.max_retries,
                    initial_delay=config.llm.retry.initial_delay,
                    max_delay=config.llm.retry.max_delay,
                    exponential_base=config.llm.retry.exponential_base,
                    retryable_exceptions=(Exception,),
                )
                
                llm_client = LLMClient(
                    api_key=config.llm.api_key,
                    provider=provider_enum,
                    api_base=config.llm.api_base,
                    model=config.llm.model,
                    retry_config=retry_config if config.llm.retry.enabled else None,
                )
                
                report.add_success("LLM client initialized successfully")
                
                # Test a simple API call
                print(f"\n  {Colors.BRIGHT_YELLOW}Testing API connectivity...{Colors.RESET}")
                try:
                    from mini_agent.schema import Message
                    test_message = Message(role="user", content="Say 'Hello, this is a test' in exactly these words.")
                    response = await llm_client.generate(messages=[test_message])
                    
                    if response.content:
                        report.add_success(f"API test successful: {response.content[:100]}...")
                    else:
                        report.add_warning("API call succeeded but returned empty content")
                        
                except Exception as e:
                    error_msg = str(e)
                    if "401" in error_msg or "unauthorized" in error_msg.lower():
                        report.add_issue("API authentication failed - check your API key")
                    elif "404" in error_msg or "not found" in error_msg.lower():
                        report.add_issue("API endpoint not found - check your api_base URL")
                    else:
                        report.add_issue(f"API call failed: {error_msg}")
                
            except Exception as e:
                report.add_issue(f"Failed to initialize LLM client: {e}")
                
        else:
            report.add_issue("Could not load configuration from any config file")
            
    except Exception as e:
        report.add_issue(f"Error during LLM client testing: {e}")
        traceback.print_exc()

def check_vscode_extension(report: DiagnosticReport):
    """Check VSCode extension files"""
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}6. VSCODE EXTENSION{Colors.RESET}")
    
    vsix_files = [
        'mini-agent-acp-1.0.0.vsix',
        'vscode-extension/mini-agent-acp-1.0.0.vsix'
    ]
    
    vsix_found = False
    for vsix_file in vsix_files:
        if Path(vsix_file).exists():
            report.add_success(f"VSIX file found: {vsix_file}")
            vsix_found = True
            break
    
    if not vsix_found:
        report.add_warning("No VSIX files found")
    
    # Check extension.js
    extension_js = Path('vscode-extension/extension.js')
    if extension_js.exists():
        size = extension_js.stat().st_size
        report.add_success(f"extension.js exists ({size} bytes)")
        
        # Check if it references mini-agent
        try:
            with open(extension_js) as f:
                content = f.read()
                if 'mini-agent' in content.lower():
                    report.add_success("extension.js references mini-agent")
                else:
                    report.add_warning("extension.js doesn't seem to reference mini-agent")
        except Exception as e:
            report.add_issue(f"Error reading extension.js: {e}")
    else:
        report.add_issue("extension.js not found")

def main():
    """Run comprehensive diagnostics"""
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}🤖 Mini-Agent_ACP Comprehensive Diagnostic{Colors.RESET}")
    print(f"{Colors.DIM}This script will identify issues causing CLI and VSCode extension failures{Colors.RESET}")
    
    report = DiagnosticReport()
    
    try:
        check_environment_variables(report)
        check_configuration_files(report)
        check_repository_structure(report)
        check_python_dependencies(report)
        asyncio.run(test_llm_client_initialization(report))
        check_vscode_extension(report)
        
        report.print_summary()
        
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}=== RECOMMENDATIONS ==={Colors.RESET}")
        
        if report.issues:
            print(f"\n{Colors.RED}Fix these issues first:{Colors.RESET}")
            for i, issue in enumerate(report.issues, 1):
                print(f"  {i}. {issue}")
        
        print(f"\n{Colors.BRIGHT_YELLOW}Next steps:{Colors.RESET}")
        print(f"  1. {Colors.GREEN}Run: python3 comprehensive_diagnostic.py{Colors.RESET}")
        print(f"  2. {Colors.GREEN}Share the output to get specific fix instructions{Colors.RESET}")
        print(f"  3. {Colors.GREEN}Test the CLI: python3 -m mini_agent.cli{Colors.RESET}")
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Diagnostic script failed: {e}{Colors.RESET}")
        traceback.print_exc()

if __name__ == "__main__":
    main()