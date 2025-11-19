# 🔬 Deep Dive: config.yaml and mcp.json - How They Control Mini-Agent

This document explains **exactly when, where, and how** the configuration files control the Mini-Agent system.

---

## 📋 Table of Contents

1. [Execution Timeline](#execution-timeline)
2. [config.yaml Deep Dive](#configyaml-deep-dive)
3. [mcp.json Deep Dive](#mcpjson-deep-dive)
4. [How They Interact](#how-they-interact)
5. [What Each Setting Actually Does](#what-each-setting-actually-does)

---

## ⏱️ Execution Timeline

### When You Type `mini-agent`

Here's the **exact sequence** of what happens:

```
T+0.0s: mini-agent.exe starts
    ↓
T+0.1s: cli.py main() function called
    ↓
T+0.2s: Load .env file (if exists)
    └─ Makes ZAI_API_KEY available as environment variable
    ↓
T+0.3s: Parse command line arguments
    └─ --workspace flag (defaults to current directory)
    ↓
T+0.4s: run_agent() async function starts
    ↓
T+0.5s: CONFIG SEARCH BEGINS ← FIRST CONFIG FILE INTERACTION
    ↓
    Search Priority:
    1. C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\config.yaml ✓ FOUND
    2. C:\Users\Jazeel-Home\.mini-agent\config\config.yaml (skipped)
    3. <package>\mini_agent\config\config.yaml (skipped)
    ↓
T+0.6s: Config.from_yaml() called - YAML PARSING BEGINS
    ↓
T+0.7s: LLM Client initialized with config values
    ↓
T+0.8s: Tool loading begins (using config.tools.enable_* flags)
    ↓
T+1.0s: MCP LOADER CALLED ← MCP.JSON INTERACTION BEGINS
    ↓
T+1.5s: MCP servers starting (3 subprocess spawns)
    ↓
T+2.0s: Agent created with all tools
    ↓
T+2.1s: Interactive loop starts (waiting for your input)
```

---

## 🎯 config.yaml Deep Dive

### File Location & Loading

**When it's loaded:**
- Line 357 in `cli.py`: `config_path = Config.get_default_config_path()`
- Line 385 in `cli.py`: `config = Config.from_yaml(config_path)`

**Priority Search (from config.py lines 164-193):**
```python
def find_config_file(cls, filename: str) -> Path | None:
    # Priority 1: Development mode
    dev_config = Path.cwd() / "mini_agent" / "config" / filename
    if dev_config.exists():  # ← YOUR FILE IS FOUND HERE
        return dev_config
    
    # Priority 2: User config
    user_config = Path.home() / ".mini-agent" / "config" / filename
    
    # Priority 3: Package install
    package_config = cls.get_package_dir() / "config" / filename
```

**Your active config:**
```
C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\config.yaml
```

---

### Structure Breakdown

Your `config.yaml` has **three main sections** that map to Python dataclasses:

#### **Section 1: LLM Configuration**

```yaml
api_key: "eyJhbGc..."           # ← Read at line 120 (config.py)
api_base: "https://api.minimax.io"  # ← Read at line 121
model: "MiniMax-M2"             # ← Read at line 122
provider: "anthropic"           # ← Read at line 123

retry:
  enabled: true                 # ← Read at line 112
  max_retries: 5                # ← Read at line 113
  initial_delay: 1.0            # ← Read at line 114
  max_delay: 60.0               # ← Read at line 115
  exponential_base: 2.0         # ← Read at line 116
```

**Parsing Code (config.py lines 119-125):**
```python
llm_config = LLMConfig(
    api_key=data["api_key"],              # Mandatory - fails if missing
    api_base=data.get("api_base", "https://api.minimax.io"),
    model=data.get("model", "MiniMax-M2"),
    provider=data.get("provider", "anthropic"),
    retry=retry_config,
)
```

**What happens next (cli.py lines 418-426):**
```python
# Provider string converted to enum
provider = LLMProvider.ANTHROPIC if config.llm.provider.lower() == "anthropic" else LLMProvider.OPENAI

# LLM client created with these exact values
llm_client = LLMClient(
    api_key=config.llm.api_key,        # Your JWT token
    provider=provider,                  # ANTHROPIC enum
    api_base=config.llm.api_base,      # "https://api.minimax.io"
    model=config.llm.model,             # "MiniMax-M2"
    retry_config=retry_config if config.llm.retry.enabled else None,
)
```

**Then (llm_wrapper.py lines 48-64):**
```python
# API base URL modified based on provider
if provider == LLMProvider.ANTHROPIC:
    full_api_base = f"{api_base.rstrip('/')}/anthropic"
    # Result: "https://api.minimax.io/anthropic"
elif provider == LLMProvider.OPENAI:
    full_api_base = f"{api_base.rstrip('/')}/v1"
    # Would be: "https://api.minimax.io/v1"

self.api_base = full_api_base
```

**Effect on system:**
```
Every LLM call goes to: https://api.minimax.io/anthropic
Using model: MiniMax-M2
With authentication: Bearer eyJhbGc...

If API call fails:
  → Wait 1.0s, retry (attempt 2)
  → Wait 2.0s, retry (attempt 3)
  → Wait 4.0s, retry (attempt 4)
  → Wait 8.0s, retry (attempt 5)
  → Wait 16.0s, retry (attempt 6)
  → After 5 retries total, give up
```

---

#### **Section 2: Agent Configuration**

```yaml
max_steps: 200                  # ← Read at line 129 (config.py)
workspace_dir: "./workspace"    # ← Read at line 130
system_prompt_path: "system_prompt.md"  # ← Read at line 131
```

**Parsing Code (config.py lines 128-132):**
```python
agent_config = AgentConfig(
    max_steps=data.get("max_steps", 50),           # Default: 50
    workspace_dir=data.get("workspace_dir", "./workspace"),
    system_prompt_path=data.get("system_prompt_path", "system_prompt.md"),
)
```

**What happens next (cli.py lines 440-446):**
```python
# System prompt file is searched using same priority logic
system_prompt_path = Config.find_config_file(config.agent.system_prompt_path)
# Searches:
# 1. ./mini_agent/config/system_prompt.md  ← YOUR FILE
# 2. ~/.mini-agent/config/system_prompt.md
# 3. <package>/config/system_prompt.md

if system_prompt_path and system_prompt_path.exists():
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
```

**Then (cli.py lines 463-469):**
```python
# Agent created with these values
agent = Agent(
    llm_client=llm_client,
    system_prompt=system_prompt,    # Full text from system_prompt.md
    tools=tools,                     # All loaded tools
    max_steps=config.agent.max_steps,  # 200 from your config
    workspace_dir=str(workspace_dir),  # From command line arg
)
```

**Effect on system:**
```
Agent will execute up to 200 tool-calling loops before stopping
  (prevents infinite loops)

System prompt defines:
  - Agent personality and behavior
  - Available tools descriptions
  - Workspace context
  - Operational guidelines
```

---

#### **Section 3: Tools Configuration**

```yaml
tools:
  enable_file_tools: true       # ← Read at line 137 (config.py)
  enable_bash: true             # ← Read at line 138
  enable_note: true             # ← Read at line 139
  enable_zai_search: true       # ← Read at line 140
  enable_skills: true           # ← Read at line 141
  skills_dir: "./skills"        # ← Read at line 142
  enable_mcp: true              # ← Read at line 143
  mcp_config_path: "mcp.json"   # ← Read at line 144
```

**Parsing Code (config.py lines 135-145):**
```python
tools_data = data.get("tools", {})
tools_config = ToolsConfig(
    enable_file_tools=tools_data.get("enable_file_tools", True),
    enable_bash=tools_data.get("enable_bash", True),
    enable_note=tools_data.get("enable_note", True),
    enable_zai_search=tools_data.get("enable_zai_search", True),
    enable_skills=tools_data.get("enable_skills", True),
    skills_dir=tools_data.get("skills_dir", "./skills"),
    enable_mcp=tools_data.get("enable_mcp", True),
    mcp_config_path=tools_data.get("mcp_config_path", "mcp.json"),
)
```

**What happens next - Tool loading sequence (cli.py lines 213-316):**

```python
async def initialize_base_tools(config: Config):
    tools = []
    
    # 1. BASH TOOLS - Controlled by enable_bash
    if config.tools.enable_bash:  # ← YOUR VALUE: true
        bash_tool = BashTool()
        tools.append(bash_tool)  # Adds: bash, bash_output, bash_kill
    
    # 2. Z.AI SEARCH - Controlled by enable_zai_search
    if config.tools.enable_zai_search:  # ← YOUR VALUE: true
        from mini_agent.tools.zai_tools import ZAIWebSearchTool, ZAIWebReaderTool
        zai_search_tool = ZAIWebSearchTool()  # Reads ZAI_API_KEY from env
        zai_reader_tool = ZAIWebReaderTool()
        tools.append(zai_search_tool)  # Adds: zai_web_search
        tools.append(zai_reader_tool)  # Adds: zai_web_reader
    
    # 3. SKILLS - Controlled by enable_skills
    if config.tools.enable_skills:  # ← YOUR VALUE: true
        skills_dir = config.tools.skills_dir  # ← YOUR VALUE: "./skills"
        skill_tools, skill_loader = create_skill_tools(skills_dir)
        tools.extend(skill_tools)  # Adds: get_skill
    
    # 4. MCP TOOLS - Controlled by enable_mcp
    if config.tools.enable_mcp:  # ← YOUR VALUE: true
        mcp_config_path = Config.find_config_file(config.tools.mcp_config_path)
        # Searches for mcp.json in same priority order
        mcp_tools = await load_mcp_tools_async(str(mcp_config_path))
        tools.extend(mcp_tools)  # ← THIS TRIGGERS MCP.JSON LOADING
    
    return tools, skill_loader
```

**Then workspace-dependent tools (cli.py lines 318-346):**
```python
def add_workspace_tools(tools: List[Tool], config: Config, workspace_dir: Path):
    # 5. FILE TOOLS - Controlled by enable_file_tools
    if config.tools.enable_file_tools:  # ← YOUR VALUE: true
        tools.extend([
            ReadTool(workspace_dir=str(workspace_dir)),
            WriteTool(workspace_dir=str(workspace_dir)),
            EditTool(workspace_dir=str(workspace_dir)),
        ])
    
    # 6. SESSION NOTES - Controlled by enable_note
    if config.tools.enable_note:  # ← YOUR VALUE: true
        tools.append(SessionNoteTool(memory_file=str(workspace_dir / ".agent_memory.json")))
```

**Effect on system:**
```
Your current config enables ALL tools (all flags are true)

Tools loaded in order:
  1. bash, bash_output, bash_kill (3 tools)
  2. zai_web_search, zai_web_reader (2 tools)
  3. get_skill (1 tool)
  4. MCP tools (15 tools from 3 servers - see mcp.json section)
  5. read_file, write_file, edit_file (3 tools)
  6. record_note (1 tool)

Total: 25+ tools available to the agent

If you set enable_bash: false, those 3 tools would NOT load
If you set enable_mcp: false, all 15 MCP tools would NOT load
```

---

## 🔌 mcp.json Deep Dive

### File Location & Loading

**When it's loaded:**
- Line 301 in `cli.py`: `mcp_config_path = Config.find_config_file(config.tools.mcp_config_path)`
- Line 303 in `cli.py`: `mcp_tools = await load_mcp_tools_async(str(mcp_config_path))`
- Line 180 in `mcp_loader.py`: `with open(config_file, encoding="utf-8") as f:`

**Active file:**
```
C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\mcp.json
```

---

### Structure Breakdown

Your `mcp.json` defines **MCP server processes** that run as **separate child processes**:

```json
{
  "mcpServers": {
    "memory": { ... },      ← Server 1: Knowledge graph
    "filesystem": { ... },  ← Server 2: File operations
    "git": { ... }          ← Server 3: Git operations
  }
}
```

Each server entry has this structure:
```json
{
  "description": "Human-readable description",
  "command": "executable to run",
  "args": ["argument1", "argument2"],
  "env": {"ENV_VAR": "value"},
  "disabled": false
}
```

---

### Server 1: Memory (Knowledge Graph)

```json
"memory": {
  "description": "Memory - Knowledge graph memory system (long-term memory based on graph database)",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-memory"
  ],
  "disabled": false
}
```

**What actually happens (mcp_loader.py lines 192-210):**

```python
# Loop through mcp.json servers
for server_name, server_config in mcp_servers.items():
    if server_config.get("disabled", False):  # ← YOUR VALUE: false
        continue  # Skip disabled servers
    
    command = server_config.get("command")    # ← "npx"
    args = server_config.get("args", [])      # ← ["-y", "@modelcontextprotocol/server-memory"]
    env = server_config.get("env", {})        # ← {} (empty)
    
    connection = MCPServerConnection(server_name, command, args, env)
    success = await connection.connect()
```

**Then (mcp_loader.py lines 83-148):**

```python
async def connect(self) -> bool:
    # Create server parameters
    server_params = StdioServerParameters(
        command=self.command,  # "npx"
        args=self.args,        # ["-y", "@modelcontextprotocol/server-memory"]
        env=self.env if self.env else None
    )
    
    # Start subprocess and connect via stdio
    read_stream, write_stream = await self.exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    
    # Create client session (JSON-RPC over stdio)
    session = await self.exit_stack.enter_async_context(
        ClientSession(read_stream, write_stream)
    )
    
    # Initialize handshake
    await session.initialize()
    
    # List available tools from this server
    tools_list = await session.list_tools()
    
    # Wrap each tool as MCPTool
    for tool in tools_list.tools:
        mcp_tool = MCPTool(
            name=tool.name,
            description=tool.description,
            parameters=tool.inputSchema,
            session=session  # ← Keeps connection alive
        )
        self.tools.append(mcp_tool)
```

**Subprocess created:**
```bash
npx -y @modelcontextprotocol/server-memory

# This command:
# 1. Uses npx (Node package executor)
# 2. -y flag: auto-confirm package download
# 3. Downloads @modelcontextprotocol/server-memory from npm
# 4. Runs the server (communicates via stdin/stdout)
```

**Tools exposed by memory server:**
```
create_entities      - Create nodes in knowledge graph
create_relations     - Create edges between nodes
add_observations     - Add facts to existing nodes
delete_entities      - Remove nodes
delete_relations     - Remove edges
delete_observations  - Remove facts
read_graph           - Get entire graph
search_nodes         - Search by content
open_nodes           - Get specific nodes

Total: 5 tools
```

**Communication protocol:**
```
Mini-Agent → (JSON-RPC) → Memory Server Process
                                ↓
                          SQLite Database
                          (in-memory or file)
                                ↓
                          Graph operations
                                ↓
Mini-Agent ← (JSON-RPC) ← Results
```

**Effect on system:**
```
While mini-agent runs, a separate Node.js process runs in background:
  Process: npx -y @modelcontextprotocol/server-memory
  Communication: stdin/stdout pipes (JSON-RPC protocol)
  Data storage: In-memory graph database
  
When agent calls create_entities tool:
  1. Agent serializes tool call to JSON
  2. Sends via pipe to memory server
  3. Memory server creates graph nodes
  4. Returns result via pipe
  5. Agent deserializes result
  6. Continues execution
  
When mini-agent exits:
  → Memory server process is killed
  → All graph data is lost (unless persisted)
```

---

### Server 2: Filesystem

```json
"filesystem": {
  "description": "Filesystem - Secure file system access with path restrictions",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:\\Users\\Jazeel-Home\\Mini-Agent"
  ],
  "disabled": false
}
```

**Subprocess created:**
```bash
npx -y @modelcontextprotocol/server-filesystem "C:\Users\Jazeel-Home\Mini-Agent"

# The last argument is the ALLOWED ROOT DIRECTORY
# Server will ONLY allow operations within this path
```

**Tools exposed by filesystem server:**
```
read_file              - Read file contents
read_multiple_files    - Read multiple files at once
write_file             - Write/create files
edit_file              - Edit existing files (search/replace)
create_directory       - Create directories
list_directory         - List directory contents
directory_tree         - Get recursive tree structure
move_file              - Move/rename files
search_files           - Search for files by pattern
get_file_info          - Get file metadata

Total: 10 tools (approximately)
```

**Security restriction:**
```python
# Inside the filesystem MCP server (Node.js code):
const allowedRoot = "C:\\Users\\Jazeel-Home\\Mini-Agent"

function validatePath(requestedPath) {
    const normalized = path.normalize(requestedPath)
    const absolute = path.resolve(normalized)
    
    // CRITICAL: Prevent directory traversal
    if (!absolute.startsWith(allowedRoot)) {
        throw new Error("Access denied: Path outside allowed directory")
    }
}

// Every file operation calls validatePath() first
```

**Effect on system:**
```
Filesystem server provides SANDBOXED file access:

✅ Allowed:
  read_file("C:\\Users\\Jazeel-Home\\Mini-Agent\\file.txt")
  write_file("./documents/test.md", "content")
  edit_file("mini_agent/config.py", old, new)

❌ Blocked:
  read_file("C:\\Windows\\System32\\config\\SAM")  ← Outside allowed root
  write_file("../../../etc/passwd", "hack")        ← Directory traversal blocked
  
This prevents the LLM from accessing your entire filesystem.
Only the Mini-Agent project directory is accessible.
```

---

### Server 3: Git

```json
"git": {
  "description": "Git - Git repository operations and version control",
  "command": "python",
  "args": [
    "-m",
    "mcp_server_git"
  ],
  "env": {},
  "disabled": false
}
```

**Subprocess created:**
```bash
python -m mcp_server_git

# This runs a Python MCP server
# Package: mcp_server_git (must be installed via pip)
```

**Tools exposed by git server:**
```
git_status           - Show working tree status
git_diff_unstaged    - Show unstaged changes
git_diff_staged      - Show staged changes
git_diff             - Compare branches/commits
git_commit           - Create commit
git_add              - Stage files
git_reset            - Unstage changes
git_log              - Show commit history
git_create_branch    - Create new branch
git_checkout         - Switch branches
git_show             - Show commit contents
git_branch           - List branches

Total: 12+ tools
```

**Effect on system:**
```
Git server wraps git commands in a safe interface:

When agent calls git_status(repo_path):
  1. Server validates repo_path exists
  2. Runs: git status --porcelain
  3. Parses output into structured format
  4. Returns JSON response
  
Advantages over raw bash:
  - Structured output (JSON not text)
  - Input validation
  - Error handling
  - Cross-platform compatibility
```

---

### MCP Server Lifecycle

**Startup sequence:**
```
1. mini-agent starts
2. config.yaml parsed → enable_mcp: true
3. mcp.json loaded
4. For each enabled server:
   a. Spawn subprocess (npx/python)
   b. Connect via stdio pipes
   c. Send initialize request (JSON-RPC)
   d. Receive tool list
   e. Wrap tools as MCPTool objects
5. All MCP tools added to agent.tools
6. Agent ready for user input
```

**During operation:**
```
User: "Search my knowledge graph for 'API'"
  ↓
Agent decides to use: search_nodes(query="API")
  ↓
MCPTool.execute(query="API") called
  ↓
JSON-RPC call sent to memory server:
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "search_nodes",
      "arguments": {"query": "API"}
    }
  }
  ↓
Memory server processes request
  ↓
Response received:
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "content": [
        {"type": "text", "text": "Found 3 nodes matching 'API'..."}
      ]
    }
  }
  ↓
MCPTool returns ToolResult to agent
  ↓
Agent continues reasoning
```

**Shutdown sequence:**
```
1. User types /exit
2. cleanup_mcp_connections() called
3. For each connection:
   a. Close stdio pipes
   b. Wait for subprocess to terminate
   c. SIGTERM sent if not closed gracefully
4. All child processes killed
5. mini-agent exits
```

---

## 🔗 How They Interact

### Dependency Chain

```
config.yaml
    ↓
    ├─ LLM section → Controls which AI model is used
    ↓
    ├─ Agent section → Controls behavior limits and prompts
    ↓
    └─ Tools section → Controls which capabilities are enabled
           ↓
           └─ enable_mcp: true → Triggers mcp.json loading
                                        ↓
                                     mcp.json
                                        ↓
                                     Spawns MCP servers
                                        ↓
                                     Exposes 15+ tools
```

### Configuration Flow

```
[config.yaml]
tools:
  enable_mcp: true          ← Gate keeper flag
  mcp_config_path: "mcp.json"  ← Which file to load
                    ↓
              [mcp.json]
              mcpServers:
                memory:
                  disabled: false   ← Individual server toggle
                  command: "npx"    ← How to start server
                  args: [...]       ← Server parameters
                    ↓
              [Subprocess Started]
              npx -y @modelcontextprotocol/server-memory
                    ↓
              [Tools Exposed]
              - create_entities
              - create_relations
              - read_graph
              ...
```

### Toggle Effects

**Scenario 1: Disable all MCP**
```yaml
# config.yaml
tools:
  enable_mcp: false  ← Change this
```
**Result:**
- mcp.json is NOT loaded
- No MCP servers started
- 15+ MCP tools unavailable
- Agent still has 10+ native tools

---

**Scenario 2: Disable specific MCP server**
```json
// mcp.json
{
  "mcpServers": {
    "memory": {
      "disabled": true  ← Change this
    }
  }
}
```
**Result:**
- config.yaml enable_mcp: true still active
- mcp.json IS loaded
- Memory server NOT started
- Filesystem and git servers still active
- Only memory tools (5) unavailable

---

**Scenario 3: Change filesystem access**
```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users"  ← Change from "Mini-Agent" to "Users"
      ]
    }
  }
}
```
**Result:**
- Agent can now access entire C:\Users directory
- Security perimeter expanded
- Can read files outside Mini-Agent project
- ⚠️ **SECURITY RISK** - LLM has broader file access

---

## 🎛️ What Each Setting Actually Does

### config.yaml Reference

| Setting | Type | Current Value | Effect | What Happens If Changed |
|---------|------|---------------|--------|------------------------|
| **api_key** | string | `eyJhbGc...` | LLM authentication token | Different key → Different MiniMax account/quota |
| **api_base** | string | `https://api.minimax.io` | API endpoint | Change to `.com` for China region |
| **model** | string | `MiniMax-M2` | Which LLM to use | Could use different model (if available) |
| **provider** | string | `anthropic` | API protocol format | `openai` changes URL to `/v1` instead of `/anthropic` |
| **retry.enabled** | boolean | `true` | Enable retry on failures | `false` → Fail immediately, no retries |
| **retry.max_retries** | integer | `5` | Max retry attempts | `0` → No retries, `10` → More persistence |
| **retry.initial_delay** | float | `1.0` | First retry delay (seconds) | `5.0` → Wait 5s before first retry |
| **retry.max_delay** | float | `60.0` | Maximum delay cap | `10.0` → Never wait more than 10s |
| **retry.exponential_base** | float | `2.0` | Backoff multiplier | `1.5` → Slower growth, `3.0` → Faster growth |
| **max_steps** | integer | `200` | Max tool call loops | `50` → Stop sooner, `1000` → Run longer |
| **workspace_dir** | string | `./workspace` | Default workspace | NOT USED (overridden by CLI arg) |
| **system_prompt_path** | string | `system_prompt.md` | Prompt file name | `custom_prompt.md` → Use different prompt |
| **enable_file_tools** | boolean | `true` | File read/write/edit | `false` → No file operations |
| **enable_bash** | boolean | `true` | PowerShell execution | `false` → No terminal commands |
| **enable_note** | boolean | `true` | Session notes | `false` → No memory persistence |
| **enable_zai_search** | boolean | `true` | Web search | `false` → No internet search capability |
| **enable_skills** | boolean | `true` | Specialized skills | `false` → No skill system (lose 20+ skills) |
| **skills_dir** | string | `./skills` | Skills folder | `custom_skills/` → Use different skills |
| **enable_mcp** | boolean | `true` | MCP servers | `false` → No MCP tools (lose 15+ tools) |
| **mcp_config_path** | string | `mcp.json` | MCP config file | `custom_mcp.json` → Different servers |

---

### mcp.json Reference

| Setting | Type | Current Value | Effect | What Happens If Changed |
|---------|------|---------------|--------|------------------------|
| **disabled** | boolean | `false` | Server enable/disable | `true` → Skip this server entirely |
| **command** | string | `npx`/`python` | Executable to run | `node` → Run directly (if server installed) |
| **args** | array | `["-y", "..."]` | Command arguments | Remove `-y` → Manual confirm required |
| **env** | object | `{}` | Environment variables | `{"DEBUG": "1"}` → Enable server debug logs |

**Memory Server Args:**
```json
["- "-y", "@modelcontextprotocol/server-memory"]
```
- `-y`: Auto-confirm npm package download
- Package: `@modelcontextprotocol/server-memory`

**Filesystem Server Args:**
```json
["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Jazeel-Home\\Mini-Agent"]
```
- Last arg: **Security boundary** (allowed root directory)
- Change this to expand/restrict file access

**Git Server Args:**
```json
["-m", "mcp_server_git"]
```
- `-m`: Python module flag
- Module: `mcp_server_git` (must be installed)

---

## 💡 Practical Examples

### Example 1: Disable Web Search (Save API Costs)

**Change:**
```yaml
# config.yaml
tools:
  enable_zai_search: false  ← Change from true
```

**Result:**
```
✅ LLM retry mechanism enabled (max 5 retries)
✅ Loaded Bash tool
✅ Loaded Bash Output tool
✅ Loaded Bash Kill tool
⚠️  Z.AI Web Search disabled  ← NOT LOADED
✅ Loaded Skill tool (get_skill)
✅ Loaded 15 MCP tools
✅ Loaded file operation tools
✅ Loaded session note tool

Total tools: 23 (instead of 25)
```

**When agent tries to search web:**
```
Agent: I need to search the web for information
Error: No web search tool available
Agent: I cannot search the web in this environment
```

---

### Example 2: Expand Filesystem Access

**Change:**
```json
// mcp.json
{
  "mcpServers": {
    "filesystem": {
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\"  ← Change to entire C: drive
      ]
    }
  }
}
```

**Result:**
```
Agent can now:
  ✅ Read C:\Windows\System32\drivers\etc\hosts
  ✅ Write C:\temp\output.txt
  ✅ List C:\Program Files\
  ⚠️  Access your entire C: drive!
```

**Security Impact:**
```
Before: Sandboxed to Mini-Agent project
After: Full C: drive access
Risk: LLM can read sensitive files, modify system files
```

---

### Example 3: Reduce Retry Attempts

**Change:**
```yaml
# config.yaml
retry:
  max_retries: 1  ← Change from 5
```

**Result:**
```
API call fails (network error)
  ↓
Wait 1.0s
  ↓
Retry attempt 2
  ↓
Still fails
  ↓
Give up immediately (instead of trying 5 times)
```

**When to use:**
- Fast failure detection
- Development testing
- Limited patience

---

### Example 4: Add Custom MCP Server

**Add to mcp.json:**
```json
{
  "mcpServers": {
    "memory": { ... },
    "filesystem": { ... },
    "git": { ... },
    "slack": {  ← NEW SERVER
      "description": "Slack - Send messages to Slack",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-slack"
      ],
      "env": {
        "SLACK_TOKEN": "xoxb-your-token-here"
      },
      "disabled": false
    }
  }
}
```

**Result:**
```
On startup:
  ✓ Connected to MCP server 'slack' - loaded 3 tools
    - send_message: Send a message to a Slack channel
    - list_channels: List available channels
    - get_channel_history: Get recent messages

Agent now has Slack integration!
```

---

## 🔧 Troubleshooting

### "Configuration file not found"

**Problem:**
```
❌ Configuration file not found
```

**Cause:**
- No config.yaml in any search location

**Search locations (in order):**
1. `C:\Users\Jazeel-Home\Mini-Agent\mini_agent\config\config.yaml`
2. `C:\Users\Jazeel-Home\.mini-agent\config\config.yaml`
3. `<python-site-packages>\mini_agent\config\config.yaml`

**Solution:**
```bash
# Verify file exists
ls mini_agent/config/config.yaml

# If missing, copy from example
cp mini_agent/config/config-example.yaml mini_agent/config/config.yaml
```

---

### "Please configure a valid API Key"

**Problem:**
```
❌ Error: Please configure a valid API Key
```

**Cause:**
```yaml
api_key: "YOUR_API_KEY_HERE"  ← Placeholder not replaced
```

**Solution:**
```yaml
api_key: "eyJhbGciOiJSUzI1NiI..."  ← Real JWT token
```

---

### "Failed to load MCP tools"

**Problem:**
```
⚠️  Failed to load MCP tools: [Errno 2] No such file or directory: 'npx'
```

**Cause:**
- Node.js/npx not installed
- npx not in PATH

**Solution:**
```bash
# Install Node.js (includes npx)
# Download from: https://nodejs.org/

# Verify
npx --version
```

---

### "MCP server timeout"

**Problem:**
```
✗ Failed to connect to MCP server 'memory': Connection timeout
```

**Cause:**
- Server package download failed
- Network issues
- Server crash on startup

**Solution:**
```bash
# Test server manually
npx -y @modelcontextprotocol/server-memory

# Should start without errors
# Press Ctrl+C to stop
```

---

### "Access denied: Path outside allowed directory"

**Problem:**
```
Error: Access denied: Path outside allowed directory
```

**Cause:**
```json
{
  "filesystem": {
    "args": [..., "C:\\Users\\Jazeel-Home\\Mini-Agent"]
  }
}
```
Trying to access: `C:\Windows\System32\file.txt`

**Solution:**
- Change allowed root in mcp.json args
- Or move target file into allowed directory

---

## 📝 Summary

**config.yaml controls:**
- Which LLM to use (MiniMax M2 via Anthropic protocol)
- How to handle failures (5 retries with exponential backoff)
- Which tool categories to load (bash, files, web search, skills, MCP)
- Agent behavior limits (200 max steps)

**mcp.json controls:**
- Which external server processes to start
- What arguments to pass them (especially filesystem root directory)
- Which servers are enabled/disabled
- Environment variables for servers

**Key relationship:**
```
config.yaml enables MCP system → mcp.json defines which servers → servers expose tools → agent uses tools
```

**Power user tip:**
Both files support hot-reloading! Restart mini-agent to apply changes.

---

**You now have complete knowledge of how Mini-Agent's configuration works.** 🎓
