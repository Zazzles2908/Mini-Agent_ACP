#!/usr/bin/env python3
"""
MANUAL VALIDATION: MCP Format Standardization

This validates that the MCP server format is properly standardized.
"""

def validate_mcp_format():
    """Validate the MCP format standardization"""
    print("🧪 VALIDATING MCP FORMAT STANDARDIZATION")
    print("=" * 45)
    
    # Read MCP config file
    mcp_path = "mini_agent/config/z_mcp_servers.json"
    
    with open(mcp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📁 Reading MCP config from: {mcp_path}")
    
    # Check JSON validity
    import json
    try:
        data = json.loads(content)
        print("✅ SUCCESS: Valid JSON syntax")
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON: {e}")
        return False
    
    # Check for standard MCP structure
    if "mcpServers" in data:
        print("✅ SUCCESS: Contains standard 'mcpServers' key")
    else:
        print("❌ FAIL: Missing 'mcpServers' key")
        return False
    
    # Check for non-standard fields (should be removed)
    non_standard_fields = ["tools", "quotas", "security"]
    found_non_standard = []
    
    for field in non_standard_fields:
        if field in data:
            found_non_standard.append(field)
    
    if found_non_standard:
        print(f"❌ FAIL: Found non-standard fields: {found_non_standard}")
        return False
    else:
        print("✅ SUCCESS: Non-standard fields removed")
    
    # Check server configurations
    mcp_servers = data.get("mcpServers", {})
    print(f"🔍 Found {len(mcp_servers)} MCP servers:")
    
    required_servers = ["zai-web-search", "zai-web-reader"]
    all_servers_found = True
    
    for server_name in required_servers:
        if server_name in mcp_servers:
            server_config = mcp_servers[server_name]
            print(f"✅ {server_name}:")
            print(f"   - Command: {server_config.get('command', 'N/A')}")
            print(f"   - URL: {server_config.get('url', 'N/A')}")
            
            # Check for proper remote command
            if server_config.get('command') == 'remote':
                print("   - ✅ Uses 'remote' command (correct)")
            else:
                print(f"   - ⚠️ Command: {server_config.get('command', 'N/A')} (check if correct)")
                
        else:
            print(f"❌ {server_name}: NOT FOUND")
            all_servers_found = False
    
    if not all_servers_found:
        print("❌ FAIL: Required MCP servers missing")
        return False
    
    # Verify structure matches MCP specification
    print("\n🔍 Checking MCP specification compliance:")
    
    for server_name, server_config in mcp_servers.items():
        required_keys = ["command", "url"]
        missing_keys = []
        
        for key in required_keys:
            if key not in server_config:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ {server_name}: Missing keys {missing_keys}")
            return False
        else:
            print(f"✅ {server_name}: Has required keys {required_keys}")
    
    # Test server configuration functionality
    print("\n🧪 Testing server configuration:")
    try:
        for server_name, server_config in mcp_servers.items():
            url = server_config.get('url', '')
            if url.startswith('https://api.z.ai/api/mcp/'):
                print(f"✅ {server_name}: Valid Z.AI MCP endpoint")
            else:
                print(f"⚠️ {server_name}: URL format: {url}")
                
    except Exception as e:
        print(f"❌ ERROR: Server config test failed: {e}")
        return False
    
    print("\n✅ SUCCESS: MCP format is properly standardized")
    return True

if __name__ == "__main__":
    success = validate_mcp_format()
    if success:
        print("\n🎉 MCP FORMAT VALIDATION PASSED")
    else:
        print("\n💥 MCP FORMAT VALIDATION FAILED")
