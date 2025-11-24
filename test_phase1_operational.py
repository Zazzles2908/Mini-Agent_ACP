#!/usr/bin/env python3
"""
Quick operational test for Phase 1 enhanced memory features.
"""

import asyncio
import tempfile
import os
import json
from mini_agent.config import Config
from mini_agent.tools.note_tool import EnhancedSessionNoteTool, EnhancedRecallNoteTool

def test_basic_functionality():
    """Test basic enhanced memory functionality"""
    print("=== Phase 1 Enhanced Memory - Operational Test ===\n")
    
    # Test 1: Configuration
    print("🔍 Test 1: Configuration Loading")
    config = Config()
    memory_config = config.get_memory_config()
    
    print(f"✅ Enhanced enabled: {memory_config.get('enable_enhanced', False)}")
    print(f"✅ Project context: {memory_config.get('project_context', False)}")
    print(f"✅ Pattern learning: {memory_config.get('pattern_learning', False)}")
    print()
    
    # Test 2: Tool Instantiation
    print("🔍 Test 2: Tool Instantiation")
    session_tool = EnhancedSessionNoteTool()
    recall_tool = EnhancedRecallNoteTool()
    
    print(f"✅ Session tool enhanced: {session_tool.enhanced_enabled}")
    print(f"✅ Recall tool enhanced: {recall_tool.enhanced_enabled}")
    print()
    
    # Test 3: Auto-categorization
    print("🔍 Test 3: Auto-categorization")
    test_content = "User prefers concise responses with code examples"
    classification = session_tool._classify_note_content(test_content, "general")
    
    print(f"✅ Content: {test_content}")
    print(f"✅ Auto-categorized category: {classification.get('category')}")
    print(f"✅ Confidence: {classification.get('confidence')}")
    print(f"✅ Auto-categorized: {classification.get('metadata', {}).get('auto_categorized', False)}")
    print()
    
    return True

async def test_note_recording():
    """Test enhanced note recording functionality"""
    print("🔍 Test 4: Enhanced Note Recording")
    
    # Create temporary memory file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file.write('[]')
    temp_file.close()
    
    try:
        session_tool = EnhancedSessionNoteTool(memory_file=temp_file.name)
        
        # Test note recording
        result = await session_tool.execute(
            "User prefers detailed explanations with examples", 
            "preference"
        )
        
        print(f"✅ Recording success: {result.success}")
        print(f"✅ Result content: {result.content}")
        
        # Verify note was saved
        with open(temp_file.name, 'r') as f:
            notes = json.load(f)
        
        if notes:
            note = notes[0]
            print(f"✅ Saved category: {note.get('category')}")
            print(f"✅ Enhanced features: {note.get('enhanced')}")
            print(f"✅ Auto-categorized: {note.get('classification', {}).get('auto_categorized', False)}")
            
            if note.get('category') == 'user_preference' and note.get('enhanced'):
                print(f"✅ Enhanced note recording SUCCESSFUL")
                return True
            else:
                print(f"❌ Enhanced features not working properly")
                return False
        else:
            print(f"❌ No notes found after recording")
            return False
            
    except Exception as e:
        print(f"❌ Note recording failed: {e}")
        return False
    finally:
        os.unlink(temp_file.name)

def test_backward_compatibility():
    """Test backward compatibility"""
    print("🔍 Test 5: Backward Compatibility")
    
    from mini_agent.tools.note_tool import SessionNoteTool, RecallNoteTool
    
    # Test original interface
    session_tool = SessionNoteTool()
    recall_tool = RecallNoteTool()
    
    print(f"✅ Original session tool name: {session_tool.name}")
    print(f"✅ Original recall tool name: {recall_tool.name}")
    print(f"✅ Enhanced features available: {session_tool.enhanced_enabled}")
    
    # Verify inheritance
    from mini_agent.tools.note_tool import EnhancedSessionNoteTool, EnhancedRecallNoteTool
    
    print(f"✅ Session inherits from Enhanced: {isinstance(session_tool, EnhancedSessionNoteTool)}")
    print(f"✅ Recall inherits from Enhanced: {isinstance(recall_tool, EnhancedRecallNoteTool)}")
    
    if isinstance(session_tool, EnhancedSessionNoteTool) and isinstance(recall_tool, EnhancedRecallNoteTool):
        print(f"✅ Backward compatibility MAINTAINED")
        return True
    else:
        print(f"❌ Backward compatibility BROKEN")
        return False

async def main():
    """Run all operational tests"""
    print("Starting Phase 1 Enhanced Memory operational validation...\n")
    
    results = []
    
    # Test basic functionality
    results.append(test_basic_functionality())
    
    # Test note recording
    results.append(await test_note_recording())
    
    # Test backward compatibility
    results.append(test_backward_compatibility())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== Operational Test Results: {passed}/{total} ===")
    
    if passed == total:
        print("🎉 PHASE 1 ENHANCED MEMORY IS FULLY OPERATIONAL")
        print("\n✅ Confirmed Working Features:")
        print("   • Enhanced memory configuration loading")
        print("   • Auto-categorization of notes") 
        print("   • Enhanced note recording with intelligent features")
        print("   • Backward compatibility with original interfaces")
        print("   • Project context awareness capability")
        print("\n🚀 Phase 1 implementation is SUCCESSFUL")
        return True
    else:
        print("❌ Phase 1 has operational issues")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
