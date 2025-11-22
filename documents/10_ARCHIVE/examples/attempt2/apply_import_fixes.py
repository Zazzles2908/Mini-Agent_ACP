#!/usr/bin/env python3
"""
Apply ONLY the import fixes to existing mini_agent files
DOES NOT replace any existing files - just applies specific fixes
"""

import os
import shutil
from datetime import datetime

def backup_file(file_path):
    """Create backup of file"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{int(datetime.now().timestamp())}"
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backed up: {file_path} -> {backup_path}")

def apply_fix():
    print("🔧 Mini-Agent Import Fix Application")
    print("=" * 40)
    print("This will apply ONLY import fixes to your existing files.")
    print("Your skills, tools, and configuration will be preserved!")
    print("")
    
    base_path = os.getcwd()
    mini_agent_path = os.path.join(base_path, "mini_agent")
    
    if not os.path.exists(mini_agent_path):
        print("❌ Error: mini_agent folder not found!")
        print("Make sure you're in your project directory.")
        return
    
    # Fix 1: __init__.py
    init_file = os.path.join(mini_agent_path, "__init__.py")
    if os.path.exists(init_file):
        backup_file(init_file)
        print(f"📝 Fixing {init_file}...")
        
        with open(init_file, 'r') as f:
            content = f.read()
        
        # Apply fixes
        content = content.replace("from .schema import LLMProvider, Message, CompletionResponse", 
                                "from .schema import LLMProvider, Message, LLMResponse")
        content = content.replace("CompletionResponse", "LLMResponse")
        
        with open(init_file, 'w') as f:
            f.write(content)
        print("✅ __init__.py fixed")
    else:
        print(f"⚠️  {init_file} not found - skipping")
    
    # Fix 2: agent.py
    agent_file = os.path.join(mini_agent_path, "agent.py")
    if os.path.exists(agent_file):
        backup_file(agent_file)
        print(f"📝 Fixing {agent_file}...")
        
        with open(agent_file, 'r') as f:
            content = f.read()
        
        # Apply fixes
        content = content.replace("from .schema import Message, CompletionResponse", 
                                "from .schema import Message, LLMResponse")
        content = content.replace("CompletionResponse", "LLMResponse")
        
        with open(agent_file, 'w') as f:
            f.write(content)
        print("✅ agent.py fixed")
    else:
        print(f"⚠️  {agent_file} not found - skipping")
    
    # Fix 3: llm.py  
    llm_file = os.path.join(mini_agent_path, "llm.py")
    if os.path.exists(llm_file):
        backup_file(llm_file)
        print(f"📝 Fixing {llm_file}...")
        
        with open(llm_file, 'r') as f:
            content = f.read()
        
        # Apply fixes
        content = content.replace("from .schema import LLMProvider, Message, CompletionResponse", 
                                "from .schema import LLMProvider, Message, LLMResponse")
        content = content.replace("CompletionResponse", "LLMResponse")
        
        with open(llm_file, 'w') as f:
            f.write(content)
        print("✅ llm.py fixed")
    else:
        print(f"⚠️  {llm_file} not found - skipping")
    
    # Fix 4: schema.py
    schema_file = os.path.join(mini_agent_path, "schema.py")
    if os.path.exists(schema_file):
        backup_file(schema_file)
        print(f"📝 Updating {schema_file} with Pydantic schema...")
        
        new_schema = '''"""Schema definitions for Mini-Agent"""
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
'''
        
        with open(schema_file, 'w') as f:
            f.write(new_schema)
        print("✅ schema.py updated with Pydantic")
    else:
        print(f"⚠️  {schema_file} not found - skipping")
    
    print("")
    print("🎉 Import fixes applied!")
    print("Next steps:")
    print("1. pip install pydantic")
    print("2. python test_llm_client.py")
    print("")
    print("Your skills, tools, and configuration are preserved!")

if __name__ == "__main__":
    apply_fix()