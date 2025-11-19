#!/usr/bin/env python3
"""
Langfuse Setup and Configuration Script
Sets up Langfuse project and generates configuration
"""

import os
import json
import requests
from datetime import datetime

def check_langfuse_status():
    """Check if Langfuse is accessible"""
    
    print("=== CHECKING LANGFUSE STATUS ===")
    
    try:
        # Check if Langfuse is accessible
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("[OK] Langfuse is accessible at http://localhost:3000")
            return True
        else:
            print(f"[WARN] Langfuse returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Langfuse is not accessible: {e}")
        return False

def create_langfuse_config():
    """Create Langfuse configuration with placeholder API keys"""
    
    print("\n=== CREATING LANGFUSE CONFIGURATION ===")
    
    # Langfuse configuration template
    langfuse_config = {
        "langfuse": {
            "secret_key": "sk-lf-your-secret-key-here",
            "public_key": "pk-lf-your-public-key-here",
            "host": "http://localhost:3000"
        },
        "setup_instructions": {
            "step_1": "Access http://localhost:3000",
            "step_2": "Create a new project or use existing",
            "step_3": "Get your API keys from project settings",
            "step_4": "Replace the placeholder keys in this config",
            "step_5": "Update environment variables"
        },
        "test_endpoints": {
            "health_check": "http://localhost:3000/api/public/health",
            "projects": "http://localhost:3000/api/public/projects",
            "traces": "http://localhost:3000/api/public/traces"
        }
    }
    
    # Save configuration
    config_path = "langfuse_config.json"
    
    try:
        with open(config_path, 'w') as f:
            json.dump(langfuse_config, f, indent=2)
        print(f"[OK] Langfuse configuration saved to {config_path}")
        
        print("\nNext Steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Create a new project for Mini-Agent Observability")
        print("3. Get your API keys from project settings")
        print("4. Update langfuse_config.json with your actual keys")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not save configuration: {e}")
        return False

def create_production_config():
    """Create production environment configuration"""
    
    print("\n=== CREATING PRODUCTION CONFIG ===")
    
    # Production environment configuration
    env_config = {
        "development": {
            "LANGFUSE_SECRET_KEY": "sk-lf-dev-your-secret-key",
            "LANGFUSE_PUBLIC_KEY": "pk-lf-dev-your-public-key",
            "LANGFUSE_HOST": "http://localhost:3000"
        },
        "production": {
            "LANGFUSE_SECRET_KEY": "sk-lf-prod-your-secret-key",
            "LANGFUSE_PUBLIC_KEY": "pk-lf-prod-your-public-key",
            "LANGFUSE_HOST": "https://your-production-langfuse.com"
        }
    }
    
    # Save environment configuration
    env_path = "langfuse_env_config.json"
    
    try:
        with open(env_path, 'w') as f:
            json.dump(env_config, f, indent=2)
        print(f"[OK] Environment configuration saved to {env_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not save environment config: {e}")
        return False

def create_dashboard_config():
    """Create Langfuse dashboard configuration for Mini-Agent monitoring"""
    
    print("\n=== CREATING DASHBOARD CONFIG ===")
    
    dashboard_config = {
        "mini_agent_dashboard": {
            "name": "Mini-Agent Observability Dashboard",
            "description": "Comprehensive monitoring dashboard for Mini-Agent activities",
            "charts": {
                "tool_execution_timeline": {
                    "type": "timeline",
                    "data_source": "agent_tool_executions",
                    "metrics": ["duration_ms", "success_rate"],
                    "filters": {"category": ["file", "mcp", "core"]}
                },
                "performance_metrics": {
                    "type": "line_chart",
                    "data_source": "agent_performance_metrics",
                    "metrics": ["latency", "memory_usage", "cpu_usage"],
                    "time_range": "24h"
                },
                "error_analysis": {
                    "type": "pie_chart",
                    "data_source": "agent_tool_executions",
                    "metrics": ["error_count_by_tool"],
                    "filters": {"success": False}
                },
                "session_overview": {
                    "type": "summary",
                    "data_source": "agent_traces",
                    "metrics": ["total_sessions", "avg_session_duration", "success_rate"]
                },
                "agent_decisions": {
                    "type": "table",
                    "data_source": "agent_decisions",
                    "columns": ["decision_type", "selected_option", "confidence_score", "reasoning"]
                }
            },
            "alerts": {
                "high_latency": {
                    "condition": "duration_ms > 5000",
                    "message": "High latency detected in tool execution",
                    "severity": "warning"
                },
                "error_rate": {
                    "condition": "error_rate > 10%",
                    "message": "High error rate in agent operations",
                    "severity": "critical"
                },
                "memory_usage": {
                    "condition": "memory_usage > 1024",
                    "message": "High memory usage detected",
                    "severity": "warning"
                }
            }
        }
    }
    
    # Save dashboard configuration
    dashboard_path = "langfuse_dashboard_config.json"
    
    try:
        with open(dashboard_path, 'w') as f:
            json.dump(dashboard_config, f, indent=2)
        print(f"[OK] Dashboard configuration saved to {dashboard_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not save dashboard config: {e}")
        return False

