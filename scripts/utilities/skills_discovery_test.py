#!/usr/bin/env python3
"""
Skills Discovery Test
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, '.')

# Load environment
from start_mini_agent import load_environment
load_environment()

print("🔍 Skills Discovery Test")
print("=" * 40)

# Test skill discovery with correct path
skills_dir = Path("mini_agent/skills")

print(f"Skills directory: {skills_dir.absolute()}")
print(f"Directory exists: {skills_dir.exists()}")

if skills_dir.exists():
    skill_files = list(skills_dir.rglob("SKILL.md"))
    print(f"Found {len(skill_files)} skill files:")
    for skill_file in skill_files[:5]:
        print(f"  - {skill_file}")
    if len(skill_files) > 5:
        print(f"  ... and {len(skill_files) - 5} more")

# Test SkillLoader with correct path
print("\n🧪 Testing SkillLoader:")
try:
    from mini_agent.tools.skill_loader import SkillLoader
    
    loader = SkillLoader("mini_agent/skills")
    skills = loader.discover_skills()
    
    print(f"✅ Loaded {len(skills)} skills:")
    for skill in skills[:3]:
        print(f"  - {skill.name}: {skill.description[:60]}...")
    if len(skills) > 3:
        print(f"  ... and {len(skills) - 3} more")
    
    # Test list_skills method
    skill_names = loader.list_skills()
    print(f"\n📋 Skill names ({len(skill_names)} total):")
    for name in skill_names[:5]:
        print(f"  - {name}")
    if len(skill_names) > 5:
        print(f"  ... and {len(skill_names) - 5} more")

except Exception as e:
    print(f"❌ SkillLoader failed: {e}")
    import traceback
    traceback.print_exc()
