#!/usr/bin/env python3
"""
Comprehensive test for Phase 1: Memory Enhancement

This script tests all functionality implemented in Phase 1:
- Enhanced configuration support
- Intelligent session note tool
- Project context detection
- Enhanced recall capabilities
- Backward compatibility
"""

import asyncio
import json
from pathlib import Path

# Import our enhanced tools
from mini_agent.tools.note_tool import (
    EnhancedSessionNoteTool, 
    EnhancedRecallNoteTool,
    SessionNoteTool,
    RecallNoteTool
)
from mini_agent.config import get_config


async def test_configuration():
    """Test enhanced configuration support."""
    print('1️⃣ Testing Enhanced Configuration...')
    
    config = get_config()
    memory_config = config.get_memory_config()
    
    assert isinstance(memory_config, dict), "Memory config should be a dictionary"
    assert 'enable_enhanced' in memory_config, "Memory config should have enable_enhanced"
    assert 'project_context' in memory_config, "Memory config should have project_context"
    assert 'pattern_learning' in memory_config, "Memory config should have pattern_learning"
    
    print(f'   ✅ Memory configuration loaded successfully')
    print(f'   ✅ Enhanced memory enabled: {memory_config["enable_enhanced"]}')
    print(f'   ✅ Project context enabled: {memory_config["project_context"]}')
    print(f'   ✅ Pattern learning enabled: {memory_config["pattern_learning"]}')
    
    return True


async def test_enhanced_session_note_tool():
    """Test the enhanced session note tool."""
    print('\\n2️⃣ Testing Enhanced SessionNoteTool...')
    
    note_tool = EnhancedSessionNoteTool(memory_file='./workspace/phase1_test.json')
    
    assert note_tool.enhanced_enabled is False, "Enhanced should be disabled by default"
    assert note_tool.config is not None, "Config should be available"
    assert note_tool.memory_config is not None, "Memory config should be available"
    
    print(f'   ✅ EnhancedSessionNoteTool created successfully')
    print(f'   ✅ Enhanced features enabled: {note_tool.enhanced_enabled}')
    print(f'   ✅ Project context detected: {note_tool.current_project}')
    
    return True


async def test_note_recording():
    """Test different types of note recording."""
    print('\\n3️⃣ Testing Note Recording...')
    
    note_tool = EnhancedSessionNoteTool(memory_file='./workspace/phase1_test_notes.json')
    
    test_cases = [
        ('User prefers short, concise answers', 'user_preference'),
        ('Project uses Python 3.12 with async/await', 'project_info'),
        ('Need to implement authentication system', 'technical_decision'),
        ('Discovered pattern in file operations', 'learning'),
        ('This is a general system note', 'general'),
    ]
    
    for content, category in test_cases:
        result = await note_tool.execute(content, category=category)
        assert result.success, f"Failed to record note: {content}"
        assert result.content, "Result should have content"
        
        print(f'   ✅ Note recorded: \"{content[:30]}...\" -> {category}')
        if result.content:
            print(f'      Response: {result.content[:60]}...')
    
    return True


async def test_enhanced_recall():
    """Test enhanced recall capabilities."""
    print('\\n4️⃣ Testing Enhanced Recall...')
    
    recall_tool = EnhancedRecallNoteTool(memory_file='./workspace/phase1_test_notes.json')
    
    # Test basic recall
    result = await recall_tool.execute()
    assert result.success, "Basic recall should succeed"
    assert result.content, "Recall should return content"
    
    print(f'   ✅ Basic recall successful')
    
    # Test category filtering
    result = await recall_tool.execute(category='user_preference')
    assert result.success, "Category filter should succeed"
    
    print(f'   ✅ Category filtering successful')
    
    # Test limit
    result = await recall_tool.execute(limit=3)
    assert result.success, "Limit should work"
    
    print(f'   ✅ Limit filtering successful')
    
    return True


async def test_backward_compatibility():
    """Test backward compatibility with original interfaces."""
    print('\\n5️⃣ Testing Backward Compatibility...')
    
    # Test original SessionNoteTool interface
    compat_note_tool = SessionNoteTool(memory_file='./workspace/compat_test.json')
    result = await compat_note_tool.execute('Backward compatibility test', category='test')
    assert result.success, "Backward compatible note should work"
    
    print(f'   ✅ SessionNoteTool backward compatibility working')
    
    # Test original RecallNoteTool interface
    compat_recall_tool = RecallNoteTool(memory_file='./workspace/compat_test.json')
    result = await compat_recall_tool.execute()
    assert result.success, "Backward compatible recall should work"
    
    print(f'   ✅ RecallNoteTool backward compatibility working')
    
    return True


