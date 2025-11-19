#!/usr/bin/env python3
"""Main entry point for ACP server"""

from mini_agent.acp import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())