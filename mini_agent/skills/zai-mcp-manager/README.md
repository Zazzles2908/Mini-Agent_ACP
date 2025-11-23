# Z.AI MCP Manager Skill

> **Comprehensive management tool for Z.AI MCP servers with quota tracking, health monitoring, and configuration validation**

## 🎯 Overview

The Z.AI MCP Manager skill provides complete management capabilities for Z.AI MCP servers, ensuring optimal usage of the FREE Z.AI Lite Plan (100 searches + 100 readers) while providing advanced monitoring and analytics.

## ✨ Features

- **🔍 Quota Monitoring**: Real-time tracking of search and reader usage with intelligent alerts
- **🏥 Health Checking**: Comprehensive connectivity and performance monitoring
- **⚙️ Configuration Validation**: Automated setup validation and error detection
- **📊 Usage Analytics**: Detailed reports and optimization recommendations
- **🛠️ Management Tools**: Scripts for configuration generation and maintenance
- **🔐 Security Best Practices**: API key validation and secure configuration

## 🚀 Quick Start

### 1. Validate Your Setup
```bash
python scripts/config_validator.py
```

### 2. Check Health Status
```bash
python scripts/health_checker.py
```

### 3. Monitor Quota Usage
```bash
python scripts/quota_monitor.py
```

### 4. Generate Configuration Templates
```bash
python scripts/config_template_generator.py
```

## 📁 Skill Structure

```
zai-mcp-manager/
├── SKILL.md                     # Comprehensive skill documentation
├── scripts/
│   ├── quota_monitor.py         # Real-time quota tracking
│   ├── health_checker.py        # Connectivity and performance tests
│   ├── config_validator.py      # Configuration validation
│   └── config_template_generator.py  # Generate optimized configs
└── README.md                    # This file
```

## 🛠️ Available Scripts

### Quota Monitor (`quota_monitor.py`)
**Real-time quota tracking and alerting**

```python
from zai_mcp_manager.scripts.quota_monitor import ZAIMCPQuotaMonitor

monitor = ZAIMCPQuotaMonitor()
status = await monitor.check_quota_status()
report = await monitor.generate_quota_report()
```

**Features:**
- ✅ Real-time quota status
- ✅ Usage alerts at 80% and 95%
- ✅ Usage analytics and trends
- ✅ JSON and markdown reports

### Health Checker (`health_checker.py`)
**Comprehensive endpoint health monitoring**

```python
from zai_mcp_manager.scripts.health_checker import ZAIMCPHealthChecker

checker = ZAIMCPHealthChecker()
health_status = await checker.check_all_endpoints()
```

**Features:**
- ✅ Connectivity testing
- ✅ Response time monitoring
- ✅ Performance scoring (0-100)
- ✅ Error detection and reporting

### Configuration Validator (`config_validator.py`)
**Automated configuration validation**

```python
from zai_mcp_manager.scripts.config_validator import ZAIMCPConfigurationValidator

validator = ZAIMCPConfigurationValidator()
report = await validator.validate_configuration()
```

**Features:**
- ✅ File existence checks
- ✅ API key validation
- ✅ Endpoint verification
- ✅ Security assessment
- ✅ Configuration scoring (0-100)

### Template Generator (`config_template_generator.py`)
**Generate optimized configuration templates**

```python
from zai_mcp_manager.scripts.config_template_generator import generate_all_templates

generated_files = generate_all_templates("./zai_config")
```

**Generated Files:**
- ✅ `.mcp.json` - Optimized MCP server configuration
- ✅ `.env.template` - Environment variables template
- ✅ `zai_mcp_client.py` - Python client code template
- ✅ `zai_integration_guide.md` - Mini-Agent integration guide

## 📊 Monitoring Dashboard

Create a monitoring dashboard by combining multiple scripts:

```python
import asyncio
from zai_mcp_manager.scripts.quota_monitor import ZAIMCPQuotaMonitor
from zai_mcp_manager.scripts.health_checker import ZAIMCPHealthChecker
from zai_mcp_manager.scripts.config_validator import ZAIMCPConfigurationValidator

async def generate_dashboard():
    """Generate comprehensive monitoring dashboard"""
    
    # Get quota status
    monitor = ZAIMCPQuotaMonitor()
    quota_status = await monitor.check_quota_status()
    
    # Get health status
    checker = ZAIMCPHealthChecker()
    health_status = await checker.check_all_endpoints()
    
    # Get configuration status
    validator = ZAIMCPConfigurationValidator()
    config_status = await validator.validate_configuration()
    
    # Generate combined report
    print("=== Z.AI MCP DASHBOARD ===")
    print(f"Overall Health: {health_status.overall_status}")
    print(f"Config Score: {config_status.overall_score}/100")
    print(f"Quota Usage: {quota_status.usage_percentage}%")
    print("===========================")

asyncio.run(generate_dashboard())
```

