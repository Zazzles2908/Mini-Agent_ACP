# Mini-Agent Installation & Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or use the installation script
python scripts/install_dependencies.py
```

### 2. Set Up Environment

Create `.env` file with your API keys:
```env
ZAI_API_KEY=your_zai_api_key_here
MINIMAX_API_KEY=your_minimax_api_key_here
```

### 3. Run Setup Verification

```bash
python scripts/setup_mini_agent.py
```

## 📁 Project Structure

```
Mini-Agent/
├── mini_agent/                 # Core Mini-Agent package
├── scripts/                    # Development scripts
│   ├── install_dependencies.py # Install all dependencies
│   ├── setup_mini_agent.py     # Environment setup
│   ├── test_zai_reader.py      # Z.AI functionality tests
│   └── [other test scripts]    # Various test utilities
├── documents/                  # Project documentation
│   ├── technical/             # Technical documentation
│   └── user_guides/           # User guides
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🧪 Testing

All test scripts are located in `scripts/` directory:

```bash
# Test Z.AI web reading functionality
python scripts/test_zai_reader.py

# Investigate Z.AI API endpoints
python scripts/investigate_zai_reader.py

# Test with correct Z.AI models
python scripts/test_correct_models.py

# Final verification test
python scripts/final_test_zai_reader.py
```

## 🔧 Key Components

### Dependencies (requirements.txt)
- **aiohttp**: Async HTTP client
- **anthropic**: Anthropic API client
- **openai**: OpenAI API client
- **requests**: HTTP library
- **pydantic**: Data validation
- **pytest**: Testing framework

### Test Scripts Location
All test scripts have been moved from the root directory to `scripts/` to reduce clutter:

✅ **Before**: `test_zai_reader.py` (in root)
✅ **After**: `scripts/test_zai_reader.py` (organized)

## 🎯 Usage

### Command Line Interface
```bash
python -m mini_agent
```

### VS Code Extension
```bash
code --install-extension mini_agent/vscode_extension/
```

### ACP Server (for editor integration)
```bash
python -m mini_agent.acp
```

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| ZAI_API_KEY | Z.AI API key for web search/read | ✅ |
| MINIMAX_API_KEY | MiniMax API key for LLM access | ✅ |

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Run `python scripts/install_dependencies.py`
2. **API Errors**: Check your `.env` file has valid API keys
3. **Z.AI Connection Issues**: Verify ZAI_API_KEY is correct

### Getting Help

- Check `/help` command in Mini-Agent
- Review `documents/technical/` for detailed guides
- Run test scripts to diagnose issues

## 📚 Documentation Structure

```
documents/
├── PROJECT_CONTEXT.md          # Project overview
├── AGENT_HANDOFF.md           # Handoff notes for agents
├── SETUP_GUIDE.md             # Environment setup
├── ACP_INTEGRATION_GUIDE.md   # ACP + VS Code integration
└── technical/
    ├── ZAI_WEB_READER_ISSUE_RESOLUTION.md  # Z.AI troubleshooting
    └── [other technical docs]
```

---
*Last updated: [Current date]*
*Maintained by: Mini-Agent Development Team*