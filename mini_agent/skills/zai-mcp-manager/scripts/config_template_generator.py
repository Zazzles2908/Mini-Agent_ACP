#!/usr/bin/env python3
"""
Z.AI MCP Configuration Template Generator
Generate optimized configuration templates for Z.AI MCP servers
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class ZAIMCPTemplateGenerator:
    """Generate optimized configuration templates for Z.AI MCP"""
    
    def __init__(self):
        self.api_key = os.getenv('ZAI_API_KEY', '${ZAI_API_KEY}')
    
    def generate_mcp_config_template(self) -> Dict[str, Any]:
        """Generate comprehensive MCP configuration template"""
        return {
            "mcpServers": {
                "zai-web-search": {
                    "command": "remote",
                    "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
                    "headers": {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"
                    },
                    "timeout": 30,
                    "retry": {
                        "max_retries": 3,
                        "initial_delay": 1.0,
                        "backoff_factor": 2.0
                    },
                    "quotas": {
                        "daily_limit": 100,
                        "monthly_limit": 100,
                        "warnings": [80, 95],
                        "reset_period": "monthly"
                    },
                    "features": {
                        "response_format": "markdown",
                        "max_results": 5,
                        "include_snippets": True,
                        "timeout_behavior": "graceful_degradation"
                    }
                },
                "zai-web-reader": {
                    "command": "remote",
                    "url": "https://api.z.ai/api/mcp/web_reader/mcp",
                    "headers": {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"
                    },
                    "timeout": 45,
                    "retry": {
                        "max_retries": 3,
                        "initial_delay": 2.0,
                        "backoff_factor": 1.5
                    },
                    "quotas": {
                        "daily_limit": 100,
                        "monthly_limit": 100,
                        "warnings": [80, 95],
                        "reset_period": "monthly"
                    },
                    "features": {
                        "response_format": "markdown",
                        "extract_links": True,
                        "content_length_limit": 25000,
                        "timeout_behavior": "graceful_degradation"
                    }
                }
            },
            "monitoring": {
                "health_check_interval": 300,  # 5 minutes
                "quota_check_interval": 3600,  # 1 hour
                "alert_channels": ["console", "log"],
                "performance_tracking": True
            },
            "security": {
                "enable_api_key_validation": True,
                "log_api_calls": True,
                "rate_limit_per_minute": 60,
                "require_https": True
            },
            "optimization": {
                "enable_caching": True,
                "cache_ttl": 300,  # 5 minutes
                "batch_operations": True,
                "parallel_requests": False
            },
            "fallback": {
                "enable_fallback": True,
                "fallback_timeout": 10,
                "fallback_methods": ["direct_api", "alternative_search"]
            }
        }
    
    def generate_env_template(self) -> str:
        """Generate .env file template"""
        return f"""# Z.AI MCP Configuration
# This file contains your API keys and configuration

# Z.AI API Key (REQUIRED)
# Get your API key from: https://console.z.ai/
ZAI_API_KEY=your_api_key_here

# MCP Server Configuration (OPTIONAL)
# Override default timeout settings
ZAI_SEARCH_TIMEOUT=30
ZAI_READER_TIMEOUT=45

# Quota Settings (OPTIONAL)
# Adjust quota limits based on your plan
ZAI_SEARCH_QUOTA_LIMIT=100
ZAI_READER_QUOTA_LIMIT=100

# Monitoring Settings (OPTIONAL)
# Enable/disable monitoring features
ZAI_ENABLE_MONITORING=true
ZAI_HEALTH_CHECK_INTERVAL=300

# Security Settings (OPTIONAL)
# API key validation and logging
ZAI_REQUIRE_HTTPS=true
ZAI_LOG_API_CALLS=true

