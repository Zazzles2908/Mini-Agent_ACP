# 🧠 Knowledge Graph Representation - Mini-Agent System

This visualization uses the native knowledge graph system to represent Mini-Agent's architecture as interconnected entities and relationships.

## Entity Types

### 1️⃣ **Infrastructure Components** (Foundation Layer)
- Configuration Manager
- Utility Modules
- Credit Protection System

### 2️⃣ **LLM Providers** (Intelligence Layer)
- OpenAI GPT
- MiniMax GLM
- Z.AI Coding Plan

### 3️⃣ **External Tools** (Capability Layer)
- Web Search
- Web Reader
- File Operations
- Git Commands

### 4️⃣ **Skills** (Specialized Capabilities)
- Document Skills: PDF, DOCX, PPTX, XLSX
- Visual Skills: Canvas Design, Algorithmic Art
- Development Skills: MCP Builder, Webapp Testing
- Utility Skills: Fact Checking, Theme Factory, etc.

### 5️⃣ **User Interfaces** (Interaction Layer)
- CLI Interface
- VS Code Extension
- Python API

## Relationship Types

- **depends_on**: Component A requires Component B to function
- **provides**: Component A offers services to Component B
- **integrates_with**: Component A works alongside Component B
- **uses**: Component A utilizes Component B as a tool
- **manages**: Component A oversees Component B

## Graph Structure Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE GRAPH VIEW                          │
└─────────────────────────────────────────────────────────────────────┘

[Configuration Manager] ──depends_on──> [Environment Variables]
                       └──provides────> [LLM Providers]
                       └──provides────> [Tools]

[Credit Protection] ──manages──> [Z.AI Usage]
                   └──monitors──> [Token Consumption]

[OpenAI GPT] ──provides──> [Document Skills]
            └──integrates_with──> [Web Tools]

[MiniMax GLM] ──provides──> [Visual Skills]
             └──integrates_with──> [Canvas Design]

[Z.AI Coding Plan] ──provides──> [Web Search]
                  └──provides──> [Web Reader]
                  └──uses──> [Credit Protection]

[Web Search] ──used_by──> [Fact Checking]
            └──used_by──> [MCP Builder]

[PDF Skill] ──uses──> [File Operations]
           └──uses──> [OpenAI GPT]
           └──used_by──> [CLI Interface]

[Canvas Design] ──uses──> [MiniMax GLM]
               └──follows──> [Design Philosophy]
               └──produces──> [Visual Artifacts]

[Algorithmic Art] ──uses──> [p5.js Library]
                 └──follows──> [Algorithmic Philosophy]
                 └──produces──> [Interactive HTML]

[CLI Interface] ──accesses──> [All Skills]
               └──uses──> [Configuration Manager]

[VS Code Extension] ──integrates_with──> [MCP Builder]
                   └──accesses──> [Document Skills]

[Python API] ──exposes──> [Skills Framework]
            └──uses──> [Direct Imports]
```

## Query Examples

### "What does Canvas Design depend on?"
- **Direct**: MiniMax GLM (LLM provider)
- **Indirect**: Configuration Manager, Utility Modules
- **Philosophy**: Design Philosophy documentation
- **Output**: Visual Artifacts (PNG/PDF)

### "What skills use Web Search?"
- Fact Checking (validation)
- Research Analysis
- Content Discovery
- MCP Builder (documentation lookup)

### "What are the paths from User to PDF processing?"
1. **CLI** → Skills Framework → PDF Skill → File Operations
2. **VS Code** → MCP Server → PDF Skill → pypdf library
3. **Python API** → Direct Import → PDF Skill → OpenAI GPT

## Entity-Relationship Matrix

| Entity Type | Count | Primary Relations | Key Dependencies |
|-------------|-------|-------------------|------------------|
| Infrastructure | 3 | provides, manages | None (foundation) |
| LLM Providers | 3 | provides, integrates | Configuration |
| Tools | 4 | used_by, uses | Configuration |
| Skills | 14 | uses, produces | LLM + Tools |
| User Interfaces | 3 | accesses, exposes | Skills Framework |

## Knowledge Graph Benefits

### For Understanding
- **Trace dependencies**: Follow any component to its requirements
- **Discover capabilities**: Find all skills using a specific tool
- **Map data flow**: Track information from user to output

### For Development
- **Impact analysis**: Changes to Config affect what?
- **Integration planning**: What does a new skill need?
- **Debugging**: Trace error paths through relationships

### For Documentation
- **Automatic diagrams**: Generate visuals from graph
- **Relationship tracking**: Document evolves with code
- **Context preservation**: Entity observations capture knowledge

## Interactive Queries

To explore this knowledge graph programmatically:

```python
from mini_agent.knowledge import search_nodes, open_nodes

# Find all document skills
results = search_nodes("PDF DOCX PPTX XLSX")

# Get details on specific component
config_details = open_nodes(["Configuration Manager"])

# Explore relationships
llm_providers = search_nodes("LLM provider")
```

---

## Visual Metaphor

Think of the Knowledge Graph as:
- **Neural Network**: Nodes are neurons, edges are synapses
- **Ecosystem**: Components are species, relationships are food chains
- **City Map**: Entities are buildings, relationships are roads
- **Family Tree**: Components are members, relationships are lineage

The graph captures not just *what exists* but *how it all fits together*.

---

*This knowledge representation complements the other 6 visualization types by providing queryable, machine-readable structure.*
*Generated: November 22, 2025*
