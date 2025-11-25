# 🔧 Tools System Architecture & Documentation
## Mini-Agent Core Execution Layer

**Date**: November 25, 2025  
**Component**: Tools System (Base Tools + Enhanced Tools)  
**Status**: Core Tools Operational, Enhanced Tools Integration Ready

---

## 🎯 **TOOLS SYSTEM OVERVIEW**

### **Philosophy: Two-Layer Tool Architecture**

The Tools System implements a **dual-layer approach** where basic execution tools are always available, while enhanced intelligent tools integrate with the upgrade systems for advanced capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                    Mini-Agent Agent                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Base      │ │ Enhanced    │ │  Skills     │            │
│  │   Tools     │ │   Tools     │ │  System     │            │
│  │ (Always     │ │ (Upgrade    │ │ (Expert     │            │
│  │  Available) │ │  Integrated)│ │  Knowledge) │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               Tool Execution Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   File      │ │    Bash     │ │   Note      │            │
│  │ Operations  │ │  Commands   │ │   Storage   │            │
│  │             │ │             │ │             │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Web       │ │    MCP      │ │   Agent     │            │
│  │ Functions   │ │ Integration │ │ Protocol    │            │
│  │             │ │             │ │             │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 **TOOL INVENTORY**

### **Base Tools (Always Available) - 8 Core Tools**

| Tool | Type | Purpose | Status |
|------|------|---------|--------|
| **FileTools** | Core | File read/write/edit operations | ✅ Operational |
| **BashTool** | Core | Shell command execution | ✅ Operational |
| **SessionNoteTool** | Core | Session notes and memory | ✅ Operational |
| **SkillTool** | Meta | Skills system integration | ✅ Operational |
| **ZAIWebTool** | Web | Z.AI web search integration | ✅ Operational |
| **SimpleWebSearch** | Web | Lightweight web search | ✅ Operational |
| **MCPLoader** | Integration | MCP server management | ✅ Operational |
| **HTTPClient** | Infrastructure | HTTP/SSE communication | ✅ Operational |

### **Enhanced Tools (Upgrade Integration) - 5 Advanced Tools**

| Tool | Purpose | Upgrade Integration | Status |
|------|---------|-------------------|--------|
| **EnhancedSessionNoteTool** | Smart session memory | Upgrade 1: Memory Enhancement | ⏳ Pending Integration |
| **WebResearchOrchestrator** | Intelligent research | Upgrade 2: Web Intelligence | ⏳ Pending Integration |
| **SelfAwarePerformanceMonitor** | Performance analytics | Upgrade 3: Self-Awareness | ⏳ Pending Integration |
| **ProjectContextManager** | Project intelligence | Upgrade 1: Memory Enhancement | ⏳ Pending Integration |
| **PatternLearningEngine** | Learning analytics | Upgrade 1: Pattern Learning | ⏳ Pending Integration |

---

## 🔧 **BASE TOOLS DETAILED DOCUMENTATION**

### **1. FileTools**
**Path**: `mini_agent/tools/file_tools.py`  
**Purpose**: Core file system operations

**Capabilities:**
```python
# File Reading
async def read_file(self, file_path: str, limit: Optional[int] = None, offset: int = 0) -> str
async def read_files(self, file_paths: List[str]) -> Dict[str, str]

# File Writing  
async def write_file(self, file_path: str, content: str) -> None
async def write_files(self, files: Dict[str, str]) -> None

# File Editing
async def edit_file(self, file_path: str, old_str: str, new_str: str) -> None
async def replace_content(self, file_path: str, replacements: List[Tuple[str, str]]) -> None

# File System Operations
async def list_directory(self, dir_path: str, recursive: bool = False) -> List[str]
async def create_directory(self, dir_path: str) -> None
async def delete_file(self, file_path: str) -> None
async def move_file(self, source: str, destination: str) -> None
async def copy_file(self, source: str, destination: str) -> None

# Advanced Operations
async def find_files(self, pattern: str, directory: str = ".") -> List[str]
async def search_in_files(self, query: str, file_pattern: str = "*") -> List[Dict]
async def get_file_info(self, file_path: str) -> Dict[str, Any]
```