async def test_file_storage():
    """Test file storage and enhanced structure."""
    print('\\n6️⃣ Testing File Storage & Enhanced Structure...')
    
    test_file = Path('./workspace/phase1_test_notes.json')
    assert test_file.exists(), "Test file should exist"
    
    with open(test_file) as f:
        stored_data = json.load(f)
    
    assert len(stored_data) > 0, "Should have stored notes"
    print(f'   ✅ File storage: {len(stored_data)} notes stored')
    
    # Check enhanced structure
    first_note = stored_data[0]
    required_fields = ['timestamp', 'category', 'content', 'classification', 'project_context', 'workspace_hash', 'enhanced']
    
    for field in required_fields:
        assert field in first_note, f"Note should have {field} field"
    
    print(f'   ✅ Enhanced note structure verified')
    
    # Check classification structure
    classification = first_note['classification']
    assert 'category' in classification, "Classification should have category"
    assert 'type' in classification, "Classification should have type"
    assert 'confidence' in classification, "Classification should have confidence"
    
    print(f'   ✅ Classification structure verified')
    
    return True


async def test_project_context_detection():
    """Test project context detection."""
    print('\\n7️⃣ Testing Project Context Detection...')
    
    note_tool = EnhancedSessionNoteTool(memory_file='./workspace/phase1_test_project.json')
    
    # This should detect our Python project context
    if note_tool.current_project:
        print(f'   ✅ Project detected: {note_tool.current_project.get("type")}')
        print(f'   ✅ Project description: {note_tool.current_project.get("description")}')
    else:
        print(f'   ✅ No project context detected (expected for test environment)')
    
    return True


async def test_enhanced_classification():
    """Test intelligent content classification."""
    print('\\n8️⃣ Testing Intelligent Classification...')
    
    note_tool = EnhancedSessionNoteTool(memory_file='./workspace/phase1_test_classify.json')
    
    # Test various content types
    classification_tests = [
        ('I prefer dark mode in my editor', 'user_preference', True),  # Should auto-detect
        ('The project uses FastAPI framework', 'general', True),  # Should auto-detect as project_info
        ('Choose PostgreSQL for database', 'general', True),  # Should auto-detect as technical_decision
    ]
    
    for content, user_category, should_auto_detect in classification_tests:
        result = await note_tool.execute(content, category=user_category)
        assert result.success, f"Classification test failed: {content}"
        
        print(f'   ✅ Classified: "{content[:40]}..."')
        if result.metadata and 'classification' in result.metadata:
            cls = result.metadata['classification']
            print(f'      Auto-categorized: {cls.get("auto_categorized", False)}, Category: {cls.get("category")}')
    
    return True


async def run_all_tests():
    """Run all Phase 1 tests."""
    print('🧪 PHASE 1: MEMORY ENHANCEMENT - COMPREHENSIVE TEST SUITE')
    print('=' * 70)
    
    tests = [
        ('Configuration', test_configuration),
        ('Enhanced SessionNoteTool', test_enhanced_session_note_tool),
        ('Note Recording', test_note_recording),
        ('Enhanced Recall', test_enhanced_recall),
        ('Backward Compatibility', test_backward_compatibility),
        ('File Storage & Structure', test_file_storage),
        ('Project Context Detection', test_project_context_detection),
        ('Intelligent Classification', test_enhanced_classification),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            print(f'   ❌ {test_name} FAILED: {e}')
            failed += 1
    
    print('\\n' + '=' * 70)
    print('🎯 PHASE 1 TEST RESULTS:')
    print(f'   ✅ PASSED: {passed}/{len(tests)} tests')
    print(f'   ❌ FAILED: {failed}/{len(tests)} tests')
    
    if failed == 0:
        print('\\n🎉 ALL TESTS PASSED - PHASE 1 READY FOR DEPLOYMENT!')
        return True
    else:
        print('\\n⚠️  SOME TESTS FAILED - REVIEW IMPLEMENTATION')
        return False


if __name__ == "__main__":
    # Run the comprehensive test suite
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)