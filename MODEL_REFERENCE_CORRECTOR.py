#!/usr/bin/env python3
"""
Mini-Agent Model Reference Corrector
===================================
Corrects all AI model references throughout the system to reflect the true architecture:
- Primary: MiniMax-M2 (300 prompts/5hrs)
- Secondary: GLM-4.6 via Z.AI (120 prompts/5hrs) 
- NOT MiniMax-M2 (OpenAI SDK format format)s, NOT MiniMax-M2, NOT GLM-4.6 (via Z.AI)
"""

import os
import re
import glob
from pathlib import Path

class ModelReferenceCorrector:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.corrections_made = 0
        self.files_processed = 0
        self.errors = []
        
        # Define correction patterns - OLD -> NEW
        self.corrections = {
            # Primary model corrections
            "MiniMax-M2": "MiniMax-M2",
            "MiniMax-M2": "MiniMax-M2",
            "minimax": "minimax",
            "MINIMAX": "MINIMAX",
            
            # MiniMax-M2 (OpenAI SDK format format) corrections
            "MiniMax-M2 (OpenAI SDK format format)": "MiniMax-M2 (OpenAI SDK format format)",
            "MiniMax-M2 (OpenAI SDK format format)s": "MiniMax-M2 (OpenAI SDK format format)",
            "MiniMax-M2 integration": "MiniMax-M2 integration",
            "OpenAI SDK format": "OpenAI SDK format format",
            
            # Specific model corrections
            "glm-4.6 (via Z.AI)": "glm-4.6 (via Z.AI)",
            "GLM-4.6 (via Z.AI)": "GLM-4.6 (via Z.AI)",
            "glm-4.6": "glm-4.6",
            "GLM-4.6": "GLM-4.6",
            "MiniMax-M2": "MiniMax-M2",
            "MiniMax-M2": "MiniMax-M2",
            
            # AI model corrections
            "MiniMax-M2 primary + GLM-4.6 secondary": "MiniMax-M2 primary + GLM-4.6 secondary",
            "2 AI models": "2 AI models",
            "AI models": "AI models",
            "AI model": "AI model",
            
            # Configuration corrections
            "minimax_model": "minimax_model", # Keep context-specific
            "MiniMax Model": "MiniMax Model",
            "MiniMax Integration": "MiniMax Integration",
            
            # Web function corrections (when specifically about GPT)
            "MiniMax-M2 backend)": "MiniMax-M2 backend) (GLM-4.6 backend)",
            "web functions": "web functions",
        }
        
        # Files to process
        self.file_patterns = [
            "*.md",
            "*.py", 
            "*.yaml",
            "*.yml",
            "*.json",
            "*.html",
            "*.txt"
        ]
        
        # Files to exclude (dependencies, etc.)
        self.exclude_dirs = [
            ".venv",
            "__pycache__",
            "node_modules",
            ".git"
        ]
        
    def should_process_file(self, file_path):
        """Check if file should be processed"""
        # Check if file is in excluded directory
        for excluded_dir in self.exclude_dirs:
            if excluded_dir in file_path.parts:
                return False
        
        # Check file extension
        if file_path.suffix.lower() in ['.md', '.py', '.yaml', '.yml', '.json', '.html', '.txt']:
            return True
            
        return False
    
    def get_files_to_process(self):
        """Get all files to process"""
        files = []
        for pattern in self.file_patterns:
            for file_path in self.root_dir.rglob(pattern):
                if self.should_process_file(file_path):
                    files.append(file_path)
        return files
    
    def correct_text(self, content):
        """Apply all corrections to text content"""
        original_content = content
        corrections_applied = 0
        
        for old, new in self.corrections.items():
            if old in content:
                content = content.replace(old, new)
                corrections_applied += self.corrections_made + 1
                self.corrections_made += 1
        
        # Additional context-aware corrections
        content = self._apply_context_aware_corrections(content)
        
        return content, corrections_applied
    
    def _apply_context_aware_corrections(self, content):
        """Apply context-specific corrections that need more sophisticated matching"""
        
        # Fix specific patterns in documentation
        patterns_to_fix = [
            # Architecture diagrams
            (r'(\|.*?\b)MiniMax-M2\b(.*?\|)', r'\1MiniMax-M2\2'),
            (r'(\|.*?\b)MiniMax-M2\b(.*?\|)', r'\1MiniMax-M2\2'),
            (r'(\|.*?\b)GLM-4.6 (via Z.AI)\b(.*?\|)', r'\1GLM-4.6 (Z.AI)\2'),
            
            # Configuration references
            (r'model: MiniMax-M2', 'model: MiniMax-M2'),
            (r'provider: "openai"  # OpenAI SDK format', 'provider: "openai"  # OpenAI SDK format"  # OpenAI SDK format format'),
            
            # List references
            (r'(?i)MiniMax-M2 primary + GLM-4.6 secondary', 'MiniMax-M2 primary + GLM-4.6 secondary'),
            (r'(?i)two AI models', 'two AI models'),
            
            # Technical descriptions
            (r'(?i)using.*?openai.*?model: MiniMax-M2 SDK format format'),
            (r'(?i)MiniMax-M2 backend', 'MiniMax-M2 backend'),
            (r'(?i)openai.*?sdk.*?model: MiniMax-M2 SDK format format (MiniMax-M2 + GLM-4.6)'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            matches = len(re.findall(pattern, content))
            if matches > 0:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                self.corrections_made += matches
        
        return content
    
    def process_file(self, file_path):
        """Process a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            corrected_content, corrections_in_file = self.correct_text(content)
            
            if corrections_in_file > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(corrected_content)
                
                print(f"✅ {file_path}: {corrections_in_file} corrections applied")
                return True
            else:
                print(f"⚪ {file_path}: No changes needed")
                return False
                
        except Exception as e:
            error_msg = f"❌ {file_path}: {str(e)}"
            self.errors.append(error_msg)
            print(error_msg)
            return False
    
    def run_correction(self):
        """Run the full correction process"""
        print("🔧 Mini-Agent Model Reference Corrector")
        print("=" * 50)
        print("Correcting AI model references to reflect true architecture:")
        print("• Primary: MiniMax-M2 (300 prompts/5hrs)")
        print("• Secondary: GLM-4.6 via Z.AI (120 prompts/5hrs)")
        print("• NOT MiniMax-M2 (OpenAI SDK format format)s, NOT MiniMax-M2, NOT GLM-4.6 (via Z.AI)")
        print("=" * 50)
        
        files = self.get_files_to_process()
        print(f"\n📁 Found {len(files)} files to process")
        
        for file_path in files:
            self.files_processed += 1
            self.process_file(file_path)
        
        print("\n" + "=" * 50)
        print("📊 CORRECTION SUMMARY")
        print(f"Files processed: {self.files_processed}")
        print(f"Corrections made: {self.corrections_made}")
        
        if self.errors:
            print(f"Errors encountered: {len(self.errors)}")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print("✅ All files processed successfully!")
        
        print("\n🎯 Architecture Truth Restored!")
        print("MiniMax-M2 = Primary agent (NOT MiniMax-M2)")
        print("GLM-4.6 = Web functions (NOT GLM-4.6 (via Z.AI))")
        print("OpenAI SDK format format = API compatibility (NOT MiniMax-M2 (OpenAI SDK format format)s)")

if __name__ == "__main__":
    corrector = ModelReferenceCorrector()
    corrector.run_correction()