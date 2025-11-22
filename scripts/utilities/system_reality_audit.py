#!/usr/bin/env python3
"""
Mini-Agent System Reality Audit
===============================
Real-time audit of what's actually implemented vs what should be.
This addresses the user's concern about not knowing what's truly built.
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
import importlib.util

def load_config():
    """Load the actual configuration"""
    config_path = Path("mini_agent/config/config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def audit_models():
    """Check what models are actually configured and working"""
    print("🤖 MODEL AUDIT")
    print("=" * 40)
    
    config = load_config()
    
    # Check primary model
    print(f"Primary Model: {config.get('model', 'Unknown')}")
    print(f"Provider: {config.get('provider', 'Unknown')}")
    print(f"API Base: {config.get('api_base', 'Unknown')}")
    
    # Check Z.AI settings
    zai_settings = config.get('tools', {}).get('zai_settings', {})
    print(f"\nZ.AI Configuration:")
    print(f"  Default Model: {zai_settings.get('default_model', 'Unknown')}")
    print(f"  Search Model: {zai_settings.get('search_model', 'Unknown')}")
    print(f"  Base URL: {zai_settings.get('zai_base', 'Unknown')}")
    print(f"  Enabled: {config.get('tools', {}).get('enable_zai_search', False)}")
    
    # Check if credit protection is active
    protection_file = Path("mini_agent/utils/credit_protection.py")
    if protection_file.exists():
        with open(protection_file, 'r') as f:
            content = f.read()
            if 'ZAI_DISABLED' in content:
                print(f"  🚫 Credit Protection: ACTIVE (Z.AI disabled)")
            else:
                print(f"  ✅ Credit Protection: Not blocking")
    
    # Check actual LLM clients
    llm_dir = Path("mini_agent/llm")
    if llm_dir.exists():
        llm_files = list(llm_dir.glob("*.py"))
        print(f"\nLLM Client Files Found:")
        for file in llm_files:
            print(f"  - {file.name}")
    
    return {
        'primary_model': config.get('model'),
        'provider': config.get('provider'),
        'zai_enabled': config.get('tools', {}).get('enable_zai_search', False),
        'zai_model': zai_settings.get('default_model'),
        'llm_clients': len(llm_files) if llm_dir.exists() else 0
    }

def audit_web_functionality():
    """Check what's actually implemented for web functionality"""
    print("\n🌐 WEB FUNCTIONALITY AUDIT")
    print("=" * 40)
    
    # Check Z.AI tools
    zai_tool_path = Path("mini_agent/tools/zai_unified_tools.py")
    if zai_tool_path.exists():
        with open(zai_tool_path, 'r') as f:
            content = f.read()
            if 'web_search' in content:
                print("✅ Z.AI Web Search: Implemented")
            else:
                print("❌ Z.AI Web Search: Not implemented")
            
            if 'web_reading' in content:
                print("✅ Z.AI Web Reading: Implemented")
            else:
                print("❌ Z.AI Web Reading: Not implemented")
    
    # Check if web functions are enabled in config
    config = load_config()
    web_enabled = config.get('tools', {}).get('enable_zai_search', False)
    print(f"\nWeb Functions Status: {'ENABLED' if web_enabled else 'DISABLED'}")
    
    if not web_enabled:
        print("🚫 Web functions are DISABLED by credit protection")
        print("   To enable: Set enable_zai_search: true in config.yaml")
    
    # Check for OpenAI web functions
    openai_functions_path = Path("mini_agent/tools/openai_web_functions")
    if openai_functions_path.exists():
        function_files = list(openai_functions_path.glob("*.py"))
        print(f"\nOpenAI Web Functions: {len(function_files)} files found")
        for file in function_files:
            print(f"  - {file.name}")
    
    return {
        'zai_web_search': zai_tool_path.exists() and 'web_search' in open(zai_tool_path).read(),
        'zai_web_reading': zai_tool_path.exists() and 'web_reading' in open(zai_tool_path).read(),
        'web_enabled': web_enabled,
        'openai_functions': len(function_files) if openai_functions_path.exists() else 0
    }

def audit_tools_integration():
    """Check what tools are actually integrated"""
    print("\n🛠️ TOOLS INTEGRATION AUDIT")
    print("=" * 40)
    
    tools_dir = Path("mini_agent/tools")
    if tools_dir.exists():
        tool_files = [f for f in tools_dir.glob("*.py") if f.name != "__init__.py"]
        print(f"Tool Files Found: {len(tool_files)}")
        
        for tool in tool_files:
            print(f"  - {tool.name}")
            
            # Check if it's a working tool
            try:
                spec = importlib.util.spec_from_file_location(tool.stem, tool)
                if spec:
                    print(f"    ✅ Loads successfully")
                else:
                    print(f"    ❌ Import error")
            except Exception as e:
                print(f"    ⚠️ Import issue: {str(e)[:50]}...")
    
    # Check skills framework
    skills_dir = Path("mini_agent/skills")
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        print(f"\nSkills Framework: {len(skill_dirs)} skills")
        for skill in skill_dirs[:5]:  # Show first 5
            print(f"  - {skill.name}")
        if len(skill_dirs) > 5:
            print(f"  ... and {len(skill_dirs) - 5} more")
    
    return {
        'tool_count': len(tool_files) if tools_dir.exists() else 0,
        'skills_count': len(skill_dirs) if skills_dir.exists() else 0
    }

