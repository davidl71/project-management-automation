#!/usr/bin/env python3
"""Analyze _convert_to_content function and its usage."""

import re
from pathlib import Path

fastmcp_tool_file = Path("/Users/davidl/Projects/project-management-automation/.venv/lib/python3.11/site-packages/fastmcp/tools/tool.py")

print("="*80)
print("ANALYZING _convert_to_content FUNCTION")
print("="*80)
print()

# Read the file
with open(fastmcp_tool_file) as f:
    content = f.read()

# Find _convert_to_content definition
convert_match = re.search(r'def _convert_to_content\([^)]*\):.*?(?=\n\ndef |\nclass |\Z)', content, re.DOTALL)
if convert_match:
    print("_convert_to_content FUNCTION:")
    print("-" * 80)
    print(convert_match.group(0)[:1000])
    print()

# Find where it's called in run method
run_match = re.search(r'async def run\([^)]*\):.*?(?=\n    async def |\n    def |\nclass |\Z)', content, re.DOTALL)
if run_match:
    run_code = run_match.group(0)
    print("run METHOD (showing _convert_to_content usage):")
    print("-" * 80)
    # Find the line with _convert_to_content
    lines = run_code.split('\n')
    for i, line in enumerate(lines):
        if '_convert_to_content' in line:
            # Show context around this line
            start = max(0, i - 10)
            end = min(len(lines), i + 20)
            print('\n'.join(lines[start:end]))
            break
    print()

# Find helper functions
print("HELPER FUNCTIONS:")
print("-" * 80)
for func_name in ['_convert_to_single_content_block', '_serialize_with_fallback']:
    func_match = re.search(rf'def {func_name}\([^)]*\):.*?(?=\n\ndef |\nclass |\Z)', content, re.DOTALL)
    if func_match:
        print(f"\n{func_name}:")
        print(func_match.group(0)[:500])
        print()

