# 🔄 Mermaid Interactive Diagrams - Mini-Agent System

These diagrams render natively in GitHub, VS Code, and many markdown viewers.

## System Architecture Overview

```mermaid
graph TB
    User[👤 User Input]
    
    subgraph "Mini-Agent Core"
        CLI[CLI Interface]
        VSCode[VS Code Extension]
        Config[Configuration Manager]
        Orchestrator[Tool Orchestrator]
        SkillLoader[Skill Loader]
    end
    
    subgraph "LLM Providers"
        OpenAI[OpenAI GPT-4]
        MiniMax[MiniMax GLM-4.6]
        ZAI[Z.AI Coding Plan]
    end
    
    subgraph "Specialized Skills"
        DocSkills[Document Skills<br/>pdf, docx, pptx, xlsx]
        VisualSkills[Visual Skills<br/>canvas-design, algorithmic-art]
        DevSkills[Development Skills<br/>mcp-builder, webapp-testing]
        UtilitySkills[Utility Skills<br/>fact-checking, theme-factory]
    end
    
    subgraph "External Tools"
        WebSearch[Web Search API]
        WebReader[Web Reader API]
        FileOps[File Operations]
        GitOps[Git Commands]
    end
    
    User --> CLI
    User --> VSCode
    CLI --> Config
    VSCode --> Config
    Config --> Orchestrator
    Orchestrator --> SkillLoader
    Orchestrator --> OpenAI
    Orchestrator --> MiniMax
    Orchestrator --> ZAI
    SkillLoader --> DocSkills
    SkillLoader --> VisualSkills
    SkillLoader --> DevSkills
    SkillLoader --> UtilitySkills
    Orchestrator --> WebSearch
    Orchestrator --> WebReader
    Orchestrator --> FileOps
    Orchestrator --> GitOps
    
    style User fill:#e1f5ff
    style CLI fill:#ffe1f5
    style VSCode fill:#ffe1f5
    style Config fill:#fff4e1
    style Orchestrator fill:#fff4e1
    style SkillLoader fill:#fff4e1
    style OpenAI fill:#e8f5e9
    style MiniMax fill:#e8f5e9
    style ZAI fill:#e8f5e9
```

## Skill Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant SkillLoader
    participant Skill
    participant LLM
    participant Tools
    
    User->>Orchestrator: Request task
    Orchestrator->>SkillLoader: Identify required skill
    SkillLoader->>Skill: Load skill definition
    Skill-->>SkillLoader: Skill loaded
    SkillLoader-->>Orchestrator: Skill ready
    
    loop Task Execution
        Orchestrator->>LLM: Get guidance from skill
        LLM-->>Orchestrator: Action plan
        Orchestrator->>Tools: Execute tool calls
        Tools-->>Orchestrator: Results
        Orchestrator->>Skill: Apply skill logic
        Skill-->>Orchestrator: Processed output
    end
    
    Orchestrator-->>User: Final result
```

## Document Skill Architecture

```mermaid
graph LR
    subgraph "Document Processing Skills"
        PDF[PDF Skill]
        DOCX[DOCX Skill]
        PPTX[PPTX Skill]
        XLSX[XLSX Skill]
    end
    
    subgraph "Python Libraries"
        PyPDF[pypdf]
        PyDocx[python-docx]
        PyPPTX[python-pptx]
        OpenPyXL[openpyxl]
    end
    
    subgraph "Common Operations"
        Extract[Text Extraction]
        Create[Document Creation]
        Edit[Content Editing]
        Format[Formatting]
        Analyze[Data Analysis]
    end
    
    PDF --> PyPDF
    DOCX --> PyDocx
    PPTX --> PyPPTX
    XLSX --> OpenPyXL
    
    PyPDF --> Extract
    PyDocx --> Create
    PyPPTX --> Edit
    OpenPyXL --> Analyze
    
    Extract --> Format
    Create --> Format
    Edit --> Format
    
    style PDF fill:#ff9999
    style DOCX fill:#99ccff
    style PPTX fill:#ffcc99
    style XLSX fill:#99ff99