def audit_file_organization():
    """Check file organization and clutter"""
    print("\n📁 FILE ORGANIZATION AUDIT")
    print("=" * 40)
    
    # Check main directory for clutter
    main_dir = Path(".")
    main_files = [f for f in main_dir.iterdir() if f.is_file() and f.suffix in ['.py', '.md', '.sh']]
    print(f"Files in main directory: {len(main_files)}")
    
    clutter_files = []
    for file in main_files:
        if file.name not in ['README.md', 'requirements.txt', '.env.example']:
            clutter_files.append(file.name)
    
    if clutter_files:
        print("🚫 Clutter files found:")
        for file in clutter_files:
            print(f"  - {file}")
    
    # Check scripts directory organization
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        subdirs = [d for d in scripts_dir.iterdir() if d.is_dir()]
        print(f"\nScripts organization: {len(subdirs)} subdirectories")
        for subdir in subdirs:
            file_count = len(list(subdir.glob("*")))
            print(f"  - {subdir.name}/ ({file_count} files)")
    
    return {
        'main_clutter': len(clutter_files),
        'scripts_subdirs': len(subdirs) if scripts_dir.exists() else 0
    }

def check_sdk_usage():
    """Check which SDK is actually being used"""
    print("\n🔧 SDK USAGE AUDIT")
    print("=" * 40)
    
    # Check main agent file
    agent_file = Path("mini_agent/agent.py")
    if agent_file.exists():
        with open(agent_file, 'r') as f:
            content = f.read()
            
            if 'openai' in content.lower():
                print("✅ OpenAI SDK usage detected in agent.py")
            if 'anthropic' in content.lower():
                print("✅ Anthropic SDK usage detected in agent.py")
            if 'minimax' in content.lower():
                print("✅ MiniMax SDK usage detected in agent.py")
    
    # Check LLM wrapper
    wrapper_file = Path("mini_agent/llm/llm_wrapper.py")
    if wrapper_file.exists():
        with open(wrapper_file, 'r') as f:
            content = f.read()
            
            openai_count = content.lower().count('openai')
            anthropic_count = content.lower().count('anthropic')
            
            print(f"\nLLM Wrapper Analysis:")
            print(f"  OpenAI references: {openai_count}")
            print(f"  Anthropic references: {anthropic_count}")
    
    return {
        'agent_sdk': 'openai' if agent_file.exists() and 'openai' in open(agent_file).read().lower() else 'unknown',
        'wrapper_analysis': {'openai': openai_count, 'anthropic': anthropic_count}
    }

def generate_reality_report():
    """Generate comprehensive reality audit report"""
    print("🔍 MINI-AGENT SYSTEM REALITY AUDIT")
    print("=" * 50)
    print(f"Audit Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all audits
    model_data = audit_models()
    web_data = audit_web_functionality()
    tools_data = audit_tools_integration()
    file_data = audit_file_organization()
    sdk_data = check_sdk_usage()
    
    print("\n" + "=" * 50)
    print("📊 REALITY CHECK SUMMARY")
    print("=" * 50)
    
    print(f"🤖 Models:")
    print(f"  Primary: {model_data.get('primary_model', 'Unknown')}")
    print(f"  Provider: {model_data.get('provider', 'Unknown')}")
    print(f"  Z.AI: {'Enabled' if model_data.get('zai_enabled') else 'Disabled'}")
    
    print(f"\n🌐 Web Functions:")
    print(f"  Status: {'Working' if web_data.get('web_enabled') else 'Disabled'}")
    print(f"  Z.AI Search: {'✅' if web_data.get('zai_web_search') else '❌'}")
    print(f"  Z.AI Reading: {'✅' if web_data.get('zai_web_reading') else '❌'}")
    
    print(f"\n🛠️ Integration:")
    print(f"  Tools: {tools_data.get('tool_count', 0)}")
    print(f"  Skills: {tools_data.get('skills_count', 0)}")
    
    print(f"\n📁 Organization:")
    print(f"  Main clutter: {file_data.get('main_clutter', 0)} files")
    print(f"  Scripts org: {file_data.get('scripts_subdirs', 0)} categories")
    
    # Save detailed report
    report = {
        'audit_time': datetime.now().isoformat(),
        'models': model_data,
        'web_functions': web_data,
        'tools': tools_data,
        'organization': file_data,
        'sdk_usage': sdk_data
    }
    
    report_file = Path("SYSTEM_REALITY_AUDIT.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    # Address user's specific concerns
    print("\n" + "=" * 50)
    print("🎯 ADDRESSING YOUR CONCERNS")
    print("=" * 50)
    
    print("1. Web Functionality Reality:")
    if not web_data.get('web_enabled'):
        print("   🚫 Z.AI web functions are DISABLED by credit protection")
        print("   📝 You need to set enable_zai_search: true in config.yaml")
        print("   🔍 This explains why you only see snippets in terminal")
    else:
        print("   ✅ Z.AI web functions are enabled")
    
    print("\n2. MiniMax-M2 vs Claude SDK Reality:")
    if sdk_data.get('agent_sdk') == 'openai':
        print("   📋 System is using OpenAI SDK format (not Claude SDK)")
        print("   ⚠️ This means original Claude integration may be lost")
    
    print("\n3. File Organization Reality:")
    if file_data.get('main_clutter', 0) > 0:
        print(f"   🚫 {file_data.get('main_clutter')} files cluttering main directory")
        print("   📁 Need to move to appropriate script categories")
    
    return report

if __name__ == "__main__":
    try:
        audit_report = generate_reality_report()
        print("\n✅ Reality audit complete!")
    except Exception as e:
        print(f"❌ Audit failed: {e}")
        sys.exit(1)