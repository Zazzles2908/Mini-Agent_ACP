# 🛠️ EXACT CODE CHANGES NEEDED

## File 1: `mini_agent/__init__.py`

**Line 4 - Change:**
```python
# OLD:
from .schema import LLMProvider, Message, CompletionResponse

# NEW:
from .schema import LLMProvider, Message, LLMResponse
```

**Line 9 - Change:**
```python
# OLD:
__all__ = [..., "CompletionResponse", ...]

# NEW:
__all__ = [..., "LLMResponse", ...]
```

---

## File 2: `mini_agent/agent.py`

**Line 4 - Change:**
```python
# OLD:
from .schema import Message, CompletionResponse

# NEW:
from .schema import Message, LLMResponse
```

**Line 19 - Change:**
```python
# OLD:
async def run(self, messages: List[Message]) -> CompletionResponse:

# NEW:
async def run(self, messages: List[Message]) -> LLMResponse:
```

**Line 33 - Change:**
```python
# OLD:
def run_sync(self, messages: List[Message]) -> CompletionResponse:

# NEW:
def run_sync(self, messages: List[Message]) -> LLMResponse:
```

---

## File 3: `mini_agent/llm.py`

**Line 5 - Change:**
```python
# OLD:
from .schema import LLMProvider, Message, CompletionResponse

# NEW:
from .schema import LLMProvider, Message, LLMResponse
```

**Line 41 - Change:**
```python
# OLD:
async def chat(self, messages: List[Message]) -> CompletionResponse:

# NEW:
async def chat(self, messages: List[Message]) -> LLMResponse:
```

**Constructor calls (lines ~87-100) - Change all instances:**
```python
# OLD:
return CompletionResponse(
    content=text_content,
    model=self.model,
    finish_reason=finish_reason,
    usage=usage
)

# NEW:
return LLMResponse(
    content=text_content,
    finish_reason=finish_reason
)

# And:
# OLD:
return CompletionResponse(
    content=f"Error: {str(e)}",
    model="error",
    finish_reason="error",
    usage={}
)

# NEW:
return LLMResponse(
    content=f"Error: {str(e)}",
    finish_reason="error"
)
```

---

## File 4: `mini_agent/schema.py`

**Replace ENTIRE FILE with:**
```python
"""Schema definitions for Mini-Agent"""
from enum import Enum
from typing import Any
from pydantic import BaseModel

class LLMProvider(str, Enum):
    """AI model types."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"

class FunctionCall(BaseModel):
    """Function call details."""
    name: str
    arguments: dict[str, Any]

class ToolCall(BaseModel):
    """Tool call details."""
    id: str
    type: str
    function: FunctionCall

class Message(BaseModel):
    """Message schema."""
    role: str
    content: str
    thinking: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    name: str | None = None

class LLMResponse(BaseModel):
    """Response from LLM."""
    content: str
    thinking: str | None = None
    tool_calls: list[ToolCall] | None = None
    finish_reason: str
```

---

## After making changes:

1. **Install pydantic:** `pip install pydantic`
2. **Test:** `python test_llm_client.py`

That's it! These 4 files, 4 specific changes each, and your complete sophisticated setup will work perfectly.