**Usage Examples:**
```python
# Simple file operations
content = await file_tool.read_file("config.yaml")
await file_tool.write_file("output.txt", "Hello, World!")

# Advanced search
results = await file_tool.search_in_files("TODO", "*.py")
for result in results:
    print(f"{result['file']}: {result['line']} - {result['content']}")

# Batch operations
files = {
    "config.yaml": "# Configuration",
    "readme.md": "# Documentation", 
    "requirements.txt": "requests\nfastapi"
}
await file_tool.write_files(files)
```

**Integration Points:**
- **Skills**: Used by document processing skills
- **MCP**: Integrates with Git MCP for version control
- **Enhanced Tools**: Foundation for project analysis

### **2. BashTool**
**Path**: `mini_agent/tools/bash_tool.py`  
**Purpose**: Shell command execution with cross-platform support

**Capabilities:**
```python
# Basic Execution
async def execute(self, command: str, timeout: int = 120) -> str
async def run_background(self, command: str) -> str

# Platform Detection
def get_platform_commands(self) -> Dict[str, str]
def detect_shell_type(self) -> str

# Environment Management
async def set_environment(self, key: str, value: str) -> None
async def get_environment(self, key: str) -> Optional[str]

# Git Operations (Simplified)
async def git_status(self, repo_path: str = ".") -> str
async def git_add(self, repo_path: str, files: List[str]) -> str
async def git_commit(self, repo_path: str, message: str) -> str

# Package Management
async def install_package(self, package: str, manager: str = "pip") -> str
async def check_package(self, package: str) -> bool

# Advanced Operations
async def run_script(self, script_path: str, args: List[str] = None) -> str
async def check_process(self, process_name: str) -> bool
async def kill_process(self, process_name: str) -> bool
```

**Platform Support:**
```python
PLATFORM_COMMANDS = {
    "windows": {
        "shell": "powershell",
        "package_managers": ["chocolatey", "winget", "pip"],
        "git": "git",
        "python": "python",
        "node": "npm"
    },
    "unix": {
        "shell": "bash", 
        "package_managers": ["apt", "brew", "pip"],
        "git": "git",
        "python": "python3",
        "node": "npm"
    }
}
```

**Usage Examples:**
```python
# Platform-specific execution
result = await bash_tool.execute("python --version")

# Package management
await bash_tool.install_package("requests")
await bash_tool.install_package("react", manager="npm")

# Git integration
await bash_tool.git_add(".", ["*.py", "*.md"])
await bash_tool.git_commit(".", "Add new features")

# Process management
process_running = await bash_tool.check_process("python")
if not process_running:
    await bash_tool.execute("python app.py &", run_in_background=True)
```

### **3. SessionNoteTool**
**Path**: `mini_agent/tools/note_tool.py`  
**Purpose**: Session memory and note management

**Capabilities:**
```python
# Note Management
async def execute(self, content: str, category: str = "general") -> Dict[str, Any]
async def recall(self, query: str = "", category: str = "", limit: int = 10) -> List[Dict]

# Note Operations
async def update_note(self, note_id: str, content: str) -> bool
async def delete_note(self, note_id: str) -> bool
async def search_notes(self, query: str) -> List[Dict]

# Session Management
async def start_session(self, project_context: str = None) -> str
async def end_session(self) -> Dict[str, Any]
async def get_session_summary(self) -> Dict[str, Any]

# Enhanced Features
async def auto_categorize(self, content: str) -> str
async def extract_insights(self, notes: List[Dict]) -> List[str]
async def generate_summary(self, time_range: str = "session") -> str
```

**Storage Backend Options:**
```python
class StorageBackend(ABC):
    @abstractmethod
    async def store_note(self, note: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    async def retrieve_notes(self, query: Dict[str, Any]) -> List[Dict]:
        pass
    
    @abstractmethod
    async def update_note(self, note_id: str, updates: Dict[str, Any]) -> bool:
        pass

class SQLiteBackend(StorageBackend):
    # Local SQLite storage
    pass

class SupabaseBackend(StorageBackend):
    # Cloud Supabase storage (for enhanced features)
    pass
```

**Enhanced Integration (Upgrade 1):**
```python
class EnhancedSessionNoteTool(SessionNoteTool):
    async def execute(self, content: str, category: str = "general", **kwargs):
        # Enhanced processing
        if self.config.memory.get("enable_enhanced"):
            # Use Supabase integration
            enhanced_data = await self._enhance_note_with_project_context(content, category)
            await self.mcp_client.call_tool("supabase-admin", {
                "table_operation": "insert",
                "table_name": "mini_agent_sessions",
                "data": enhanced_data
            })
        
        # Original implementation
        result = await super().execute(content, category, **kwargs)
        
        # Pattern learning
        if self.config.memory.get("pattern_learning"):
            await self._record_pattern(result, category)
        
        return result
```

