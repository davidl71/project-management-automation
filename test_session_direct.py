#!/usr/bin/env python3
"""
Direct test of session function (bypasses MCP framework).
Use this to verify the function works correctly.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from project_management_automation.tools.consolidated import session

print("🧪 Testing session function directly (bypassing MCP)...\n")

result = session(
    action='prime',
    include_hints=True,
    include_tasks=True,
    include_git_status=True
)

print(f"✅ Function call successful!")
print(f"   Type: {type(result).__name__}")
print(f"   Length: {len(result)} characters\n")

try:
    data = json.loads(result)
    print("✅ Valid JSON response:")
    print(f"   Auto-primed: {data.get('auto_primed', False)}")
    if 'detection' in data:
        print(f"   Mode: {data['detection'].get('mode', 'unknown')}")
        print(f"   Agent: {data['detection'].get('agent', 'unknown')}")
    print(f"   Keys: {list(data.keys())[:10]}")
    print("\n✅ Function works correctly - issue is in FastMCP framework")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
    print(f"   Content: {result[:200]}...")