# Optimization Settings (OPTIONAL)
# Performance tuning
ZAI_ENABLE_CACHING=true
ZAI_CACHE_TTL=300
ZAI_ENABLE_BATCH_OPERATIONS=true
"""
    
    def generate_python_client_template(self) -> str:
        """Generate Python client code template"""
        return '''#!/usr/bin/env python3
"""
Z.AI MCP Client Template
Template for using Z.AI MCP servers in Python applications
"""

import os
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List


class ZAIMCPClient:
    """Z.AI MCP client for web search and reading operations"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        if not self.api_key:
            raise ValueError("ZAI_API_KEY not found in environment or provided")
        
        # Configuration
        self.search_endpoint = "https://api.z.ai/api/mcp/web_search_prime/mcp"
        self.reader_endpoint = "https://api.z.ai/api/mcp/web_reader/mcp"
        
        # Quota tracking
        self.search_quota_used = 0
        self.reader_quota_used = 0
        self.quota_limit = 100  # Lite plan limit
        
        # Session management
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
    
    def _check_quota(self, operation_type: str) -> bool:
        """Check if quota is available for the operation"""
        if operation_type == "search":
            return self.search_quota_used < self.quota_limit
        elif operation_type == "reader":
            return self.reader_quota_used < self.quota_limit
        return False
    
    async def search(self, query: str, max_results: int = 3, 
                   response_format: str = "markdown") -> Dict[str, Any]:
        """
        Perform web search using Z.AI MCP
        
        Args:
            query: Search query
            max_results: Number of results (1-5)
            response_format: "markdown" or "json"
        
        Returns:
            Search results dictionary
        """
        if not self._check_quota("search"):
            return {
                "success": False,
                "error": "Search quota exceeded",
                "quota_used": self.search_quota_used,
                "quota_limit": self.quota_limit
            }
        
        try:
            mcp_request = {
                "method": "tools/call",
                "params": {
                    "name": "webSearchPrime",
                    "arguments": {
                        "query": query,
                        "max_results": min(max_results, 5),
                        "format": response_format
                    }
                }
            }
            
            async with self.session.post(
                self.search_endpoint,
                headers=self._get_headers(),
                json=mcp_request,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.search_quota_used += 1
                    
                    return {
                        "success": True,
                        "data": result,
                        "quota_used": self.search_quota_used,
                        "quota_remaining": self.quota_limit - self.search_quota_used,
                        "method": "mcp"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"Search failed: {response.status} - {error_text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Search request failed: {str(e)}"
            }
    
    async def read_url(self, url: str, extract_links: bool = True, 
                      response_format: str = "markdown") -> Dict[str, Any]:
        """
        Read content from a URL using Z.AI MCP
        
        Args:
            url: URL to read
            extract_links: Whether to extract links
            response_format: "markdown" or "json"
        
        Returns:
            Page content and metadata
        """
        if not self._check_quota("reader"):
            return {
                "success": False,
                "error": "Reader quota exceeded",
                "quota_used": self.reader_quota_used,
                "quota_limit": self.quota_limit
            }
        
        try:
            mcp_request = {
                "method": "tools/call",
                "params": {
                    "name": "webReader",
                    "arguments": {
                        "url": url,
                        "extract_links": extract_links,
                        "format": response_format
                    }
                }
            }
            
            async with self.session.post(
                self.reader_endpoint,
                headers=self._get_headers(),
                json=mcp_request,
                timeout=aiohttp.ClientTimeout(total=45)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.reader_quota_used += 1
                    
                    return {
                        "success": True,
                        "data": result,
                        "quota_used": self.reader_quota_used,
                        "quota_remaining": self.quota_limit - self.reader_quota_used,
                        "method": "mcp"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"Reader failed: {response.status} - {error_text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Reader request failed: {str(e)}"
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on both endpoints"""
        results = {}
        
        # Test search endpoint
        try:
            async with self.session.get(
                self.search_endpoint,
                headers=self._get_headers(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                results["search_endpoint"] = {
                    "accessible": response.status == 200,
                    "status_code": response.status,
                    "response_time": "< 10s"
                }
        except Exception as e:
            results["search_endpoint"] = {
                "accessible": False,
                "error": str(e)
            }
        
        # Test reader endpoint
        try:
            async with self.session.get(
                self.reader_endpoint,
                headers=self._get_headers(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                results["reader_endpoint"] = {
                    "accessible": response.status == 200,
                    "status_code": response.status,
                    "response_time": "< 10s"
                }
        except Exception as e:
            results["reader_endpoint"] = {
                "accessible": False,
                "error": str(e)
            }
        
        return results
    
    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota status"""
        return {
            "search": {
                "used": self.search_quota_used,
                "remaining": self.quota_limit - self.search_quota_used,
                "limit": self.quota_limit,
                "percentage": (self.search_quota_used / self.quota_limit) * 100
            },
            "reader": {
                "used": self.reader_quota_used,
                "remaining": self.quota_limit - self.reader_quota_used,
                "limit": self.quota_limit,
                "percentage": (self.reader_quota_used / self.quota_limit) * 100
            },
            "total": {
                "used": self.search_quota_used + self.reader_quota_used,
                "remaining": (self.quota_limit * 2) - (self.search_quota_used + self.reader_quota_used),
                "limit": self.quota_limit * 2,
                "percentage": ((self.search_quota_used + self.reader_quota_used) / (self.quota_limit * 2)) * 100
            }
        }


# Example usage
async def example_usage():
    """Example of how to use the Z.AI MCP client"""
    
    async with ZAIMCPClient() as client:
        # Check quota status
        quota_status = client.get_quota_status()
        print(f"Quota Status: {quota_status}")
        
        # Perform search
        search_result = await client.search(
            query="Mini-Agent AI assistant features",
            max_results=3
        )
        print(f"Search Result: {search_result}")
        
        # Read content from first result
        if search_result["success"] and "urls" in search_result["data"]:
            first_url = search_result["data"]["urls"][0] if search_result["data"]["urls"] else None
            if first_url:
                content_result = await client.read_url(first_url)
                print(f"Content Result: {content_result}")
        
        # Health check
        health_status = await client.health_check()
        print(f"Health Status: {health_status}")


if __name__ == "__main__":
    asyncio.run(example_usage())
'''
    
    def generate_mini_agent_integration_template(self) -> str:
        """Generate Mini-Agent integration template"""
        return '''# Z.AI MCP Integration for Mini-Agent

This template shows how to integrate Z.AI MCP servers with the Mini-Agent system.

## 1. Configuration Files

### `.mcp.json`
```json
{
  "mcpServers": {
    "zai-web-search": {
      "command": "remote",
      "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
      "headers": {
        "Authorization": "Bearer ${ZAI_API_KEY}"
      },
      "timeout": 30,
      "retry": {
        "max_retries": 3,
        "initial_delay": 1.0
      }
    },
    "zai-web-reader": {
      "command": "remote", 
      "url": "https://api.z.ai/api/mcp/web_reader/mcp",
      "headers": {
        "Authorization": "Bearer ${ZAI_API_KEY}"
      },
      "timeout": 45,
      "retry": {
        "max_retries": 3,
        "initial_delay": 1.0
      }
    }
  }
}
```

### `.env`
```
ZAI_API_KEY=your_api_key_here
```

## 2. Tool Integration

### Existing Z.AI Tool (`mini_agent/tools/zai_web_tool.py`)
The Mini-Agent already has comprehensive Z.AI integration with:
- MCP-first approach (FREE quotas)
- Direct API fallback (credit protected)
- Quota tracking and usage monitoring
- Intelligent error handling

### Adding New Z.AI MCP Tools

```python
from mini_agent.tools.base import Tool, ToolResult

class ZAIMCPTool(Tool):
    """Template for creating new Z.AI MCP tools"""
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv('ZAI_API_KEY')
        self.available = bool(self.api_key)
    
    @property
    def name(self) -> str:
        return "zai_mcp_tool"
    
    @property
    def description(self) -> str:
        return "Description of your Z.AI MCP tool"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Your query description"
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, **kwargs) -> ToolResult:
        """Execute tool with Z.AI MCP integration"""
        if not self.available:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI API key not configured"
            )
        
        try:
            # Use Z.AI MCP protocol
            result = await self._call_mcp_tool(kwargs)
            
            return ToolResult(
                success=result["success"],
                content=result.get("content", ""),
                error=result.get("error")
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"Tool execution failed: {str(e)}"
            )
    
    async def _call_mcp_tool(self, params: dict) -> dict:
        """Make MCP call to Z.AI endpoint"""
        # Implementation details...
        pass
```

## 3. MCP Server Loader Integration

The Mini-Agent system already includes MCP loader functionality in `mini_agent/tools/mcp_loader.py`. To use it:

```python
# Load MCP tools automatically
async def load_zai_mcp_tools():
    tools = await load_mcp_tools_async("mcp.json")
    return tools

# The MCP loader will automatically:
# 1. Read .mcp.json configuration
# 2. Connect to Z.AI MCP endpoints
# 3. Load available tools as Tool objects
# 4. Handle error recovery and cleanup
```

## 4. Monitoring and Analytics

### Quota Monitoring
```python
from zai_mcp_manager.scripts.quota_monitor import ZAIMCPQuotaMonitor

monitor = ZAIMCPQuotaMonitor()
quota_status = await monitor.check_quota_status()
```

### Health Checking
```python
from zai_mcp_manager.scripts.health_checker import ZAIMCPHealthChecker

checker = ZAIMCPHealthChecker()
health_status = await checker.check_all_endpoints()
```

### Configuration Validation
```python
from zai_mcp_manager.scripts.config_validator import ZAIMCPConfigurationValidator

validator = ZAIMCPConfigurationValidator()
report = await validator.validate_configuration()
```

## 5. Best Practices

### Quota Management
- Monitor usage with the quota monitor script
- Set up alerts for quota exhaustion (80% and 95% thresholds)
- Use batching for multiple similar operations
- Cache results when appropriate

### Error Handling
- Always implement retry logic with exponential backoff
- Provide graceful degradation when quotas are exhausted
- Log all MCP calls for debugging
- Monitor error rates and patterns

### Security
- Store API keys in environment variables only
- Never commit API keys to version control
- Validate all API responses before processing
- Use HTTPS for all API communications

### Performance
- Use async/await for all network operations
- Implement proper timeout handling
- Cache frequently accessed data
- Monitor response times and optimize accordingly

## 6. Deployment

### Environment Setup
1. Copy `.env` template and add your API key
2. Copy `.mcp.json` configuration to your project root
3. Install required dependencies: `aiohttp`
4. Test configuration with validation script

### Health Monitoring
1. Set up scheduled health checks (every 5 minutes)
2. Configure quota monitoring alerts
3. Log all operations for debugging
4. Set up failure notifications

### Scaling Considerations
- The Lite Plan has 100 searches + 100 readers per month
- For higher usage, consider upgrading to paid plans
- Implement caching to reduce API calls
- Use batch operations when possible
'''

    def generate_configuration_report(self, config: Dict[str, Any]) -> str:
        """Generate a configuration report"""
        return f"""# Z.AI MCP Configuration Generated
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files Generated

1. **Z.AI MCP Configuration** - `.mcp.json`
2. **Environment Template** - `.env.template`
3. **Python Client Template** - `zai_mcp_client.py`
4. **Mini-Agent Integration** - `zai_integration_guide.md`

## Next Steps

1. **Set up API key:**
   - Copy `.env.template` to `.env`
   - Add your Z.AI API key

2. **Validate configuration:**
   ```bash
   python mini_agent/skills/zai-mcp-manager/scripts/config_validator.py
   ```

3. **Test connectivity:**
   ```bash
   python mini_agent/skills/zai-mcp-manager/scripts/health_checker.py
   ```

4. **Monitor quota usage:**
   ```bash
   python mini_agent/skills/zai-mcp-manager/scripts/quota_monitor.py
   ```

5. **Integrate with Mini-Agent:**
   - Copy the generated `.mcp.json` to your project
   - Follow the integration guide in `zai_integration_guide.md`

## Features Included

- ✅ MCP server configuration for search and reader
- ✅ Proper authentication and headers
- ✅ Retry logic and timeout handling
- ✅ Quota tracking and monitoring
- ✅ Health checking and monitoring
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Fallback mechanisms

## Support

For issues or questions:
1. Check the validation reports
2. Review the health check results
3. Monitor quota usage
4. Consult Mini-Agent documentation
"""


def generate_all_templates(output_dir: str = ".") -> List[str]:
    """Generate all configuration templates"""
    generator = ZAIMCPTemplateGenerator()
    generated_files = []
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate .mcp.json template
    config = generator.generate_mcp_config_template()
    config_file = Path(output_dir) / "zai_mcp_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    generated_files.append(str(config_file))
    
    # Generate .env template
    env_content = generator.generate_env_template()
    env_file = Path(output_dir) / ".env.template"
    with open(env_file, 'w') as f:
        f.write(env_content)
    generated_files.append(str(env_file))
    
    # Generate Python client template
    client_content = generator.generate_python_client_template()
    client_file = Path(output_dir) / "zai_mcp_client.py"
    with open(client_file, 'w') as f:
        f.write(client_content)
    generated_files.append(str(client_file))
    
    # Generate integration guide
    integration_content = generator.generate_mini_agent_integration_template()
    integration_file = Path(output_dir) / "zai_integration_guide.md"
    with open(integration_file, 'w') as f:
        f.write(integration_content)
    generated_files.append(str(integration_file))
    
    # Generate report
    report_content = generator.generate_configuration_report(config)
    report_file = Path(output_dir) / "zai_mcp_generation_report.md"
    with open(report_file, 'w') as f:
        f.write(report_content)
    generated_files.append(str(report_file))
    
    return generated_files


def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Z.AI MCP configuration templates")
    parser.add_argument(
        "--output-dir", 
        default=".", 
        help="Output directory for generated files (default: current directory)"
    )
    
    args = parser.parse_args()
    
    generated_files = generate_all_templates(args.output_dir)
    
    print(f"Generated {len(generated_files)} files in {args.output_dir}:")
    for file_path in generated_files:
        print(f"  - {file_path}")
    
    print("\nNext steps:")
    print("1. Review the generated files")
    print("2. Copy .env.template to .env and add your API key")
    print("3. Validate configuration with config_validator.py")
    print("4. Test connectivity with health_checker.py")


if __name__ == "__main__":
    main()