## 🔍 Validation Categories

The configuration validator checks:

### File Structure
- ✅ Required files exist (`.env`, `.mcp.json`)
- ✅ Recommended files present
- ✅ Proper file permissions

### Environment Configuration
- ✅ ZAI_API_KEY format and validity
- ✅ Environment variable accessibility

### MCP Configuration
- ✅ Server definitions and endpoints
- ✅ Authentication headers
- ✅ Timeout and retry settings
- ✅ JSON syntax validation

### Connectivity
- ✅ API endpoint accessibility
- ✅ Authentication verification
- ✅ Response format validation

### Security
- ✅ API key protection
- ✅ Secure file permissions
- ✅ HTTPS enforcement

## 📈 Quota Management

### Understanding Quotas
The Z.AI Lite Plan includes:
- **100 Web Searches** per month
- **100 Web Readers** per month
- **Reset:** Monthly cycle
- **Warnings:** 80% and 95% usage thresholds

### Optimization Strategies
1. **Batch Operations**: Group similar requests
2. **Caching**: Store results for repeated queries
3. **Smart Filtering**: Use specific search terms
4. **Strategic Timing**: Plan usage around renewal

### Alert System
- **80% Warning**: "Quota approaching limit"
- **95% Critical**: "Quota nearly exhausted"
- **100% Blocked**: Operations disabled

## 🔧 Integration Examples

### With Mini-Agent
The Z.AI MCP Manager integrates seamlessly with your existing Mini-Agent setup:

```python
# Your existing Z.AI tools already work with MCP manager
from mini_agent.tools.zai_web_tool import ZAIWebTool

# Add monitoring
from zai_mcp_manager.scripts.quota_monitor import ZAIMCPQuotaMonitor

tool = ZAIWebTool()
monitor = ZAIMCPQuotaMonitor()

# Check status before operations
quota_status = await monitor.check_quota_status()
if quota_status.status == "critical":
    print("⚠️ Quota nearly exhausted")
    # Implement fallback strategy
```

### Standalone Usage
Use the MCP manager independently of Mini-Agent:

```python
import asyncio
from zai_mcp_manager.scripts.quota_monitor import ZAIMCPQuotaMonitor

async def standalone_usage():
    monitor = ZAIMCPQuotaMonitor()
    
    # Check quota status
    status = await monitor.check_quota_status()
    print(f"Searches: {status.searches_used}/{status.searches_total}")
    print(f"Readers: {status.readers_used}/{status.readers_total}")
    
    # Generate usage report
    report = await monitor.generate_quota_report()
    print(report)

asyncio.run(standalone_usage())
```

## 🚨 Troubleshooting

### Common Issues

**API Key Invalid**
```bash
Error: Authentication failed - API key invalid
```
**Solution**: Verify your ZAI_API_KEY in `.env` file

**Quota Exhausted**
```bash
Error: Search quota exceeded (100/100)
```
**Solution**: Wait for monthly reset or upgrade plan

**Connection Timeout**
```bash
Error: Connection timeout
```
**Solution**: Check network connectivity and try again

### Debug Commands
```bash
# Validate setup
python scripts/config_validator.py

# Test connectivity
python scripts/health_checker.py

# Check quota usage
python scripts/quota_monitor.py
```

## 🎓 Best Practices

### Configuration
- ✅ Keep API keys in environment variables only
- ✅ Use version control for configuration templates
- ✅ Validate configuration before deployment

### Monitoring
- ✅ Set up automated health checks
- ✅ Monitor quota usage daily
- ✅ Configure alerts for quota exhaustion

### Security
- ✅ Never commit API keys to version control
- ✅ Rotate API keys regularly
- ✅ Use HTTPS for all communications

### Performance
- ✅ Implement retry logic with exponential backoff
- ✅ Cache frequently accessed data
- ✅ Use batch operations when possible

## 📚 Additional Resources

- **Z.AI Documentation**: https://docs.z.ai/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Mini-Agent Guide**: See project documentation
- **API Limits**: Check your Z.AI account dashboard

## 🤝 Contributing

This skill is part of the Mini-Agent ecosystem. To improve it:

1. Test thoroughly in your environment
2. Report issues through Mini-Agent channels
3. Share optimization strategies
4. Contribute to the documentation

## 📄 License

Part of the Mini-Agent project. See project license for details.

---

**🎯 Ready to optimize your Z.AI MCP usage? Start with `python scripts/config_validator.py`!**