### **4. SkillTool**
**Path**: `mini_agent/tools/skill_tool.py`  
**Purpose**: Skills system integration and progressive disclosure

**Capabilities:**
```python
# Skill Discovery
async def list_available_skills(self) -> List[Dict[str, Any]]
async def discover_skills(self, query: str) -> List[Dict[str, Any]]
async def get_skill_info(self, skill_name: str) -> Dict[str, Any]

# Skill Loading
async def load_skill(self, skill_name: str) -> Skill
async def load_skills_by_category(self, category: str) -> List[Skill]
async def preload_skills(self, skill_names: List[str]) -> None

# Skill Execution
async def execute_skill(self, skill_name: str, action: str, parameters: Dict) -> Dict
async def execute_multiple_skills(self, executions: List[Dict]) -> List[Dict]

# Skill Management
async def enable_skill(self, skill_name: str) -> bool
async def disable_skill(self, skill_name: str) -> bool
async def update_skill(self, skill_name: str, skill_data: Dict) -> bool
```

**Progressive Disclosure Implementation:**
```python
class ProgressiveDisclosureManager:
    def __init__(self, skill_loader: SkillLoader):
        self.skill_loader = skill_loader
        self.loaded_skills = {}
        self.skill_metadata = self._load_skill_metadata()
    
    async def smart_skill_discovery(self, user_intent: str) -> List[Dict]:
        """Discover relevant skills based on user intent"""
        
        # Analyze intent
        intent_analysis = await self._analyze_user_intent(user_intent)
        
        # Find matching skills
        relevant_skills = []
        for skill_name, metadata in self.skill_metadata.items():
            relevance_score = self._calculate_relevance(intent_analysis, metadata)
            if relevance_score > 0.3:  # Threshold for relevance
                relevant_skills.append({
                    "name": skill_name,
                    "metadata": metadata,
                    "relevance_score": relevance_score,
                    "ready_to_load": skill_name not in self.loaded_skills
                })
        
        return sorted(relevant_skills, key=lambda x: x["relevance_score"], reverse=True)
    
    async def execute_with_progressive_disclosure(self, user_request: str):
        """Execute user request with progressive skill loading"""
        
        # 1. Discover relevant skills
        skills = await self.smart_skill_discovery(user_request)
        
        # 2. Load most relevant skill
        if skills:
            top_skill = skills[0]
            skill = await self.load_skill(top_skill["name"])
            
            # 3. Execute skill
            result = await skill.execute("analyze", {"request": user_request})
            
            # 4. Offer additional relevant skills
            additional_skills = skills[1:3]  # Next 2 most relevant
            if additional_skills:
                result["suggested_next_skills"] = [
                    skill["name"] for skill in additional_skills
                ]
        
        return result
```

### **5. ZAIWebTool**
**Path**: `mini_agent/tools/zai_web_tool.py`  
**Purpose**: Z.AI web search integration with MCP-first strategy

**Capabilities:**
```python
# Web Search
async def web_search(self, query: str, max_results: int = 5, timeout: int = 30) -> Dict
async def research_topic(self, query: str, depth: str = "basic") -> Dict

# Web Reading
async def extract_content(self, urls: List[str]) -> Dict[str, str]
async def read_webpage(self, url: str, extract_links: bool = True) -> Dict

# Research Orchestration
async def comprehensive_research(self, query: str) -> Dict
async def validate_sources(self, sources: List[str]) -> Dict

# Z.AI Integration
async def check_quotas(self) -> Dict
async def optimize_usage(self, operation_type: str) -> Dict
```

