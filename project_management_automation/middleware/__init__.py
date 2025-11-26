"""
FastMCP Middleware for Exarp MCP Server.

Provides:
- RateLimitMiddleware: Token bucket rate limiting per client/tool
- PathValidationMiddleware: Path boundary enforcement on all file operations
- AccessControlMiddleware: Tool-level access control
- LoggingMiddleware: Request/response logging with timing
- SecurityMiddleware: Combined security (rate limit + path + access)

Usage:
    from project_management_automation.middleware import (
        SecurityMiddleware,
        RateLimitMiddleware,
        LoggingMiddleware,
    )
    
    mcp.add_middleware(SecurityMiddleware())
    # or individual:
    mcp.add_middleware(RateLimitMiddleware(calls_per_minute=60))
"""

from .rate_limit import RateLimitMiddleware
from .path_validation import PathValidationMiddleware
from .access_control import AccessControlMiddleware
from .logging_middleware import LoggingMiddleware
from .security import SecurityMiddleware

__all__ = [
    "RateLimitMiddleware",
    "PathValidationMiddleware",
    "AccessControlMiddleware",
    "LoggingMiddleware",
    "SecurityMiddleware",
]

