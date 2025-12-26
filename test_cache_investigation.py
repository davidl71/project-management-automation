#!/usr/bin/env python3
"""Investigate FastMCP's TypeAdapter cache to see if it's causing the issue."""

import sys
import inspect
from pathlib import Path

# Read the types.py file to understand the cache
types_file = Path("/Users/davidl/Projects/project-management-automation/.venv/lib/python3.11/site-packages/fastmcp/utilities/types.py")

print("="*80)
print("INVESTIGATING FASTMCP TYPEDAPTER CACHE")
print("="*80)
print()

with open(types_file) as f:
    content = f.read()
    
    # Find the cache implementation
    if "@lru_cache" in content or "@cache" in content:
        print("Found cache decorator in types.py")
        # Find the line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "@lru_cache" in line or "@cache" in line:
                print(f"\nLine {i+1}: {line}")
                # Show context
                start = max(0, i - 5)
                end = min(len(lines), i + 20)
                print("\nContext:")
                for j in range(start, end):
                    marker = ">>>" if j == i else "   "
                    print(f"{marker} {j+1:4d}: {lines[j]}")
                break
    
    # Check if there's a module-level cache dict
    if "_type_adapter_cache" in content or "type_adapter_cache" in content:
        print("\nFound cache variable")
        import re
        matches = re.finditer(r'(_?type_adapter_cache\s*=\s*[^\n]+)', content)
        for match in matches:
            print(f"  {match.group(1)}")
    
    # Check how get_cached_typeadapter works
    if "def get_cached_typeadapter" in content:
        print("\nAnalyzing get_cached_typeadapter implementation...")
        # Extract the function
        import re
        func_match = re.search(r'def get_cached_typeadapter\([^)]*\):.*?(?=\n\ndef |\nclass |\Z)', content, re.DOTALL)
        if func_match:
            func_code = func_match.group(0)
            # Check if it uses a dict cache
            if "{}" in func_code or "dict()" in func_code or "Dict" in func_code:
                print("  Uses dict-based cache")
            # Check if it's decorated with lru_cache
            lines_before = content[:func_match.start()].split('\n')
            for i in range(max(0, len(lines_before) - 5), len(lines_before)):
                if "@lru_cache" in lines_before[i] or "@cache" in lines_before[i]:
                    print(f"  Decorated with cache: {lines_before[i].strip()}")
                    break