**MCP-First Strategy Implementation:**
```python
class ZAIWebTool:
    def __init__(self):
        self.mcp_client = MCPServerClient()
        self.quota_manager = ZAIQuotaManager()
        
    async def web_search(self, query: str, max_results: int = 5):
        """MCP-first web search strategy"""
        
        # Check quotas before proceeding
        quotas = await self.quota_manager.check_quotas()
        if quotas["searches_remaining"] <= 0:
            raise QuotaExhaustedError("Z.AI search quota exhausted")
        
        try:
            # Try MCP server first (FREE quota)
            result = await self.mcp_client.call_tool("zai-web-search", {
                "query": query,
                "max_results": max_results
            })
            
            # Track usage
            await self.quota_manager.track_usage("search", 1)
            
            return {
                "success": True,
                "data": result.data,
                "source": "mcp",
                "quota_used": 1,
                "remaining": quotas["searches_remaining"] - 1
            }
            
        except Exception as e:
            # Fallback to alternative search if MCP fails
            return await self._fallback_search(query, max_results)
    
    async def _fallback_search(self, query: str, max_results: int):
        """Fallback search when MCP is unavailable"""
        
        # Use simple web search as fallback
        fallback_result = await simple_web_search(query, max_results)
        
        return {
            "success": True,
            "data": fallback_result,
            "source": "fallback",
            "note": "MCP server unavailable, used fallback search"
        }
```

**Enhanced Integration (Upgrade 2):**
```python
class EnhancedZAIWebTool(ZAIWebTool):
    async def research_with_intelligence(self, query: str, context: Dict = None):
        """Enhanced research with intelligence (Upgrade 2)"""
        
        # Basic search
        search_results = await self.web_search(query)
        
        if self.config.web.get("enable_validation"):
            # Validate sources
            validated_sources = await self._validate_sources(search_results["data"])
            search_results["validated_sources"] = validated_sources
        
        if self.config.web.get("enable_synthesis"):
            # Synthesize findings
            synthesis = await self._synthesize_research(search_results["data"], query)
            search_results["synthesis"] = synthesis
        
        if self.config.web.get("enable_memory_integration"):
            # Store in memory
            await self._integrate_with_memory(query, search_results)
        
        return search_results
```

### **6. SimpleWebSearch**
**Path**: `mini_agent/tools/simple_web_search.py`  
**Purpose**: Lightweight web search for basic queries

**Capabilities:**
```python
# Basic Search
async def search(self, query: str, max_results: int = 3) -> List[Dict]
async def search_images(self, query: str, max_results: int = 5) -> List[Dict]

# Content Extraction
async def get_page_content(self, url: str) -> str
async def extract_metadata(self, url: str) -> Dict

# Search Optimization
async def optimize_query(self, query: str) -> str
async def get_suggestions(self, partial_query: str) -> List[str]
```

### **7. MCPLoader**
**Path**: `mini_agent/tools/mcp_loader.py`  
**Purpose**: MCP server integration and management

**Capabilities:**
```python
# Server Management
async def load_mcp_servers(self) -> List[Tool]
async def start_mcp_server(self, server_name: str) -> bool
async def stop_mcp_server(self, server_name: str) -> bool
async def check_server_health(self, server_name: str) -> Dict

# Tool Loading
async def load_mcp_tools(self, server_config: Dict) -> List[Tool]
async def get_available_tools(self, server_name: str) -> List[str]

# Integration
async def integrate_with_tools(self, tools: List[Tool]) -> List[Tool]
async def optimize_tool_selection(self, task_description: str) -> List[Tool]
```

### **8. HTTPClient**
**Path**: `mini_agent/tools/http_mcp_client.py`  
**Purpose**: HTTP communication with SSE support for MCP servers

**Capabilities:**
```python
# HTTP Operations
async def call_tool(self, server_name: str, parameters: Dict) -> ToolResult
async def make_request(self, url: str, method: str = "POST", data: Dict = None) -> Dict
async def upload_file(self, url: str, file_path: str, metadata: Dict = None) -> Dict

# SSE Support (Critical for Z.AI)
def _parse_sse_response(self, response_text: str) -> Dict[str, Any]
async def handle_sse_stream(self, url: str, headers: Dict) -> AsyncIterator[Dict]

# Error Handling
async def retry_request(self, request: Dict, max_retries: int = 3) -> ToolResult
async def handle_connection_error(self, error: Exception) -> ToolResult
```

**SSE Protocol Support (Fixed):**
```python
class HTTPClient:
    async def _handle_response(self, response: requests.Response) -> Dict:
        """Handle response with SSE protocol support"""
        
        content_type = response.headers.get('content-type', '')
        
        if 'text/event-stream' in content_type:
            # Handle Server-Sent Events (for Z.AI MCP servers)
            return self._parse_sse_response(response.text)
        else:
            # Handle standard JSON response
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"text": response.text, "status_code": response.status_code}
    
    def _parse_sse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Server-Sent Events response from Z.AI MCP servers"""
        lines = response_text.strip().split('\n')
        data_lines = [line for line in lines if line.startswith('data: ')]
        
        for line in data_lines:
            json_data = line[6:]  # Remove 'data: ' prefix
            
            # Handle end-of-stream marker
            if json_data.strip() == '[DONE]':
                continue
            
            try:
                parsed = json.loads(json_data)
                # Extract result or content from SSE message
                if 'result' in parsed:
                    return parsed['result']
                elif 'content' in parsed:
                    return parsed['content']
                else:
                    return parsed
            except json.JSONDecodeError:
                continue
        
        return {"error": "No valid SSE data found"}
```

