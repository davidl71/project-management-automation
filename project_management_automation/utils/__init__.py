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

from .dev_reload import (
    get_module_info,
    is_dev_mode,
    reload_all_modules,
    reload_module,
    reload_specific_modules,
)
from .logging_config import configure_logging, get_logger, is_mcp_mode, suppress_noisy_loggers
from .output import compact_json, output_to_human_and_ai, progress_wrapper, split_output
from .security import (
    AccessController,
    # Access control
    AccessLevel,
    # Input validation
    InputValidationError,
    # Path validation
    PathBoundaryError,
    PathValidator,
    # Rate limiting
    RateLimiter,
    get_access_controller,
    get_default_path_validator,
    get_rate_limiter,
    rate_limit,
    require_access,
    sanitize_string,
    set_access_controller,
    set_default_path_validator,
    validate_enum,
    validate_identifier,
    validate_path,
    validate_range,
)
from .todo2_utils import (
    annotate_task_project,
    filter_tasks_by_project,
    get_current_project_id,
    get_repo_project_id,
    load_todo2_project_info,
    task_belongs_to_project,
    validate_project_ownership,
)


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
    # Project utilities
    'find_project_root',
    'split_output',
    'progress_wrapper',
    'compact_json',
    'output_to_human_and_ai',
    # Logging
    'configure_logging',
    'get_logger',
    'is_mcp_mode',
    'suppress_noisy_loggers',
    # Dev reload
    'is_dev_mode',
    'reload_all_modules',
    'reload_specific_modules',
    'reload_module',
    'get_module_info',
    # Security - Path validation
    'PathBoundaryError',
    'PathValidator',
    'set_default_path_validator',
    'get_default_path_validator',
    'validate_path',
    # Security - Input validation
    'InputValidationError',
    'sanitize_string',
    'validate_identifier',
    'validate_enum',
    'validate_range',
    # Security - Rate limiting
    'RateLimiter',
    'get_rate_limiter',
    'rate_limit',
    # Security - Access control
    'AccessLevel',
    'AccessController',
    'get_access_controller',
    'set_access_controller',
    'require_access',
    'annotate_task_project',
    'filter_tasks_by_project',
    'get_current_project_id',
    'get_repo_project_id',
    'load_todo2_project_info',
    'task_belongs_to_project',
    'validate_project_ownership',
]

