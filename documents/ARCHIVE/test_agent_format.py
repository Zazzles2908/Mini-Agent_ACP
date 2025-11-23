#!/usr/bin/env python3
"""Test agent formatting to verify the fix."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mini_agent.agent import Agent, Colors, ICON_INFO, ICON_STEP

# Test the current formatting
print("=== TESTING AGENT FORMATTING ===")

# Simulate the exact code from agent.py
BOX_WIDTH = 20  # Current value
step_text = f"{Colors.BOLD}{Colors.BRIGHT_CYAN}[EXECUTION] Step 1/200{Colors.RESET}"
step_display_width = len(step_text)
padding = max(0, BOX_WIDTH - 1 - step_display_width)

print(f"\nCurrent ICON_INFO: {repr(ICON_INFO)}")
print(f"Current ICON_STEP: {repr(ICON_STEP)}")
print(f"BOX_WIDTH: {BOX_WIDTH}")
print(f"Padding: {padding}")
print()

# Test the actual output
print(f"{Colors.DIM}─{'─' * BOX_WIDTH}─{Colors.RESET}")
print(f"{Colors.DIM}│{Colors.RESET} {step_text}{' ' * padding}{Colors.DIM}│{Colors.RESET}")
print(f"{Colors.DIM}─{'─' * BOX_WIDTH}─{Colors.RESET}")

print("\n=== EXPECTED: Clean box border ===")
print("=== IF YOU SEE LONG REPEATING TEXT, CACHE ISSUE EXISTS ===")