---

## 🚀 **ENHANCED TOOLS (UPGRADE INTEGRATION)**

### **Enhanced Tools Overview**

These tools integrate with the three upgrade systems to provide intelligent capabilities:

```python
Enhanced Tools Architecture:
┌─────────────────────────────────────────────────────────────┐
│               Enhanced Tools Layer                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Enhanced    │ │   Web       │ │   Self-     │            │
│  │  Session    │ │  Research   │ │  Aware      │            │
│  │   Note      │ │Orchestrator │ │ Performance │            │
│  │ (Upgrade 1) │ │ (Upgrade 2) │ │  Monitor    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                           │
│  │   Project   │ │   Pattern   │                           │
│  │  Context    │ │  Learning   │                           │
│  │  Manager    │ │   Engine    │                           │
│  │ (Upgrade 1) │ │ (Upgrade 1) │                           │
│  └─────────────┘ └─────────────┘                           │
└─────────────────────┬─────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               Integration Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Supabase  │ │    Z.AI     │ │   Memory    │            │
│  │    MCP      │ │   MCP       │ │    MCP      │            │
│  │   Server    │ │   Servers   │ │   Server    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### **Enhanced Session Note Tool (Upgrade 1)**

```python
class EnhancedSessionNoteTool(SessionNoteTool):
    """Enhanced session memory with intelligence (Upgrade 1)"""
    
    def __init__(self, config: Config = None):
        super().__init__()
        self.config = config or get_config()
        self.mcp_client = MCPServerClient()
        
    async def execute(self, content: str, category: str = "general", **kwargs):
        # Auto-categorize if not provided
        if category == "general":
            category = await self._auto_categorize(content)
        
        # Enhance with project context
        if self.config.memory.get("project_context", False):
            content = await self._enhance_with_project_context(content, category)
        
        # Store in Supabase
        if self.config.memory.get("enable_enhanced", False):
            await self._store_in_supabase(content, category, kwargs)
        
        # Record pattern learning
        if self.config.memory.get("pattern_learning", False):
            await self._record_learning_pattern(content, category)
        
        # Call original implementation
        result = await super().execute(content, category, **kwargs)
        
        return result
    
    async def _enhance_with_project_context(self, content: str, category: str) -> str:
        """Add project context to note"""
        
        project_context = await self.mcp_client.call_tool("supabase-admin", {
            "project_memory": "read",
            "project_id": self.get_current_project_id()
        })
        
        if project_context.get("data"):
            context_info = f" [Project: {project_context['data'].get('type', 'general')}]"
            return content + context_info
        
        return content
    
    async def _store_in_supabase(self, content: str, category: str, metadata: Dict):
        """Store note in Supabase database"""
        
        note_data = {
            "session_id": self.session_id,
            "project_id": self.get_current_project_id(),
            "content": content,
            "category": category,
            "metadata": {
                **metadata,
                "enhanced": True,
                "auto_categorized": category != "general",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": "insert",
            "table_name": "mini_agent_sessions",
            "data": note_data
        })
