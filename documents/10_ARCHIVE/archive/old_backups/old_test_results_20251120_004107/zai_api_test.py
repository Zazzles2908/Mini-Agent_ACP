#!/usr/bin/env python3
"""
Direct Z.AI API Test Script
Tests the raw API endpoints as requested by user
"""

import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('ZAI_API_KEY')

def test_web_search():
    print('=== RAW Z.AI WEB SEARCH RESULTS ===')
    
    url = 'https://api.z.ai/api/paas/v4/web_search'
    
    payload = {
        'search_engine': 'search-prime',
        'search_query': 'latest AI developments 2025',
        'count': 5,
        'search_domain_filter': '',
        'search_recency_filter': 'noLimit',
        'request_id': 'test_' + str(int(time.time())),
        'user_id': 'test_user'
    }
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        end_time = time.time()
        
        print(f'HTTP Status: {response.status_code}')
        print(f'Response Time: {response.elapsed.total_seconds():.2f}s')
        
        if response.status_code == 200:
            data = response.json()
            print(f'Request ID: {data.get("id", "N/A")}')
            print(f'Created: {data.get("created", "N/A")}')
            print(f'Results Found: {len(data.get("search_result", []))}')
            
            # Save full results to test_results folder
            with open('test_results/zai_websearch_raw.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print('\n=== SEARCH RESULTS ===')
            for i, result in enumerate(data.get('search_result', [])[:3], 1):
                print(f'\nResult {i}:')
                print(f'Title: {result.get("title", "N/A")}')
                print(f'Link: {result.get("link", "N/A")}')
                print(f'Media: {result.get("media", "N/A")}')
                print(f'Content Preview: {result.get("content", "N/A")[:150]}...')
                print(f'Publish Date: {result.get("publish_date", "N/A")}')
                
                # Save individual result to research folder
                with open(f'research/result_{i}.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            
            return data
        else:
            print(f'ERROR: {response.text}')
            return None
            
    except Exception as e:
        print(f'Exception occurred: {str(e)}')
        return None

def test_web_reader():
    print('\n\n=== Z.AI WEB READER TEST ===')
    
    url = 'https://api.z.ai/api/paas/v4/reader'
    
    payload = {
        'url': 'https://www.example.com'
    }
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f'HTTP Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            
            # Save reader results
            with open('test_results/zai_reader_raw.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f'Reader Results: {json.dumps(data, indent=2, ensure_ascii=False)}')
            return data
        else:
            print(f'ERROR: {response.text}')
            return None
            
    except Exception as e:
        print(f'Exception occurred: {str(e)}')
        return None

if __name__ == '__main__':
    # Test web search
    search_results = test_web_search()
    
    # Test web reader  
    reader_results = test_web_reader()
    
    print(f'\n\n=== SUMMARY ===')
    print(f'Web Search: {"SUCCESS" if search_results else "FAILED"}')
    print(f'Web Reader: {"SUCCESS" if reader_results else "FAILED"}')
    
    # Save summary
    summary = {
        'timestamp': time.time(),
        'web_search_success': search_results is not None,
        'web_reader_success': reader_results is not None,
        'api_key_present': bool(api_key),
        'test_completed': True
    }
    
    with open('test_results/api_test_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)