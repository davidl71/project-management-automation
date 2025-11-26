"""
Project Management Automation MCP Server

MCP server for project management automation tools.

FastMCP 2 Features:
- Middleware: Rate limiting, path validation, access control, logging
- Lifespan: Startup/shutdown hooks for database init, cleanup
- Resource Templates: Dynamic resources (tasks://{id}, advisor://{id}, etc.)
- Context Helpers: Progress reporting, client-side logging, LLM sampling
"""

from .version import __version__, BASE_VERSION, get_version, get_version_info

# Export context helpers for tool authors
from .context_helpers import (
    report_progress,
    ProgressTracker,
    log_info,
    log_debug,
    log_warning,
    log_error,
    get_state,
    set_state,
    sample_llm,
)

# Export lifespan for custom servers
from .lifespan import exarp_lifespan, basic_lifespan, get_app_state

__all__ = [
    # Version
    '__version__',
    'BASE_VERSION',
    'get_version',
    'get_version_info',
    # Context helpers
    'report_progress',
    'ProgressTracker',
    'log_info',
    'log_debug',
    'log_warning',
    'log_error',
    'get_state',
    'set_state',
    'sample_llm',
    # Lifespan
    'exarp_lifespan',
    'basic_lifespan',
    'get_app_state',
]
