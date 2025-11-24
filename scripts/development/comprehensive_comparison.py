#!/usr/bin/env python3
"""Comprehensive comparison between our mini-agent and reference implementation."""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path.cwd()))

def compare_file_sizes():
    """Compare file sizes between our implementation and reference."""
    print("📊 FILE SIZE COMPARISON")
    print("=" * 60)
    
    files_to_compare = [
        "config/config.yaml",
        "llm/anthropic_client.py", 
        "llm/base.py",
        "llm/llm_wrapper.py",
        "llm/openai_client.py",
        "schema/schema.py",
        "agent.py",
        "cli.py", 
        "config.py",
        "llm.py",
        "logger.py",
        "retry.py"
    ]
    
    for file_path in files_to_compare:
        our_file = Path(f"mini_agent/{file_path}")
        ref_file = Path(f"reference_mini_agent/mini_agent/{file_path}")
        
        our_size = our_file.stat().st_size if our_file.exists() else 0
        ref_size = ref_file.stat().st_size if ref_file.exists() else 0
        
        status = "✅" if our_size == ref_size else "❌"
        size_diff = our_size - ref_size
        
        print(f"{status} {file_path}")
        print(f"   Our size: {our_size:,} bytes")
        print(f"   Ref size: {ref_size:,} bytes")
        print(f"   Difference: {size_diff:+,} bytes")
        print()

def compare_config_yaml():
    """Compare config.yaml files."""
    print("📋 CONFIG.YAML COMPARISON")
    print("=" * 60)
    
    # Read both config files
    our_config = Path("mini_agent/config/config.yaml")
    ref_config = Path("reference_mini_agent/mini_agent/config/config-example.yaml")
    
    print("🔍 Reading our config.yaml...")
    our_content = our_config.read_text(encoding="utf-8") if our_config.exists() else "NOT FOUND"
    print(f"✅ Our config length: {len(our_content)} characters")
    
    print("🔍 Reading reference config.yaml...")
    ref_content = ref_config.read_text(encoding="utf-8") if ref_config.exists() else "NOT FOUND"
    print(f"✅ Reference config length: {len(ref_content)} characters")
    
    # Analyze key differences
    our_lines = our_content.split('\n')
    ref_lines = ref_content.split('\n')
    
    print(f"\n📊 CONFIGURATION ANALYSIS:")
    print(f"   Our lines: {len(our_lines)}")
    print(f"   Ref lines: {len(ref_lines)}")
    
    # Check for key differences
    key_differences = []
    
    if "Z.AI" in our_content and "Z.AI" not in ref_content:
        key_differences.append("Z.AI integration (our implementation has, reference doesn't)")
    
    if "provider:" in our_content and "provider:" in ref_content:
        our_provider = [line for line in our_lines if "provider:" in line][0] if any("provider:" in line for line in our_lines) else "NOT FOUND"
        ref_provider = [line for line in ref_lines if "provider:" in line][0] if any("provider:" in line for line in ref_lines) else "NOT FOUND"
        if our_provider != ref_provider:
            key_differences.append(f"Provider configuration: '{our_provider}' vs '{ref_provider}'")
    
    if "debug:" in our_content and "debug:" not in ref_content:
        key_differences.append("Debug mode (our implementation has, reference doesn't)")
        
    if key_differences:
        print(f"\n🚨 KEY DIFFERENCES:")
        for diff in key_differences:
            print(f"   • {diff}")
    else:
        print(f"\n✅ No major configuration differences found")

