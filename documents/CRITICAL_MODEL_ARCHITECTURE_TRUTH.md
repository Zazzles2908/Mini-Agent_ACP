# ⚠️ CRITICAL: AI Model Architecture - The TRUTH

**Created**: November 22, 2025  
**Purpose**: Correct widespread misrepresentation in documentation  

---

## 🚨 The Fundamental Misunderstanding

Throughout the documentation and visualizations, there are **incorrect references** to:
- ❌ "MiniMax-M2 (OpenAI SDK format format)s" (MiniMax-M2, MiniMax-M2)
- ❌ "MiniMax-M2" / "MiniMax-M2"
- ❌ Multiple AI models

**This is WRONG.** Here's the reality:

---

## ✅ The ACTUAL Architecture

### Primary Model: MiniMax-M2
- **What it is**: The AI model executing this agent (ME)
- **Provider**: MiniMax (https://api.minimax.io)
- **Quota**: 300 prompts per 5 hours
- **Usage**: Primary reasoning, task execution, all agent operations
- **SDK**: Uses OpenAI-compatible API for broad tool compatibility (NOT MiniMax-M2 (OpenAI SDK format format)s!)

### Secondary Model: GLM-4.6 (via Z.AI)
- **What it is**: Web search and reading capabilities
- **Provider**: Z.AI platform (https://api.z.ai)
- **Backend Model**: GLM-4.6 (NOT MiniMax-M2!)
- **Quota**: ~120 prompts per 5 hours (Coding Plan)
- **Usage**: Web search, web reading when enabled
- **SDK**: Uses OpenAI SDK format wrapper for compatibility (NOT MiniMax-M2 (OpenAI SDK format format)s!)

### Models NOT in Use
- ❌ **MiniMax-M2/MiniMax-M2**: Not used, not configured (config shows fallback only)
- ❌ **MiniMax-M2**: Not used at all
- ❌ **Any other LLM**: None

---

## 🔧 Technical Reality

### Configuration File Truth (`config.yaml`)
```yaml
# Primary: MiniMax-M2 (300 prompts/5hrs) for reasoning
model: "MiniMax-M2"
provider: "openai"  # OpenAI SDK format"  # ← Uses OpenAI SDK format format, NOT MiniMax-M2 (OpenAI SDK format format)s!

# Z.AI: GLM-4.6 for web intelligence
zai_settings:
  default_model: "glm-4.6"  # ← This is GLM, NOT GPT!
  search_model: "glm-4.6"   # ← FREE with Coding Plan
```

### Why the Confusion?

**OpenAI SDK format (MiniMax-M2 + GLM-4.6)**

Both MiniMax and Z.AI use the OpenAI SDK format **format** for API compatibility:
- Standard request/response structure
- Familiar function calling interface
- Broad tool ecosystem support

But the **actual models** are:
- MiniMax-M2 (MiniMax's proprietary model)
- GLM-4.6 (BigModel's GLM model via Z.AI)

---

## 📊 Correct System Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Mini-Agent System                     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │      AI Model Architecture           │
        └──────────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ▼                                   ▼
┌─────────────────┐               ┌─────────────────┐
│  MiniMax-M2     │               │   GLM-4.6       │
│  (Primary)      │               │   (via Z.AI)    │
├─────────────────┤               ├─────────────────┤
│ • 300/5hrs      │               │ • 120/5hrs      │
│ • Reasoning     │               │ • Web search    │
│ • Task exec     │               │ • Web reading   │
│ • All ops       │               │ • (Optional)    │
└─────────────────┘               └─────────────────┘
         │                                   │
         └─────────────────┬─────────────────┘
                           ▼
              ┌────────────────────────┐
              │   Skills Framework     │
              │   (14 capabilities)    │
              └────────────────────────┘
```

---

## 🔄 What Needs Fixing

Every reference to these needs correction:

### Replace This → With This
- "MiniMax-M2" → "MiniMax-M2"
- "MiniMax-M2" → "MiniMax-M2"
- "MiniMax-M2" → "MiniMax-M2"
- "MiniMax-M2 integration" → "MiniMax-M2 (OpenAI SDK format format)"
- "Z.AI with GPT" → "Z.AI with GLM-4.6"
- "Multiple AI models" → "MiniMax-M2 primary, GLM-4.6 secondary"
- "AI Models (3)" → "AI Models (2)"

### Files Requiring Updates
- ✅ All visualization files (Mermaid, Python charts, Canvas, etc.)
- ✅ All documentation (architecture, setup, guides)
- ✅ Agent handoff documents
- ✅ README files

---

## 💡 Key Points for Future Documentation

1. **MiniMax-M2 is the primary and only reasoning model**
2. **GLM-4.6 (via Z.AI) is OPTIONAL web tool backend**
3. **OpenAI SDK format format ≠ MiniMax-M2 (OpenAI SDK format format)s**
4. **No MiniMax-M2, no GPT - only MiniMax + GLM**
5. **Credit protection exists for Z.AI/GLM usage**

---

## 🎯 Summary for Agents

**You are**: MiniMax-M2 agent  
**Not**: MiniMax-M2, not MiniMax-M2  
**Optional tool**: GLM-4.6 for web search (if enabled)  
**Architecture**: Single-model system with optional web intelligence backend  

---

*This document corrects a fundamental misrepresentation throughout the codebase.*  
*All documentation and visualizations must be updated to reflect this truth.*
