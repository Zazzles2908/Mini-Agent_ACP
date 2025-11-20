#!/usr/bin/env python3
"""
Configuration Fix Utility for Mini-Agent_ACP

This script automatically identifies and fixes common configuration issues:
1. Environment variable substitution in config files
2. Provider consistency across files
3. API key validation
4. Configuration file cleanup

Usage:
    python3 fix_config_issues.py [--fix] [--clean]
"""

import os
import sys
import argparse
from pathlib import Path
import yaml

# ANSI colors
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"

def find_config_files():
    """Find all configuration files"""
    config_files = [
        'local_config.yaml',
        'test_config.yaml',
        'config.yaml',
        'mini_agent/config/config.yaml',
        'mini_agent/config/config-example.yaml'
    ]
    
    found_files = []
    for file_path in config_files:
        path = Path(file_path)
        if path.exists():
            found_files.append(path)
    return found_files

def check_environment_substitution(content):
    """Check for unresolved environment variables"""
    import re
    env_vars = re.findall(r'\$\{([^}]+)\}', content)
    return env_vars

def fix_environment_substitution(content, api_key):
    """Fix environment variable substitution in config content"""
    content = content.replace('${MINIMAX_API_KEY}', api_key)
    return content

def validate_api_key(api_key):
    """Basic API key validation"""
    if not api_key:
        return False, "API key is empty"
    
    if len(api_key) < 10:
        return False, "API key seems too short"
    
    # Check for common patterns
    if not any(c.isalnum() for c in api_key):
        return False, "API key contains no alphanumeric characters"
    
    return True, "API key looks valid"

def consolidate_configs(config_files, api_key, dry_run=True):
    """Create a single, clean configuration file"""
    
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}=== CONFIGURATION CONSOLIDATION ==={Colors.RESET}")
    
    # Determine which file to use as base
    preferred_files = [
        'mini_agent/config/config.yaml',
        'config.yaml',
        'local_config.yaml'
    ]
    
    base_config = None
    base_file = None
    
    for file_path in preferred_files:
        path = Path(file_path)
        if path.exists():
            try:
                with open(path) as f:
                    content = f.read()
                    # Check for environment variables
                    env_vars = check_environment_substitution(content)
                    if env_vars:
                        print(f"  {Colors.YELLOW}⚠{Colors.RESET} {file_path} has unresolved environment variables: {env_vars}")
                        # Fix the content
                        content = fix_environment_substitution(content, api_key)
                    
                    config_data = yaml.safe_load(content)
                    if config_data and 'llm' in config_data:
                        base_config = config_data
                        base_file = file_path
                        print(f"  {Colors.GREEN}✓{Colors.RESET} Using {file_path} as base configuration")
                        break
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} Error reading {file_path}: {e}")
                continue
    
    if not base_config:
        print(f"  {Colors.RED}✗{Colors.RESET} No valid configuration found")
        return False
    
    # Ensure consistent provider
    base_config['llm']['provider'] = 'openai'  # Force openai for MiniMax compatibility
    base_config['llm']['api_base'] = 'https://api.minimax.io'
    
    # Write consolidated config
    output_file = 'fixed_config.yaml'
    if not dry_run:
        try:
            with open(output_file, 'w') as f:
                yaml.dump(base_config, f, default_flow_style=False, indent=2)
            print(f"  {Colors.GREEN}✓{Colors.RESET} Created consolidated config: {output_file}")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} Error writing {output_file}: {e}")
            return False
    else:
        print(f"  {Colors.BRIGHT_YELLOW}→{Colors.RESET} Would create consolidated config: {output_file}")
    
    return True

def clean_duplicate_configs(config_files, dry_run=True):
    """Remove or rename duplicate configuration files"""
    
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}=== CONFIGURATION CLEANUP ==={Colors.RESET}")
    
    keep_file = 'fixed_config.yaml'
    backup_dir = Path('config_backup')
    
    if not dry_run:
        backup_dir.mkdir(exist_ok=True)
    
    files_to_move = []
    for config_file in config_files:
        if config_file.name != keep_file and 'config' in config_file.name:
            files_to_move.append(config_file)
    
    for config_file in files_to_move:
        backup_name = backup_dir / f"{config_file.name}.backup"
        if not dry_run:
            try:
                config_file.rename(backup_name)
                print(f"  {Colors.GREEN}✓{Colors.RESET} Moved {config_file} to {backup_name}")
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} Error moving {config_file}: {e}")
        else:
            print(f"  {Colors.BRIGHT_YELLOW}→{Colors.RESET} Would move {config_file} to {backup_name}")

