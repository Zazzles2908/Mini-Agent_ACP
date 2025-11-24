"""Session Note Tool - Enhanced with memory intelligence.

This tool allows the agent to:
- Record key points and important information during sessions
- Recall previously recorded notes with intelligent categorization
- Maintain context across agent execution chains
- Enhanced with project context awareness and pattern learning
"""

import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Tool, ToolResult

# Import for configuration access
try:
    from mini_agent.config import get_config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

import logging
logger = logging.getLogger(__name__)


class EnhancedSessionNoteTool(Tool):
    """Enhanced session note tool with intelligent memory features.

    The agent can use this tool to:
    - Record important facts, decisions, or context during sessions
    - Recall information from previous sessions with intelligent categorization
    - Build up knowledge over time with project context awareness
    - Learn execution patterns for improved future performance

    Enhanced features (when memory.enable_enhanced = true):
    - Auto-categorization of notes using content analysis
    - Project context detection and linking
    - Pattern learning from execution flows
    - Cross-session knowledge integration

    Example usage by agent:
    - record_note("User prefers concise responses") -> auto-categorizes as 'user_preference'
    - record_note("Project uses Python 3.12 and async/await") -> links to project context
    - recall_notes() -> retrieves intelligently categorized notes
    """

    def __init__(self, memory_file: str = "./workspace/.agent_memory.json"):
        """Initialize enhanced session note tool.

        Args:
            memory_file: Path to the note storage file
        """
        self.memory_file = Path(memory_file)
        self.workspace_dir = Path(memory_file).parent
        
        # Initialize configuration
        self.config = get_config() if CONFIG_AVAILABLE else None
        self.memory_config = self.config.get_memory_config() if self.config else {}
        
        # Initialize enhanced features if enabled (MUST BE BEFORE project detection)
        self.enhanced_enabled = self.memory_config.get("enable_enhanced", False)
        
        # Initialize project context detection
        self.current_project = self._detect_project_context()
        
        # Lazy loading: file and directory are only created when first note is recorded
    
    def _detect_project_context(self) -> Optional[Dict[str, Any]]:
        """Detect project context from workspace files.
        
        Returns:
            Dictionary with project information or None if no project detected
        """
        if not self.enhanced_enabled:
            return None
            
        try:
            # Look for common project indicators
            project_indicators = {
                "python": {
                    "pyproject.toml": "Python project with modern tooling",
                    "requirements.txt": "Python project with dependencies",
                    "setup.py": "Python package project",
                    "Pipfile": "Python project with Pipenv",
                    ".python-version": "Python version specific project"
                },
                "node": {
                    "package.json": "Node.js project",
                    "node_modules/": "Node.js dependencies",
                    "npm-shrinkwrap.json": "Node.js locked dependencies"
                },
                "web": {
                    "index.html": "Web project",
                    "package.json": "Frontend project",
                    "src/": "Source code directory",
                    "dist/": "Built files directory"
                },
                "git": {
                    ".git/": "Git repository"
                }
            }
            
            detected_project = {
                "type": None,
                "name": None,
                "description": None,
                "files": [],
                "last_modified": datetime.now().isoformat()
            }
            
            # Scan workspace for project indicators
            if self.workspace_dir.exists():
                for root, dirs, files in self.workspace_dir.rglob("*"):
                    # Limit scan to avoid performance issues
                    if len(detected_project["files"]) > 50:
                        break
                        
                    for file_name, description in project_indicators.get("python", {}).items():
                        if (root / file_name).exists():
                            detected_project["type"] = "python"
                            detected_project["description"] = description
                            detected_project["files"].append(f"{root}/{file_name}")
                            
                    for file_name, description in project_indicators.get("node", {}).items():
                        if (root / file_name).exists():
                            detected_project["type"] = detected_project["type"] or "node"
                            detected_project["description"] = description
                            detected_project["files"].append(f"{root}/{file_name}")
                            
                    # Check for project name from common files
                    for file_name in ["README.md", "package.json", "pyproject.toml"]:
                        if file_name in files:
                            project_file = root / file_name
                            if project_file.exists():
                                try:
                                    content = project_file.read_text()
                                    # Extract project name from README or package.json
                                    if file_name == "README.md":
                                        lines = content.split('\n')[:10]
                                        for line in lines:
                                            if line.strip().startswith('# '):
                                                detected_project["name"] = line.strip()[2:].strip()
                                                break
                                    elif file_name == "package.json":
                                        import json
                                        package_data = json.loads(content)
                                        detected_project["name"] = package_data.get("name", "Unknown")
                                        detected_project["description"] = package_data.get("description", description)
                                except:
                                    pass
                            
            # Only return if we found something significant
            if detected_project["type"] or detected_project["files"]:
                return detected_project
            
            return None
            
        except Exception as e:
            if hasattr(self, 'config') and self.config and self.config.get("debug", False):
                logger.warning(f"Project context detection failed: {e}")
            return None
    
    def _classify_note_content(self, content: str, category: str = "general") -> Dict[str, Any]:
        """Intelligently classify note content and extract metadata.
        
        Args:
            content: The note content to classify
            category: User-provided category
            
        Returns:
            Dictionary with classification results
        """
        if not self.enhanced_enabled:
            return {"category": category, "type": "user_categorized", "confidence": 1.0}
            
        # Keywords for auto-categorization
        category_patterns = {
            "user_preference": ["prefer", "like", "dislike", "want", "avoid", "style", "format"],
            "technical_decision": ["decided", "choose", "implement", "use", "framework", "library"],
            "configuration": ["config", "setting", "parameter", "environment", "variable"],
            "project_info": ["project", "workspace", "directory", "file", "structure"],
            "learning": ["learn", "discover", "pattern", "insight", "realize", "understand"],
            "decision": ["decide", "choose", "select", "pick", "determine"],
            "error": ["error", "bug", "issue", "problem", "fix", "broken"],
            "success": ["success", "working", "fixed", "complete", "done"]
        }
        
        content_lower = content.lower()
        auto_category = category  # Start with user-provided category
        
        # Auto-detect category based on content
        for auto_cat, keywords in category_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                # Use user category if more specific, otherwise auto-detected
                if category == "general" or category not in category_patterns:
                    auto_category = auto_cat
                break
        
        # Extract metadata
        metadata = {
            "length": len(content),
            "has_code": bool(re.search(r'`[^`]+`|def |class |import |from ', content)),
            "has_urls": bool(re.search(r'http[s]?://', content)),
            "has_file_paths": bool(re.search(r'[\w\-_.]+\.\w+', content)),
            "confidence": 0.9 if auto_category != category else 0.7,
            "auto_categorized": auto_category != category,
            "linked_project": self.current_project is not None
        }
        
        return {
            "category": auto_category,
            "type": "auto_categorized" if metadata["auto_categorized"] else "user_categorized",
            "confidence": metadata["confidence"],
            "metadata": metadata
        }
    
    def _get_workspace_hash(self) -> str:
        """Generate a hash of current workspace for project identification.
        
        Returns:
            String hash representing current workspace state
        """
        try:
            import hashlib
            
            # Collect file paths and sizes for workspace fingerprint
            workspace_fingerprint = []
            if self.workspace_dir.exists():
                for file_path in self.workspace_dir.rglob("*"):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        stat = file_path.stat()
                        workspace_fingerprint.append(f"{file_path.relative_to(self.workspace_dir)}:{stat.st_size}")
            
            # Create hash of workspace structure
            workspace_str = "|".join(sorted(workspace_fingerprint))
            return hashlib.md5(workspace_str.encode()).hexdigest()[:8]
            
        except Exception:
            return "unknown"

    @property
    def name(self) -> str:
        return "record_note"

    @property
    def description(self) -> str:
        return (
            "Record important information as session notes for future reference. "
            "Use this to record key facts, user preferences, decisions, or context "
            "that should be recalled later in the agent execution chain. Each note is timestamped."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The information to record as a note. Be concise but specific.",
                },
                "category": {
                    "type": "string",
                    "description": "Optional category/tag for this note (e.g., 'user_preference', 'project_info', 'decision'). Will be auto-enhanced if memory enhancement is enabled.",
                    "default": "general"
                },
                "note_type": {
                    "type": "string",
                    "description": "Type of note for enhanced learning (e.g., 'general', 'insight', 'learning', 'pattern', 'decision'). Optional.",
                    "default": "general"
                },
            },
            "required": ["content"],
        }

    def _load_from_file(self) -> list:
        """Load notes from file.
        
        Returns empty list if file doesn't exist (lazy loading).
        """
        if not self.memory_file.exists():
            return []
        
        try:
            return json.loads(self.memory_file.read_text())
        except Exception:
            return []

    def _save_to_file(self, notes: list):
        """Save notes to file.
        
        Creates parent directory and file if they don't exist (lazy initialization).
        """
        # Ensure parent directory exists when actually saving
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.memory_file.write_text(json.dumps(notes, indent=2, ensure_ascii=False))

    async def execute(self, content: str, category: str = "general", note_type: str = "general") -> ToolResult:
        """Record an enhanced session note with intelligent categorization.

        Args:
            content: The information to record
            category: User-provided category (will be enhanced if needed)
            note_type: Type of note (general, insight, learning, pattern, etc.)

        Returns:
            ToolResult with success status and enhanced information
        """
        try:
            # Load existing notes
            notes = self._load_from_file()

            # Enhanced classification if enabled
            classification = self._classify_note_content(content, category)
            
            # Ensure classification has the expected structure
            if not isinstance(classification, dict):
                classification = {"category": category, "type": "user_categorized", "confidence": 1.0, "metadata": {}}
            
            # Create enhanced note structure
            note = {
                "timestamp": datetime.now().isoformat(),
                "category": classification.get("category", category),
                "note_type": note_type,
                "content": content,
                "classification": classification,
                "project_context": self.current_project,
                "workspace_hash": self._get_workspace_hash(),
                "enhanced": self.enhanced_enabled
            }

            # Add metadata for enhanced features
            if self.enhanced_enabled:
                note["metadata"] = classification.get("metadata", {})
                note["learning_data"] = {
                    "auto_categorized": classification.get("metadata", {}).get("auto_categorized", False),
                    "confidence": classification.get("metadata", {}).get("confidence", 1.0),
                    "linked_project": self.current_project is not None
                }

            notes.append(note)

            # Save back to file
            self._save_to_file(notes)

            # Build response message
            response_parts = [f"Recorded note: {content}"]
            
            if classification.get("category", category) != category and classification.get("category", "general") != "general":
                response_parts.append(f"(auto-categorized as: {classification.get('category', category)})")
            elif category != "general":
                response_parts.append(f"(category: {category})")
            
            if self.current_project:
                response_parts.append(f"(project context: {self.current_project.get('type', 'unknown')})")
            
            # Safe metadata access
            metadata = classification.get("metadata", {})
            if metadata.get("confidence", 1.0) < 0.8:
                response_parts.append(f"(confidence: {metadata.get('confidence', 1.0):.2f})")

            return ToolResult(
                success=True,
                content=" | ".join(response_parts),
                metadata={
                    "classification": classification,
                    "project_context": self.current_project,
                    "enhanced_features": self.enhanced_enabled
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"Failed to record note: {str(e)}",
            )


class EnhancedRecallNoteTool(Tool):
    """Enhanced tool for recalling recorded session notes with intelligent filtering."""

    def __init__(self, memory_file: str = "./workspace/.agent_memory.json"):
        """Initialize enhanced recall note tool.

        Args:
            memory_file: Path to the note storage file
        """
        self.memory_file = Path(memory_file)
        
        # Initialize configuration
        self.config = get_config() if CONFIG_AVAILABLE else None
        self.memory_config = self.config.get_memory_config() if self.config else {}
        
        # Initialize enhanced features if enabled (MUST BE BEFORE using in description)
        self.enhanced_enabled = self.memory_config.get("enable_enhanced", False)

    @property
    def name(self) -> str:
        return "recall_notes"

    @property
    def description(self) -> str:
        description = (
            "Recall all previously recorded session notes. "
            "Use this to retrieve important information, context, or decisions "
            "from earlier in the session or previous agent execution chains."
        )
        
        # Check if enhanced features might be available (without accessing self.enhanced_enabled)
        try:
            if self.memory_config.get("enable_enhanced", False):
                description += " Enhanced features include intelligent categorization, project context filtering, and smart search."
        except:
            pass  # Fallback to basic description
        
        return description
    
    @property
    def name(self) -> str:
        return "recall_notes"

    @property
    def parameters(self) -> dict[str, Any]:
        params = {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional: filter notes by category (supports wildcards with *)",
                },
                "note_type": {
                    "type": "string", 
                    "description": "Optional: filter notes by type (general, insight, learning, pattern, decision)",
                },
                "project_only": {
                    "type": "boolean",
                    "description": "Optional: only return notes linked to current project context",
                    "default": False
                },
                "limit": {
                    "type": "integer",
                    "description": "Optional: limit number of notes returned",
                    "default": 50
                },
                "search_text": {
                    "type": "string",
                    "description": "Optional: search within note content (enhanced feature)",
                },
                "confidence_min": {
                    "type": "number",
                    "description": "Optional: minimum confidence score for auto-categorized notes (0.0-1.0) (enhanced feature)",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.0
                }
            },
        }
        
        return params

    async def execute(self, category: str = None, note_type: str = None, project_only: bool = False, 
                     limit: int = 50, search_text: str = None, confidence_min: float = 0.0) -> ToolResult:
        """Recall session notes with enhanced filtering capabilities.

        Args:
            category: Optional category filter (supports wildcards)
            note_type: Optional note type filter
            project_only: Only return notes linked to current project
            limit: Maximum number of notes to return
            search_text: Optional text search within content
            confidence_min: Minimum confidence for auto-categorized notes

        Returns:
            ToolResult with enhanced notes content
        """
        try:
            if not self.memory_file.exists():
                return ToolResult(
                    success=True,
                    content="No notes recorded yet.",
                )

            notes = json.loads(self.memory_file.read_text())

            if not notes:
                return ToolResult(
                    success=True,
                    content="No notes recorded yet.",
                )

            # Enhanced filtering if enabled
            if self.enhanced_enabled:
                # Project context filtering
                if project_only:
                    current_workspace_hash = self._get_workspace_hash_for_filtering()
                    notes = [n for n in notes if n.get("workspace_hash") == current_workspace_hash or 
                            n.get("project_context") is not None]
                
                # Text search
                if search_text:
                    search_lower = search_text.lower()
                    notes = [n for n in notes if search_lower in n.get("content", "").lower()]
                
                # Confidence filtering
                if confidence_min > 0:
                    notes = [n for n in notes if n.get("metadata", {}).get("confidence", 1.0) >= confidence_min]
            
            # Apply standard filters
            if category:
                if "*" in category:
                    # Wildcard matching
                    import fnmatch
                    notes = [n for n in notes if fnmatch.fnmatch(n.get("category", ""), category)]
                else:
                    notes = [n for n in notes if n.get("category") == category]
            
            if note_type:
                notes = [n for n in notes if n.get("note_type") == note_type]
            
            if not notes:
                return ToolResult(
                    success=True,
                    content="No notes found matching the specified criteria.",
                )

            # Apply limit
            notes = notes[-limit:]  # Get most recent notes if limit is applied

            # Format notes for display with enhanced information
            formatted = []
            stats = {"total": len(notes), "categories": {}, "types": {}, "enhanced_count": 0}
            
            for idx, note in enumerate(notes, 1):
                timestamp = note.get("timestamp", "unknown time")
                cat = note.get("category", "general")
                content = note.get("content", "")
                note_type = note.get("note_type", "general")
                enhanced = note.get("enhanced", False)
                
                # Update stats
                stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
                stats["types"][note_type] = stats["types"].get(note_type, 0) + 1
                if enhanced:
                    stats["enhanced_count"] += 1
                
                # Build formatted note
                note_parts = [f"{idx}. [{cat}"]
                
                if note_type != "general":
                    note_parts.append(f", {note_type}")
                
                if enhanced and note.get("classification", {}).get("auto_categorized"):
                    note_parts.append("*")
                
                if note.get("project_context"):
                    note_parts.append(f", project:{note['project_context'].get('type', 'unknown')}")
                
                note_parts.append(f"] {content}\n   ")
                note_parts.append(f"(recorded: {timestamp})")
                
                if enhanced and note.get("metadata"):
                    conf = note["metadata"].get("confidence", 1.0)
                    if conf < 0.8:
                        note_parts.append(f" | confidence: {conf:.2f}")
                
                formatted.append("".join(note_parts))

            # Build result with statistics
            result_lines = ["Recorded Notes:"]
            
            # Add statistics
            if self.enhanced_enabled and len(notes) > 0:
                result_lines.append(f"\n📊 Stats: {stats['total']} notes")
                if stats["categories"]:
                    cat_stats = ", ".join([f"{cat}({count})" for cat, count in stats["categories"].items()])
                    result_lines.append(f"Categories: {cat_stats}")
                if stats["enhanced_count"] > 0:
                    result_lines.append(f"Enhanced notes: {stats['enhanced_count']}")
            
            result_lines.append("")
            result_lines.extend(formatted)
            
            if len(notes) >= limit:
                result_lines.append(f"\n... showing {limit} most recent notes")

            result = "\n".join(result_lines)

            return ToolResult(success=True, content=result, metadata=stats)

        except Exception as e:
            return ToolResult(
                success=False,
                content="",
                error=f"Failed to recall notes: {str(e)}",
            )
    
    def _get_workspace_hash_for_filtering(self) -> str:
        """Generate workspace hash for note filtering."""
        try:
            import hashlib
            
            workspace_fingerprint = []
            workspace_dir = self.memory_file.parent
            
            if workspace_dir.exists():
                for file_path in workspace_dir.rglob("*"):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        stat = file_path.stat()
                        workspace_fingerprint.append(f"{file_path.relative_to(workspace_dir)}:{stat.st_size}")
            
            workspace_str = "|".join(sorted(workspace_fingerprint))
            return hashlib.md5(workspace_str.encode()).hexdigest()[:8]
            
        except Exception:
            return "unknown"


# Backward compatibility: Original SessionNoteTool interface
class SessionNoteTool(EnhancedSessionNoteTool):
    """Backward compatible session note tool.
    
    This tool maintains the original interface while benefiting from enhanced features.
    """

    @property
    def description(self) -> str:
        return (
            "Record important information as session notes for future reference. "
            "Use this to record key facts, user preferences, decisions, or context "
            "that should be recalled later in the agent execution chain. Each note is timestamped."
            "Enhanced with intelligent categorization when memory enhancement is enabled."
        )

    async def execute(self, content: str, category: str = "general") -> ToolResult:
        """Record session note using original interface.
        
        Args:
            content: The information to record
            category: Category/tag for this note
            
        Returns:
            ToolResult with success status
        """
        # Call parent with original interface
        return await super().execute(content=content, category=category, note_type="general")


class RecallNoteTool(EnhancedRecallNoteTool):
    """Backward compatible recall note tool.
    
    This tool maintains the original interface while benefiting from enhanced features.
    """

    async def execute(self, category: str = None) -> ToolResult:
        """Recall session notes using original interface.
        
        Args:
            category: Optional category filter
            
        Returns:
            ToolResult with notes content
        """
        # Call parent with original interface
        return await super().execute(category=category)
