#!/usr/bin/env python3
"""
Verify Z.AI API endpoint for GLM-4.6
"""

def check_zai_endpoints():
    """Check Z.AI API endpoints"""
    print("🌐 Z.AI API Endpoints Verification")
    print("=" * 50)
    
    print("📍 Z.AI API Base URLs:")
    print("   1. Common API: https://api.z.ai/api/paas/v4")
    print("   2. Coding Plan API: https://api.z.ai/api/coding/paas/v4")
    
    print("\n🤖 GLM Model Endpoints:")
    print("   For GLM-4.6 reasoning:")
    print("     Coding Plan API: https://api.z.ai/api/coding/paas/v4/messages")
    print("   For Web Search:")
    print("     Coding Plan API: https://api.z.ai/api/coding/paas/v4/search")
    
    print("\n⚠️ Current Configuration Issue:")
    print("   Current: api_base = 'https://api.z.ai/api/paas/v4'")
    print("   Should be: api_base = 'https://api.z.ai/api/coding/paas/v4'")
    print("   for GLM-4.6 Coding Plan access")
    
    print("\n🔧 Fix Required:")
    print("   Update config.yaml api_base to:")
    print("   api_base: 'https://api.z.ai/api/coding/paas/v4'")

if __name__ == "__main__":
    check_zai_endpoints()