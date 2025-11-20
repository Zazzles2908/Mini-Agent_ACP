# Quick Fix Guide for Mini-Agent_ACP Issues

## 🚨 Most Common Issues & Quick Fixes

### 1. **"Retries 6 times and fails" - API Authentication Error**

**Cause:** API key not set or incorrect provider configuration

**Quick Fix:**
```bash
# Step 1: Set your API key
export MINIMAX_API_KEY="your_actual_api_key_here"

# Step 2: Verify the key is set
echo $MINIMAX_API_KEY

# Step 3: Test with diagnostic script
python3 comprehensive_diagnostic.py
```

### 2. **Configuration File Confusion**

**Cause:** Multiple config files with different settings

**Quick Fix:**
```bash
# Use the package config (recommended)
cp mini_agent/config/config.yaml config.yaml

# Or set your API key in existing .env file
echo "MINIMAX_API_KEY=your_key_here" >> .env
```

### 3. **VSCode Extension Not Working**

**Cause:** Extension not installed or wrong version

**Quick Fix:**
```bash
# Install the extension
code --install-extension mini-agent-acp-1.0.0.vsix

# Or manually in VSCode:
# 1. Ctrl+Shift+P -> "Extensions: Install from VSIX"
# 2. Select the .vsix file
# 3. Restart VSCode
```

### 4. **"command not found: mini-agent"**

**Cause:** Package not installed or path issues

**Quick Fix:**
```bash
# Install in development mode
pip install -e .

# Or run directly
python3 -m mini_agent.cli

# Or create an alias
alias mini-agent="python3 -m mini_agent.cli"
```

## 🔧 Step-by-Step Resolution Process

### Step 1: Run Diagnostics
```bash
python3 comprehensive_diagnostic.py
```

### Step 2: Fix Configuration Issues
Based on diagnostic output, fix these in order:

1. **Environment Variables**: Ensure `MINIMAX_API_KEY` is set
2. **Config Files**: Use only one config file (preferably `mini_agent/config/config.yaml`)
3. **Dependencies**: Install missing packages with `pip install -r requirements.txt`

### Step 3: Test CLI
```bash
# Simple test
echo "Hello, can you help me with a simple task?" | python3 -m mini_agent.cli

# Or interactive mode
python3 -m mini_agent.cli
```

### Step 4: Test VSCode Extension
```bash
# Check extension installation
code --list-extensions | grep mini-agent

# If not installed, install it
code --install-extension mini-agent-acp-1.0.0.vsix
```

## 🆘 Emergency Fixes

### Reset Everything
```bash
# 1. Clean install
pip uninstall mini-agent -y
pip install -e .

# 2. Reset configuration
rm -f config.yaml .env
cp mini_agent/config/config.yaml ./

# 3. Set environment
export MINIMAX_API_KEY="your_key_here"

# 4. Test
python3 comprehensive_diagnostic.py
```

### Alternative Config Setup
If you're having trouble with the main config, try using a simple approach:

```bash
# Create simple config
cat > config.yaml << EOF
api_key: "your_actual_api_key"
api_base: "https://api.minimax.io"
model: "MiniMax-M2"
provider: "openai"

retry:
  enabled: true
  max_retries: 3
  initial_delay: 1.0
  max_delay: 30.0
  exponential_base: 2.0

max_steps: 50
workspace_dir: "./workspace"
system_prompt_path: "system_prompt.md"

tools:
  enable_file_tools: true
  enable_bash: true
  enable_note: true
  enable_zai_search: false  # Disable if not using ZAI
  enable_skills: false      # Disable if not using skills
  enable_mcp: false         # Disable if not using MCP
  mcp_config_path: "mcp.json"
EOF
```

## 📋 Checklist for Working Setup

- [ ] Python packages installed: `pip install -r requirements.txt`
- [ ] API key set: `echo $MINIMAX_API_KEY`
- [ ] Configuration file exists and is valid
- [ ] CLI test works: `python3 -m mini_agent.cli` (should start without errors)
- [ ] VSCode extension installed and visible
- [ ] No import errors when running diagnostic script

## 🔍 Debug Commands

```bash
# Check Python path and imports
python3 -c "import sys; print('\n'.join(sys.path))"
python3 -c "import mini_agent; print('✅ mini_agent imported successfully')"

# Test configuration loading
python3 -c "
from mini_agent.config import Config
try:
    config = Config.from_yaml('mini_agent/config/config.yaml')
    print(f'✅ Config loaded: {config.llm.provider}')
except Exception as e:
    print(f'❌ Config error: {e}')
"

# Test LLM client
python3 -c "
import asyncio
from mini_agent.config import Config
from mini_agent.llm import LLMClient
from mini_agent.schema import LLMProvider, Message

async def test():
    config = Config.from_yaml('mini_agent/config/config.yaml')
    provider = LLMProvider.OPENAI
    client = LLMClient(
        api_key=config.llm.api_key,
        provider=provider,
        api_base=config.llm.api_base,
        model=config.llm.model,
    )
    
    msg = Message(role='user', content='Say hello')
    response = await client.generate(messages=[msg])
    print(f'✅ API test: {response.content[:50]}...')

asyncio.run(test())
"
```

## 📞 Getting Help

If issues persist:

1. **Run the diagnostic script** and save the output
2. **Check the GitHub issues** in the original repository
3. **Provide specific error messages** when asking for help
4. **Include your configuration** (with API keys masked)

Remember: The most common issue is simply missing or incorrect API key configuration!