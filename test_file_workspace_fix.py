#!/usr/bin/env python3
"""
Test script to verify file tools work correctly with proper workspace directory.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from pathlib import Path
from mini_agent.tools.file_tools import ReadTool, WriteTool, ListDirectoryTool


async def test_file_tools_workspace():
    """Test that file tools work with the correct workspace directory"""
    
    print("🧪 Testing file tools with proper workspace directory...")
    
    # Test workspace directory
    workspace_dir = Path.cwd()  # Current working directory
    print(f"   Using workspace directory: {workspace_dir}")
    
    # Test 1: List directory
    print("\n1️⃣  Testing ListDirectoryTool:")
    try:
        list_tool = ListDirectoryTool(workspace_dir=str(workspace_dir))
        result = await list_tool.execute(path=".", recursive=False)
        
        if result.success:
            print("   ✅ ListDirectoryTool works!")
            print(f"   Output preview: {result.content[:200]}...")
        else:
            print(f"   ❌ ListDirectoryTool failed: {result.error}")
            
    except Exception as e:
        print(f"   ❌ ListDirectoryTool error: {e}")
    
    # Test 2: Write and read a test file
    print("\n2️⃣  Testing WriteTool and ReadTool:")
    test_file = workspace_dir / "test_workspace_fix.txt"
    test_content = "This is a test file to verify workspace directory handling."
    
    try:
        # Write test file
        write_tool = WriteTool(workspace_dir=str(workspace_dir))
        write_result = await write_tool.execute(path="test_workspace_fix.txt", content=test_content)
        
        if write_result.success:
            print("   ✅ WriteTool works!")
        else:
            print(f"   ❌ WriteTool failed: {write_result.error}")
            return
            
        # Read test file
        read_tool = ReadTool(workspace_dir=str(workspace_dir))
        read_result = await read_tool.execute(path="test_workspace_fix.txt")
        
        if read_result.success:
            print("   ✅ ReadTool works!")
            print(f"   Content matches: {test_content in read_result.content}")
        else:
            print(f"   ❌ ReadTool failed: {read_result.error}")
            
        # Clean up test file
        if test_file.exists():
            test_file.unlink()
            print("   ✅ Cleanup complete")
            
    except Exception as e:
        print(f"   ❌ Read/Write test error: {e}")
    
    # Test 3: Test with absolute path
    print("\n3️⃣  Testing with absolute paths:")
    try:
        list_tool = ListDirectoryTool(workspace_dir=str(workspace_dir))
        result = await list_tool.execute(path=str(workspace_dir), recursive=False)
        
        if result.success:
            print("   ✅ Absolute path handling works!")
        else:
            print(f"   ❌ Absolute path test failed: {result.error}")
            
    except Exception as e:
        print(f"   ❌ Absolute path test error: {e}")
    
    print("\n🎉 File tools workspace test completed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_file_tools_workspace())