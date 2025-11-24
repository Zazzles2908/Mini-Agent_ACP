#!/usr/bin/env python3
"""Compare __init__.py files across all directories."""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path.cwd()))

def compare_init_files():
    """Compare all __init__.py files."""
    print("📦 __INIT__.PY FILES COMPARISON")
    print("=" * 60)
    
    init_files = [
        ("Root", "mini_agent/__init__.py", "reference_mini_agent/mini_agent/__init__.py"),
        ("llm/", "mini_agent/llm/__init__.py", "reference_mini_agent/mini_agent/llm/__init__.py"),
        ("schema/", "mini_agent/schema/__init__.py", "reference_mini_agent/mini_agent/schema/__init__.py"),
        ("tools/", "mini_agent/tools/__init__.py", "reference_mini_agent/mini_agent/tools/__init__.py"),
        ("utils/", "mini_agent/utils/__init__.py", "reference_mini_agent/mini_agent/utils/__init__.py"),
        ("acp/", "mini_agent/acp/__init__.py", "reference_mini_agent/mini_agent/acp/__init__.py"),
    ]
    
    # Add our enhanced directories
    our_enhanced_dirs = [
        ("core/", "mini_agent/core/__init__.py"),
        ("integrations/", "mini_agent/integrations/__init__.py"),
    ]
    
    print("🔍 COMPARING __INIT__.PY FILES:")
    
    for category, our_file, ref_file in init_files:
        print(f"\n📁 {category}:")
        our_path = Path(our_file)
        ref_path = Path(ref_file)
        
        our_content = our_path.read_text(encoding="utf-8") if our_path.exists() else "NOT FOUND"
        ref_content = ref_path.read_text(encoding="utf-8") if ref_path.exists() else "NOT FOUND"
        
        our_size = len(our_content) if our_content != "NOT FOUND" else 0
        ref_size = len(ref_content) if ref_content != "NOT FOUND" else 0
        
        status = "✅" if our_content == ref_content else "❌"
        
        print(f"   {status} Our: {our_size:,} chars")
        print(f"   {status} Ref: {ref_size:,} chars")
        
        if our_content != ref_content and our_content != "NOT FOUND" and ref_content != "NOT FOUND":
            our_lines = our_content.split('\n')
            ref_lines = ref_content.split('\n')
            print(f"   📊 Our lines: {len(our_lines)}")
            print(f"   📊 Ref lines: {len(ref_lines)}")
            
            # Show key differences
            our_exports = [line.strip() for line in our_lines if 'export' in line or 'from' in line]
            ref_exports = [line.strip() for line in ref_lines if 'export' in line or 'from' in line]
            
            if our_exports:
                print(f"   🔥 Our exports: {len(our_exports)} items")
            if ref_exports:
                print(f"   📖 Ref exports: {len(ref_exports)} items")
        elif our_content == "NOT FOUND":
            print(f"   ❌ Our file not found")
        elif ref_content == "NOT FOUND":
            print(f"   ❌ Reference file not found")
    
    print(f"\n🔥 OUR ENHANCED DIRECTORIES:")
    for category, our_file in our_enhanced_dirs:
        our_path = Path(our_file)
        if our_path.exists():
            our_content = our_path.read_text(encoding="utf-8")
            our_size = len(our_content)
            print(f"   📁 {category}: {our_size:,} chars (NEW)")
            # Show what it exports
            our_lines = our_content.split('\n')
            our_exports = [line.strip() for line in our_lines if 'export' in line or 'from' in line or line.strip().startswith('from') or line.strip().startswith('import')]
            if our_exports:
                print(f"      🔥 Exports: {len(our_exports)} items")
        else:
            print(f"   📁 {category}: NOT FOUND")

def main():
    """Run __init__.py comparison."""
    print("🔍 __INIT__.PY FILES DETAILED COMPARISON")
    print("=" * 70)
    
    compare_init_files()
    
    print(f"\n✅ __INIT__.PY COMPARISON COMPLETE")

if __name__ == "__main__":
    main()
