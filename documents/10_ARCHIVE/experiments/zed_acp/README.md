# Zed Editor ACP Integration Research

## Goal
Implement Agent Client Protocol (ACP) integration to enable Mini-Agent to work natively with Zed editor.

## Status
📋 **Planning Phase** - Research not yet started

## Background
Previous attempts to create VS Code extensions (.vsix files) did not successfully integrate with Zed editor. These failed builds are archived in `/documents/builds/archive/` for reference.

## Related Components
- **ACP Server**: `/mini_agent/acp/` - Agent Client Protocol server implementation
- **VS Code Extension**: `/vscode-extension/` - Reference implementation for VS Code Chat API
- **Failed Builds**: `/documents/builds/archive/` - Archived VSIX files from failed attempts

## Research Questions
1. What is the current state of ACP support in Zed editor?
2. What differences exist between Zed's ACP implementation and VS Code's?
3. Why did previous VSIX-based approaches fail?
4. What is the correct architecture for Zed integration?

## Next Steps
When beginning this research:

### 1. Environment Setup
```bash
# Install Zed editor
# Install Zed extension development tools
# Review Zed ACP documentation
```

### 2. Protocol Analysis
- Compare Zed ACP vs VS Code Chat API
- Document protocol differences
- Identify required adaptations

### 3. Implementation Strategy
- Decide: Extension vs direct ACP connection?
- Design architecture
- Create proof-of-concept

### 4. Testing
- Create minimal working example
- Test with Mini-Agent ACP server
- Document any issues

## Resources
- Zed Documentation: https://zed.dev/docs
- Agent Client Protocol Spec: (add link)
- VS Code Chat API (for comparison): https://code.visualstudio.com/api/extension-guides/chat

## Notes
- Keep this directory updated as research progresses
- Document all learnings, even failed approaches
- Create subdirectories for prototypes, tests, etc.
