# 🔄 Mini-Agent System - Mermaid Diagram Visualizations

## 1. **System Architecture Flowchart**

```mermaid
graph TB
    subgraph "User Interface"
        UI[User Request]
    end
    
    subgraph "Core System"
        CORE[Mini-Agent Core]
        ROUTER[Task Router]
        STATE[State Manager]
        ERROR[Error Handler]
    end
    
    subgraph "Skills Framework"
        SKILLS[14+ Specialized Skills]
        
        subgraph "Design Skills"
            DESIGN[Canvas Design<br/>Algorithmic Art<br/>Brand Guidelines]
        end
        
        subgraph "Document Skills"
            DOC[PDF Processing<br/>PowerPoint<br/>Word Documents]
        end
        
        subgraph "Web Skills"
            WEB[Web Testing<br/>Artifacts Builder<br/>React Components]
        end
        
        subgraph "Integration Skills"
            INTEGRATION[MCP Builder<br/>VS Code Integration<br/>Slack GIF]
        end
    end
    
    subgraph "Integration Layer"
        OPENAI[OpenAI APIs]
        MINIMAX[MiniMax GLM]
        ZAI[Z.AI Platform]
        GITHUB[GitHub Integration]
    end
    
    subgraph "Documentation System"
        DOCS[Organized Documentation<br/>100+ Files]
        VISUALS[Visual Guides<br/>System Diagrams]
        INDEX[Master Index<br/>Quick Start]
    end
    
    UI --> CORE
    CORE --> ROUTER
    ROUTER --> SKILLS
    SKILLS --> DESIGN
    SKILLS --> DOC
    SKILLS --> WEB
    SKILLS --> INTEGRATION
    
    ROUTER --> OPENAI
    ROUTER --> MINIMAX
    ROUTER --> ZAI
    ROUTER --> GITHUB
    
    CORE --> DOCS
    SKILLS --> VISUALS
    ROUTER --> INDEX
    
    OPENAI --> DOC
    MINIMAX --> DESIGN
    ZAI --> INTEGRATION
    GITHUB --> WEB
    
    DOCS --> VISUALS
    VISUALS --> INDEX
```

## 2. **Skills Network Relationship Diagram**

```mermaid
graph TD
    subgraph "Central Hub"
        HUB[Mini-Agent Core Hub]
    end
    
    subgraph "Design & Visual Category"
        D1[Canvas Design]
        D2[Algorithmic Art]
        D3[Brand Guidelines]
        D4[Theme Factory]
        
        D1 -.-> D2
        D2 -.-> D3
        D3 -.-> D4
    end
    
    subgraph "Document & Content Category"
        DOC1[PDF Skills]
        DOC2[PowerPoint Skills]
        DOC3[Word Skills]
        DOC4[Office Integration]
        
        DOC1 -.-> DOC2
        DOC2 -.-> DOC3
        DOC3 -.-> DOC4
    end
    
    subgraph "Web & Testing Category"
        WEB1[Web Testing]
        WEB2[Artifacts Builder]
        WEB3[React Components]
        WEB4[UI Testing]
        
        WEB1 -.-> WEB2
        WEB2 -.-> WEB3
        WEB3 -.-> WEB4
    end
    
    subgraph "Integration & Tools Category"
        INT1[MCP Builder]
        INT2[VS Code Integration]
        INT3[Slack GIF Creator]
        INT4[Internal Communications]
        
        INT1 -.-> INT2
        INT2 -.-> INT3
        INT3 -.-> INT4
    end
    
    subgraph "Development & Workflow Category"
        DEV1[Skill Creator]
        DEV2[Code Quality]
        DEV3[Fact Checking]
        DEV4[Assessment Tools]
        
        DEV1 -.-> DEV2
        DEV2 -.-> DEV3
        DEV3 -.-> DEV4
    end
    
    HUB --> D1
    HUB --> DOC1
    HUB --> WEB1
    HUB --> INT1
    HUB --> DEV1
    
    D1 --> D2
    DOC1 --> DOC2
    WEB1 --> WEB2
    INT1 --> INT2
    DEV1 --> DEV2
```

## 3. **Data Flow Sequence Diagram**