def create_test_endpoints():
    """Create test endpoints for Langfuse integration"""
    
    print("\n=== CREATING TEST ENDPOINTS ===")
    
    test_script = '''#!/usr/bin/env python3
"""
Langfuse Integration Test
Tests the connection between Mini-Agent and Langfuse
"""

import os
import requests
import json
from datetime import datetime

def test_langfuse_api():
    """Test Langfuse API endpoints"""
    
    print("Testing Langfuse API integration...")
    
    # Test health check
    try:
        response = requests.get("http://localhost:3000/api/public/health")
        if response.status_code == 200:
            print("[OK] Langfuse health check passed")
        else:
            print(f"[WARN] Health check returned: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
    
    # Test creating a trace (this requires proper API keys)
    trace_data = {
        "name": "Test Trace",
        "input": {"test": True},
        "metadata": {"source": "integration_test"}
    }
    
    try:
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "http://localhost:3000/api/public/traces",
            json=trace_data,
            headers=headers
        )
        
        if response.status_code == 200:
            print("[OK] Test trace creation passed")
        else:
            print(f"[WARN] Trace creation returned: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"[WARN] Trace creation test failed (expected without API keys): {e}")

if __name__ == "__main__":
    test_langfuse_api()
'''
    
    # Save test script
    test_path = "test_langfuse_integration.py"
    
    try:
        with open(test_path, 'w') as f:
            f.write(test_script)
        print(f"[OK] Test script saved to {test_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not save test script: {e}")
        return False

def main():
    """Main setup function"""
    
    print("LANGFUSE SETUP AND CONFIGURATION")
    print("=" * 50)
    print(f"Setup Time: {datetime.now()}")
    print()
    
    # Check Langfuse status
    langfuse_ok = check_langfuse_status()
    
    if not langfuse_ok:
        print("\n[ERROR] Langfuse is not accessible. Please ensure:")
        print("1. Docker stack is running: docker-compose up -d")
        print("2. Port 3000 is not blocked")
        print("3. Langfuse service is healthy")
        return False
    
    # Create configurations
    config_ok = create_langfuse_config()
    env_ok = create_production_config()
    dashboard_ok = create_dashboard_config()
    test_ok = create_test_endpoints()
    
    # Final summary
    print("\n" + "=" * 50)
    print("LANGFUSE SETUP SUMMARY")
    print("=" * 50)
    
    if all([config_ok, env_ok, dashboard_ok, test_ok]):
        print("[SUCCESS] All Langfuse configuration files created!")
        print("\nFiles created:")
        print("- langfuse_config.json (API key configuration)")
        print("- langfuse_env_config.json (Environment variables)")
        print("- langfuse_dashboard_config.json (Dashboard layout)")
        print("- test_langfuse_integration.py (Integration test)")
        
        print("\nNext Steps:")
        print("1. Access http://localhost:3000")
        print("2. Create a Mini-Agent Observability project")
        print("3. Get API keys from project settings")
        print("4. Update langfuse_config.json with real keys")
        print("5. Set environment variables")
        print("6. Run integration test: python test_langfuse_integration.py")
        
        return True
    else:
        print("[ERROR] Some configuration files could not be created")
        return False

if __name__ == "__main__":
    main()
