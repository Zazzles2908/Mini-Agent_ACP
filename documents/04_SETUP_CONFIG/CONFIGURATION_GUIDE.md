# 🎯 Mini-Agent Configuration & System Architecture

## 📁 **Configuration Files Location**

### **Primary Configuration Directory**
```
C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\
├── config.yaml          # Main configuration (LLM, tools, agent settings)
├── .mcp.json             # MCP server configuration  
├── system_prompt.md     # System prompt for the agent
└── config-example.yaml  # Example/template configuration
```

### **Environment Configuration**
```
C:\Users\Jazeel-Home\Mini-Agent\
├── .env                 # Environment variables (ZAI_API_KEY, etc.)
└── pyproject.toml       # Project dependencies and settings
```

---

## 🔧 **How the System Works Now**

### **1. Launch Sequence**
```bash
python launch_mini_agent.py --workspace .
```

**What happens:**
1. **`launch_mini_agent.py`** sets up Python paths correctly
2. Loads environment variables from `.env`
3. Imports and runs `mini_agent.cli.main()`
4. Loads configuration from `mini_agent/config/`

### **2. Configuration Loading Flow**
```
1. CLI loads config.py
2. config.yaml → parsed for LLM/provider settings  
3. .mcp.json → parsed for MCP server configurations
4. .env → provides ZAI_API_KEY and other environment variables
5. All settings combined into unified configuration
```

### **3. Tool Registration**
Based on `config.yaml` settings:
- **File Tools**: `enable_file_tools: true` → ReadTool, WriteTool, EditTool
- **Bash Tool**: `enable_bash: true` → BashTool + Kill/Output tools
- **Z.AI Tools**: `enable_zai_search: true` → zai_web_search, zai_web_reader
- **MCP Tools**: `enable_mcp: true` → Load servers from .mcp.json
- **Skills**: `enable_skills: true` → Load all skills from mini_agent/skills/

---

## 📋 **Current Configuration Files (Live)**

### **`config.yaml` (Mini-Agent Settings)**
```yaml
# LLM Configuration
api_key: "eyJhbGciOiJSUzI1NiIs..."  # MiniMax API key
api_base: "https://api.minimax.io"
model: "MiniMax-M2"
provider: "anthropic"

# Agent Configuration  
max_steps: 200
workspace_dir: "./workspace"

# Tools Configuration
tools:
  enable_file_tools: true    # File operations
  enable_bash: true         # Bash commands
  enable_zai_search: true   # Native Z.AI web search
  enable_skills: true       # Skills system
  enable_mcp: true          # MCP tools
  mcp_config_path: ".mcp.json"
```

### **`mcp.json` (MCP Servers)**
```json
{
  "mcpServers": {
    "memory": { 
      "command": "npx -y @modelcontextprotocol/server-memory",
      "disabled": false 
    },
    "filesystem": {
      "command": "npx -y @modelcontextprotocol/server-filesystem C:\\Users\\Jazeel-Home\\Mini-Agent",
      "disabled": false 
    },
    "git": {
      "command": "python -m mcp_server_git", 
      "disabled": false 
    }
  },
  "_note": "minimax_search removed - using Z.AI instead"
}
```

### **`.env` (Environment Variables)**
```
ZAI_API_KEY=7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe
```

---

## 🚀 **What Gets Loaded When You Start**

### **39+ Tools Available:**
1. **File Tools** (3): ReadTool, WriteTool, EditTool
2. **Bash Tools** (3): BashTool, BashKillTool, BashOutputTool  
3. **Z.AI Tools** (2): zai_web_search, zai_web_reader
4. **MCP Tools** (Varies): Based on .mcp.json servers
5. **Skills** (10+): Document skills, specialized tools
6. **Session Tools** (1): SessionNoteTool

### **Configuration Sources:**
1. **`.env`** → ZAI_API_KEY, other environment variables
2. **`config.yaml`** → LLM settings, tool toggles, agent behavior
3. **`.mcp.json`** → External MCP server configurations
4. **`pyproject.toml`** → Python dependencies
5. **`mini_agent/skills/`** → Built-in skills (all enabled)

---

## ⚙️ **Configuration Priority Order**

According to `config.yaml` comments:
1. **`mini_agent/config/config.yaml`** ← Development mode (current)
2. **`~/.mini-agent/config/config.yaml`** ← User config directory  
3. **`<package>/mini_agent/config/config.yaml`** ← Package installation

**Current setup uses #1** (development mode in the same directory)

---

## 🔧 **How to Modify Configuration**

### **Change LLM Settings:**
Edit `mini_agent/config/config.yaml`:
```yaml
api_base: "https://api.minimax.io"  # Change if needed
model: "MiniMax-M2"                # Change model if needed
```

### **Toggle Tools:**
Edit `mini_agent/config/config.yaml`:
```yaml
tools:
  enable_zai_search: true/false    # Enable/disable web search
  enable_skills: true/false        # Enable/disable skills
  enable_mcp: true/false           # Enable/disable MCP tools
```

### **Add/Remove MCP Servers:**
Edit `mini_agent/config/.mcp.json`:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "your-command",
      "args": ["your", "args"],
      "disabled": false
    }
  }
}
```

### **Change Environment Variables:**
Edit `.env`:
```bash
ZAI_API_KEY=your-new-api-key
YOUR_CUSTOM_VAR=value
```

---

## 🎯 **System Status**

✅ **Configuration**: All files in place and functional  
✅ **Environment**: .env loaded with ZAI_API_KEY  
✅ **Launch Script**: `launch_mini_agent.py` working correctly  
✅ **Tool Loading**: All 39+ tools registered based on config  
✅ **MCP Integration**: 3 MCP servers configured and ready  

**Ready to use**: Run `python launch_mini_agent.py --workspace .`
