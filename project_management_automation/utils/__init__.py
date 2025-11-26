# project_management_automation/utils/__init__.py
"""
Utility functions for project management automation.

Exports:
    - find_project_root: Locate project root directory
    - split_output: Separate human/AI output for token efficiency
    - progress_wrapper: Progress reporting wrapper
    - compact_json: Compact JSON serialization
"""

from pathlib import Path
from typing import Optional

from .output import split_output, progress_wrapper, compact_json, output_to_human_and_ai


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find project root by looking for marker files.

    Looks for .git, .todo2, or CMakeLists.txt to identify project root.

    Args:
        start_path: Starting path for search (default: current file location)

    Returns:
        Path to project root, or current working directory if not found
    """
    if start_path is None:
        # Default to current working directory
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)

    current = start_path.resolve()

    # Look for project markers
    while current != current.parent:
        if (current / '.git').exists() or (current / '.todo2').exists() or (current / 'CMakeLists.txt').exists():
            return current
        current = current.parent

    # Fallback to current working directory
    return Path.cwd()


__all__ = [
    'find_project_root',
    'split_output',
    'progress_wrapper',
    'compact_json',
    'output_to_human_and_ai'
]