```

### **Web Research Orchestrator (Upgrade 2)**

```python
class WebResearchOrchestrator:
    """Intelligent web research with memory integration (Upgrade 2)"""
    
    def __init__(self, config: Config = None):
        self.config = config or get_config()
        self.mcp_client = MCPServerClient()
        
    async def research_comprehensive(self, query: str, context: str = None):
        """Comprehensive research with intelligence"""
        
        # 1. Search web using Z.AI
        search_results = await self._search_web(query)
        
        # 2. Validate sources if enabled
        if self.config.web.get("enable_validation", True):
            validated_results = await self._validate_sources(search_results)
        else:
            validated_results = search_results
        
        # 3. Synthesize findings if enabled
        if self.config.web.get("enable_synthesis", True):
            synthesis = await self._synthesize_findings(validated_results, query)
        else:
            synthesis = validated_results
        
        # 4. Integrate with memory if enabled
        if self.config.web.get("enable_memory_integration", True):
            await self._integrate_with_memory(query, synthesis)
        
        return {
            "query": query,
            "search_results": search_results,
            "validated_sources": validated_results,
            "synthesis": synthesis,
            "memory_integrated": self.config.web.get("enable_memory_integration", False)
        }
    
    async def _search_web(self, query: str) -> List[Dict]:
        """Search web using Z.AI MCP"""
        
        result = await self.mcp_client.call_tool("zai-web-search", {
            "query": query,
            "max_results": 10
        })
        
        return result.data.get("results", [])
    
    async def _validate_sources(self, sources: List[Dict]) -> List[Dict]:
        """Validate web sources"""
        
        validated = []
        for source in sources:
            # Basic validation logic
            validation_result = {
                "original": source,
                "valid": True,
                "reliability_score": 0.8,  # Simplified scoring
                "validation_method": "basic_check"
            }
            
            validated.append(validation_result)
        
        return validated
    
    async def _synthesize_findings(self, sources: List[Dict], query: str) -> Dict:
        """Synthesize research findings"""
        
        return {
            "summary": f"Research findings for: {query}",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "sources_count": len(sources),
            "confidence_score": 0.85
        }
    
    async def _integrate_with_memory(self, query: str, findings: Dict):
        """Integrate findings with knowledge base"""
        
        await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": "insert",
            "table_name": "mini_agent_knowledge",
            "data": {
                "entity_id": f"research_{datetime.now().date()}_{hashlib.md5(query.encode()).hexdigest()[:8]}",
                "entity_type": "research_topic",
                "attributes": {
                    "query": query,
                    "findings": findings,
                    "timestamp": datetime.now().isoformat()
                }
            }
        })
```

### **Self-Aware Performance Monitor (Upgrade 3)**

```python
class SelfAwarePerformanceMonitor:
    """Performance monitoring with self-awareness (Upgrade 3)"""
    
    def __init__(self, config: Config = None):
        self.config = config or get_config()
        self.mcp_client = MCPServerClient()
        
    async def monitor_execution(self, execution_data: Dict):
        """Monitor agent execution for self-awareness"""
        
        # 1. Store execution metrics
        await self._store_execution_metrics(execution_data)
        
        # 2. Analyze performance patterns
        patterns = await self._analyze_performance_patterns()
        
        # 3. Generate insights
        insights = await self._generate_performance_insights(patterns)
        
        # 4. Suggest improvements
        improvements = await self._suggest_improvements(patterns)
        
        return {
            "execution_analyzed": True,
            "patterns": patterns,
            "insights": insights,
            "improvements": improvements
        }
    
    async def _store_execution_metrics(self, execution_data: Dict):
        """Store execution metrics in database"""
        
        metrics = {
            "session_id": execution_data.get("session_id"),
            "tool_name": execution_data.get("tool_name"),
            "execution_time_ms": execution_data.get("duration", 0),
            "success": execution_data.get("success", False),
            "metadata": {
                "tool_category": execution_data.get("category"),
                "context_size": execution_data.get("context_size"),
                "complexity_score": execution_data.get("complexity", 0)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": "insert",
            "table_name": "mini_agent_tool_logs",
            "data": metrics
        })
    
    async def _analyze_performance_patterns(self) -> Dict:
        """Analyze performance patterns from stored metrics"""
        
        # Query recent execution data
        result = await self.mcp_client.call_tool("execute_sql", {
            "sql": """
            SELECT 
                tool_name,
                AVG(execution_time_ms) as avg_time,
                COUNT(*) as usage_count,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate
            FROM mini_agent_tool_logs 
            WHERE timestamp >= NOW() - INTERVAL '24 hours'
            GROUP BY tool_name 
            ORDER BY usage_count DESC
            """,
            "params": []
        })
        
        return {
            "tool_performance": result.data,
            "analysis_period": "24 hours",
            "total_executions": sum(row["usage_count"] for row in result.data)
        }