def create_env_template():
    """Create a .env template file"""
    
    template_content = """# Mini-Agent Configuration Template
# Copy this file to .env and fill in your API keys

# Primary API Key (required)
MINIMAX_API_KEY=your_minimax_api_key_here

# Optional: Alternative providers
# ANTHROPIC_AUTH_TOKEN=your_anthropic_key_here
# ZAI_API_KEY=your_zai_key_here

# Configuration (optional overrides)
# MINIMAX_API_BASE=https://api.minimax.io
# MINIMAX_MODEL=MiniMax-M2
# MINIMAX_PROVIDER=openai
"""
    
    return template_content

def main():
    parser = argparse.ArgumentParser(description='Fix Mini-Agent configuration issues')
    parser.add_argument('--fix', action='store_true', help='Apply fixes (default is dry-run)')
    parser.add_argument('--clean', action='store_true', help='Clean up duplicate config files')
    parser.add_argument('--env-template', action='store_true', help='Create .env template')
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.BRIGHT_YELLOW}🔧 Mini-Agent Configuration Fix Utility{Colors.RESET}")
    
    if not args.fix:
        print(f"{Colors.YELLOW}Running in DRY-RUN mode. Use --fix to apply changes.{Colors.RESET}")
    
    # Step 1: Check for API key
    api_key = os.getenv('MINIMAX_API_KEY')
    if not api_key:
        print(f"\n{Colors.RED}❌ MINIMAX_API_KEY not found in environment{Colors.RESET}")
        
        # Check for .env file
        env_file = Path('.env')
        if env_file.exists():
            print(f"{Colors.YELLOW}Found .env file, checking contents...{Colors.RESET}")
            try:
                with open(env_file) as f:
                    for line in f:
                        if line.startswith('MINIMAX_API_KEY='):
                            api_key = line.split('=', 1)[1].strip()
                            if api_key and api_key != 'your_minimax_api_key_here':
                                print(f"{Colors.GREEN}✓ Found API key in .env file{Colors.RESET}")
                                break
            except Exception as e:
                print(f"{Colors.RED}Error reading .env file: {e}{Colors.RESET}")
    
    if not api_key:
        print(f"\n{Colors.RED}No API key found. Options:{Colors.RESET}")
        print(f"  1. Set environment variable: export MINIMAX_API_KEY=your_key")
        print(f"  2. Create .env file with: MINIMAX_API_KEY=your_key")
        print(f"  3. Use --env-template to create template")
        
        if args.env_template:
            template = create_env_template()
            with open('.env.template', 'w') as f:
                f.write(template)
            print(f"\n{Colors.GREEN}✓ Created .env.template file{Colors.RESET}")
        return
    
    # Step 2: Validate API key
    is_valid, message = validate_api_key(api_key)
    if is_valid:
        print(f"\n{Colors.GREEN}✓ API key validation: {message}{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠ API key validation: {message}{Colors.RESET}")
    
    # Step 3: Find and analyze config files
    config_files = find_config_files()
    print(f"\n{Colors.BOLD}Found {len(config_files)} configuration files:{Colors.RESET}")
    
    for config_file in config_files:
        try:
            with open(config_file) as f:
                content = f.read()
                env_vars = check_environment_substitution(content)
                
                # Load and check provider
                config_data = yaml.safe_load(content)
                provider = config_data.get('llm', {}).get('provider', 'unknown') if config_data else 'unknown'
                
                status = "⚠" if env_vars else "✓"
                color = Colors.YELLOW if env_vars else Colors.GREEN
                print(f"  {color}{status}{Colors.RESET} {config_file} (provider: {provider})")
                
                if env_vars:
                    print(f"    {Colors.YELLOW}  → Contains unresolved variables: {env_vars}{Colors.RESET}")
                    
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} {config_file} (error: {e})")
    
    # Step 4: Consolidate configuration
    if consolidate_configs(config_files, api_key, dry_run=not args.fix):
        print(f"\n{Colors.BRIGHT_GREEN}Configuration consolidation completed{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}Configuration consolidation failed{Colors.RESET}")
    
    # Step 5: Clean up duplicates
    if args.clean:
        clean_duplicate_configs(config_files, dry_run=not args.fix)
    
    # Step 6: Final recommendations
    print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}=== RECOMMENDATIONS ==={Colors.RESET}")
    
    if not args.fix:
        print(f"\n{Colors.YELLOW}To apply fixes, run:{Colors.RESET}")
        print(f"  python3 fix_config_issues.py --fix")
    
    print(f"\n{Colors.BRIGHT_YELLOW}Next steps:{Colors.RESET}")
    print(f"  1. {Colors.GREEN}Test the fixed configuration:{Colors.RESET}")
    print(f"     python3 comprehensive_diagnostic.py")
    print(f"  2. {Colors.GREEN}Test the CLI:{Colors.RESET}")
    print(f"     python3 -m mini_agent.cli")
    print(f"  3. {Colors.GREEN}Use the fixed config:{Colors.RESET}")
    print(f"     export MINIMAX_CONFIG_FILE=fixed_config.yaml")

if __name__ == "__main__":
    main()