```mermaid
sequenceDiagram
    participant User
    participant Core as Mini-Agent Core
    participant Router as Task Router
    participant Skill as Skills Framework
    participant Integr as Integration Layer
    participant Output as Results
    
    User->>Core: Send Request
    Core->>Router: Route Task
    Router->>Skill: Execute Skill
    
    alt Canvas Design Request
        Skill->>Integr: Canvas Design Tool
        Integr->>Integr: Create Visual Artifact
        Skill-->>Router: Return Visual Result
    else Document Request
        Skill->>Integr: PDF/PPT Tools
        Integr->>Integr: Process Documents
        Skill-->>Router: Return Documents
    else Web Testing Request
        Skill->>Integr: Web Testing Framework
        Integr->>Integr: Run Tests
        Skill-->>Router: Return Test Results
    end
    
    Router->>Output: Format Results
    Output-->>User: Return Response
```

## 4. **Component Dependency Diagram**

```mermaid
graph LR
    subgraph "Foundation Layer"
        CORE[Mini-Agent Core]
        CONFIG[Configuration]
        LLM[LLM Integration]
    end
    
    subgraph "Application Layer"
        SKILLS[Skills Framework]
        TOOLS[Tools & Utilities]
        SCHEMA[Schema & Validation]
    end
    
    subgraph "Integration Layer"
        OPENAI[OpenAI APIs]
        MINIMAX[MiniMax GLM]
        ZAI[Z.AI Platform]
        GITHUB[GitHub]
    end
    
    subgraph "Documentation Layer"
        DOCS[Documentation]
        EXAMPLES[Examples]
        TESTS[Testing]
    end
    
    CORE --> SKILLS
    CONFIG --> CORE
    LLM --> CORE
    
    SKILLS --> TOOLS
    SCHEMA --> TOOLS
    
    SKILLS --> OPENAI
    SKILLS --> MINIMAX
    SKILLS --> ZAI
    SKILLS --> GITHUB
    
    CORE --> DOCS
    SKILLS --> EXAMPLES
    CORE --> TESTS
```

## 5. **System Capabilities Mind Map**

```mermaid
mindmap
  root((Mini-Agent System))
    Core Capabilities
      Task Routing
      State Management
      Error Handling
      AI Integration
    
    Visual Skills
      Canvas Design
      Algorithmic Art
      Brand Guidelines
      Visual Reports
    
    Document Skills
      PDF Creation
      PowerPoint Design
      Word Processing
      Office Integration
    
    Web Skills
      Web Testing
      UI Testing
      Component Testing
      Integration Testing
    
    Development Skills
      Code Quality
      Fact Checking
      Assessment Tools
      Skill Creation
    
    Integration Skills
      MCP Building
      VS Code Extension
      API Integration
      Platform Connection
    
    Documentation
      System Guides
      Visual Diagrams
      Architecture Docs
      Quick References
```

## 6. **Deployment Architecture Diagram**

```mermaid
graph TB
    subgraph "Development Environment"
        DEV[VS Code Extension]
        SCRIPT[Development Scripts]
        TEST[Testing Framework]
    end
    
    subgraph "Core System"
        CORE[Mini-Agent Core]
        CONFIG[Configuration Management]
        ENV[Python Environment]
    end
    
    subgraph "Skills Framework"
        DESIGN_SKILLS[Design Skills]
        DOC_SKILLS[Document Skills]
        WEB_SKILLS[Web Skills]
        DEV_SKILLS[Development Skills]
    end
    
    subgraph "External Integrations"
        OPENAI[OpenAI Platform]
        MINIMAX[MiniMax Platform]
        ZAI[Z.AI Platform]
        GITHUB[GitHub Platform]
    end
    
    subgraph "Documentation System"
        ORGANIZED[Organized Docs<br/>100+ Files]
        VISUALS[Visual Guides]
        INDEX[Navigation System]
    end
    
    DEV --> SCRIPT
    SCRIPT --> TEST
    TEST --> CORE
    
    CORE --> CONFIG
    CONFIG --> ENV
    
    CORE --> DESIGN_SKILLS
    CORE --> DOC_SKILLS
    CORE --> WEB_SKILLS
    CORE --> DEV_SKILLS
    
    DESIGN_SKILLS --> OPENAI
    DOC_SKILLS --> MINIMAX
    WEB_SKILLS --> ZAI
    DEV_SKILLS --> GITHUB
    
    CORE --> ORGANIZED
    ORGANIZED --> VISUALS
    VISUALS --> INDEX
```

## 💡 **Mermaid Usage Benefits**
- ✅ **GitHub Compatible** - Renders in GitHub/VS Code
- ✅ **Version Controlled** - Text-based, easy to maintain
- ✅ **Interactive** - Clickable elements, zoom, pan
- ✅ **Professional** - Clean, technical documentation
- ✅ **Multiple Types** - Flowcharts, sequence, mind maps