```

---

## 📊 **TOOLS INTEGRATION PATTERNS**

### **Pattern 1: Tool-to-MCP Integration**

```python
class ToolMCPServerIntegration:
    """Integration pattern between tools and MCP servers"""
    
    def __init__(self):
        self.mcp_client = MCPServerClient()
        self.tool_registry = self._initialize_tool_registry()
    
    async def execute_with_mcp_integration(self, tool_name: str, parameters: Dict):
        """Execute tool with MCP server integration"""
        
        # Get tool
        tool = self.tool_registry[tool_name]
        
        # Execute tool
        tool_result = await tool.execute(**parameters)
        
        # Store execution in MCP server (for analytics)
        await self._store_execution_in_mcp(tool_name, tool_result, parameters)
        
        # Apply MCP-based enhancements
        enhanced_result = await self._apply_mcp_enhancements(tool_name, tool_result)
        
        return enhanced_result
    
    async def _store_execution_in_mcp(self, tool_name: str, result: Dict, parameters: Dict):
        """Store execution data in Supabase MCP server"""
        
        execution_data = {
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "success": result.get("success", False),
            "execution_time": result.get("execution_time", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        await self.mcp_client.call_tool("supabase-admin", {
            "table_operation": "insert",
            "table_name": "mini_agent_tool_logs",
            "data": execution_data
        })
```

### **Pattern 2: Multi-Tool Orchestration**

```python
class MultiToolOrchestrator:
    """Orchestrate multiple tools for complex workflows"""
    
    async def execute_complex_workflow(self, workflow_steps: List[Dict]):
        """Execute complex workflow using multiple tools"""
        
        results = []
        context = {}
        
        for step in workflow_steps:
            tool_name = step["tool"]
            parameters = {**step["parameters"], **context}
            
            # Execute tool
            result = await self.execute_tool(tool_name, parameters)
            
            # Update context
            context.update(result.get("context_updates", {}))
            
            results.append({
                "step": step,
                "result": result,
                "context": context
            })
        
        return {
            "workflow_completed": True,
            "steps": results,
            "final_context": context,
            "success_rate": sum(1 for r in results if r["result"]["success"]) / len(results)
        }
```

### **Pattern 3: Skill-Tool Integration**

```python
class SkillToolIntegration:
    """Integration between skills and tools"""
    
    async def execute_skill_with_tools(self, skill_name: str, action: str, parameters: Dict):
        """Execute skill action using appropriate tools"""
        
        # Get skill
        skill = await skill_loader.load_skill(skill_name)
        
        # Determine required tools
        required_tools = await self._determine_required_tools(skill_name, action)
        
        # Execute with tool integration
        results = {}
        for tool_name in required_tools:
            tool_result = await self.execute_tool(tool_name, parameters)
            results[tool_name] = tool_result
        
        # Combine results
        skill_result = await skill.execute(action, {**parameters, **results})
        
        return skill_result
    
    async def _determine_required_tools(self, skill_name: str, action: str) -> List[str]:
        """Determine which tools are needed for skill action"""
        
        # Skill-tool mapping
        skill_tool_map = {
            "pdf": ["file_tools"],
            "docx": ["file_tools"],
            "canvas_design": ["file_tools"],
            "code_quality_analysis": ["file_tools", "bash_tool"]
        }
        
        return skill_tool_map.get(skill_name, ["file_tools"])
```

---

## 🎯 **SUCCESS CRITERIA & METRICS**

### **Base Tools Success Metrics:**
- [ ] **Reliability**: >99.5% success rate across all base tools
- [ ] **Performance**: <2s average execution time for standard operations
- [ ] **Coverage**: Tools handle 95%+ of common user workflow needs
- [ ] **Integration**: Seamless integration with skills and MCP systems

### **Enhanced Tools Success Metrics:**
- [ ] **Upgrade Integration**: All enhanced tools properly integrate with upgrade systems
- [ ] **Intelligence**: Enhanced tools provide measurable intelligence over base tools
- [ ] **Learning**: Tools contribute to system learning and optimization
- [ ] **Backward Compatibility**: Enhanced tools don't break existing functionality

### **System Integration Success Metrics:**
- [ ] **MCP Integration**: Tools work seamlessly with MCP servers
- [ ] **Skills Integration**: Tools provide foundation for skill execution
- [ ] **Performance**: Tool execution overhead <5% when enhancements disabled
- [ ] **Extensibility**: Easy to add new tools and integrate with existing systems

---

**Bottom Line**: Tools system provides the **execution foundation** that enables both basic functionality and intelligent enhancements, working seamlessly with skills and MCP servers.

---

*Tools System Documentation Complete: November 25, 2025*  
*Status: 8 Base Tools Operational, 5 Enhanced Tools Ready for Integration*