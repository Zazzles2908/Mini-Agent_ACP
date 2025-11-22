"""
Comprehensive Model Architecture Correction Script
Fixes incorrect AI model references throughout the codebase
Run with: uv run python fix_model_references.py
"""

import os
import re
from pathlib import Path

# Correct mappings
CORRECTIONS = {
    # Primary model corrections
    r'OpenAI GLM-4.6 (via Z.AI)': 'MiniMax-M2',
    r'OpenAI GLM-4.6 (via Z.AI)o': 'MiniMax-M2',
    r'GLM-4.6 (via Z.AI)o': 'MiniMax-M2',
    r'GLM-4.6 (via Z.AI)': 'MiniMax-M2',
    r'OpenAI\[OpenAI GLM-4.6 (via Z.AI)\]': 'MiniMax[MiniMax-M2]',
    r'OpenAI\[OpenAI GLM-4.6 (via Z.AI)o\]': 'MiniMax[MiniMax-M2]',
    
    # Z.AI model corrections  
    r'MiniMax GLM-4\.6': 'GLM-4.6 (Z.AI)',
    r'MiniMax\[MiniMax GLM-4\.6\]': 'ZAI_GLM[GLM-4.6 (Z.AI)]',
    r'MiniMax\nGLM': 'GLM-4.6\n(Z.AI)',
    
    # Provider section corrections
    r'LLM Providers': 'AI Models',
    r'"LLM PROVIDERS"': '"AI MODELS"',
    r'LLM Provider Comparison': 'AI Model Comparison',
    
    # Descriptions
    r'OpenAI, MiniMax GLM, Z\.AI': 'MiniMax-M2, GLM-4.6 (Z.AI)',
    r'OpenAI, MiniMax, Z\.AI': 'MiniMax-M2, GLM-4.6',
    r'GLM-4.6 (via Z.AI), GLM-4.6 (via Z.AI)o': 'MiniMax-M2',
    r'GLM-4\.6, GLM-4\.5': 'GLM-4.6 (free), GLM-4.5 (paid)',
    
    # Legend/stats corrections
    r'AI models / execution': 'AI models / execution',
    r'2 AI models': '2 AI models',
    r'LLM integration': 'AI model integration',
    r'LLM Integration': 'AI Model Integration',
    
    # Color descriptions
    r'LLM Providers \(OpenAI, MiniMax, Z\.AI\)': 'AI Models (MiniMax-M2, GLM-4.6)',
    
    # Dashboard specific
    r'<div class="font-semibold">OpenAI</div>': '<div class="font-semibold">MiniMax-M2</div>',
    r'<div class="text-sm text-gray-500">GLM-4.6 (via Z.AI), GLM-4.6 (via Z.AI)o</div>': '<div class="text-sm text-gray-500">Primary reasoning model</div>',
    r'<div class="font-semibold">MiniMax GLM</div>': '<div class="font-semibold">GLM-4.6 (Z.AI)</div>',
    r'<div class="text-sm text-gray-500">GLM-4\.6, GLM-4\.5</div>': '<div class="text-sm text-gray-500">Web search & reading</div>',
    r'<div class="font-semibold">Z\.AI Coding Plan</div>': '<div class="font-semibold">GLM-4.6 Backend</div>',
    r'<span class="px-2 py-1 bg-emerald-100 text-emerald-700 text-xs rounded-full">Primary</span>': '<span class="px-2 py-1 bg-emerald-100 text-emerald-700 text-emerald-700 text-xs rounded-full">Primary Model</span>',
    r'<span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">Efficient</span>': '<span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">Web Tools</span>',
    r'<span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">Web Tools</span>': '<span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">Backend Only</span>',
}

# Files to process
TARGET_DIRS = [
    'documents/VISUALS',
    'documents/01_OVERVIEW',
    'documents/02_SYSTEM_CORE',
    'documents/03_ARCHITECTURE',
    'documents'
]

FILE_PATTERNS = ['*.md', '*.html', '*.py']

def fix_file(filepath: Path) -> tuple[bool, int]:
    """Fix a single file. Returns (changed, num_replacements)"""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        replacements = 0
        
        for pattern, replacement in CORRECTIONS.items():
            new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
            if count > 0:
                content = new_content
                replacements += count
        
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            return True, replacements
        return False, 0
    except Exception as e:
        print(f"  ⚠️  Error processing {filepath.name}: {e}")
        return False, 0

def main():
    print("\n" + "="*70)
    print("  AI MODEL ARCHITECTURE CORRECTION SCRIPT")
    print("="*70 + "\n")
    
    print("Correcting misrepresentations:")
    print("  ❌ OpenAI GLM-4.6 (via Z.AI) → ✅ MiniMax-M2")
    print("  ❌ MiniMax-M2 → ✅ MiniMax-M2")
    print("  ❌ MiniMax GLM → ✅ GLM-4.6 (Z.AI)\n")
    
    total_files = 0
    total_changes = 0
    total_replacements = 0
    
    for dir_path in TARGET_DIRS:
        if not os.path.exists(dir_path):
            continue
            
        print(f"📁 Processing: {dir_path}/")
        
        for pattern in FILE_PATTERNS:
            for filepath in Path(dir_path).rglob(pattern):
                total_files += 1
                changed, replacements = fix_file(filepath)
                if changed:
                    total_changes += 1
                    total_replacements += replacements
                    print(f"  ✅ Fixed {filepath.name} ({replacements} changes)")
    
    print("\n" + "="*70)
    print(f"  SUMMARY")
    print("="*70)
    print(f"  Files scanned: {total_files}")
    print(f"  Files modified: {total_changes}")
    print(f"  Total corrections: {total_replacements}")
    print("="*70 + "\n")
    
    if total_changes > 0:
        print("✅ Corrections applied successfully!")
        print("   Review changes with: git diff")
        print("   Commit with: git add . && git commit -m 'fix: Correct AI model references'\n")
    else:
        print("ℹ️  No changes needed - all references already correct\n")

if __name__ == '__main__':
    main()
