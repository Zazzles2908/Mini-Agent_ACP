# Z.AI Claude Search Results Integration

## Overview
This integration enables Claude to naturally cite Z.AI web search results by formatting them as Claude's `search_result` blocks, providing web search-quality citations through the Claude SDK interface.

## Architecture
```
User Query → Claude Code (Z.AI Anthropic endpoint) → Z.AI Web Search → Claude cites results naturally
```

## Configuration
- **Endpoint**: `https://api.z.ai/api/anthropic`
- **API Key**: Z.AI Coding Plan key
- **Models**: GLM-4.6, GLM-4.5-air
- **Usage Quota**: ~120 prompts every 5 hours

## Implementation
The integration works by:
1. Using Z.AI's Anthropic-compatible endpoint for Claude Code
2. Formatting Z.AI web search results as `search_result` blocks
3. Enabling Claude to cite sources naturally like web search results

## Benefits
- Natural citation format matching web search
- Same usage quota as Claude Code (3x Claude Pro)
- Cost-effective through Coding Plan
- Seamless integration with existing Claude workflow

## Usage
1. Configure Claude Code with Z.AI endpoint
2. Use web search tool that returns `search_result` blocks
3. Claude automatically cites sources when using information

## Files Referenced
- `C:\Users\Jazeel-Home\Mini-Agent\documents\examples\Z_AI_Connects_Claude_SDK_WEB.md`
- `C:\Users\Jazeel-Home\Mini-Agent\documents\examples\Claude_Code_Lite_Plan_integration.md`
