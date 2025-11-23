#!/usr/bin/env python3
"""Fix JWT authentication for MiniMax API calls."""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path.cwd()))

import anthropic
import aiohttp

async def test_jwt_authentication():
    """Test JWT authentication with MiniMax API."""
    print("🔐 Testing JWT Authentication Fix")
    print("=" * 50)
    
    # Read JWT token from .env
    env_path = Path(".env")
    jwt_token = None
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("MINIMAX_API_KEY="):
                    jwt_token = line.split("=", 1)[1].strip()
                    break
    
    if not jwt_token:
        print("❌ No JWT token found in .env")
        return False
    
    print(f"🔑 JWT Token: {jwt_token[:20]}...{jwt_token[-20:]}")
    
    # Test different authentication formats
    test_cases = [
        {
            "name": "Bearer JWT (Standard)",
            "headers": {
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        },
        {
            "name": "Direct JWT (No Bearer)",
            "headers": {
                "Authorization": jwt_token,  # Direct JWT without Bearer
                "Content-Type": "application/json", 
                "anthropic-version": "2023-06-01"
            }
        },
        {
            "name": "Bearer + X-API-Key",
            "headers": {
                "Authorization": f"Bearer {jwt_token}",
                "x-api-key": jwt_token,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        }
    ]
    
    payload = {
        "model": "MiniMax-M2",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Say 'Authentication test successful'"}]
    }
    
    # Test China platform
    api_base = "https://api.minimaxi.com/anthropic"
    
    async with aiohttp.ClientSession() as session:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📤 Test {i}: {test_case['name']}")
            
            try:
                async with session.post(
                    f"{api_base}/messages",
                    headers=test_case['headers'],
                    json=payload
                ) as resp:
                    status = resp.status
                    response_text = await resp.text()
                    
                    print(f"📊 Status: {status}")
                    
                    if status == 200:
                        print(f"✅ SUCCESS! Authentication format: {test_case['name']}")
                        print(f"📥 Response: {response_text[:200]}...")
                        return True, test_case['headers']
                    elif status == 401:
                        print(f"❌ Auth failed (401): {response_text[:200]}")
                    else:
                        print(f"❌ Error ({status}): {response_text[:200]}")
                        
            except Exception as e:
                print(f"❌ Exception: {e}")
    
    return False, None

async def test_anthropic_sdk_custom_auth():
    """Test Anthropic SDK with custom authentication."""
    print(f"\n🔧 Testing Anthropic SDK with JWT authentication...")
    
    # Read JWT token
    env_path = Path(".env")
    jwt_token = None
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("MINIMAX_API_KEY="):
                    jwt_token = line.split("=", 1)[1].strip()
                    break
    
    if not jwt_token:
        return False
    
    try:
        # Test with custom headers
        client = anthropic.AsyncAnthropic(
            base_url="https://api.minimaxi.com/anthropic",
            api_key=jwt_token,
            default_headers={
                "Authorization": f"Bearer {jwt_token}",
                "anthropic-version": "2023-06-01"
            }
        )
        
        messages = [{"role": "user", "content": "Say 'SDK test successful'"}]
        response = await client.messages.create(
            model="MiniMax-M2",
            max_tokens=100,
            messages=messages
        )
        
        print(f"✅ Anthropic SDK SUCCESS!")
        print(f"📥 Content: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"❌ Anthropic SDK failed: {e}")
        
        # Check error details
        if "401" in str(e):
            print(f"🔍 Authentication failed - JWT token format issue")
        elif "404" in str(e):
            print(f"🔍 Endpoint issue - check API base URL")
        else:
            print(f"🔍 Other error - may need different approach")
            
        return False

async def main():
    """Run JWT authentication tests."""
    print("🚀 Testing JWT Authentication Fix")
    print("Testing different JWT authentication formats for MiniMax...\n")
    
    # Test direct HTTP requests
    success, working_headers = await test_jwt_authentication()
    
    if success:
        print(f"\n🎉 JWT AUTHENTICATION FIXED!")
        print(f"✅ Working authentication: {working_headers}")
        return True, working_headers
    else:
        # Test Anthropic SDK with custom auth
        sdk_success = await test_anthropic_sdk_custom_auth()
        return sdk_success, None

if __name__ == "__main__":
    success, headers = asyncio.run(main())
    if success:
        print(f"\n✅ JWT authentication works!")
        print(f"💡 Next: Update Anthropic client with working auth format")
    else:
        print(f"\n❌ JWT authentication still needs work")
        print(f"💡 May need different authentication approach")
    
    sys.exit(0 if success else 1)
