"""Z.AI Web Search with Claude Citation Format.

This module provides Z.AI web search results formatted as Claude's search_result blocks
with proper citations, following the Claude API specification for search results.

Based on user's requirement to use Z.AI web search results formatted as Claude
search_result blocks with citations through the Anthropic-compatible interface.
"""

import logging
from typing import Any, List, Dict

from ..llm.zai_client import ZAIClient, get_zai_api_key
from .base import Tool, ToolResult

logger = logging.getLogger(__name__)


class ClaudeCitationSearchResult:
    """Format Z.AI search results as Claude search_result blocks with citations."""
    
    def __init__(self, source: str, title: str, content: str):
        """Initialize a search result block.
        
        Args:
            source: Source URL or identifier
            title: Title of the search result
            content: Content to be included in the search result
        """
        self.source = source
        self.title = title
        self.content = content
    
    def to_claude_search_result_block(self) -> dict[str, Any]:
        """Convert to Claude search_result block format."""
        return {
            "type": "search_result",
            "source": self.source,
            "title": self.title,
            "content": [
                {
                    "type": "text",
                    "text": self.content
                }
            ],
            "citations": {
                "enabled": True
            }
        }


class ZAIWebSearchWithCitationsTool(Tool):
    """Z.AI web search tool that returns results in Claude's search_result format.
    
    This tool uses Z.AI's GLM web search and formats the results as
    Claude's search_result blocks with proper citations, enabling
    natural source attribution in Claude responses.
    
    Integration: Use with GLM Coding Plan setup (ANTHROPIC_BASE_URL: https://api.z.ai/api/anthropic)
    """
    
    def __init__(self, api_key: str | None = None):
        """Initialize Z.AI web search tool with citation formatting.
        
        Args:
            api_key: Z.AI API key (if None, loads from ZAI_API_KEY env var)
        """
        self.api_key = api_key or get_zai_api_key()
        if not self.api_key:
            logger.warning("Z.AI API key not found. Web search with citations will not be available.")
            self.available = False
            self.client = None
        else:
            try:
                self.client = ZAIClient(self.api_key)
                self.available = True
                logger.info("Z.AI web search tool with citations initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Z.AI client: {e}")
                self.available = False
                self.client = None

    @property
    def name(self) -> str:
        return "zai_web_search_with_citations"

    @property
    def description(self) -> str:
        return (
            "Z.AI GLM web search with Claude citation formatting. "
            "Performs web search using GLM and returns results in Claude's search_result "
            "format with proper source attribution and citations. "
            "Enables natural citations in Claude responses like Claude's native web search. "
            "Usage quota: ~120 prompts every 5 hours (GLM Coding Plan)."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query or research question",
                },
                "depth": {
                    "type": "string",
                    "description": "Analysis depth: 'quick' (3 sources), 'comprehensive' (7 sources), 'deep' (10 sources)",
                    "enum": ["quick", "comprehensive", "deep"],
                    "default": "comprehensive",
                },
                "model": {
                    "type": "string",
                    "description": "GLM model to use: 'glm-4.6' (comprehensive), 'glm-4.5' (optimized), or 'auto' (automatic)",
                    "enum": ["auto", "glm-4.6", "glm-4.5"],
                    "default": "glm-4.5",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results to return (default: 5)",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10,
                }
            },
            "required": ["query"],
        }

    async def execute(
        self,
        query: str,
        depth: str = "comprehensive",
        model: str = "auto",
        max_results: int = 5,
        **kwargs,
    ) -> ToolResult:
        """Execute Z.AI web search and format results as Claude search_result blocks.
        
        Args:
            query: Search query
            depth: Analysis depth
            model: GLM model preference
            max_results: Maximum results to return
            **kwargs: Additional parameters
            
        Returns:
            ToolResult with Claude-formatted search results
        """
        if not self.available or not self.client:
            return ToolResult(
                success=False,
                content="",
                error="Z.AI web search with citations not available. Set ZAI_API_KEY environment variable.",
            )

        try:
            # Perform Z.AI web search
            result = await self.client.research_and_analyze(
                query=query,
                depth=depth,
                model_preference=model,
            )

            if result.get("success"):
                # Format results as Claude search_result blocks
                search_results = self._format_search_results(result, max_results)
                
                # Return formatted for Claude tool use
                content = {
                    "type": "tool_result",
                    "content": search_results,  # List of search_result blocks
                    "name": "zai_web_search_with_citations"
                }
                
                return ToolResult(
                    success=True,
                    content=str(content),  # Return as string for tool result
                )
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Z.AI web search with citations failed: {error_msg}")
                return ToolResult(
                    success=False,
                    content="",
                    error=f"Web search with citations failed: {error_msg}",
                )

        except Exception as e:
            logger.exception("Z.AI web search with citations execution failed")
            return ToolResult(
                success=False,
                content="",
                error=f"Web search with citations error: {str(e)}",
            )

    def _format_search_results(self, zai_result: Dict[str, Any], max_results: int) -> List[Dict[str, Any]]:
        """Format Z.AI search results as Claude search_result blocks.
        
        Args:
            zai_result: Z.AI search result from research_and_analyze
            max_results: Maximum number of results to format
            
        Returns:
            List of Claude search_result block dictionaries
        """
        search_results = []
        
        # Extract search evidence (URLs and information from Z.AI)
        search_evidence = zai_result.get('search_evidence', [])
        
        # Limit to max_results
        evidence_items = search_evidence[:max_results]
        
        for i, evidence in enumerate(evidence_items):
            # Format each evidence as a search result block
            if isinstance(evidence, dict):
                source = evidence.get('url', f"source_{i+1}")
                title = evidence.get('title', f"Search Result {i+1}")
                
                # Extract meaningful content
                content = evidence.get('content', '')
                if not content:
                    # Use description or summary if available
                    content = evidence.get('description', evidence.get('summary', 'No content available'))
                
                # Create Claude search result block
                search_result = ClaudeCitationSearchResult(
                    source=source,
                    title=title,
                    content=content
                )
                
                search_results.append(search_result.to_claude_search_result_block())
            else:
                # Handle case where evidence is just text
                search_result = ClaudeCitationSearchResult(
                    source=f"source_{i+1}",
                    title=f"Search Result {i+1}",
                    content=str(evidence)
                )
                search_results.append(search_result.to_claude_search_result_block())
        
        # If no search evidence, create a result from the analysis
        if not search_results:
            analysis_content = zai_result.get('analysis', 'No search results available')
            search_result = ClaudeCitationSearchResult(
                source="zai_web_search",
                title="Z.AI Web Search Analysis",
                content=analysis_content
            )
            search_results.append(search_result.to_claude_search_result_block())
        
        return search_results

    def get_claude_tool_schema(self) -> Dict[str, Any]:
        """Get the tool schema formatted for Claude tool calling.
        
        Returns:
            Tool schema dictionary for Claude
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters
        }

    def format_for_anthropic_client(self) -> List[Dict[str, Any]]:
        """Format the tool for use with Anthropic client.
        
        Returns:
            List containing the formatted tool schema for Anthropic
        """
        return [self.get_claude_tool_schema()]