def compare_directory_structure():
    """Compare directory structures."""
    print("📁 DIRECTORY STRUCTURE COMPARISON")
    print("=" * 60)
    
    def get_directory_structure(path, prefix=""):
        """Get directory structure."""
        if not path.exists():
            return []
        
        structure = []
        items = sorted(path.iterdir())
        
        for item in items:
            if item.name.startswith('.'):
                continue
                
            if item.is_dir():
                structure.append(f"{prefix}📁 {item.name}/")
                # Add subdirectories
                sub_structure = get_directory_structure(item, prefix + "   ")
                structure.extend(sub_structure)
            else:
                structure.append(f"{prefix}📄 {item.name}")
        
        return structure
    
    print("🔍 Our Implementation Structure:")
    our_structure = get_directory_structure(Path("mini_agent"))
    for item in our_structure[:20]:  # Limit output
        print(f"   {item}")
    if len(our_structure) > 20:
        print(f"   ... and {len(our_structure) - 20} more items")
    
    print(f"\n🔍 Reference Implementation Structure:")
    ref_structure = get_directory_structure(Path("reference_mini_agent/mini_agent"))
    for item in ref_structure[:20]:  # Limit output
        print(f"   {item}")
    if len(ref_structure) > 20:
        print(f"   ... and {len(ref_structure) - 20} more items")

def compare_specific_files():
    """Compare specific files mentioned by user."""
    print("\n🔍 SPECIFIC FILE COMPARISON")
    print("=" * 60)
    
    files_to_analyze = [
        ("anthropic_client.py", "llm/anthropic_client.py"),
        ("base.py", "llm/base.py"),
        ("llm_wrapper.py", "llm/llm_wrapper.py"),
        ("openai_client.py", "llm/openai_client.py"),
        ("schema.py", "schema/schema.py"),
        ("agent.py", "agent.py"),
        ("cli.py", "cli.py"),
        ("config.py", "config.py"),
        ("llm.py", "llm.py"),
        ("logger.py", "logger.py"),
        ("retry.py", "retry.py")
    ]
    
    for our_file, ref_file in files_to_analyze:
        print(f"\n📄 COMPARING: {our_file}")
        print("-" * 40)
        
        our_path = Path(f"mini_agent/{ref_file}")
        ref_path = Path(f"reference_mini_agent/mini_agent/{ref_file}")
        
        if not our_path.exists():
            print(f"   ❌ Our {our_file}: NOT FOUND")
            continue
            
        if not ref_path.exists():
            print(f"   ❌ Reference {our_file}: NOT FOUND")
            continue
            
        # Read both files
        our_content = our_path.read_text(encoding="utf-8")
        ref_content = ref_path.read_text(encoding="utf-8")
        
        print(f"   📊 Our size: {len(our_content):,} chars")
        print(f"   📊 Ref size: {len(ref_content):,} chars")
        print(f"   📊 Difference: {len(our_content) - len(ref_content):+,} chars")
        
        # Quick analysis of differences
        our_lines = our_content.split('\n')
        ref_lines = ref_content.split('\n')
        
        print(f"   📊 Our lines: {len(our_lines):,}")
        print(f"   📊 Ref lines: {len(ref_lines):,}")
        
        # Look for major differences in imports
        our_imports = [line.strip() for line in our_lines if line.strip().startswith('import') or line.strip().startswith('from')]
        ref_imports = [line.strip() for line in ref_lines if line.strip().startswith('import') or line.strip().startswith('from')]
        
        print(f"   📊 Our imports: {len(our_imports)}")
        print(f"   📊 Ref imports: {len(ref_imports)}")
        
        # Look for key differences
        if "Z.AI" in our_content and "Z.AI" not in ref_content:
            print(f"   🚨 Our implementation has Z.AI integration (reference doesn't)")
            
        if "MCP" in our_content and "MCP" not in ref_content:
            print(f"   🚨 Our implementation has MCP integration (reference doesn't)")
            
        if "debug" in our_content and "debug" not in ref_content:
            print(f"   🚨 Our implementation has debug mode (reference doesn't)")

def main():
    """Run comprehensive comparison."""
    print("🔬 COMPREHENSIVE MINI-AGENT COMPARISON ANALYSIS")
    print("Comparing our implementation with reference implementation")
    print("=" * 70)
    
    # Compare file sizes
    compare_file_sizes()
    
    # Compare config files
    compare_config_yaml()
    
    # Compare directory structures
    compare_directory_structure()
    
    # Compare specific files
    compare_specific_files()
    
    print(f"\n🎯 COMPARISON COMPLETE")
    print("This provides a comprehensive overview of differences between")
    print("our implementation and the reference implementation.")

if __name__ == "__main__":
    main()
