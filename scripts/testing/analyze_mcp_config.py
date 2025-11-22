#!/usr/bin/env python3
"""
MCP Configuration Analysis Tool
Analyzes MCP server configuration and connection issues

Usage:
    python analyze_mcp_config.py
"""

import json
import os
import sys
from pathlib import Path


def find_mcp_config():
    """Find MCP configuration file"""
    search_paths = [
        "mcp.json",
        "mini_agent/config/mcp.json",
        ".mini-agent/config/mcp.json"
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return Path(path).resolve()
    
    return None


def analyze_mcp_config(config_path):
    """Analyze MCP configuration for issues"""
    print(f"📁 Analyzing MCP config: {config_path}")
    print("=" * 60)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Configuration loaded successfully")
        
        # Check structure
        if 'mcpServers' in config:
            servers = config['mcpServers']
            print(f"📊 Found {len(servers)} MCP servers:")
            
            for server_name, server_config in servers.items():
                print(f"\n🔧 Server: {server_name}")
                print(f"   Config: {json.dumps(server_config, indent=6)}")
                
                # Check for common issues
                issues = []
                
                if 'disabled' in server_config and server_config['disabled']:
                    issues.append("⚠️  Server is disabled")
                
                if 'command' not in server_config:
                    issues.append("❌ Missing 'command' field")
                
                if 'args' not in server_config and 'command' in server_config:
                    issues.append("⚠️  No arguments specified")
                
                # Check for known problematic servers
                if server_name == 'minimax_search':
                    issues.append("🚨 Known problematic server - causes 'Connection closed' errors")
                    issues.append("💡 This should be disabled since Z.AI provides native web search")
                
                if server_name == 'filesystem':
                    issues.append("ℹ️  Filesystem server - may restrict directory access")
                
                if issues:
                    print(f"   Issues found:")
                    for issue in issues:
                        print(f"     {issue}")
                else:
                    print(f"   ✅ No obvious issues")
        
        else:
            print("❌ No 'mcpServers' section found in configuration")
    
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False
    
    return True


def generate_recommendations(config_path):
    """Generate recommendations based on analysis"""
    print(f"\n💡 Recommendations")
    print("=" * 60)
    
    print("🎯 Based on your setup, here are the recommended actions:")
    
    print("\n1. **For Web Search Issues:**")
    print("   • Disable 'minimax_search' MCP server")
    print("   • Use native Z.AI web search instead")
    print("   • Z.AI provides better web search via GLM models")
    
    print("\n2. **For File Access Issues:**")
    print("   • Mini-Agent has native file tools (ReadTool, WriteTool, EditTool)")
    print("   • These work with workspace directory by design")
    print("   • Filesystem MCP server may restrict access in MiniMax-M2 Desktop")
    
    print("\n3. **MCP Server Strategy:**")
    print("   • Keep: git, memory (if needed)")
    print("   • Disable: minimax_search (use Z.AI instead)")
    print("   • Monitor: filesystem (may need for broader access)")
    
    print("\n4. **Z.AI Integration Benefits:**")
    print("   • Native GLM web search (no external MCP needed)")
    print("   • Built-in AI analysis of search results")
    print("   • Multiple GLM models (glm-4.6, glm-4.5, glm-4-air)")
    print("   • Intelligent model selection based on task")


def create_fixed_config(config_path):
    """Create a fixed version of the MCP configuration"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Create backup
        backup_path = f"{config_path}.backup.{int(os.path.getmtime(config_path))}"
        import shutil
        shutil.copy2(config_path, backup_path)
        print(f"💾 Created backup: {backup_path}")
        
        # Create fixed configuration
        fixed_config = {
            "mcpServers": {}
        }
        
        # Process existing servers
        if 'mcpServers' in config:
            for server_name, server_config in config['mcpServers'].items():
                if server_name == 'minimax_search':
                    # Skip problematic server
                    print(f"⚠️  Skipping problematic server: {server_name}")
                    continue
                elif server_name == 'filesystem':
                    # Keep but add note
                    server_config['_note'] = "Filesystem server - may restrict directory access"
                    fixed_config['mcpServers'][server_name] = server_config
                    print(f"✅ Keeping filesystem server")
                else:
                    # Keep other servers
                    fixed_config['mcpServers'][server_name] = server_config
                    print(f"✅ Keeping server: {server_name}")
        
        # Add comment about Z.AI integration
        fixed_config['_note'] = "minimax_search disabled - using native Z.AI web search instead"
        
        # Write fixed configuration
        fixed_path = f"{config_path}.fixed"
        with open(fixed_path, 'w') as f:
            json.dump(fixed_config, f, indent=2)
        
        print(f"✅ Created fixed configuration: {fixed_path}")
        print(f"   To apply: copy {fixed_path} to {config_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating fixed configuration: {e}")
        return False


def main():
    """Main analysis function"""
    print("🔍 MCP Configuration Analysis Tool")
    print("=" * 60)
    print(f"Working Directory: {os.getcwd()}")
    
    # Find configuration file
    config_path = find_mcp_config()
    
    if not config_path:
        print("❌ MCP configuration file not found")
        print("   Searched in:")
        print("   • mcp.json")
        print("   • mini_agent/config/mcp.json") 
        print("   • .mini-agent/config/mcp.json")
        print("\n💡 This is normal if using only Z.AI tools without MCP servers")
        return
    
    print(f"✅ Found configuration: {config_path}")
    
    # Analyze configuration
    if analyze_mcp_config(config_path):
        generate_recommendations(config_path)
        
        # Offer to create fixed configuration
        print(f"\n🛠️  Fix Configuration?")
        response = input("Create a fixed configuration without problematic servers? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            if create_fixed_config(config_path):
                print(f"\n✅ Fixed configuration created!")
                print(f"   Review the fixed config and apply if it looks good")
            else:
                print(f"\n❌ Failed to create fixed configuration")
        else:
            print(f"\n⏭️  Skipping configuration fix")
    
    else:
        print(f"\n❌ Configuration analysis failed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Analysis failed with exception: {e}")
        import traceback
        traceback.print_exc()