```

## State Machine - Skill Loading

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> CheckCache: Skill requested
    CheckCache --> LoadFromCache: Skill cached
    CheckCache --> LoadFromDisk: Not cached
    LoadFromDisk --> Validate: File read
    Validate --> Cache: Valid
    Validate --> Error: Invalid
    LoadFromCache --> Ready
    Cache --> Ready
    Ready --> Executing: Execute skill
    Executing --> Ready: Task complete
    Ready --> Idle: Unload
    Error --> Idle: Reset
```

## Data Flow - Web Search Integration

```mermaid
flowchart TD
    Start([User Query]) --> WebTool{Web Tool<br/>Selection}
    
    WebTool --> |Need snippets| Search[Web Search API]
    WebTool --> |Need full content| Reader[Web Reader API]
    
    Search --> ParseSnippets[Parse Search Results]
    Reader --> ParseContent[Extract Full Content]
    
    ParseSnippets --> Format[Format Response]
    ParseContent --> Format
    
    Format --> Cache[Cache Results]
    Cache --> Return([Return to User])
    
    style Start fill:#e1f5ff
    style Return fill:#c8e6c9
    style WebTool fill:#fff4e1
    style Search fill:#ffe1f5
    style Reader fill:#ffe1f5
```

## Component Dependency Graph

```mermaid
graph TD
    subgraph "Layer 1: Core Infrastructure"
        Config[Configuration<br/>YAML + ENV]
        Utils[Utilities<br/>credit_protection]
    end
    
    subgraph "Layer 2: Integrations"
        LLM[LLM Clients<br/>OpenAI, MiniMax, Z.AI]
        Tools[External Tools<br/>Web, File, Git]
    end
    
    subgraph "Layer 3: Skills Framework"
        SkillBase[Skill Base System]
        DocSkills[Document Skills]
        VisualSkills[Visual Skills]
        DevSkills[Dev Skills]
    end
    
    subgraph "Layer 4: User Interface"
        CLI[Command Line]
        VSCode[VS Code Extension]
        API[Python API]
    end
    
    Config --> LLM
    Config --> Tools
    Utils --> LLM
    LLM --> SkillBase
    Tools --> SkillBase
    SkillBase --> DocSkills
    SkillBase --> VisualSkills
    SkillBase --> DevSkills
    DocSkills --> CLI
    VisualSkills --> CLI
    DevSkills --> CLI
    DocSkills --> VSCode
    VisualSkills --> VSCode
    DevSkills --> VSCode
    DocSkills --> API
    VisualSkills --> API
    DevSkills --> API
    
    style Config fill:#e3f2fd
    style Utils fill:#e3f2fd
    style LLM fill:#f3e5f5
    style Tools fill:#f3e5f5
    style SkillBase fill:#e8f5e9
    style DocSkills fill:#fff9c4
    style VisualSkills fill:#fff9c4
    style DevSkills fill:#fff9c4
```

## Z.AI Credit Protection System

```mermaid
graph TB
    Request[User Request] --> Check{Credit<br/>Protection<br/>Enabled?}
    
    Check --> |Yes| Monitor[Monitor Token Usage]
    Check --> |No| DirectCall[Direct Z.AI Call]
    
    Monitor --> Estimate[Estimate Token Cost]
    Estimate --> SafetyCheck{Within<br/>Quota?}
    
    SafetyCheck --> |Yes| Execute[Execute Request]
    SafetyCheck --> |No| Fallback[Use Fallback LLM]
    
    Execute --> Log[Log Usage]
    Fallback --> Log
    DirectCall --> Log
    
    Log --> Return[Return Result]
    
    style Request fill:#e1f5ff
    style Check fill:#fff4e1
    style Monitor fill:#e8f5e9
    style SafetyCheck fill:#ffccbc
    style Execute fill:#c8e6c9
    style Fallback fill:#fff9c4
```

---

## How to Use These Diagrams

1. **GitHub**: Commit this file - diagrams render automatically
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Standalone**: Use [Mermaid Live Editor](https://mermaid.live)
4. **Export**: Most viewers support exporting to SVG/PNG

## Diagram Legend

| Color | Meaning |
|-------|---------|
| 🔵 Blue | User interaction points |
| 🟣 Purple | Core system components |
| 🟢 Green | LLM providers / execution |
| 🟡 Yellow | Skills and specialized modules |
| 🔴 Orange | Decision points / validation |

---

*These interactive diagrams update automatically when viewed in compatible markdown renderers.*
*Best viewed in: GitHub, VS Code with Mermaid extension, or mermaid.live*
