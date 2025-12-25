#!/usr/bin/env python3
"""
Check for duplicate test function names across test files.

This script helps prevent duplicate test names that can cause confusion
and maintenance issues.

Usage:
    uv run python scripts/check_duplicate_test_names.py
"""

import re
from pathlib import Path
from collections import defaultdict
import sys


def find_test_functions_with_context(test_file: Path) -> list[tuple[str, str]]:
    """Extract test function names with their class context."""
    content = test_file.read_text()
    functions = []
    current_class = None
    
    for line in content.split('\n'):
        # Match class definitions
        class_match = re.match(r'class (\w+):', line)
        if class_match:
            current_class = class_match.group(1)
        
        # Match function definitions
        func_match = re.match(r'\s+def (test_\w+)\(', line)
        if func_match:
            func_name = func_match.group(1)
            functions.append((func_name, current_class))
    
    return functions


def main():
    """Check for duplicate test names across all test files."""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / 'tests'
    
    if not tests_dir.exists():
        print(f"Error: {tests_dir} does not exist")
        sys.exit(1)
    
    # Collect all test functions with file and class context
    test_functions = defaultdict(list)
    
    for test_file in sorted(tests_dir.glob('test_*.py')):
        functions = find_test_functions_with_context(test_file)
        file_path = str(test_file.relative_to(project_root))
        for func_name, test_class in functions:
            test_functions[func_name].append((file_path, test_class))
    
    # Find duplicates across different files (same name in different files = bad)
    # Same name in different classes within same file is acceptable
    cross_file_duplicates = {}
    for name, locations in test_functions.items():
        files = set(loc[0] for loc in locations)
        if len(files) > 1:  # Same name in different files
            cross_file_duplicates[name] = locations
    
    print("=" * 80)
    print("DUPLICATE TEST NAME CHECK (Cross-File Only)")
    print("=" * 80)
    print("\nNote: Same test names in different classes within the same file are acceptable.")
    
    if cross_file_duplicates:
        print(f"\n⚠️  Found {len(cross_file_duplicates)} duplicate test names across different files:\n")
        for name, locations in sorted(cross_file_duplicates.items()):
            print(f"  {name}:")
            for file, test_class in locations:
                print(f"    - {file} (class: {test_class})")
        print("\n" + "=" * 80)
        print("RECOMMENDATION:")
        print("=" * 80)
        print("Rename duplicate tests to be more specific:")
        print("  - Include module/tool name in test name")
        print("  - Add context (e.g., test_mcp_client_no_config_basic vs test_mcp_client_no_config_agentic)")
        print("  - See docs/TEST_ORGANIZATION_GUIDELINES.md for naming conventions")
        sys.exit(1)
    else:
        print("\n✅ No duplicate test names across different files!")
        print("=" * 80)
        sys.exit(0)


if __name__ == '__main__':
    main()

