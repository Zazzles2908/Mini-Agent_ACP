#!/usr/bin/env python3
"""
Terminal Bridge for Mini-Agent ACP
Provides ACP functionality from terminal
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from mini_agent.acp.__init___FIXED import main

if __name__ == "__main__":
    print("Starting Mini-Agent ACP Terminal Bridge")
    print("=" * 50)
    print("This bridge provides ACP protocol access from terminal")
    print("Protocol messages will be handled here")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nACP bridge terminated")
    except Exception as e:
        print(f"Bridge error: {e}")
