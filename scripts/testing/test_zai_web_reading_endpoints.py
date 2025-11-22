#!/usr/bin/env python3
"""
Test Z.AI web reading endpoints to identify the correct configuration.
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from pathlib import Path

# Test different endpoints and configurations
async def test_web_reading_endpoints():
    """Test various web reading API configurations."""
    
    api_key = "1cd42fbb5c474884bddce3b534577199.dy9Fpa1x5TMES0qQ"
    target_url = "https://docs.z.ai/devpack/tool/minimax"
    
    print("🧪 Z.AI WEB READING ENDPOINT TESTING")
    print("=" * 60)
    print(f"API Key: {api_key[:20]}...")
    print(f"Target URL: {target_url}")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
    }
    
    # Test configurations
    test_configs = [
        {
            "name": "Coding Plan /reader",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "endpoint": "/reader",
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
            }
        },
        {
            "name": "Common API /reader", 
            "base_url": "https://api.z.ai/api/paas/v4",
            "endpoint": "/reader",
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
            }
        },
        {
            "name": "Coding Plan /web_reader",
            "base_url": "https://api.z.ai/api/coding/paas/v4", 
            "endpoint": "/web_reader",
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
            }
        },
        {
            "name": "Common API /web_reader",
            "base_url": "https://api.z.ai/api/paas/v4",
            "endpoint": "/web_reader", 
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
            }
        },
        {
            "name": "Coding Plan /reader with model",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "endpoint": "/reader",
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
                "model": "glm-4.5",
            }
        },
        {
            "name": "Coding Plan /reader with model glm-4.6",
            "base_url": "https://api.z.ai/api/coding/paas/v4",
            "endpoint": "/reader", 
            "payload": {
                "url": target_url,
                "return_format": "markdown",
                "retain_images": False,
                "model": "glm-4.6",
            }
        }
    ]
    
    results = []
    
    for config in test_configs:
        print(f"\n🔍 Testing: {config['name']}")
        print(f"   URL: {config['base_url']}{config['endpoint']}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['base_url']}{config['endpoint']}",
                    headers=headers,
                    json=config['payload'],
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    
                    status = response.status
                    response_text = await response.text()
                    
                    print(f"   Status: {status}")
                    
                    if status == 200:
                        try:
                            response_json = json.loads(response_text)
                            print(f"   ✅ SUCCESS! JSON response received")
                            print(f"   Content length: {len(response_text)} characters")
                            
                            # Extract content if available
                            content = ""
                            if "web_page_reader_result" in response_json:
                                content = response_json["web_page_reader_result"].get("content", "")
                            elif "content" in response_json:
                                content = response_json["content"]
                            
                            print(f"   Extracted content length: {len(content)} characters")
                            if content:
                                print(f"   Content preview: {content[:200]}...")
                            
                            results.append({
                                "config": config['name'],
                                "status": status,
                                "success": True,
                                "content_length": len(content),
                                "content_preview": content[:200] if content else "",
                                "response": response_json
                            })
                            
                        except json.JSONDecodeError:
                            print(f"   ⚠️  SUCCESS but not JSON: {response_text[:100]}...")
                            results.append({
                                "config": config['name'],
                                "status": status,
                                "success": True,
                                "content_length": len(response_text),
                                "content_preview": response_text[:200],
                                "response": response_text
                            })
                    
                    else:
                        try:
                            error_json = json.loads(response_text)
                            print(f"   ❌ FAILED: {error_json}")
                            results.append({
                                "config": config['name'],
                                "status": status,
                                "success": False,
                                "error": error_json
                            })
                        except json.JSONDecodeError:
                            print(f"   ❌ FAILED: {response_text[:100]}...")
                            results.append({
                                "config": config['name'],
                                "status": status,
                                "success": False,
                                "error": response_text
                            })
        
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            results.append({
                "config": config['name'],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print(f"\n📊 TESTING SUMMARY")
    print("=" * 40)
    
    successful_tests = [r for r in results if r.get("success")]
    failed_tests = [r for r in results if not r.get("success")]
    
    print(f"Successful: {len(successful_tests)}/{len(results)}")
    print(f"Failed: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print(f"\n✅ WORKING CONFIGURATIONS:")
        for test in successful_tests:
            print(f"   • {test['config']}")
            print(f"     Content length: {test.get('content_length', 0)} chars")
    
    if failed_tests:
        print(f"\n❌ FAILED CONFIGURATIONS:")
        for test in failed_tests:
            print(f"   • {test['config']}: {test.get('error', 'Unknown error')}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output/research")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = output_dir / f"zai_web_reading_endpoint_test_{timestamp}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "api_key_prefix": api_key[:20] + "...",
            "target_url": target_url,
            "total_tests": len(results),
            "successful_tests": len(successful_tests),
            "failed_tests": len(failed_tests),
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    asyncio.run(test_web_reading_endpoints())