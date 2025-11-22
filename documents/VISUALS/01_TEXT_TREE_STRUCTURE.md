# 🌳 Mini-Agent System Structure - Text-Based Visualization

## Complete Directory Tree

```
C:\Users\Jazeel-Home\Mini-Agent\
│
├── 📦 CORE APPLICATION
│   ├── mini_agent/                    [Core package - 50+ modules]
│   │   ├── config/                    [Configuration management]
│   │   ├── llm/                       [AI model integrations: MiniMax-M2, GLM-4.6]
│   │   ├── skills/                    [14+ specialized skills]
│   │   │   ├── algorithmic-art/       [Generative art with p5.js]
│   │   │   ├── artifacts-builder/     [React + shadcn/ui components]
│   │   │   ├── canvas-design/         [Professional visual design]
│   │   │   ├── docx/                  [Word document operations]
│   │   │   ├── pdf/                   [PDF manipulation]
│   │   │   ├── pptx/                  [PowerPoint operations]
│   │   │   ├── xlsx/                  [Excel spreadsheet ops]
│   │   │   ├── fact-checking-self-assessment/
│   │   │   ├── mcp-builder/           [MCP server creation]
│   │   │   ├── skill-creator/         [Meta-skill for creating skills]
│   │   │   ├── slack-gif-creator/     [Animated GIFs for Slack]
│   │   │   ├── theme-factory/         [Artifact styling themes]
│   │   │   └── webapp-testing/        [Playwright browser testing]
│   │   ├── tools/                     [External tool integrations]
│   │   │   ├── openai_web_functions/  [Web search + web reader]
│   │   │   ├── _deprecated_zai/       [Legacy ZAI implementations]
│   │   │   └── simple_web_search.py   [Unified web search interface]
│   │   └── utils/                     [Utility modules]
│   │       ├── credit_protection.py   [Z.AI quota management]
│   │       └── [25+ utility modules]
│   │
│   ├── scripts/                       [Development & testing scripts]
│   │   ├── assessment/                [Validation scripts]
│   │   ├── cleanup/                   [Maintenance tools]
│   │   ├── integration/               [Integration bridges]
│   │   ├── maintenance/               [System maintenance]
│   │   ├── setup/                     [Installation & config]
│   │   ├── testing/                   [85+ test scripts]
│   │   ├── utilities/                 [Helper scripts]
│   │   └── validation/                [Compliance checks]
│   │
│   └── vscode-extension/              [VS Code integration]
│       ├── src/                       [TypeScript source]
│       └── package.json               [Node.js dependencies]
│
├── 📚 DOCUMENTATION
│   └── documents/
│       ├── 01_OVERVIEW/               [Project intro, quick starts]
│       ├── 02_SYSTEM_CORE/            [Core system documentation]
│       ├── 03_ARCHITECTURE/           [System design, patterns]
│       ├── 04_SETUP_CONFIG/           [Installation guides]
│       ├── 05_DEVELOPMENT/            [Development workflows]
│       ├── 06_TESTING_QA/             [Testing strategies]
│       ├── 07_RESEARCH_ANALYSIS/      [Research findings]
│       ├── 08_TOOLS_INTEGRATION/      [Tool integration docs]
│       ├── 09_PRODUCTION/             [Production readiness]
│       ├── 10_ARCHIVE/                [Historical artifacts]
│       ├── VISUALS/                   [Visual documentation]
│       └── _deprecated_zai_docs/      [Archived ZAI docs]
│
├── 🧪 TESTING & EXAMPLES
│   ├── tests/                         [Unit & integration tests]
│   ├── examples/                      [Example implementations]
│   └── workspace/                     [Test workspace]
│
├── ⚙️ CONFIGURATION
│   ├── .venv/                         [Python virtual environment]
│   ├── .env                           [Environment variables]
│   ├── pyproject.toml                 [Python project config]
│   ├── requirements.txt               [Python dependencies]
│   ├── package.json                   [Node.js dependencies]
│   └── local_config.yaml.example      [Config template]
│
└── 🔧 DEVELOPMENT TOOLS
    ├── .vscode/                       [VS Code settings]
    ├── .git/                          [Git repository]
    └── .git_old_backup/               [Backup of previous git state]

```

## Key System Metrics

- **Skills Available**: 14+ specialized capabilities
- **Test Scripts**: 85+ comprehensive tests
- **Documentation Files**: 100+ organized documents
- **Python Modules**: 50+ in core package
- **Integration Points**: MiniMax-M2, GLM-4.6 (Z.AI), VS Code
- **Visualization Tools**: 7 different modalities

## System Flow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                         │
│  (CLI, VS Code Extension, Direct Python Import)              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  MINI-AGENT CORE                             │
│  • Configuration Management                                  │
│  • Tool Orchestration                                        │
│  • Skill Loading System                                      │
└───────────┬─────────────────────┬───────────────────────────┘
            │                     │
            ▼                     ▼
┌───────────────────┐   ┌─────────────────────────┐
│   LLM PROVIDERS   │   │   SPECIALIZED SKILLS     │
│  • OpenAI GPT     │   │  • Document Processing   │
│  • MiniMax GLM    │   │  • Visual Design         │
│  • Z.AI (Coding)  │   │  • Algorithmic Art       │
└───────────────────┘   │  • Web Testing           │
                        │  • MCP Development       │
                        └─────────────────────────┘
                                  │
                                  ▼
                        ┌─────────────────────┐
                        │   EXTERNAL TOOLS     │
                        │  • Web Search        │
                        │  • Web Reader        │
                        │  • File Operations   │
                        │  • Git Commands      │
                        └─────────────────────┘
```

## Directory Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| Skills | 14 | Specialized capabilities |
| Core Modules | 50+ | System functionality |
| Test Scripts | 85+ | Quality assurance |
| Documentation | 100+ | Knowledge base |
| Integration Points | 4 | External services |

---

*This visualization provides a complete text-based overview of the system architecture.*
*For interactive versions, see other visualization files in this directory.*
