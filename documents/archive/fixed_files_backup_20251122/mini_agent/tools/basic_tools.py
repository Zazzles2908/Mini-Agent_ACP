"""Basic tool implementations for Mini-Agent"""
import subprocess
from typing import Dict, Any, List


class BashTool:
    """Tool for running bash commands"""
    
    def __init__(self):
        self.name = "bash"
        self.description = "Execute bash commands"
    
    def execute(self, command: str) -> Dict[str, Any]:
        """Execute a bash command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }


class ReadTool:
    """Tool for reading files"""
    
    def __init__(self, workspace_dir: str = "."):
        self.name = "read"
        self.description = "Read files from workspace"
        self.workspace_dir = workspace_dir
    
    def execute(self, file_path: str) -> Dict[str, Any]:
        """Read a file"""
        try:
            from pathlib import Path
            full_path = Path(self.workspace_dir) / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "success": True,
                "content": content,
                "file_path": str(full_path)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }


class WriteTool:
    """Tool for writing files"""
    
    def __init__(self, workspace_dir: str = "."):
        self.name = "write"
        self.description = "Write files to workspace"
        self.workspace_dir = workspace_dir
    
    def execute(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write content to a file"""
        try:
            from pathlib import Path
            full_path = Path(self.workspace_dir) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "success": True,
                "file_path": str(full_path)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }


class EditTool:
    """Tool for editing files"""
    
    def __init__(self, workspace_dir: str = "."):
        self.name = "edit"
        self.description = "Edit file content"
        self.workspace_dir = workspace_dir
    
    def execute(self, file_path: str, find_text: str, replace_text: str) -> Dict[str, Any]:
        """Edit a file by replacing text"""
        try:
            from pathlib import Path
            full_path = Path(self.workspace_dir) / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if find_text not in content:
                return {
                    "success": False,
                    "error": f"Text '{find_text}' not found in file",
                    "file_path": file_path
                }
            
            new_content = content.replace(find_text, replace_text)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {
                "success": True,
                "file_path": str(full_path)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }