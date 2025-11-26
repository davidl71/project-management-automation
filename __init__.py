"""
Project Management Automation MCP Server

Model Context Protocol server for project management automation tools.
Exposes IntelligentAutomationBase tools for AI assistant access.
"""

# Version is managed in project_management_automation/version.py
# This file is kept for backwards compatibility but the package
# version should be imported from the main package:
#   from project_management_automation import __version__
try:
    from project_management_automation.version import __version__
except ImportError:
    __version__ = "0.0.0"  # Fallback for edge cases
