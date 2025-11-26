# project_management_automation/utils/__init__.py
"""
Utility functions for project management automation.

Exports:
    - find_project_root: Locate project root directory
    - split_output: Separate human/AI output for token efficiency
    - progress_wrapper: Progress reporting wrapper
    - compact_json: Compact JSON serialization
    - configure_logging: MCP-aware logging configuration
    - get_logger: Get MCP-aware logger
    - is_mcp_mode: Check if running as MCP server
"""

from pathlib import Path
from typing import Optional

from .output import split_output, progress_wrapper, compact_json, output_to_human_and_ai
from .logging_config import configure_logging, get_logger, is_mcp_mode, suppress_noisy_loggers


def find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find project root by looking for marker files.

    Looks for .git, .todo2, or CMakeLists.txt to identify project root.
    
    Search order:
    1. If start_path provided, search up from there
    2. Search up from current working directory
    3. Search up from package location (for MCP server context)

    Args:
        start_path: Starting path for search (optional)

    Returns:
        Path to project root, or current working directory if not found
    """
    def _search_up(path: Path) -> Optional[Path]:
        """Search upward for project markers."""
        current = path.resolve()
        while current != current.parent:
            if (current / '.git').exists() or (current / '.todo2').exists() or (current / 'CMakeLists.txt').exists():
                return current
            current = current.parent
        return None
    
    # If explicit start_path, use only that
    if start_path is not None:
        result = _search_up(Path(start_path))
        if result:
            return result
        return Path(start_path).resolve()
    
    # Try current working directory first
    result = _search_up(Path.cwd())
    if result:
        return result
    
    # Try package location (for MCP server context)
    # Go up from utils/__init__.py to project root
    package_path = Path(__file__).parent.parent.parent  # utils -> project_management_automation -> project root
    result = _search_up(package_path)
    if result:
        return result

    # Fallback to current working directory
    return Path.cwd()


__all__ = [
    'find_project_root',
    'split_output',
    'progress_wrapper',
    'compact_json',
    'output_to_human_and_ai',
    'configure_logging',
    'get_logger',
    'is_mcp_mode',
    'suppress_noisy_loggers'
]

