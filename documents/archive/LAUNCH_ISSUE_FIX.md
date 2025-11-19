# Mini-Agent Launch Issue: Dependencies & Environment

**Status:** Dependencies missing in global Python install

---

## Issue Summary

When running `mini-agent`, you encountered:
```
ModuleNotFoundError: No module named 'aiohttp'
```

Even though dependencies are installed, they're in the **user site-packages** but mini-agent is running from a **global Python** install.

---

## Root Cause

Mini-Agent has multiple installations:
```
C:\Users\Jazeel-Home\.local\bin\mini-agent.bat          # Wrapper script
C:\Users\Jazeel-Home\.local\bin\mini-agent.exe          # Local install
C:\Users\Jazeel-Home\AppData\Roaming\Python\...         # User install
```

The `.bat` wrapper is using `C:\Python313\python.exe` which doesn't have access to user-installed packages when running in editable mode.

---

## Solution 1: Fix Dependencies (Quick Fix)

Add missing dependencies to `pyproject.toml`:

```toml
dependencies = [
    ...
    "aiohttp>=3.8.0",        # Added ✅
    "python-dotenv>=1.0.0",  # Added ✅
    ...
]
```

**Already done!** Now reinstall:

```bash
cd C:\Users\Jazeel-Home\Mini-Agent
pip install -e .
```

---

## Solution 2: Run Python Module Directly (Recommended)

Instead of using the `mini-agent` command, run the module directly:

```bash
cd C:\Users\Jazeel-Home\Mini-Agent
python -m mini_agent.cli --workspace .
```

This ensures the correct Python environment with all dependencies.

---

## Solution 3: Load .env File

Mini-Agent CLI doesn't automatically load `.env` from the current directory. You need to either:

**Option A: Set environment variable before running:**
```powershell
$env:ZAI_API_KEY = "7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe"
python -m mini_agent.cli --workspace .
```

**Option B: Update CLI to load .env** (Better fix):

Edit `mini_agent/cli.py` to load .env at startup:

```python
# Add at top of file
from dotenv import load_dotenv
from pathlib import Path

# In main() function, before loading config:
def main():
    # Load .env file if it exists
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    # Rest of code...
```

---

## Recommended Workflow

**For Development (Now):**
```bash
cd C:\Users\Jazeel-Home\Mini-Agent

# Set environment variable
$env:ZAI_API_KEY = "7a4720203ba745d09eba3ee511340d0c.ecls7G5Qh6cPF4oe"

# Run directly
python -m mini_agent.cli --workspace .
```

**For Production (After fixing .env loading):**
```bash
cd C:\Users\Jazeel-Home\Mini-Agent
mini-agent --workspace .
```

---

## Update pyproject.toml ✅ DONE

The dependencies have been added:
- `aiohttp>=3.8.0`
- `python-dotenv>=1.0.0`

And reinstalled with `pip install -e .`

---

## Next Step: Fix .env Loading in CLI

The CLI should automatically load `.env` from the workspace directory. This is a simple fix in `mini_agent/cli.py`.

Would you like me to implement this fix?
