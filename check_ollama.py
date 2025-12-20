#!/usr/bin/env python3
"""Quick script to check Ollama status.
Uses uv for package management (project standard).
Run with: uv run python check_ollama.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from project_management_automation.tools.ollama_integration import check_ollama_status
    result = check_ollama_status()
    print(result)
except ImportError as e:
    print(f"Error: {e}")
    print("\nTo install dependencies, run: uv sync")
    print("Then run with: uv run python check_ollama.py")
    sys.exit(1)
except Exception as e:
    print(f"Error checking Ollama status: {e}")
    sys.exit(1)

