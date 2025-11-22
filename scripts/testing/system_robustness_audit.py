#!/usr/bin/env python3
"""
Comprehensive System Robustness Audit
Evaluates Mini-Agent system health, identifies cleanup needs, and suggests improvements
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
import subprocess

def analyze_file_structure():
    """Analyze the entire file structure for cleanup opportunities"""
    
    # Define paths to analyze
    root_path = Path(".")
    analysis_results = {
        'backup_files': [],
        'duplicate_directories': [],
        'build_artifacts': [],
        'test_cache': [],
        'log_files': [],
        'config_files': [],
        'core_modules': [],
        'skills_modules': [],
        'documentation': [],
        'scripts': []
    }
    
    # Directory patterns to identify
    backup_patterns = [
        r'backup.*',
        r'mini_agent_backup.*',
        r'backup_current_state',
        r'archival?',
        r'archive.*',
        r'old.*',
        r'previous.*'
    ]
    
    build_patterns = [
        r'build/',
        r'dist/',
        r'__pycache__',
        r'.pytest_cache',
        r'.tox',
        r'.coverage'
    ]
    
    redundant_patterns = [
        r'exai.*',
        r'exai-downloads',
        r'exai_research',
        r'redundant.*',
        r'temp.*',
        r'cache.*',
        r'.tmp'
    ]
    
    def is_pattern_match(name, patterns):
        return any(re.match(pattern, name, re.IGNORECASE) for pattern in patterns)
    
    def categorize_file(path, name):
        """Categorize files for analysis"""
        if is_pattern_match(name, backup_patterns):
            analysis_results['backup_files'].append(str(path))
        elif is_pattern_match(name, build_patterns):
            analysis_results['build_artifacts'].append(str(path))
        elif is_pattern_match(name, redundant_patterns):
            analysis_results['duplicate_directories'].append(str(path))
        elif name.startswith('.pytest_cache'):
            analysis_results['test_cache'].append(str(path))
        elif name.endswith(('.log', '.txt')) and 'test' in name.lower():
            analysis_results['log_files'].append(str(path))
        elif name.endswith(('.json', '.yaml', '.yml', '.toml')):
            analysis_results['config_files'].append(str(path))
        elif 'mini_agent' in name and path.is_file():
            analysis_results['core_modules'].append(str(path))
        elif 'skill' in name.lower():
            analysis_results['skills_modules'].append(str(path))
        elif name.endswith('.md'):
            analysis_results['documentation'].append(str(path))
        elif name.endswith('.py') and any(x in name for x in ['script', 'test', 'util']):
            analysis_results['scripts'].append(str(path))
    
    # Walk through directory structure
    for root, dirs, files in os.walk(root_path):
        root_path = Path(root)
        
        # Skip certain directories
        dirs[:] = [d for d in dirs if not d.startswith('.git') and d not in ['node_modules', '.env']]
        
        for name in dirs + files:
            full_path = root_path / name
            if full_path.exists():
                categorize_file(full_path, name)
    
    return analysis_results

def analyze_code_quality():
    """Analyze code quality and identify issues"""
    issues = []
    modules = []
    
    # Find Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.py') and not any(skip in root for skip in ['.git', '__pycache__', 'build', 'test']):
                python_files.append(Path(root) / file)
    
    for py_file in python_files[:20]:  # Limit to first 20 for performance
        try:
            content = py_file.read_text()
            lines = content.split('\n')
            
            # Check for common issues
            if 'TODO' in content or 'FIXME' in content:
                issues.append(f"TODOs/FIXMEs in {py_file}")
            
            if 'print(' in content and 'debug' not in content.lower():
                issues.append(f"Debug prints in {py_file}")
            
            if 'import *' in content:
                issues.append(f"Wildcard imports in {py_file}")
            
            # Check for long functions (>100 lines)
            function_lengths = []
            in_function = False
            function_depth = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('def ') or stripped.startswith('async def '):
                    in_function = True
                    function_depth = 0
                elif in_function:
                    if stripped:
                        function_depth += 1
                    if stripped.startswith('def ') or stripped.startswith('class '):
                        function_lengths.append(function_depth)
                        function_depth = 0 if stripped.startswith('def ') else 1
            
            if any(length > 100 for length in function_lengths):
                issues.append(f"Long functions (>100 lines) in {py_file}")
            
            modules.append({
                'file': str(py_file),
                'lines': len(lines),
                'issues': len([i for i in issues if str(py_file) in i])
            })
            
        except Exception as e:
            issues.append(f"Error reading {py_file}: {str(e)}")
    
    return {'issues': issues, 'modules': modules}

def analyze_dependencies():
    """Analyze dependency management"""
    dep_files = []
    
    # Look for dependency files
    dep_patterns = ['requirements.txt', 'pyproject.toml', 'package.json', 'Pipfile']
    for pattern in dep_patterns:
        dep_files.extend(Path('.').glob(pattern))
    
    deps = {}
    for dep_file in dep_files:
        try:
            if dep_file.name == 'pyproject.toml':
                content = dep_file.read_text()
                if '[tool.poetry.dependencies]' in content or '[project.dependencies]' in content:
                    deps[dep_file.name] = 'TOML format detected'
            elif dep_file.name == 'requirements.txt':
                deps[dep_file.name] = f"{len(dep_file.read_text().splitlines())} dependencies"
            elif dep_file.name == 'package.json':
                deps[dep_file.name] = 'Node.js dependencies'
        except Exception as e:
            deps[dep_file.name] = f"Error reading: {str(e)}"
    
    return deps

def check_system_integration():
    """Check system integration points"""
    checks = []
    
    # Check for environment variables
    env_vars = ['MINIMAX_API_KEY', 'ZAI_API_KEY', 'ANTHROPIC_API_KEY', 'OPENAI_API_KEY']
    env_status = {}
    for var in env_vars:
        env_status[var] = 'set' if os.getenv(var) else 'missing'
    
    # Check MCP configuration
    mcp_configs = []
    for mcp_file in ['.mcp.json', 'mcp.json']:
        if Path(mcp_file).exists():
            mcp_configs.append(mcp_file)
    
    # Check for configuration files
    config_files = ['config.yaml', 'config.yml', 'settings.json']
    for config_file in config_files:
        if Path(config_file).exists():
            checks.append(f"Config file found: {config_file}")
    
    return {
        'env_vars': env_status,
        'mcp_configs': mcp_configs,
        'config_checks': checks
    }

def generate_cleanup_recommendations(analysis):
    """Generate specific cleanup and improvement recommendations"""
    recommendations = []
    
    # Backup files cleanup
    if analysis['file_structure']['backup_files']:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Workspace Cleanup',
            'action': f"Remove {len(analysis['file_structure']['backup_files'])} backup directories",
            'details': 'Backup directories are polluting the workspace',
            'impact': 'Improved workspace organization'
        })
    
    # Build artifacts cleanup
    if analysis['file_structure']['build_artifacts']:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Build Management',
            'action': f"Clean {len(analysis['file_structure']['build_artifacts'])} build artifacts",
            'details': 'Build artifacts should not be in version control',
            'impact': 'Reduced repository size, faster operations'
        })
    
    # Code quality issues
    if analysis['code_quality']['issues']:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Code Quality',
            'action': f"Address {len(analysis['code_quality']['issues'])} code quality issues",
            'details': 'TODOs, debug prints, and other code smells',
            'impact': 'Better maintainability'
        })
    
    # Duplicate directories
    if analysis['file_structure']['duplicate_directories']:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Space Optimization',
            'action': f"Remove {len(analysis['file_structure']['duplicate_directories'])} duplicate directories",
            'details': 'Directory redundancy is consuming unnecessary space',
            'impact': 'Reduced disk usage, cleaner structure'
        })
    
    return recommendations

def main():
    """Main audit function"""
    print("🔍 Starting Comprehensive System Robustness Audit...")
    print("=" * 60)
    
    # Run all analyses
    print("\n📁 Analyzing File Structure...")
    file_structure = analyze_file_structure()
    
    print("\n💻 Analyzing Code Quality...")
    code_quality = analyze_code_quality()
    
    print("\n📦 Analyzing Dependencies...")
    dependencies = analyze_dependencies()
    
    print("\n🔗 Checking System Integration...")
    integration = check_system_integration()
    
    # Compile results
    analysis_results = {
        'file_structure': file_structure,
        'code_quality': code_quality,
        'dependencies': dependencies,
        'integration': integration
    }
    
    # Generate recommendations
    recommendations = generate_cleanup_recommendations(analysis_results)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 AUDIT RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"\n📁 File Structure Analysis:")
    for category, files in file_structure.items():
        print(f"  {category.replace('_', ' ').title()}: {len(files)} items")
    
    print(f"\n💻 Code Quality Analysis:")
    print(f"  Total Python modules analyzed: {len(code_quality['modules'])}")
    print(f"  Code quality issues found: {len(code_quality['issues'])}")
    
    print(f"\n📦 Dependencies:")
    for dep_file, status in dependencies.items():
        print(f"  {dep_file}: {status}")
    
    print(f"\n🔗 System Integration:")
    for var, status in integration['env_vars'].items():
        print(f"  {var}: {status}")
    
    print(f"\n📋 CLEANUP RECOMMENDATIONS ({len(recommendations)} items):")
    print("-" * 40)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. [{rec['priority']}] {rec['category']}")
        print(f"   Action: {rec['action']}")
        print(f"   Details: {rec['details']}")
        print(f"   Impact: {rec['impact']}")
    
    # Calculate overall health score
    issues = (len(file_structure['backup_files']) + 
              len(file_structure['build_artifacts']) + 
              len(code_quality['issues']) + 
              len(file_structure['duplicate_directories']))
    
    max_issues = 100  # Reasonable baseline
    health_score = max(0, 100 - (issues * 2))
    
    print(f"\n🎯 SYSTEM HEALTH SCORE: {health_score}/100")
    
    if health_score >= 90:
        print("   ✅ EXCELLENT - System is highly robust")
    elif health_score >= 80:
        print("   ✅ GOOD - System is robust with minor cleanup needed")
    elif health_score >= 70:
        print("   ⚠️  FAIR - System needs attention")
    else:
        print("   ❌ POOR - System needs significant cleanup")
    
    return analysis_results, recommendations, health_score

if __name__ == "__main__":
    main()