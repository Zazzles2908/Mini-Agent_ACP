# Z.AI MiniMax-M2 Search Results Integration

## Overview
This integration enables MiniMax-M2 to naturally cite Z.AI web search results by formatting them as MiniMax-M2's `search_result` blocks, providing web search-quality citations through the MiniMax-M2 SDK interface.

## Architecture
```
User Query → MiniMax-M2 Code (Z.AI Anthropic endpoint) → Z.AI Web Search → MiniMax-M2 cites results naturally
```

## Configuration
- **Endpoint**: `https://api.z.ai/api/anthropic`
- **API Key**: Z.AI Coding Plan key
- **Models**: GLM-4.6 (free), GLM-4.5 (paid)-air
- **Usage Quota**: ~120 prompts every 5 hours

## Implementation
The integration works by:
1. Using Z.AI's Anthropic-compatible endpoint for MiniMax-M2 Code
2. Formatting Z.AI web search results as `search_result` blocks
3. Enabling MiniMax-M2 to cite sources naturally like web search results

## Benefits
- Natural citation format matching web search
- Same usage quota as MiniMax-M2 Code (3x MiniMax-M2 Pro)
- Cost-effective through Coding Plan
- Seamless integration with existing MiniMax-M2 workflow

## Usage
1. Configure MiniMax-M2 Code with Z.AI endpoint
2. Use web search tool that returns `search_result` blocks
3. MiniMax-M2 automatically cites sources when using information

## Files Referenced
- `C:\Users\Jazeel-Home\Mini-Agent\documents\examples\Z_AI_Connects_MiniMax-M2_SDK_WEB.md`
- `C:\Users\Jazeel-Home\Mini-Agent\documents\examples\MiniMax-M2_Code_Lite_Plan_integration.md`
