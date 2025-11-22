# Mermaid Interactive System Diagram

## Flowchart: System Architecture

```mermaid
flowchart TD
    USER[👤 User Input] --> ROUTER[🧠 Skill Router]
    
    ROUTER --> DOC[📄 Document Skills]
    ROUTER --> WEB[🌐 Web & Testing Skills]
    ROUTER --> CREATIVE[🎨 Creative Skills]
    ROUTER --> DEV[🛠️ Development Skills]
    ROUTER --> QUALITY[✅ Quality Skills]
    ROUTER --> BRAND[🎯 Template & Branding]
    ROUTER --> UTIL[🔧 Utility Skills]
    
    DOC --> DOX[📝 DOCX Skill]
    DOC --> PDF[📄 PDF Skill]
    DOC --> PPT[📊 PPTX Skill]
    DOC --> XLS[📈 XLSX Skill]
    
    WEB --> WEBTEST[🧪 WebApp Testing]
    WEB --> SEARCH[🔍 Search & API]
    
    CREATIVE --> CANVAS[🎨 Canvas Design]
    CREATIVE --> ART[🎯 Algorithmic Art]
    
    DEV --> MCP[🔗 MCP Builder]
    DEV --> SKILL[⚙️ Skill Creator]
    
    QUALITY --> FACT[🔍 Fact Checking]
    QUALITY --> ASSESS[📊 Self Assessment]
    
    BRAND --> BRAND_GUIDE[📐 Brand Guidelines]
    BRAND --> THEME[🎨 Theme Factory]
    
    UTIL --> SLACK[💬 Slack GIF]
    UTIL --> TEMPLATE[📋 Template Skill]
    UTIL --> VSCODE[💻 VS Code Integration]
    
    DOX --> DOCS[(📁 Documents)]
    PDF --> DOCS
    PPT --> DOCS
    XLS --> DOCS
    CANVAS --> DOCS
    ART --> DOCS
    MCP --> MINIA[(🔧 Mini-Agent Framework)]
    SKILL --> MINIA
    FACT --> QUALITY_OUT[(✅ Quality Output)]
    ASSESS --> QUALITY_OUT
    
    DOCS --> OUTPUT[📤 Final Output]
    QUALITY_OUT --> OUTPUT
    
    style USER fill:#e1f5fe
    style ROUTER fill:#f3e5f5
    style DOCS fill:#e8f5e8
    style OUTPUT fill:#fff3e0
```

## Class Diagram: Skills Framework

```mermaid
classDiagram
    class SkillFramework {
        +load_skill(skill_name)
        +execute_skill(skill_name, params)
        +list_skills()
    }
    
    class DocumentSkill {
        +create_document()
        +edit_document()
        +format_document()
    }
    
    class CreativeSkill {
        +generate_visual()
        +apply_theme()
        +create_art()
    }
    
    class DevelopmentSkill {
        +build_mcp()
        +create_skill()
        +integrate_tool()
    }
    
    class UtilitySkill {
        +create_gif()
        +apply_brand()
        +test_webapp()
    }
    
    SkillFramework --> DocumentSkill
    SkillFramework --> CreativeSkill
    SkillFramework --> DevelopmentSkill
    SkillFramework --> UtilitySkill
```

## Sequence Diagram: Document Processing Flow

```mermaid
sequenceDiagram
    participant User
    participant Router
    participant DocumentSkill
    participant CanvasDesign
    participant Output
    
    User->>Router: Request document creation
    Router->>DocumentSkill: Load document processing skill
    DocumentSkill->>DocumentSkill: Process document structure
    DocumentSkill->>CanvasDesign: Request visual design
    CanvasDesign->>CanvasDesign: Generate visual elements
    CanvasDesign->>DocumentSkill: Return design elements
    DocumentSkill->>DocumentSkill: Integrate design into document
    DocumentSkill->>Output: Final document output
    Output->>User: Deliver completed document
```

## System Architecture Timeline

```mermaid
gantt
    title Mini-Agent Development Timeline
    dateFormat YYYY-MM-DD
    section Core Framework
    Skills Architecture     :active, core1, 2024-11-20, 1d
    Tool Integration       :core2, after core1, 1d
    Configuration System   :core3, after core2, 1d
    
    section Skills Modules
    Document Skills        :skills1, after core1, 2d
    Creative Skills        :skills2, after skills1, 2d
    Development Skills     :skills3, after skills2, 1d
    
    section Integration
    OpenAI Web Functions   :int1, after skills2, 1d
    Z.AI Client Setup      :int2, after int1, 1d
    VS Code Extension      :int3, after int2, 2d
    
    section Documentation
    Architecture Docs      :docs1, after core2, 2d
    Visual Documentation   :docs2, after docs1, 1d
    User Guides           :docs3, after docs2, 1d
```

## Network Diagram: Skills Interconnections

```mermaid
graph LR
    subgraph "Document Processing"
        DOCX[📝 DOCX]
        PDF[📄 PDF]
        PPTX[📊 PPTX]
        XLSX[📈 XLSX]
    end
    
    subgraph "Creative Tools"
        CANVAS[🎨 Canvas Design]
        ART[🎯 Algorithmic Art]
    end
    
    subgraph "Quality Assurance"
        FACT[🔍 Fact Check]
        ASSESS[📊 Assessment]
    end
    
    subgraph "Integration Layer"
        MCP[🔗 MCP Builder]
        VSCODE[💻 VS Code]
        THEME[🎨 Theme Factory]
    end
    
    DOCX -.-> CANVAS
    PDF -.-> ART
    PPTX -.-> CANVAS
    XLSX -.-> FACT
    CANVAS -.-> THEME
    ART -.-> THEME
    MCP -.-> VSCODE
    
    style CANVAS fill:#ff9999
    style ART fill:#99ccff
    style THEME fill:#99ff99
    style MCP fill:#ffcc99
    style VSCODE fill:#cc99ff
```