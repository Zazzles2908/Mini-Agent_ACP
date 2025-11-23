#!/usr/bin/env python3
"""Test CLI startup with timeout"""

import subprocess
import sys
import os
import time

def test_cli_startup():
    """Test CLI startup with a timeout"""
    print("Testing CLI startup...")
    
    try:
        # Start the CLI process
        process = subprocess.Popen(
            [sys.executable, "-c", "import sys; sys.argv = ['mini-agent']; from mini_agent.cli import main; import asyncio; asyncio.run(main())"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # Wait for 3 seconds to see if it starts successfully
        try:
            stdout, stderr = process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait()
            print("CLI started successfully and was running without errors for 3 seconds")
            return True
        
        # If we get here, the process finished quickly - check for errors
        if process.returncode != 0:
            print(f"CLI exited with error code: {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
        else:
            print("CLI started and completed successfully")
            return True
            
    except Exception as e:
        print(f"Error testing CLI: {e}")
        return False

if __name__ == "__main__":
    result = test_cli_startup()
    print(f"CLI Test Result: {'SUCCESS' if result else 'FAILED'}")