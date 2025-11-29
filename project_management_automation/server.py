#!/usr/bin/env python3
"""
Project Management Automation MCP Server

Model Context Protocol server exposing project management automation tools
built on IntelligentAutomationBase.

Provides AI assistants with access to:
- Documentation health checks
- Todo2 alignment analysis
- Duplicate task detection
- Dependency security scanning
- Automation opportunity discovery
- Todo synchronization
- PWA configuration review

Complementary MCP Servers:
- tractatus_thinking: Use BEFORE Exarp tools for structural analysis (WHAT)
- sequential_thinking: Use AFTER Exarp analysis for implementation workflows (HOW)

Recommended workflow:
1. tractatus_thinking → Understand problem structure
2. exarp → Analyze and automate project management tasks
3. sequential_thinking → Convert results into implementation steps
"""

import os
import sys

# Set MCP mode flag BEFORE any logging imports
# This tells our logging utilities to suppress console output
os.environ["EXARP_MCP_MODE"] = "1"

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import our MCP-aware logging utilities
from .utils.logging_config import configure_logging, suppress_noisy_loggers

# Dynamic version from version.py
from .version import __version__

# Configure logging (quiet in MCP mode, verbose in CLI)
logger = configure_logging("exarp", level=logging.INFO)
suppress_noisy_loggers()

# Import security utilities
from .utils.security import (
    AccessController,
    PathValidator,
    set_access_controller,
    set_default_path_validator,
)


# Robust project root detection
def _find_project_root(start_path: Path) -> Path:
    """
    Find project root by looking for .git directory or other markers.
    Falls back to relative path detection if markers not found.
    """
    # Try environment variable first
    env_root = os.getenv("PROJECT_ROOT") or os.getenv("WORKSPACE_PATH")
    if env_root:
        root_path = Path(env_root)
        if root_path.exists():
            return root_path.resolve()

    # Try relative path detection (assumes standard structure)
    current = start_path
    for _ in range(5):  # Go up max 5 levels
        # Check for project markers
        if (current / ".git").exists() or (current / ".todo2").exists() or (current / "CMakeLists.txt").exists():
            return current.resolve()
        if current.parent == current:  # Reached filesystem root
            break
        current = current.parent

    # Fallback to relative path (assumes project-management-automation/project_management_automation/server.py)
    return start_path.parent.parent.parent.parent.resolve()


# Add project root to path for script imports
project_root = _find_project_root(Path(__file__))
sys.path.insert(0, str(project_root))

# Initialize security controls
# Path boundary: only allow access within project root and common temp dirs
_path_validator = PathValidator(
    allowed_roots=[project_root, Path("/tmp"), Path("/var/tmp")],
    allow_symlinks=False,
    blocked_patterns=[
        r"\.git(?:/|$)",  # .git directory
        r"\.env",  # Environment files
        r"\.ssh",  # SSH keys
        r"\.aws",  # AWS credentials
        r"id_rsa",  # SSH private keys
        r"\.pem$",  # Certificate files
        r"secrets?\.ya?ml",  # Secrets files
    ],
)
set_default_path_validator(_path_validator)

# Access control: default write access, customizable per deployment
_access_controller = AccessController(default_level="write")
set_access_controller(_access_controller)

logger.debug(f"Security initialized: path_boundaries={len(_path_validator.allowed_roots)} roots, access_control=write")

# Add server directory to path for absolute imports when run as script
server_dir = Path(__file__).parent
sys.path.insert(0, str(server_dir))

# Import error handling (handle both relative and absolute imports)
try:
    # Try relative imports first (when run as module)
    try:
        from .error_handler import (
            AutomationError,
            ErrorCode,
            format_error_response,
            format_success_response,
            handle_automation_error,
            log_automation_execution,
        )
    except ImportError:
        # Fallback to absolute imports (when run as script)
        from error_handler import (
            AutomationError,
            ErrorCode,
            format_error_response,
            format_success_response,
            handle_automation_error,
            log_automation_execution,
        )

    ERROR_HANDLING_AVAILABLE = True
except ImportError as e:
    ERROR_HANDLING_AVAILABLE = False
    logger.warning(f"Error handling module not available - using basic error handling: {e}")

# Try to import MCP - Phase 2 tools complete, MCP installation needed for runtime
MCP_AVAILABLE = False
USE_STDIO = False
FastMCP = None

try:
    # Try FastMCP from mcp package (may be available in newer versions)
    from mcp import FastMCP
    from mcp.types import TextContent, Tool

    MCP_AVAILABLE = True
    USE_STDIO = False
    Server = None
    stdio_server = None
except ImportError:
    try:
        # Try FastMCP from separate fastmcp package
        from fastmcp import FastMCP
        from mcp.types import TextContent, Tool

        MCP_AVAILABLE = True
        USE_STDIO = False
        Server = None
        stdio_server = None
    except ImportError:
        try:
            from mcp.server import Server
            from mcp.server.stdio import stdio_server

            # For stdio server, we'll construct Tool objects manually
            from mcp.types import TextContent, Tool

            MCP_AVAILABLE = True
            USE_STDIO = True
            FastMCP = None
            logger.info("MCP stdio server available - using stdio server")
        except ImportError:
            logger.warning("MCP not installed - server structure ready, install with: pip install mcp")
        MCP_AVAILABLE = False
        Server = None
        stdio_server = None
        Tool = None
        TextContent = None

# Logging already configured above

# Initialize MCP server
mcp = None
stdio_server_instance = None
if MCP_AVAILABLE:
    # Suppress FastMCP/stdio server initialization logging
    # FastMCP logs "Starting MCP server" messages to stderr during initialization
    # We temporarily redirect stderr to suppress these during initialization
    import contextlib
    import io

    @contextlib.contextmanager
    def suppress_fastmcp_output():
        """Temporarily suppress stdout and stderr during FastMCP initialization"""
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            # Redirect both stdout and stderr to suppress FastMCP banner and startup messages
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            yield
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    # Import lifespan for FastMCP
    try:
        from .lifespan import exarp_lifespan
        LIFESPAN_AVAILABLE = True
    except ImportError:
        exarp_lifespan = None
        LIFESPAN_AVAILABLE = False

    # Suppress FastMCP output during initialization (banner, startup messages)
    with suppress_fastmcp_output():
        if not USE_STDIO and FastMCP:
            # Initialize with lifespan if available
            if LIFESPAN_AVAILABLE and exarp_lifespan:
                mcp = FastMCP("exarp", lifespan=exarp_lifespan)
            else:
                mcp = FastMCP("exarp")
        elif USE_STDIO and Server:
            # Initialize stdio server
            stdio_server_instance = Server("exarp")
            # Note: Tools will be registered below using stdio server API

    # Log initialization after suppressing FastMCP output
    if not USE_STDIO and FastMCP and mcp:
        pass  # Version info logged after banner in main()
    elif USE_STDIO and Server and stdio_server_instance:
        pass  # Version info logged after banner

    # Re-apply logger suppression after initialization (in case FastMCP added new loggers)
    suppress_noisy_loggers()

    # ═══════════════════════════════════════════════════════════════════════
    # MIDDLEWARE REGISTRATION (FastMCP 2 feature)
    # ═══════════════════════════════════════════════════════════════════════
    if not USE_STDIO and FastMCP and mcp:
        try:
            from .middleware import LoggingMiddleware, SecurityMiddleware, ToolFilterMiddleware

            # Add security middleware (rate limiting + path validation + access control)
            mcp.add_middleware(SecurityMiddleware(
                allowed_roots=[project_root, Path("/tmp"), Path("/var/tmp")],
                calls_per_minute=120,  # 2 calls/sec sustained
                burst_size=20,         # Allow bursts
            ))

            # Add logging middleware (request timing)
            mcp.add_middleware(LoggingMiddleware(
                log_arguments=False,   # Don't log args (may contain sensitive data)
                log_results=False,     # Don't log results (too verbose)
                slow_threshold_ms=5000,  # Warn on slow tools
            ))

            # Add tool filter middleware (dynamic tool loading)
            # Reduces context pollution by showing only relevant tools per workflow mode
            # See: https://www.jlowin.dev/blog/stop-converting-rest-apis-to-mcp
            mcp.add_middleware(ToolFilterMiddleware(enabled=True))

            logger.debug("✅ Middleware registered: SecurityMiddleware, LoggingMiddleware, ToolFilterMiddleware")
        except ImportError as e:
            logger.debug(f"Middleware not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register middleware: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # RESOURCE TEMPLATES (FastMCP 2 feature)
    # ═══════════════════════════════════════════════════════════════════════
    if not USE_STDIO and FastMCP and mcp:
        try:
            from .resources.templates import register_resource_templates
            register_resource_templates(mcp)
            logger.debug("✅ Resource templates registered")
        except ImportError as e:
            logger.debug(f"Resource templates not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register resource templates: {e}")
        
        # Context primer resources for AI priming
        try:
            from .resources.context_primer import register_context_primer_resources
            register_context_primer_resources(mcp)
            logger.debug("✅ Context primer resources registered")
        except ImportError as e:
            logger.debug(f"Context primer resources not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register context primer resources: {e}")
        
        # Hint registry resources for dynamic hint loading
        try:
            from .resources.hint_registry import register_hint_registry_resources
            register_hint_registry_resources(mcp)
            logger.debug("✅ Hint registry resources registered")
        except ImportError as e:
            logger.debug(f"Hint registry resources not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register hint registry resources: {e}")
        
        # Auto-primer tools for session start
        try:
            from .tools.auto_primer import register_auto_primer_tools
            register_auto_primer_tools(mcp)
            logger.debug("✅ Auto-primer tools registered")
        except ImportError as e:
            logger.debug(f"Auto-primer tools not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register auto-primer tools: {e}")
        
        # Prompt discovery resources and tools
        try:
            from .resources.prompt_discovery import (
                register_prompt_discovery_resources,
                register_prompt_discovery_tools,
            )
            register_prompt_discovery_resources(mcp)
            register_prompt_discovery_tools(mcp)
            logger.debug("✅ Prompt discovery resources and tools registered")
        except ImportError as e:
            logger.debug(f"Prompt discovery not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register prompt discovery: {e}")

        # Assignee management resources and tools
        try:
            from .resources.assignees import register_assignee_resources
            from .tools.task_assignee import register_assignee_tools
            register_assignee_resources(mcp)
            register_assignee_tools(mcp)
            logger.debug("✅ Assignee management resources and tools registered")
        except ImportError as e:
            logger.debug(f"Assignee management not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register assignee management: {e}")

        # Capabilities resource for agent priming
        try:
            from .resources.capabilities import register_capabilities_resources
            register_capabilities_resources(mcp)
            logger.debug("✅ Capabilities resources registered")
        except ImportError as e:
            logger.debug(f"Capabilities resources not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register capabilities resources: {e}")

        # Session handoff tool for multi-dev coordination
        try:
            from .tools.session_handoff import register_handoff_tools
            register_handoff_tools(mcp)
            logger.debug("✅ Session handoff tool registered")
        except ImportError as e:
            logger.debug(f"Session handoff not available: {e}")
        except Exception as e:
            logger.warning(f"Failed to register session handoff: {e}")

# Import automation tools (handle both relative and absolute imports)
try:
    # Try relative imports first (when run as module)
    try:
        from .tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from .tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from .tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from .tools.context_summarizer import (
            batch_summarize as _batch_summarize,
        )
        from .tools.context_summarizer import (
            estimate_context_budget as _estimate_context_budget,
        )
        from .tools.context_summarizer import (
            summarize_context as _summarize_context,
        )
        from .tools.cursor_rules_generator import generate_cursor_rules as _generate_cursor_rules
        from .tools.cursorignore_generator import generate_cursorignore as _generate_cursorignore
        from .tools.daily_automation import run_daily_automation as _run_daily_automation
        from .tools.definition_of_done import check_definition_of_done as _check_definition_of_done
        from .tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from .tools.docs_health import check_documentation_health as _check_documentation_health
        from .tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from .tools.dynamic_tools import (
            focus_mode as _focus_mode,
        )
        from .tools.dynamic_tools import (
            get_tool_manager,
        )
        from .tools.dynamic_tools import (
            get_tool_usage_stats as _get_tool_usage_stats,
        )
        from .tools.dynamic_tools import (
            suggest_mode as _suggest_mode,
        )
        from .tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from .tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from .tools.hint_catalog import (
            get_tool_help as _get_tool_help,
        )
        from .tools.hint_catalog import (
            list_tools as _list_tools,
        )
        from .tools.linter import get_linter_status as _get_linter_status
        from .tools.linter import run_linter as _run_linter
        from .tools.model_recommender import (
            list_available_models as _list_available_models,
        )
        from .tools.model_recommender import (
            recommend_model as _recommend_model,
        )
        from .tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from .tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from .tools.prd_alignment import analyze_prd_alignment as _analyze_prd_alignment
        from .tools.prd_generator import generate_prd as _generate_prd
        from .tools.problems_advisor import analyze_problems_tool as _analyze_problems
        from .tools.problems_advisor import list_problem_categories as _list_problem_categories
        from .tools.project_overview import generate_project_overview as _generate_project_overview
        from .tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from .tools.prompt_iteration_tracker import (
            analyze_prompt_iterations as _analyze_prompt_iterations,
        )
        from .tools.prompt_iteration_tracker import (
            log_prompt_iteration as _log_prompt_iteration,
        )
        from .tools.run_tests import run_tests as _run_tests
        from .tools.simplify_rules import simplify_rules as _simplify_rules
        from .tools.sprint_automation import sprint_automation as _sprint_automation
        from .tools.tag_consolidation import tag_consolidation_tool as _tag_consolidation
        from .tools.task_clarification_resolution import (
            list_tasks_awaiting_clarification as _list_tasks_awaiting_clarification,
        )
        from .tools.task_clarification_resolution import (
            resolve_multiple_clarifications as _resolve_multiple_clarifications,
        )
        from .tools.task_clarification_resolution import resolve_task_clarification as _resolve_task_clarification
        from .tools.task_hierarchy_analyzer import analyze_task_hierarchy as _analyze_task_hierarchy
        from .tools.test_coverage import analyze_test_coverage as _analyze_test_coverage
        from .tools.todo2_alignment import analyze_todo2_alignment as _analyze_todo2_alignment
        from .tools.todo_sync import sync_todo_tasks as _sync_todo_tasks
        from .tools.workflow_recommender import recommend_workflow_mode as _recommend_workflow_mode
        from .tools.working_copy_health import check_working_copy_health as _check_working_copy_health
        from .tools.task_assignee import (
            assign_task as _assign_task,
            unassign_task as _unassign_task,
            list_tasks_by_assignee as _list_tasks_by_assignee,
            get_workload_summary as _get_workload_summary,
            bulk_assign_tasks as _bulk_assign_tasks,
            auto_assign_background_tasks as _auto_assign_background_tasks,
        )

        TOOLS_AVAILABLE = True
    except ImportError:
        # Fallback to absolute imports (when run as script)
        from tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from tools.context_summarizer import (
            batch_summarize as _batch_summarize,
        )
        from tools.context_summarizer import (
            estimate_context_budget as _estimate_context_budget,
        )
        from tools.context_summarizer import (
            summarize_context as _summarize_context,
        )
        from tools.cursor_rules_generator import generate_cursor_rules as _generate_cursor_rules
        from tools.cursorignore_generator import generate_cursorignore as _generate_cursorignore
        from tools.daily_automation import run_daily_automation as _run_daily_automation
        from tools.definition_of_done import check_definition_of_done as _check_definition_of_done
        from tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from tools.docs_health import check_documentation_health as _check_documentation_health
        from tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from tools.dynamic_tools import (
            focus_mode as _focus_mode,
        )
        from tools.dynamic_tools import (
            get_tool_manager,
        )
        from tools.dynamic_tools import (
            get_tool_usage_stats as _get_tool_usage_stats,
        )
        from tools.dynamic_tools import (
            suggest_mode as _suggest_mode,
        )
        from tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from tools.hint_catalog import (
            get_tool_help as _get_tool_help,
        )
        from tools.hint_catalog import (
            list_tools as _list_tools,
        )
        from tools.linter import get_linter_status as _get_linter_status
        from tools.linter import run_linter as _run_linter
        from tools.model_recommender import (
            list_available_models as _list_available_models,
        )
        from tools.model_recommender import (
            recommend_model as _recommend_model,
        )
        from tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from tools.prd_alignment import analyze_prd_alignment as _analyze_prd_alignment
        from tools.prd_generator import generate_prd as _generate_prd
        from tools.problems_advisor import analyze_problems_tool as _analyze_problems
        from tools.problems_advisor import list_problem_categories as _list_problem_categories
        from tools.project_overview import generate_project_overview as _generate_project_overview
        from tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from tools.prompt_iteration_tracker import (
            analyze_prompt_iterations as _analyze_prompt_iterations,
        )
        from tools.prompt_iteration_tracker import (
            log_prompt_iteration as _log_prompt_iteration,
        )
        from tools.run_tests import run_tests as _run_tests
        from tools.simplify_rules import simplify_rules as _simplify_rules
        from tools.sprint_automation import sprint_automation as _sprint_automation
        from tools.tag_consolidation import tag_consolidation_tool as _tag_consolidation
        from tools.task_clarification_resolution import (
            list_tasks_awaiting_clarification as _list_tasks_awaiting_clarification,
        )
        from tools.task_clarification_resolution import (
            resolve_multiple_clarifications as _resolve_multiple_clarifications,
        )
        from tools.task_clarification_resolution import resolve_task_clarification as _resolve_task_clarification
        from tools.task_hierarchy_analyzer import analyze_task_hierarchy as _analyze_task_hierarchy
        from tools.test_coverage import analyze_test_coverage as _analyze_test_coverage
        from tools.todo2_alignment import analyze_todo2_alignment as _analyze_todo2_alignment
        from tools.todo_sync import sync_todo_tasks as _sync_todo_tasks
        from tools.workflow_recommender import recommend_workflow_mode as _recommend_workflow_mode
        from tools.working_copy_health import check_working_copy_health as _check_working_copy_health
        from tools.task_assignee import (
            assign_task as _assign_task,
            unassign_task as _unassign_task,
            list_tasks_by_assignee as _list_tasks_by_assignee,
            get_workload_summary as _get_workload_summary,
            bulk_assign_tasks as _bulk_assign_tasks,
            auto_assign_background_tasks as _auto_assign_background_tasks,
        )

        TOOLS_AVAILABLE = True
    logger.info("All tools loaded successfully")
except ImportError as e:
    TOOLS_AVAILABLE = False
    logger.warning(f"Some tools not available: {e}")


# Tool registration - support both FastMCP and stdio Server
def register_tools():
    """Register tools with the appropriate MCP server instance."""
    if mcp:
        # FastMCP registration (decorator-based)
        # NOTE: server_status removed - use health(type="server")

        @mcp.tool()
        def dev_reload(modules: Optional[list[str]] = None) -> str:
            """
            [HINT: Dev reload. Hot-reload modules without restart. Requires EXARP_DEV_MODE=1.]

            Reload Python modules without restarting Cursor.
            Only available when EXARP_DEV_MODE=1 is set in environment.

            Args:
                modules: Optional list of specific modules to reload (e.g., ["tools.project_scorecard"]).
                        If not provided, reloads all package modules.

            To enable dev mode, add to your MCP config:
                "env": {"EXARP_DEV_MODE": "1"}
            """
            from .utils.dev_reload import is_dev_mode, reload_all_modules, reload_specific_modules

            if not is_dev_mode():
                return json.dumps(
                    {
                        "success": False,
                        "error": "Dev mode not enabled",
                        "hint": 'Add to MCP config: "env": {"EXARP_DEV_MODE": "1"}',
                        "config_example": {"mcpServers": {"exarp": {"command": "...", "env": {"EXARP_DEV_MODE": "1"}}}},
                    },
                    separators=(",", ":"),
                )

            if modules:
                result = reload_specific_modules(modules)
            else:
                result = reload_all_modules()

            return json.dumps(result, separators=(",", ":"))

        # Continue with more tool registrations below...

    elif stdio_server_instance:
        # Stdio Server registration (handler-based)
        @stdio_server_instance.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools."""
            tools = [
                Tool(
                    name="server_status",
                    description="Get the current status of the project management automation server.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]
            if TOOLS_AVAILABLE:
                # Add tool definitions for all automation tools
                tools.extend(
                    [
                        Tool(
                            name="check_documentation_health",
                            description="Analyze documentation structure, find broken references, identify issues.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "output_path": {"type": "string", "description": "Output file path"},
                                    "create_tasks": {
                                        "type": "boolean",
                                        "description": "Create Todo2 tasks",
                                        "default": True,
                                    },
                                },
                            },
                        ),
                        Tool(
                            name="analyze_todo2_alignment",
                            description="Analyze task alignment with project goals, find misaligned tasks.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "create_followup_tasks": {
                                        "type": "boolean",
                                        "description": "Create follow-up tasks",
                                        "default": True,
                                    },
                                    "output_path": {"type": "string", "description": "Output file path"},
                                },
                            },
                        ),
                        Tool(
                            name="detect_duplicate_tasks",
                            description="Find and consolidate duplicate Todo2 tasks.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "similarity_threshold": {
                                        "type": "number",
                                        "description": "Similarity threshold",
                                        "default": 0.85,
                                    },
                                    "auto_fix": {
                                        "type": "boolean",
                                        "description": "Auto-fix duplicates",
                                        "default": False,
                                    },
                                    "output_path": {"type": "string", "description": "Output file path"},
                                },
                            },
                        ),
                        Tool(
                            name="scan_dependency_security",
                            description="Scan project dependencies for security vulnerabilities.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "languages": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Languages to scan",
                                    },
                                    "config_path": {"type": "string", "description": "Config file path"},
                                },
                            },
                        ),
                        Tool(
                            name="find_automation_opportunities",
                            description="Discover new automation opportunities in the codebase.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "min_value_score": {
                                        "type": "number",
                                        "description": "Minimum value score",
                                        "default": 0.7,
                                    },
                                    "output_path": {"type": "string", "description": "Output file path"},
                                },
                            },
                        ),
                        Tool(
                            name="sync_todo_tasks",
                            description="Synchronize tasks between shared TODO table and Todo2.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "dry_run": {"type": "boolean", "description": "Dry run mode", "default": False},
                                    "output_path": {"type": "string", "description": "Output file path"},
                                },
                            },
                        ),
                        Tool(
                            name="add_external_tool_hints",
                            description="Automatically detect and add Context7/external tool hints to documentation.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "dry_run": {
                                        "type": "boolean",
                                        "description": "Preview changes without applying",
                                        "default": False,
                                    },
                                    "output_path": {"type": "string", "description": "Path for report output"},
                                    "min_file_size": {
                                        "type": "integer",
                                        "description": "Minimum file size in lines to process",
                                        "default": 50,
                                    },
                                },
                            },
                        ),
                        Tool(
                            name="run_daily_automation",
                            description="Run routine daily maintenance tasks and generate a combined summary report.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "tasks": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "List of task IDs to run (default: quick tasks only)",
                                    },
                                    "include_slow": {
                                        "type": "boolean",
                                        "description": "Include slow tasks like dependency security scan",
                                        "default": False,
                                    },
                                    "dry_run": {
                                        "type": "boolean",
                                        "description": "Preview changes without applying",
                                        "default": False,
                                    },
                                    "output_path": {"type": "string", "description": "Path for report output"},
                                },
                            },
                        ),
                    ]
                )
            return tools

        @stdio_server_instance.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            if name == "server_status":
                result = json.dumps(
                    {
                        "status": "operational",
                        "version": __version__,
                        "tools_available": TOOLS_AVAILABLE,
                        "project_root": str(project_root),
                    },
                    separators=(",", ":"),
                )
            elif TOOLS_AVAILABLE:
                # Route to appropriate tool function
                if name == "check_documentation_health":
                    result = _check_documentation_health(
                        arguments.get("output_path"), arguments.get("create_tasks", True)
                    )
                elif name == "analyze_todo2_alignment":
                    result = _analyze_todo2_alignment(
                        arguments.get("create_followup_tasks", True), arguments.get("output_path")
                    )
                elif name == "detect_duplicate_tasks":
                    result = _detect_duplicate_tasks(
                        arguments.get("similarity_threshold", 0.85),
                        arguments.get("auto_fix", False),
                        arguments.get("output_path"),
                    )
                elif name == "scan_dependency_security":
                    result = _scan_dependency_security(arguments.get("languages"), arguments.get("config_path"))
                elif name == "find_automation_opportunities":
                    result = _find_automation_opportunities(
                        arguments.get("min_value_score", 0.7), arguments.get("output_path")
                    )
                elif name == "sync_todo_tasks":
                    result = _sync_todo_tasks(arguments.get("dry_run", False), arguments.get("output_path"))
                elif name == "add_external_tool_hints":
                    result = _add_external_tool_hints(
                        arguments.get("dry_run", False),
                        arguments.get("output_path"),
                        arguments.get("min_file_size", 50),
                    )
                elif name == "run_daily_automation":
                    result = _run_daily_automation(
                        arguments.get("tasks"),
                        arguments.get("include_slow", False),
                        arguments.get("dry_run", False),
                        arguments.get("output_path"),
                    )
                else:
                    result = json.dumps({"error": f"Unknown tool: {name}"})
            else:
                result = json.dumps({"error": "Tools not available"})

            return [TextContent(type="text", text=result)]

        return None


# Register tools
register_tools()

if mcp:
    # Register high-priority tools
    if TOOLS_AVAILABLE:

        # NOTE: check_documentation_health removed - use health(type="docs")
        # NOTE: analyze_todo2_alignment removed - use analyze_alignment(type="todo2")

        # NOTE: detect_duplicate_tasks removed - use task_analysis(action="duplicates")
        # NOTE: scan_dependency_security removed - use security(action="scan")
        # NOTE: find_automation_opportunities removed - use run_automation(mode="discover")
        # NOTE: sync_todo_tasks removed - use task_workflow(action="sync")

        @mcp.tool()
        def add_external_tool_hints(
            dry_run: bool = False, output_path: Optional[str] = None, min_file_size: int = 50
        ) -> str:
            """[HINT: Tool hints. Files scanned, modified, hints added.]"""
            return _add_external_tool_hints(dry_run, output_path, min_file_size)

        # NOTE: analyze_problems, run_linter removed - use lint(action=analyze|run)
        # NOTE: list_problem_categories removed - use resource automation://problem-categories
        # NOTE: get_linter_status removed - use resource automation://linters

        @mcp.tool()
        def run_automation(
            action: str = "daily",
            # Daily action params
            tasks: Optional[list[str]] = None,
            include_slow: bool = False,
            # Nightly action params
            max_tasks_per_host: int = 5,
            max_parallel_tasks: int = 10,
            # Sprint action params
            max_iterations: int = 10,
            auto_approve: bool = True,
            extract_subtasks: bool = True,
            run_analysis_tools: bool = True,
            run_testing_tools: bool = True,
            # Discover action params
            min_value_score: float = 0.7,
            # Shared params
            priority_filter: Optional[str] = None,
            tag_filter: Optional[list[str]] = None,
            dry_run: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Automation runner. action: discover|daily|nightly|sprint. Unified automation control.]

            Actions:
            - discover: Find automation opportunities in codebase
            - daily: Run daily checks (docs_health, alignment, duplicates, security)
            - nightly: Process tasks automatically with host limits
            - sprint: Full sprint automation with subtask extraction
            """
            if action == "discover":
                return _find_automation_opportunities(min_value_score, output_path)
            elif action == "daily":
                return _run_daily_automation(tasks, include_slow, dry_run, output_path)
            elif action == "nightly":
                result = _run_nightly_task_automation(
                    max_tasks_per_host=max_tasks_per_host,
                    max_parallel_tasks=max_parallel_tasks,
                    priority_filter=priority_filter,
                    tag_filter=tag_filter,
                    dry_run=dry_run,
                )
                return json.dumps(result, separators=(",", ":"))
            elif action == "sprint":
                return _sprint_automation_impl(
                    max_iterations, auto_approve, extract_subtasks,
                    run_analysis_tools, run_testing_tools,
                    priority_filter, tag_filter, dry_run, output_path,
                )
            else:
                return json.dumps({"status": "error", "error": f"Unknown action: {action}. Use discover, daily, nightly, or sprint"}, separators=(",", ":"))

        # NOTE: validate_ci_cd_workflow removed - use health(action="cicd")
        # NOTE: batch_approve_tasks removed - use task_workflow(action="approve")
        # NOTE: run_nightly_task_automation removed - use run_automation(action="nightly")
        # NOTE: check_working_copy_health removed - use health(action="git")
        # NOTE: clarification removed - use task_workflow(action="clarify")
        # NOTE: setup_git_hooks removed - use setup_hooks(type="git")
        # NOTE: setup_pattern_triggers removed - use setup_hooks(type="patterns")
        # NOTE: run_tests, analyze_test_coverage removed - use testing(action=run|coverage)

        # Helper for sprint automation (shared implementation)
        def _sprint_automation_impl(
            max_iterations,
            auto_approve,
            extract_subtasks,
            run_analysis_tools,
            run_testing_tools,
            priority_filter,
            tag_filter,
            dry_run,
            output_path,
        ) -> str:
            return _sprint_automation(
                max_iterations,
                auto_approve,
                extract_subtasks,
                run_analysis_tools,
                run_testing_tools,
                priority_filter,
                tag_filter,
                dry_run,
                output_path,
            )

        # NOTE: run_sprint_automation removed - use run_automation(mode="sprint")

        # NOTE: simplify_rules removed - use generate_config(action="simplify")

        # Helper for scorecard (shared implementation)
        def _scorecard_impl(output_format: str, include_recommendations: bool, output_path: Optional[str]) -> str:
            result = _generate_project_scorecard(output_format, include_recommendations, output_path)
            return json.dumps(
                {
                    "overall_score": result["overall_score"],
                    "production_ready": result["production_ready"],
                    "blockers": result.get("blockers", []),
                    "scores": result["scores"],
                    "recommendations": result.get("recommendations", []),
                    "formatted_output": result["formatted_output"],
                },
                separators=(",", ":"),
            )

        # NOTE: generate_project_scorecard removed - use report(type="scorecard")

        # Helper for overview (shared implementation)
        def _overview_impl(output_format: str, output_path: Optional[str]) -> str:
            result = _generate_project_overview(output_format, output_path)
            return json.dumps(
                {
                    "output_format": result["output_format"],
                    "generated_at": result["generated_at"],
                    "output_file": result.get("output_file"),
                    "formatted_output": result["formatted_output"],
                },
                separators=(",", ":"),
            )

        # NOTE: generate_project_overview removed - use report(type="overview")
        # NOTE: generate_prd removed - use report(type="prd")
        # NOTE: analyze_prd_alignment removed - use analyze_alignment(type="prd")

        # NOTE: recommend_workflow_mode removed - LLM can determine from task complexity
        # NOTE: generate_cursorignore removed - use generate_config(action="ignore")

        # NOTE: check_definition_of_done removed - use health(type="dod")
        # NOTE: generate_cursor_rules removed - use generate_config(type="rules")

        # NOTE: log_prompt_iteration removed - use prompt_tracking(action="log")
        # NOTE: analyze_prompt_iterations removed - use prompt_tracking(action="analyze")

        # NOTE: recommend_model removed - use resource automation://models for model info
        # NOTE: list_available_models removed - use resource automation://models

        @mcp.tool()
        def list_tools(
            category: Optional[str] = None,
            persona: Optional[str] = None,
            include_examples: bool = True
        ) -> str:
            """[HINT: Tool catalog. Lists all tools with rich descriptions and examples.]

            📊 Output: Filtered tool catalog with usage guidance
            🔧 Side Effects: None
            ⏱️ Typical Runtime: <1 second

            Categories: Project Health, Task Management, Code Quality,
            Security, Planning, Workflow, Configuration
            """
            return _list_tools(category, persona, include_examples)

        @mcp.tool()
        async def focus_mode(
            mode: Optional[str] = None,
            enable_group: Optional[str] = None,
            disable_group: Optional[str] = None,
            status: bool = False,
            ctx: Any = None,
        ) -> str:
            """
            [HINT: Tool curation. Dynamic tool visibility based on workflow mode.]

            🎯 Output: Mode status, visible tools, context reduction metrics
            🔧 Side Effects: Updates tool visibility, sends list_changed notification
            ⏱️ Typical Runtime: <100ms

            Philosophy: "An API built for humans will poison your AI agent."
            Instead of 40+ tools polluting context, focus on what's relevant NOW.

            Modes:
            - daily_checkin: Health + overview (9 tools, 82% reduction)
            - security_review: Security-focused (12 tools, 77% reduction)
            - task_management: Task tools only (10 tools, 81% reduction)
            - sprint_planning: Tasks + automation + PRD (15 tools, 71% reduction)
            - code_review: Testing + linting (10 tools, 81% reduction)
            - development: Balanced set (25 tools, 52% reduction) [default]
            - debugging: Memory + testing (17 tools, 67% reduction)
            - all: Full tool access (52 tools)

            Groups (enable/disable individually):
            - health, tasks, security, automation, config, testing, advisors, memory, workflow, prd

            Example Prompts:
            "Switch to security review mode"
            "Focus on task management"
            "Enable the advisors tools"
            "Show current tool focus status"

            Args:
                mode: Workflow mode to switch to (see modes above)
                enable_group: Specific group to enable
                disable_group: Specific group to disable
                status: If True, return current status without changes

            Returns:
                JSON with mode info, visible tools, and context reduction metrics
            """
            result = _focus_mode(mode, enable_group, disable_group, status)

            # Send notification if mode changed
            if ctx and (mode or enable_group or disable_group):
                try:
                    from .context_helpers import notify_tools_changed
                    await notify_tools_changed(ctx)
                except Exception as e:
                    logger.debug(f"Could not notify tools changed: {e}")

            return result

        @mcp.tool()
        async def suggest_mode(
            text: Optional[str] = None,
            auto_switch: bool = False,
            ctx: Any = None,
        ) -> str:
            """
            [HINT: Adaptive mode suggestion. Infers best mode from context/usage patterns.]

            🎯 Output: Suggested mode, confidence score, rationale
            🔧 Side Effects: If auto_switch=True, changes mode and notifies client
            ⏱️ Typical Runtime: <50ms

            Uses keyword analysis and usage patterns to suggest the best workflow mode.
            Call without arguments to get suggestion based on your usage history.

            Example Prompts:
            "What mode should I use for security work?"
            "Suggest a mode based on my recent activity"
            "Auto-switch to the best mode for vulnerability scanning"

            Args:
                text: Optional text to analyze for mode suggestion
                auto_switch: If True, automatically switch to suggested mode

            Returns:
                JSON with suggested mode, confidence, and rationale
            """
            result = _suggest_mode(text, auto_switch)

            # Send notification if mode was auto-switched
            if ctx and auto_switch:
                try:
                    import json
                    parsed = json.loads(result)
                    if parsed.get("auto_switched"):
                        from .context_helpers import notify_tools_changed
                        await notify_tools_changed(ctx)
                except Exception as e:
                    logger.debug(f"Could not notify tools changed: {e}")

            return result

        @mcp.tool()
        def tool_usage_stats() -> str:
            """
            [HINT: Tool usage analytics. Shows usage patterns and co-occurrence data.]

            🎯 Output: Usage statistics, tool relationships, mode history
            🔧 Side Effects: None
            ⏱️ Typical Runtime: <10ms

            Shows which tools you use most, which tools are commonly used together,
            and your workflow mode history. Useful for understanding your patterns.

            Returns:
                JSON with comprehensive usage analytics
            """
            return _get_tool_usage_stats()

        # ═══════════════════════════════════════════════════════════════════
        # CONTEXT SUMMARIZATION TOOLS
        # ═══════════════════════════════════════════════════════════════════

        @mcp.tool()
        def summarize(
            data: str,
            level: str = "brief",
            tool_type: Optional[str] = None,
            max_tokens: Optional[int] = None,
            include_raw: bool = False,
        ) -> str:
            """
            [HINT: Context summarizer. Compresses verbose outputs to key metrics. Levels: brief|detailed|key_metrics|actionable.]

            Strategically summarizes tool outputs for efficient context usage.
            Reduces token consumption by 50-80% while preserving key information.

            📊 Output: Compressed summary with key metrics and token estimates
            🔧 Side Effects: None
            ⏱️ Typical Runtime: <10ms

            Args:
                data: JSON string to summarize (tool output, API response, etc.)
                level: Summarization level
                    - "brief": One-line summary with key metrics (default)
                    - "detailed": Multi-line with categories
                    - "key_metrics": Just the numbers/scores
                    - "actionable": Only recommendations and tasks
                tool_type: Hint for smarter summarization (auto-detected if not provided)
                    - "health", "security", "task", "testing", "scorecard", etc.
                max_tokens: Maximum tokens for output (truncates if needed)
                include_raw: Include original data in response

            Examples:
                summarize(health_result, level="brief")
                → "Health: 85/100, 3 issues, 2 actions"

                summarize(security_scan, level="key_metrics")
                → {"critical": 0, "high": 2, "medium": 5}
            """
            return _summarize_context(data, level, tool_type, max_tokens, include_raw)

        @mcp.tool()
        def context_budget(
            items: str,
            budget_tokens: int = 4000,
        ) -> str:
            """
            [HINT: Context budget. Estimates tokens and suggests what to keep/summarize to fit budget.]

            Analyze token usage and get recommendations for context reduction.

            📊 Output: Token analysis with reduction strategy
            🔧 Side Effects: None
            ⏱️ Typical Runtime: <10ms

            Args:
                items: JSON array of items to analyze
                budget_tokens: Target token budget (default: 4000)

            Returns:
                JSON with total tokens, items by size, and reduction strategy
            """
            import json
            parsed_items = json.loads(items) if isinstance(items, str) else items
            return _estimate_context_budget(parsed_items, budget_tokens)

        # NOTE: get_tool_help removed - use resource automation://tools for tool info
        # NOTE: project_overview removed - use generate_project_overview

        # NOTE: consolidate_tags removed - use task_analysis(action="tags")
        # NOTE: analyze_task_hierarchy removed - use task_analysis(action="hierarchy")

        # ═══════════════════════════════════════════════════════════════════
        # TRUSTED ADVISOR SYSTEM TOOLS
        # ═══════════════════════════════════════════════════════════════════

        @mcp.tool()
        def consult_advisor(
            metric: Optional[str] = None,
            tool: Optional[str] = None,
            stage: Optional[str] = None,
            score: float = 50.0,
            context: str = "",
        ) -> str:
            """
            [HINT: Trusted advisor. Wisdom from assigned advisors by metric/tool/stage.]

            Consult a trusted advisor assigned to a metric, tool, or workflow stage.
            Advisors provide wisdom matched to project health and context.

            Args:
                metric: Scorecard metric (security, testing, documentation, etc.)
                tool: Tool name (project_scorecard, sprint_automation, etc.)
                stage: Workflow stage (daily_checkin, planning, review, etc.)
                score: Current score for wisdom tier selection (0-100)
                context: What you're working on (for logging)

            Returns:
                Advisor wisdom with quote, encouragement, and rationale
            """
            from .tools.wisdom.advisors import consult_advisor as _consult_advisor

            result = _consult_advisor(metric=metric, tool=tool, stage=stage, score=score, context=context, log=True)
            return json.dumps(result, separators=(",", ":"))

        # NOTE: get_advisor_briefing removed - use report(type="briefing")

        # NOTE: export_advisor_podcast removed - use advisor_audio(action="export")
        # NOTE: synthesize_advisor_quote removed - use advisor_audio(action="quote")
        # NOTE: generate_podcast_audio removed - use advisor_audio(action="podcast")
        # NOTE: list_advisors removed - use resource automation://advisors
        # NOTE: check_tts_backends removed - use resource automation://tts-backends

        # ═══════════════════════════════════════════════════════════════════
        # DEPENDABOT INTEGRATION TOOLS
        # ═══════════════════════════════════════════════════════════════════

        # NOTE: fetch_dependabot_alerts removed - use security(action="alerts")
        # NOTE: generate_security_report removed - use security(action="report")

    # ═══════════════════════════════════════════════════════════════════════════════
    # CONSOLIDATED TOOLS (Phase 3 consolidation)
    # ═══════════════════════════════════════════════════════════════════════════════

    try:
        from .tools.consolidated import (
            advisor_audio as _advisor_audio,
        )
        from .tools.consolidated import (
            analyze_alignment as _analyze_alignment,
        )
        from .tools.consolidated import (
            generate_config as _generate_config,
        )
        from .tools.consolidated import (
            health as _health,
        )
        from .tools.consolidated import (
            lint as _lint,
        )
        from .tools.consolidated import (
            memory as _memory,
        )
        from .tools.consolidated import (
            prompt_tracking as _prompt_tracking,
        )
        from .tools.consolidated import (
            report as _report,
        )
        from .tools.consolidated import (
            security as _security,
        )
        from .tools.consolidated import (
            setup_hooks as _setup_hooks,
        )
        from .tools.consolidated import (
            task_analysis as _task_analysis,
        )
        from .tools.consolidated import (
            task_discovery as _task_discovery,
        )
        from .tools.consolidated import (
            task_workflow as _task_workflow,
        )
        from .tools.consolidated import (
            memory_maint as _memory_maint,
        )
        from .tools.consolidated import (
            testing as _testing,
        )
        CONSOLIDATED_AVAILABLE = True
    except ImportError:
        CONSOLIDATED_AVAILABLE = False

    if CONSOLIDATED_AVAILABLE:
        @mcp.tool()
        def analyze_alignment(
            action: str = "todo2",
            create_followup_tasks: bool = True,
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Alignment analysis. action=todo2|prd. Scores, misaligned items, recommendations.]

            Unified alignment analysis:
            - action="todo2": Task-to-goals alignment, creates follow-up tasks
            - action="prd": PRD persona mapping, advisor assignments

            📊 Output: Alignment scores, misaligned items, recommendations
            🔧 Side Effects: Creates tasks (todo2 action with create_followup_tasks=True)
            """
            result = _analyze_alignment(action, create_followup_tasks, output_path)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def security(
            action: str = "report",
            repo: str = "davidl71/project-management-automation",
            languages: Optional[list[str]] = None,
            config_path: Optional[str] = None,
            state: str = "open",
            include_dismissed: bool = False,
        ) -> str:
            """
            [HINT: Security. action=scan|alerts|report. Vulnerabilities, remediation.]

            Unified security analysis:
            - action="scan": Local pip-audit dependency scan
            - action="alerts": Fetch GitHub Dependabot alerts
            - action="report": Combined security report (Dependabot + pip-audit)

            📊 Output: Vulnerabilities by severity, remediation recommendations
            🔧 Side Effects: None (read-only)
            """
            result = _security(action, repo, languages, config_path, state, include_dismissed)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def generate_config(
            action: str = "rules",
            rules: Optional[str] = None,
            overwrite: bool = False,
            analyze_only: bool = False,
            include_indexing: bool = True,
            analyze_project: bool = True,
            rule_files: Optional[str] = None,
            output_dir: Optional[str] = None,
            dry_run: bool = False,
        ) -> str:
            """
            [HINT: Config generation. action=rules|ignore|simplify. Creates IDE config files.]

            Unified config generation:
            - action="rules": Generate .cursor/rules/*.mdc files
            - action="ignore": Generate .cursorignore/.cursorindexingignore
            - action="simplify": Simplify existing rule files

            📊 Output: Generated files, changes made
            🔧 Side Effects: Creates/updates config files (unless dry_run=True)
            """
            result = _generate_config(
                action, rules, overwrite, analyze_only,
                include_indexing, analyze_project,
                rule_files, output_dir, dry_run
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def setup_hooks(
            action: str = "git",
            hooks: Optional[list[str]] = None,
            patterns: Optional[str] = None,
            config_path: Optional[str] = None,
            install: bool = True,
            dry_run: bool = False,
        ) -> str:
            """
            [HINT: Hooks setup. action=git|patterns. Install automation hooks.]

            Unified hooks setup:
            - action="git": Install git hooks (pre-commit, pre-push, etc.)
            - action="patterns": Install pattern triggers for file/task automation

            📊 Output: Installation status, hooks configured
            🔧 Side Effects: Installs hooks (unless dry_run=True)
            """
            result = _setup_hooks(action, hooks, patterns, config_path, install, dry_run)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def prompt_tracking(
            action: str = "analyze",
            prompt: Optional[str] = None,
            task_id: Optional[str] = None,
            mode: Optional[str] = None,
            outcome: Optional[str] = None,
            iteration: int = 1,
            days: int = 7,
        ) -> str:
            """
            [HINT: Prompt tracking. action=log|analyze. Track and analyze prompts.]

            Unified prompt tracking:
            - action="log": Log a prompt iteration (requires prompt parameter)
            - action="analyze": Analyze prompt patterns over time

            📊 Output: Log confirmation or iteration statistics
            🔧 Side Effects: Writes to .cursor/prompt_history/ (log action)
            """
            result = _prompt_tracking(action, prompt, task_id, mode, outcome, iteration, days)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def health(
            action: str = "server",
            agent_name: Optional[str] = None,
            check_remote: bool = True,
            output_path: Optional[str] = None,
            create_tasks: bool = True,
            task_id: Optional[str] = None,
            changed_files: Optional[str] = None,
            auto_check: bool = True,
            workflow_path: Optional[str] = None,
            check_runners: bool = True,
        ) -> str:
            """
            [HINT: Health check. action=server|git|docs|dod|cicd. Status and health metrics.]

            Unified health check:
            - action="server": Server operational status, version
            - action="git": Working copy health, uncommitted changes, sync status
            - action="docs": Documentation health score, broken links
            - action="dod": Definition of done validation for task completion
            - action="cicd": CI/CD workflow validation, runner config

            📊 Output: Health status and metrics
            🔧 Side Effects: Creates tasks (docs action with create_tasks=True)
            """
            result = _health(
                action, agent_name, check_remote, output_path, create_tasks,
                task_id, changed_files, auto_check, workflow_path, check_runners
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def report(
            action: str = "overview",
            output_format: str = "text",
            output_path: Optional[str] = None,
            include_recommendations: bool = True,
            overall_score: float = 50.0,
            security_score: float = 50.0,
            testing_score: float = 50.0,
            documentation_score: float = 50.0,
            completion_score: float = 50.0,
            alignment_score: float = 50.0,
            project_name: Optional[str] = None,
            include_architecture: bool = True,
            include_metrics: bool = True,
            include_tasks: bool = True,
        ) -> str:
            """
            [HINT: Report generation. action=overview|scorecard|briefing|prd. Project reports.]

            Unified report generation:
            - action="overview": One-page project overview for stakeholders
            - action="scorecard": Health metrics scorecard with component scores
            - action="briefing": Advisor wisdom summary for lowest-scoring areas
            - action="prd": Product requirements document from codebase

            📊 Output: Generated report in specified format
            🔧 Side Effects: Creates file (if output_path specified)
            """
            result = _report(
                action, output_format, output_path, include_recommendations,
                overall_score, security_score, testing_score,
                documentation_score, completion_score, alignment_score,
                project_name, include_architecture, include_metrics, include_tasks
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def advisor_audio(
            action: str = "podcast",
            text: Optional[str] = None,
            advisor: str = "default",
            days: int = 7,
            output_path: Optional[str] = None,
            backend: str = "auto",
        ) -> str:
            """
            [HINT: Advisor audio. action=quote|podcast|export. Voice synthesis and podcast generation.]

            Unified advisor audio:
            - action="quote": Synthesize single advisor quote to audio
            - action="podcast": Generate full podcast from recent consultations
            - action="export": Export consultation data as JSON for external tools

            📊 Output: Audio file path or export data
            🔧 Side Effects: Creates audio files (quote/podcast actions)
            """
            result = _advisor_audio(action, text, advisor, days, output_path, backend)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def task_analysis(
            action: str = "duplicates",
            similarity_threshold: float = 0.85,
            auto_fix: bool = False,
            dry_run: bool = True,
            custom_rules: Optional[str] = None,
            remove_tags: Optional[str] = None,
            output_format: str = "text",
            include_recommendations: bool = True,
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Task analysis. action=duplicates|tags|hierarchy. Task quality and structure.]

            Unified task analysis:
            - action="duplicates": Find duplicate tasks by similarity
            - action="tags": Consolidate/cleanup task tags
            - action="hierarchy": Analyze task structure and groupings

            📊 Output: Analysis results with recommendations
            🔧 Side Effects: Modifies tasks (duplicates with auto_fix, tags without dry_run)
            """
            result = _task_analysis(
                action, similarity_threshold, auto_fix, dry_run,
                custom_rules, remove_tags, output_format,
                include_recommendations, output_path
            )
            if action == "hierarchy" and output_format != "json":
                return result.get("formatted_output", json.dumps(result, separators=(",", ":")))
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def testing(
            action: str = "run",
            test_path: Optional[str] = None,
            test_framework: str = "auto",
            verbose: bool = True,
            coverage: bool = False,
            coverage_file: Optional[str] = None,
            min_coverage: int = 80,
            format: str = "html",
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Testing tool. action=run|coverage. Execute tests or analyze coverage.]

            Unified testing:
            - action="run": Execute test suite (pytest/unittest/ctest)
            - action="coverage": Analyze test coverage with threshold

            📊 Output: Test results or coverage analysis
            🔧 Side Effects: May generate coverage reports
            """
            result = _testing(
                action, test_path, test_framework, verbose, coverage,
                coverage_file, min_coverage, format, output_path
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def lint(
            action: str = "run",
            path: Optional[str] = None,
            linter: str = "ruff",
            fix: bool = False,
            analyze: bool = True,
            select: Optional[str] = None,
            ignore: Optional[str] = None,
            problems_json: Optional[str] = None,
            include_hints: bool = True,
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Linting tool. action=run|analyze. Run linter or analyze problems.]

            Unified linting:
            - action="run": Execute linter (ruff/flake8), optionally analyze results
            - action="analyze": Analyze problems JSON with resolution hints

            📊 Output: Linter results or problem analysis
            🔧 Side Effects: May auto-fix issues (with fix=true)
            """
            return _lint(
                action, path, linter, fix, analyze, select, ignore,
                problems_json, include_hints, output_path
            )

        @mcp.tool()
        def memory(
            action: str = "search",
            title: Optional[str] = None,
            content: Optional[str] = None,
            category: str = "insight",
            task_id: Optional[str] = None,
            metadata: Optional[str] = None,
            include_related: bool = True,
            query: Optional[str] = None,
            limit: int = 10,
        ) -> str:
            """
            [HINT: Memory tool. action=save|recall|search. Persist and retrieve AI discoveries.]

            Unified memory management:
            - action="save": Store insight with title, content, category
            - action="recall": Get memories for a task_id
            - action="search": Find memories by query text

            Categories: debug, research, architecture, preference, insight

            📊 Output: Memory operation results
            🔧 Side Effects: Creates/retrieves memory files
            """
            result = _memory(
                action, title, content, category, task_id, metadata,
                include_related, query, limit
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def task_discovery(
            action: str = "all",
            file_patterns: Optional[str] = None,
            include_fixme: bool = True,
            doc_path: Optional[str] = None,
            output_path: Optional[str] = None,
            create_tasks: bool = False,
        ) -> str:
            """
            [HINT: Task discovery. action=comments|markdown|orphans|all. Find tasks from various sources.]

            Discovers tasks from:
            - action="comments": TODO/FIXME in code files
            - action="markdown": Task lists in *.md files
            - action="orphans": Orphaned Todo2 tasks (no dependencies)
            - action="all": All sources combined

            📊 Output: Discovered tasks with locations
            🔧 Side Effects: Can create Todo2 tasks (create_tasks=true)
            """
            result = _task_discovery(
                action, file_patterns, include_fixme, doc_path, output_path, create_tasks
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def task_workflow(
            action: str = "sync",
            dry_run: bool = False,
            status: str = "Review",
            new_status: str = "Todo",
            clarification_none: bool = True,
            filter_tag: Optional[str] = None,
            task_ids: Optional[str] = None,
            sub_action: str = "list",
            task_id: Optional[str] = None,
            clarification_text: Optional[str] = None,
            decision: Optional[str] = None,
            decisions_json: Optional[str] = None,
            move_to_todo: bool = True,
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Task workflow. action=sync|approve|clarify. Manage task lifecycle.]

            Unified task workflow:
            - action="sync": Sync TODO markdown tables ↔ Todo2
            - action="approve": Bulk approve/move tasks by status
            - action="clarify": Manage task clarifications (sub_action: list|resolve|batch)

            📊 Output: Workflow operation results
            🔧 Side Effects: Modifies task states
            """
            result = _task_workflow(
                action, dry_run, status, new_status, clarification_none,
                filter_tag, task_ids, sub_action, task_id,
                clarification_text, decision, decisions_json, move_to_todo, output_path
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def memory_maint(
            action: str = "health",
            max_age_days: int = 90,
            delete_orphaned: bool = True,
            delete_duplicates: bool = True,
            scorecard_max_age_days: int = 7,
            value_threshold: float = 0.3,
            keep_minimum: int = 50,
            similarity_threshold: float = 0.85,
            merge_strategy: str = "newest",
            scope: str = "week",
            advisors: Optional[str] = None,
            generate_insights: bool = True,
            save_dream: bool = True,
            dry_run: bool = True,
            interactive: bool = True,
        ) -> str:
            """
            [HINT: Memory maintenance. action=health|gc|prune|consolidate|dream. Lifecycle management.]

            Unified memory maintenance:
            - action="health": Memory system health metrics and recommendations
            - action="gc": Garbage collect stale/orphaned memories
            - action="prune": Remove low-value memories based on scoring
            - action="consolidate": Merge similar/duplicate memories
            - action="dream": Reflect on memories with wisdom advisors

            📊 Output: Maintenance results with recommendations
            🔧 Side Effects: Modifies memories (gc/prune/consolidate with dry_run=False)
            """
            result = _memory_maint(
                action, max_age_days, delete_orphaned, delete_duplicates,
                scorecard_max_age_days, value_threshold, keep_minimum,
                similarity_threshold, merge_strategy, scope, advisors,
                generate_insights, save_dream, dry_run, interactive
            )
            return json.dumps(result, separators=(",", ":"))

    # ═══════════════════════════════════════════════════════════════════════════════
    # AI SESSION MEMORY TOOLS
    # ═══════════════════════════════════════════════════════════════════════════════

    try:
        from .tools.session_memory import (
            generate_session_summary,
            get_memories_for_sprint,
            link_memory_to_task,
            recall_task_context,
            save_session_insight,
            search_session_memories,
        )

        MEMORY_TOOLS_AVAILABLE = True
    except ImportError:
        MEMORY_TOOLS_AVAILABLE = False
        logger.warning("Memory tools not available")

    if MEMORY_TOOLS_AVAILABLE:
        # NOTE: save_memory, recall_context, search_memories removed - use memory(action=save|recall|search)
        # NOTE: get_session_summary removed - use memory(action=search) with date filter
        # NOTE: get_sprint_memories removed - use memory(action=search) with category filter
        logger.info("Memory tools loaded successfully")

    # Register prompts
    try:
        # Try relative imports first (when run as module)
        try:
            from .prompts import (
                ADVISOR_AUDIO,
                ADVISOR_BRIEFING,
                # Wisdom
                ADVISOR_CONSULT,
                # Automation
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                AUTOMATION_SETUP,
                CONFIG_GENERATION,
                # Context Management
                CONTEXT_MANAGEMENT,
                DAILY_CHECKIN,
                # Documentation
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                DUPLICATE_TASK_CLEANUP,
                # Memory
                MEMORY_SYSTEM,
                # Mode Suggestion
                MODE_SUGGESTION,
                PERSONA_ARCHITECT,
                PERSONA_CODE_REVIEWER,
                # Personas
                PERSONA_DEVELOPER,
                PERSONA_EXECUTIVE,
                PERSONA_PROJECT_MANAGER,
                PERSONA_QA_ENGINEER,
                PERSONA_SECURITY_ENGINEER,
                PERSONA_TECH_WRITER,
                POST_IMPLEMENTATION_REVIEW,
                # Workflows
                PRE_SPRINT_CLEANUP,
                PROJECT_HEALTH,
                # Reports
                PROJECT_OVERVIEW,
                PROJECT_SCORECARD,
                # Security
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                SPRINT_END,
                SPRINT_START,
                # Tasks
                TASK_ALIGNMENT_ANALYSIS,
                TASK_DISCOVERY,
                TASK_REVIEW,
                TASK_SYNC,
                WEEKLY_MAINTENANCE,
            )
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from prompts import (
                ADVISOR_AUDIO,
                ADVISOR_BRIEFING,
                # Wisdom
                ADVISOR_CONSULT,
                # Automation
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                AUTOMATION_SETUP,
                CONFIG_GENERATION,
                # Context Management
                CONTEXT_MANAGEMENT,
                DAILY_CHECKIN,
                # Documentation
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                DUPLICATE_TASK_CLEANUP,
                # Memory
                MEMORY_SYSTEM,
                # Mode Suggestion
                MODE_SUGGESTION,
                PERSONA_ARCHITECT,
                PERSONA_CODE_REVIEWER,
                # Personas
                PERSONA_DEVELOPER,
                PERSONA_EXECUTIVE,
                PERSONA_PROJECT_MANAGER,
                PERSONA_QA_ENGINEER,
                PERSONA_SECURITY_ENGINEER,
                PERSONA_TECH_WRITER,
                POST_IMPLEMENTATION_REVIEW,
                # Workflows
                PRE_SPRINT_CLEANUP,
                PROJECT_HEALTH,
                # Reports
                PROJECT_OVERVIEW,
                PROJECT_SCORECARD,
                # Security
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                SPRINT_END,
                SPRINT_START,
                # Tasks
                TASK_ALIGNMENT_ANALYSIS,
                TASK_DISCOVERY,
                TASK_REVIEW,
                TASK_SYNC,
                WEEKLY_MAINTENANCE,
            )

        @mcp.prompt()
        def doc_check() -> str:
            """Analyze documentation health and create tasks for issues."""
            return DOCUMENTATION_HEALTH_CHECK

        @mcp.prompt()
        def doc_quick() -> str:
            """Quick documentation health check without creating tasks."""
            return DOCUMENTATION_QUICK_CHECK

        @mcp.prompt()
        def align() -> str:
            """Analyze Todo2 task alignment with project goals."""
            return TASK_ALIGNMENT_ANALYSIS

        @mcp.prompt()
        def dups() -> str:
            """Find and consolidate duplicate Todo2 tasks."""
            return DUPLICATE_TASK_CLEANUP

        @mcp.prompt()
        def sync() -> str:
            """Synchronize tasks between shared TODO table and Todo2."""
            return TASK_SYNC

        @mcp.prompt()
        def scan() -> str:
            """Scan all project dependencies for security vulnerabilities."""
            return SECURITY_SCAN_ALL

        @mcp.prompt()
        def scan_py() -> str:
            """Scan Python dependencies for security vulnerabilities."""
            return SECURITY_SCAN_PYTHON

        @mcp.prompt()
        def scan_rs() -> str:
            """Scan Rust dependencies for security vulnerabilities."""
            return SECURITY_SCAN_RUST

        @mcp.prompt()
        def auto() -> str:
            """Discover new automation opportunities in the codebase."""
            return AUTOMATION_DISCOVERY

        @mcp.prompt()
        def auto_high() -> str:
            """Find only high-value automation opportunities."""
            return AUTOMATION_HIGH_VALUE

        @mcp.prompt()
        def pre_sprint() -> str:
            """Pre-sprint cleanup workflow: duplicates, alignment, documentation."""
            return PRE_SPRINT_CLEANUP

        @mcp.prompt()
        def post_impl() -> str:
            """Post-implementation review workflow: docs, security, automation."""
            return POST_IMPLEMENTATION_REVIEW

        @mcp.prompt()
        def weekly() -> str:
            """Weekly maintenance workflow: docs, duplicates, security, sync."""
            return WEEKLY_MAINTENANCE

        # New workflow prompts
        @mcp.prompt()
        def daily_checkin() -> str:
            """Daily check-in workflow: server status, blockers, git health."""
            return DAILY_CHECKIN

        @mcp.prompt()
        def sprint_start() -> str:
            """Sprint start workflow: clean backlog, align tasks, queue work."""
            return SPRINT_START

        @mcp.prompt()
        def sprint_end() -> str:
            """Sprint end workflow: test coverage, docs, security check."""
            return SPRINT_END

        @mcp.prompt()
        def task_review() -> str:
            """Comprehensive task review: duplicates, alignment, staleness."""
            return TASK_REVIEW

        @mcp.prompt()
        def project_health() -> str:
            """Full project health assessment: code, docs, security, CI/CD."""
            return PROJECT_HEALTH

        @mcp.prompt()
        def automation_setup() -> str:
            """One-time automation setup: git hooks, triggers, cron."""
            return AUTOMATION_SETUP

        @mcp.prompt()
        def scorecard() -> str:
            """Generate comprehensive project health scorecard with all metrics."""
            return PROJECT_SCORECARD

        @mcp.prompt()
        def overview() -> str:
            """Generate one-page project overview for stakeholders."""
            return PROJECT_OVERVIEW

        # ═══════════════════════════════════════════════════════════════════════
        # WISDOM ADVISOR PROMPTS
        # ═══════════════════════════════════════════════════════════════════════

        @mcp.prompt()
        def advisor() -> str:
            """Consult a trusted advisor for wisdom on your current work."""
            return ADVISOR_CONSULT

        @mcp.prompt()
        def briefing() -> str:
            """Get morning briefing from advisors based on project health."""
            return ADVISOR_BRIEFING

        @mcp.prompt()
        def advisor_voice() -> str:
            """Generate audio from advisor consultations."""
            return ADVISOR_AUDIO

        # ═══════════════════════════════════════════════════════════════════════
        # ADDITIONAL PROMPTS
        # ═══════════════════════════════════════════════════════════════════════

        @mcp.prompt()
        def discover() -> str:
            """Discover tasks from TODO comments, markdown, and orphaned tasks."""
            return TASK_DISCOVERY

        @mcp.prompt()
        def config() -> str:
            """Generate IDE configuration files."""
            return CONFIG_GENERATION

        @mcp.prompt()
        def mode() -> str:
            """Suggest optimal Cursor IDE mode (Agent vs Ask) for a task."""
            return MODE_SUGGESTION

        @mcp.prompt()
        def context() -> str:
            """Manage LLM context with summarization and budget tools."""
            return CONTEXT_MANAGEMENT

        @mcp.prompt()
        def remember() -> str:
            """Use AI session memory to persist insights."""
            return MEMORY_SYSTEM

        # ═══════════════════════════════════════════════════════════════════════
        # PERSONA WORKFLOW PROMPTS
        # ═══════════════════════════════════════════════════════════════════════

        @mcp.prompt()
        def dev() -> str:
            """Developer daily workflow for writing quality code."""
            return PERSONA_DEVELOPER

        @mcp.prompt()
        def pm() -> str:
            """Project Manager workflow for delivery tracking."""
            return PERSONA_PROJECT_MANAGER

        @mcp.prompt()
        def reviewer() -> str:
            """Code Reviewer workflow for quality gates."""
            return PERSONA_CODE_REVIEWER

        @mcp.prompt()
        def exec() -> str:
            """Executive/Stakeholder workflow for strategic view."""
            return PERSONA_EXECUTIVE

        @mcp.prompt()
        def seceng() -> str:
            """Security Engineer workflow for risk management."""
            return PERSONA_SECURITY_ENGINEER

        @mcp.prompt()
        def arch() -> str:
            """Architect workflow for system design."""
            return PERSONA_ARCHITECT

        @mcp.prompt()
        def qa() -> str:
            """QA Engineer workflow for quality assurance."""
            return PERSONA_QA_ENGINEER

        @mcp.prompt()
        def writer() -> str:
            """Technical Writer workflow for documentation."""
            return PERSONA_TECH_WRITER

        PROMPTS_AVAILABLE = True
        logger.info("Registered 38 prompts successfully")
    except ImportError as e:
        PROMPTS_AVAILABLE = False
        logger.warning(f"Prompts not available: {e}")

    # Resource handlers (Phase 3)
    try:
        # Try relative imports first (when run as module)
        try:
            from .resources.cache import get_cache_status_resource
            from .resources.catalog import (
                get_advisors_resource,
                get_linters_resource,
                get_models_resource,
                get_problem_categories_resource,
                get_tts_backends_resource,
            )
            from .resources.history import get_history_resource
            from .resources.list import get_tools_list_resource
            from .resources.memories import (
                get_memories_by_category_resource,
                get_memories_by_task_resource,
                get_memories_health_resource,
                get_memories_resource,
                get_recent_memories_resource,
                get_session_memories_resource,
                get_wisdom_resource,
            )
            from .resources.status import get_status_resource
            from .resources.tasks import get_agent_tasks_resource, get_agents_resource, get_tasks_resource

            MEMORIES_AVAILABLE = True
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from resources.cache import get_cache_status_resource
            from resources.catalog import (
                get_advisors_resource,
                get_linters_resource,
                get_models_resource,
                get_problem_categories_resource,
                get_tts_backends_resource,
            )
            from resources.history import get_history_resource
            from resources.list import get_tools_list_resource
            from resources.status import get_status_resource
            from resources.tasks import get_agent_tasks_resource, get_agents_resource, get_tasks_resource

            try:
                from resources.memories import (
                    get_memories_by_category_resource,
                    get_memories_by_task_resource,
                    get_memories_health_resource,
                    get_memories_resource,
                    get_recent_memories_resource,
                    get_session_memories_resource,
                    get_wisdom_resource,
                )

                MEMORIES_AVAILABLE = True
            except ImportError:
                MEMORIES_AVAILABLE = False

        @mcp.resource("automation://status")
        def get_automation_status() -> str:
            """Get automation server status and health information."""
            return get_status_resource()

        @mcp.resource("automation://history")
        def get_automation_history() -> str:
            """Get automation tool execution history."""
            return get_history_resource(limit=50)

        @mcp.resource("automation://tools")
        def get_automation_tools() -> str:
            """Get list of available automation tools with descriptions."""
            return get_tools_list_resource()

        @mcp.resource("automation://tasks")
        def get_automation_tasks() -> str:
            """Get Todo2 tasks list."""
            return get_tasks_resource()

        @mcp.resource("automation://tasks/agent/{agent_name}")
        def get_automation_tasks_by_agent(agent_name: str) -> str:
            """Get Todo2 tasks for a specific agent."""
            return get_agent_tasks_resource(agent_name)

        @mcp.resource("automation://tasks/status/{status}")
        def get_automation_tasks_by_status(status: str) -> str:
            """Get Todo2 tasks filtered by status."""
            return get_tasks_resource(status=status)

        @mcp.resource("automation://agents")
        def get_automation_agents() -> str:
            """Get list of available agents with configurations and task counts."""
            return get_agents_resource()

        @mcp.resource("automation://cache")
        def get_automation_cache() -> str:
            """Get cache status - what data is cached and when it was last updated."""
            return get_cache_status_resource()

        # ═══════════════════════════════════════════════════════════════════════════════
        # CATALOG RESOURCES (converted from list_* tools)
        # ═══════════════════════════════════════════════════════════════════════════════

        @mcp.resource("automation://advisors")
        def get_advisors_catalog() -> str:
            """Get trusted advisors catalog with assignments by metric, tool, and stage."""
            return get_advisors_resource()

        @mcp.resource("automation://models")
        def get_models_catalog() -> str:
            """Get available AI models with recommendations for task types."""
            return get_models_resource()

        @mcp.resource("automation://problem-categories")
        def get_problem_categories_catalog() -> str:
            """Get problem categories with resolution hints."""
            return get_problem_categories_resource()

        @mcp.resource("automation://linters")
        def get_linters_catalog() -> str:
            """Get available linters and their installation status."""
            return get_linters_resource()

        @mcp.resource("automation://tts-backends")
        def get_tts_backends_catalog() -> str:
            """Get available text-to-speech backends."""
            return get_tts_backends_resource()

        @mcp.resource("automation://scorecard")
        def get_project_scorecard() -> str:
            """Get current project scorecard with all health metrics."""
            result = _generate_project_scorecard("json", True, None)
            return json.dumps(result, separators=(",", ":"))

        # Memory resources (AI Session Memory System)
        if MEMORIES_AVAILABLE:

            @mcp.resource("automation://memories")
            def get_all_memories() -> str:
                """Get all AI session memories - browsable context for session continuity."""
                return get_memories_resource()

            @mcp.resource("automation://memories/category/{category}")
            def get_memories_by_category(category: str) -> str:
                """Get memories filtered by category (debug, research, architecture, preference, insight)."""
                return get_memories_by_category_resource(category)

            @mcp.resource("automation://memories/task/{task_id}")
            def get_memories_for_task(task_id: str) -> str:
                """Get memories linked to a specific task."""
                return get_memories_by_task_resource(task_id)

            @mcp.resource("automation://memories/recent")
            def get_recent_memories() -> str:
                """Get memories from the last 24 hours."""
                return get_recent_memories_resource()

            @mcp.resource("automation://memories/session/{date}")
            def get_session_memories(date: str) -> str:
                """Get memories from a specific session date (YYYY-MM-DD format)."""
                return get_session_memories_resource(date)

            @mcp.resource("automation://wisdom")
            def get_combined_wisdom() -> str:
                """Get combined view of memories and advisor consultations."""
                return get_wisdom_resource()

            @mcp.resource("automation://memories/health")
            def get_memory_health() -> str:
                """Get memory system health metrics and maintenance recommendations."""
                return get_memories_health_resource()

            logger.info("Memory resources loaded successfully")

        RESOURCES_AVAILABLE = True
        logger.info("Resource handlers loaded successfully")
    except ImportError as e:
        RESOURCES_AVAILABLE = False
        logger.warning(f"Resource handlers not available: {e}")

        # Fallback resource handler (only if resources failed to load)
        # Note: This is a minimal fallback - full status available via server_status tool
        @mcp.resource("automation://status")
        def get_automation_status_fallback() -> str:
            """Get automation server status (fallback when resource handlers unavailable)."""
            return json.dumps(
                {
                    "status": "operational",
                    "tools_available": TOOLS_AVAILABLE,
                    "note": "Using fallback status - resource handlers unavailable",
                }
            )

    # Main entry point for FastMCP


def _is_mcp_mode() -> bool:
    """Detect if running in MCP mode (stdin is not a TTY or MCP env vars set)."""
    import sys

    # Check for explicit MCP mode
    if os.environ.get("EXARP_MCP_MODE") == "1":
        return True
    # Check for Cursor/AI environment
    if os.environ.get("CURSOR_TRACE_ID"):
        return True
    # Check if stdin is not a TTY (piped input = likely MCP)
    if not sys.stdin.isatty():
        return True
    return False


def _print_shell_setup(shell: str = "zsh") -> None:
    """Print shell configuration that can be eval'd or sourced."""
    setup = f"""# Exarp Shell Setup (generated by: exarp --shell-setup)
# Add to your ~/.{shell}rc or eval: eval "$(exarp --shell-setup)"

# ═══════════════════════════════════════════════════════════════
# EXARP CONFIGURATION
# ═══════════════════════════════════════════════════════════════

export EXARP_CACHE_DIR="${{EXARP_CACHE_DIR:-${{XDG_CACHE_HOME:-$HOME/.cache}}/exarp}}"
mkdir -p "$EXARP_CACHE_DIR" 2>/dev/null

# Optional features (uncomment to enable)
# export EXARP_PROMPT=1              # Show score in prompt
# export EXARP_MOTD=lite             # MOTD on shell start (lite|context|score|wisdom)
# export EXARP_WISDOM_SOURCE=random  # Wisdom source

# ═══════════════════════════════════════════════════════════════
# ALIASES
# ═══════════════════════════════════════════════════════════════

alias exarp="uvx exarp"
alias pma="uvx exarp"

# ═══════════════════════════════════════════════════════════════
# FULL TOOLS WITH CACHING AND FALLBACK
# ═══════════════════════════════════════════════════════════════

# Helper: Get project-specific cache dir
_exarp_project_cache() {{
    local proj_hash=$(pwd | shasum | cut -c1-8)
    echo "$EXARP_CACHE_DIR/projects/$proj_hash"
}}

# NOTE: xs() is defined below in CAPTURED OUTPUT section with score caching

# Overview with caching and offline fallback
xo() {{
    local cache_dir=$(_exarp_project_cache)
    local cache_file="$cache_dir/overview.txt"
    mkdir -p "$cache_dir" 2>/dev/null

    local result
    result=$(uvx --from exarp python3 -c "
from project_management_automation.tools.project_overview import generate_project_overview
r = generate_project_overview()
print(r.get('formatted_output', ''))
" 2>/dev/null)

    if [[ -n "$result" ]]; then
        echo "$result"
        echo "$result" > "$cache_file"
        date +%s > "$cache_file.ts"
    elif [[ -f "$cache_file" ]]; then
        local age=999999
        [[ -f "$cache_file.ts" ]] && age=$(($(date +%s) - $(cat "$cache_file.ts")))
        echo "⚠️  Using cached overview (uvx unavailable, cached $((age/60))m ago)"
        echo ""
        cat "$cache_file"
    else
        echo "❌ Overview unavailable (no uvx, no cache)"
        echo "   Try: xl (lite context) or check network"
    fi
}}

# Wisdom with caching and offline fallback
xw() {{
    local cache_dir="$EXARP_CACHE_DIR/wisdom"
    local today=$(date +%Y%m%d)
    local cache_file="$cache_dir/$today.txt"
    mkdir -p "$cache_dir" 2>/dev/null

    local result
    result=$(uvx --from exarp python3 -c "
from project_management_automation.tools.wisdom import get_wisdom, format_text
print(format_text(get_wisdom(50)))
" 2>/dev/null)

    if [[ -n "$result" ]]; then
        echo "$result"
        echo "$result" > "$cache_file"
    elif [[ -f "$cache_file" ]]; then
        echo "⚠️  Using cached wisdom (uvx unavailable)"
        echo ""
        cat "$cache_file"
    else
        # Try yesterday
        local yesterday=$(date -v-1d +%Y%m%d 2>/dev/null || date -d "yesterday" +%Y%m%d 2>/dev/null)
        if [[ -f "$cache_dir/$yesterday.txt" ]]; then
            echo "⚠️  Using yesterday wisdom (uvx unavailable)"
            echo ""
            cat "$cache_dir/$yesterday.txt"
        else
            echo "❌ Wisdom unavailable (no uvx, no cache)"
            echo "   Offline wisdom: The obstacle is the way. - Marcus Aurelius"
        fi
    fi
}}

# Clear cache
exarp_clear_cache() {{
    rm -rf "$EXARP_CACHE_DIR/projects" "$EXARP_CACHE_DIR/wisdom"
    mkdir -p "$EXARP_CACHE_DIR"
    echo "✅ Exarp cache cleared"
}}

# ═══════════════════════════════════════════════════════════════
# SHELL-ONLY FUNCTIONS (instant, no Python startup)
# ═══════════════════════════════════════════════════════════════

# Fast project detection
_exarp_detect() {{
    local dir="${{1:-.}}"
    [[ -d "$dir/.todo2" ]] || [[ -d "$dir/.git" ]] || \\
    [[ -f "$dir/pyproject.toml" ]] || [[ -f "$dir/package.json" ]] || \\
    [[ -f "$dir/Cargo.toml" ]] || [[ -f "$dir/go.mod" ]]
}}

# Fast project name
_exarp_name() {{
    local dir="${{1:-.}}"
    if [[ -f "$dir/pyproject.toml" ]]; then
        grep -m1 'name.*=' "$dir/pyproject.toml" 2>/dev/null | sed 's/.*"\\([^"]*\\)".*/\\1/' | head -1
    elif [[ -f "$dir/package.json" ]]; then
        grep -m1 '"name"' "$dir/package.json" 2>/dev/null | sed 's/.*": *"\\([^"]*\\)".*/\\1/'
    else
        basename "$(cd "$dir" 2>/dev/null && pwd || echo "$dir")"
    fi
}}

# Fast task count
_exarp_tasks() {{
    local todo_file="${{1:-.}}/.todo2/state.todo2.json"
    if [[ ! -f "$todo_file" ]]; then echo "0/0"; return; fi
    local total=$(grep -c '"id"' "$todo_file" 2>/dev/null || echo 0)
    local done=$(grep -c '"status".*[Dd]one' "$todo_file" 2>/dev/null || echo 0)
    echo "$((total - done))/$total"
}}

# Lite context (instant)
xl() {{
    local dir="${{1:-.}}"
    if ! _exarp_detect "$dir"; then echo "📁 Not a project"; return 1; fi
    local name=$(_exarp_name "$dir")
    local tasks=$(_exarp_tasks "$dir")
    echo ""
    echo "┌─────────────────────────────────────────────────────┐"
    echo "│  ⚡ EXARP LITE                                      │"
    echo "├─────────────────────────────────────────────────────┤"
    printf "│  Project: %-40s│\\n" "${{name:0:40}}"
    printf "│  Tasks:   %-40s│\\n" "$tasks (pending/total)"
    echo "└─────────────────────────────────────────────────────┘"
}}

# Lite task list
xt() {{
    local todo_file="${{1:-.}}/.todo2/state.todo2.json"
    local limit="${{2:-10}}"
    if [[ ! -f "$todo_file" ]]; then echo "No .todo2 found"; return 1; fi
    echo ""
    echo "┌─────────────────────────────────────────────────────┐"
    printf "│  📋 PENDING TASKS (top %-2s)                        │\\n" "$limit"
    echo "├─────────────────────────────────────────────────────┤"
    python3 -c "
import json
with open('$todo_file') as f:
    data = json.load(f)
count = 0
for t in data.get('todos', []):
    if t.get('status', '').lower() in ['pending', 'in_progress', 'todo', 'in progress']:
        # Support both 'content' (exarp) and 'name' (todo2) formats
        task_text = t.get('content') or t.get('name') or t.get('title') or ''
        print('│  • ' + task_text[:47].ljust(47) + '│')
        count += 1
        if count >= $limit: break
if count == 0: print('│  ✅ No pending tasks!                             │')
" 2>/dev/null
    echo "└─────────────────────────────────────────────────────┘"
}}

# Lite projects scan
xpl() {{
    local dir="${{1:-.}}"
    echo ""
    echo "┌─────────────────────────────────────────────────────┐"
    echo "│  🗂️  PROJECTS                                       │"
    echo "├─────────────────────────────────────────────────────┤"
    local count=0
    for subdir in "$dir"/*/; do
        if _exarp_detect "$subdir"; then
            local name=$(_exarp_name "$subdir")
            local tasks=$(_exarp_tasks "$subdir")
            printf "│  %-30s %-17s│\\n" "${{name:0:30}}" "$tasks"
            count=$((count + 1))
        fi
    done
    [[ $count -eq 0 ]] && echo "│  No projects found                                │"
    echo "└─────────────────────────────────────────────────────┘"
    echo "  Found $count project(s)"
}}

# Full context (with cached score)
xc() {{
    if ! _exarp_detect "."; then echo "📁 Not a project"; return 1; fi
    xl
    echo "  Full: xs (score) | xo (overview) | xw (wisdom)"
}}

# ═══════════════════════════════════════════════════════════════
# PROMPT INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Get cached score (fast, no Python)
_exarp_cached_score() {{
    local cache_file="$(_exarp_project_cache)/score.txt"
    [[ -f "$cache_file" ]] && cat "$cache_file" || echo ""
}}

# Update cached score (called after xs)
_exarp_update_score() {{
    local score="$1"
    local cache_file="$(_exarp_project_cache)/score.txt"
    mkdir -p "$(dirname "$cache_file")" 2>/dev/null
    echo "$score" > "$cache_file"
}}

# Prompt info with tasks and optional score
exarp_prompt_info() {{
    [[ "${{EXARP_PROMPT:-0}}" == "0" ]] && return
    _exarp_detect "." || return

    local tasks=$(_exarp_tasks ".")
    local pending=${{tasks%%/*}}
    local output=""

    # Task count badge
    if (( pending > 0 )); then
        if (( pending > 10 )); then
            output="%F{{red}}◇$pending%f"
        elif (( pending > 5 )); then
            output="%F{{yellow}}◇$pending%f"
        else
            output="%F{{blue}}◇$pending%f"
        fi
    fi

    # Score badge (if cached)
    local score=$(_exarp_cached_score)
    if [[ -n "$score" ]]; then
        if (( score >= 80 )); then
            output="$output %F{{green}}●$score%%%f"
        elif (( score >= 60 )); then
            output="$output %F{{yellow}}●$score%%%f"
        else
            output="$output %F{{red}}●$score%%%f"
        fi
    fi

    echo "$output"
}}

# Add to your prompt: RPROMPT='$(exarp_prompt_info) '$RPROMPT

# ═══════════════════════════════════════════════════════════════
# iTERM2 INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Set iTerm2 badge (project name + score)
exarp_iterm_badge() {{
    [[ "$TERM_PROGRAM" != "iTerm.app" ]] && return
    _exarp_detect "." || return

    local name=$(_exarp_name ".")
    local tasks=$(_exarp_tasks ".")
    local score=$(_exarp_cached_score)

    local badge="$name"
    [[ -n "$tasks" ]] && badge="$badge ◇${{tasks%%/*}}"
    [[ -n "$score" ]] && badge="$badge ●$score%"

    # iTerm2 badge escape sequence
    printf "\\033]1337;SetBadgeFormat=%s\\007" "$(echo -n "$badge" | base64)"
}}

# Set iTerm2 tab title
exarp_iterm_title() {{
    [[ "$TERM_PROGRAM" != "iTerm.app" ]] && return
    _exarp_detect "." || return

    local name=$(_exarp_name ".")
    # Set tab title
    printf "\\033]0;%s\\007" "$name"
}}

# Set iTerm2 user vars (for status bar)
exarp_iterm_vars() {{
    [[ "$TERM_PROGRAM" != "iTerm.app" ]] && return
    _exarp_detect "." || return

    local name=$(_exarp_name ".")
    local tasks=$(_exarp_tasks ".")
    local score=$(_exarp_cached_score)

    # Set user variables for iTerm2 status bar
    printf "\\033]1337;SetUserVar=exarp_project=%s\\007" "$(echo -n "$name" | base64)"
    printf "\\033]1337;SetUserVar=exarp_tasks=%s\\007" "$(echo -n "$tasks" | base64)"
    [[ -n "$score" ]] && printf "\\033]1337;SetUserVar=exarp_score=%s\\007" "$(echo -n "$score" | base64)"
}}

# Update all iTerm2 integrations
exarp_iterm_update() {{
    exarp_iterm_badge
    exarp_iterm_title
    exarp_iterm_vars
}}

# Hook into cd to update iTerm2 on directory change
if [[ "$TERM_PROGRAM" == "iTerm.app" ]] && [[ "${{EXARP_ITERM:-1}}" != "0" ]]; then
    # Save original cd
    if ! type _exarp_original_cd &>/dev/null; then
        _exarp_original_cd() {{ builtin cd "$@"; }}
    fi

    cd() {{
        _exarp_original_cd "$@" && exarp_iterm_update
    }}

    # Initial update
    exarp_iterm_update
fi

# ═══════════════════════════════════════════════════════════════
# MOTD (Message of the Day)
# ═══════════════════════════════════════════════════════════════

# Enhanced MOTD with multiple modes
exarp_motd() {{
    local mode="${{EXARP_MOTD:-lite}}"

    case "$mode" in
        lite)
            # Quick summary
            echo ""
            echo "┌─────────────────────────────────────────────────────┐"
            echo "│  🌟 EXARP                                           │"
            echo "└─────────────────────────────────────────────────────┘"
            if _exarp_detect "."; then xl; else xpl; fi
            ;;
        context)
            # Project context with tasks
            echo ""
            if _exarp_detect "."; then
                xl
                echo ""
                xt | head -12
            else
                xpl
            fi
            ;;
        score)
            # Include scorecard (slower, needs uvx)
            echo ""
            if _exarp_detect "."; then
                xs 2>/dev/null | head -20
            else
                xpl
            fi
            ;;
        wisdom)
            # Wisdom only
            xw 2>/dev/null
            ;;
        full)
            # Everything
            echo ""
            if _exarp_detect "."; then
                xl
                echo ""
                xt | head -8
                echo ""
                xw 2>/dev/null | head -15
            else
                xpl
            fi
            ;;
        *)
            # Default to lite
            exarp_motd lite
            ;;
    esac
}}

# Auto-MOTD on shell start (if enabled)
if [[ "${{EXARP_MOTD:-0}}" != "0" ]]; then
    _motd_today=$(date +%Y%m%d)
    if [[ ! -f "$EXARP_CACHE_DIR/motd_${{_motd_today}}" ]]; then
        exarp_motd
        touch "$EXARP_CACHE_DIR/motd_${{_motd_today}}"
    fi
    unset _motd_today
fi

# ═══════════════════════════════════════════════════════════════
# CAPTURED OUTPUT / TRIGGERS
# ═══════════════════════════════════════════════════════════════

# Print trigger-friendly output (for iTerm2 triggers)
exarp_trigger_output() {{
    _exarp_detect "." || return
    local tasks=$(_exarp_tasks ".")
    local pending=${{tasks%%/*}}
    local total=${{tasks##*/}}
    local score=$(_exarp_cached_score)

    # Format: [EXARP] project:name tasks:N/M score:XX
    echo "[EXARP] project:$(_exarp_name .) tasks:$pending/$total score:${{score:-??}}"
}}

# Call after xs to update score cache and triggers
xs() {{
    local cache_dir=$(_exarp_project_cache)
    local cache_file="$cache_dir/scorecard.txt"
    mkdir -p "$cache_dir" 2>/dev/null

    # Try uvx first
    local result
    result=$(uvx --from exarp python3 -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
r = generate_project_scorecard()
print(r.get('formatted_output', ''))
# Extract score for caching
import re
match = re.search(r'OVERALL SCORE: ([0-9.]+)%', r.get('formatted_output', ''))
if match:
    with open('$cache_dir/score.txt', 'w') as f:
        f.write(match.group(1).split('.')[0])
" 2>/dev/null)

    if [[ -n "$result" ]]; then
        echo "$result"
        echo "$result" > "$cache_file"
        date +%s > "$cache_file.ts"
        # Update iTerm2 after score update
        exarp_iterm_update 2>/dev/null
    elif [[ -f "$cache_file" ]]; then
        local age=999999
        [[ -f "$cache_file.ts" ]] && age=$(($(date +%s) - $(cat "$cache_file.ts")))
        echo "⚠️  Using cached scorecard (uvx unavailable, cached $((age/60))m ago)"
        echo ""
        cat "$cache_file"
    else
        echo "❌ Scorecard unavailable (no uvx, no cache)"
        echo "   Try: xl (lite context) or check network"
    fi
}}

echo "✅ Exarp loaded: xl | xt | xpl | xs/xo/xw | iTerm2: ${{TERM_PROGRAM:-n/a}}"
"""
    print(setup)


def _print_completions(shell: str = "zsh") -> None:
    """Print shell completions."""
    if shell == "zsh":
        completions = """# Exarp ZSH Completions (generated by: exarp --completions)
# Add to your ~/.zshrc or eval: eval "$(exarp --completions)"

_exarp_commands() {
    local commands=(
        "xl:Lite context (instant, shell-only)"
        "xt:Task list (instant)"
        "xpl:Projects scan (instant)"
        "xc:Full context"
        "xs:Full scorecard (via uvx)"
        "xo:Full overview (via uvx)"
        "xw:Daily wisdom (via uvx)"
    )
    _describe 'exarp commands' commands
}

_exarp() {
    local -a opts
    opts=(
        '--help[Show help]'
        '--version[Show version]'
        '--shell-setup[Print shell configuration]'
        '--completions[Print shell completions]'
        '--aliases[Print aliases only]'
        '--mcp[Run in MCP server mode]'
    )
    _arguments $opts
}

compdef _exarp exarp 2>/dev/null
compdef _exarp uvx\\ exarp 2>/dev/null
"""
    else:
        completions = f"# Completions for {shell} not yet implemented"
    print(completions)


def _print_aliases() -> None:
    """Print just the aliases (minimal setup without full functions)."""
    aliases = """# Exarp Aliases (generated by: exarp --aliases)
# eval "$(exarp --aliases)"
# Note: For caching/fallback support, use: eval "$(exarp --shell-setup)"

alias exarp="uvx exarp"
alias pma="uvx exarp"

# Simple aliases (no caching - for minimal setup)
alias xs="uvx --from exarp python3 -c 'from project_management_automation.tools.project_scorecard import generate_project_scorecard; r=generate_project_scorecard(); print(r.get(\"formatted_output\",\"\"))'"
alias xo="uvx --from exarp python3 -c 'from project_management_automation.tools.project_overview import generate_project_overview; r=generate_project_overview(); print(r.get(\"formatted_output\",\"\"))'"
alias xw="uvx --from exarp python3 -c 'from project_management_automation.tools.wisdom import get_wisdom, format_text; print(format_text(get_wisdom(50)))'"

# For full features with caching and offline fallback, use:
#   eval "$(exarp --shell-setup)"
"""
    print(aliases)


def _print_usage() -> None:
    """Print usage help for interactive mode."""
    version_str = __version__
    usage = f"""
╭──────────────────────────────────────────────────────────╮
│                                                          │
│    ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗               │
│    ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗              │
│    █████╗   ╚███╔╝ ███████║██████╔╝██████╔╝              │
│    ██╔══╝   ██╔██╗ ██╔══██║██╔══██╗██╔═══╝               │
│    ███████╗██╔╝ ██╗██║  ██║██║  ██║██║                   │
│    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                   │
│                                                          │
│    Project Management Automation                         │
│    Version: {version_str:<44}│
│                                                          │
╰──────────────────────────────────────────────────────────╯

USAGE:
    exarp [OPTIONS]
    uvx exarp [OPTIONS]

OPTIONS:
    --help, -h          Show this help message
    --version, -v       Show version
    --shell-setup       Print shell configuration (eval "$(exarp --shell-setup)")
    --completions       Print shell completions
    --aliases           Print aliases only
    --mcp               Run in MCP server mode (for AI/Cursor)

SHELL SETUP (recommended):
    # Add to ~/.zshrc:
    eval "$(uvx exarp --shell-setup)"

    # Or download the full plugin:
    curl -sL https://raw.githubusercontent.com/davidl71/project-management-automation/main/shell/exarp-uvx.plugin.zsh -o ~/.exarp.zsh
    source ~/.exarp.zsh

QUICK COMMANDS (after shell setup):
    xl      Lite context (instant, shell-only)
    xt      Task list (instant)
    xpl     Projects scan (instant)
    xs      Full scorecard
    xo      Full overview
    xw      Daily wisdom

MCP MODE (for Cursor/AI):
    Cursor auto-detects MCP mode. Configure in .cursor/mcp.json:
    {{"mcpServers": {{"exarp": {{"command": "uvx", "args": ["exarp", "--mcp"]}}}}}}

DOCS:
    https://github.com/davidl71/project-management-automation
"""
    print(usage)


def _print_banner(file=None) -> None:
    """Print MCP server banner."""
    import sys

    file = file or sys.stderr

    tools_count = 25 if TOOLS_AVAILABLE else 1
    resources_ok = RESOURCES_AVAILABLE if "RESOURCES_AVAILABLE" in globals() else False

    version_str = f"{__version__}"
    tools_str = f"{tools_count}"
    resources_str = "Available" if resources_ok else "Unavailable"

    BOX_WIDTH = 56
    banner_lines = [
        "╭" + "─" * BOX_WIDTH + "╮",
        "│" + " " * BOX_WIDTH + "│",
        "│    ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗             │",
        "│    ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗            │",
        "│    █████╗   ╚███╔╝ ███████║██████╔╝██████╔╝            │",
        "│    ██╔══╝   ██╔██╗ ██╔══██║██╔══██╗██╔═══╝             │",
        "│    ███████╗██╔╝ ██╗██║  ██║██║  ██║██║                 │",
        "│    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                 │",
        "│" + " " * BOX_WIDTH + "│",
        "│    Project Management Automation MCP Server            │",
        "│" + " " * BOX_WIDTH + "│",
        f"│    Version:    {version_str:<39}│",
        f"│    Tools:      {tools_str:<39}│",
        f"│    Resources:  {resources_str:<39}│",
        "│    Transport:  STDIO                                   │",
        "│" + " " * BOX_WIDTH + "│",
        "╰" + "─" * BOX_WIDTH + "╯",
    ]
    print("\n".join(banner_lines), file=file)


def main():
    """Entry point for exarp - detects mode and handles CLI args."""
    import sys

    args = sys.argv[1:]

    # Handle CLI arguments
    if "--help" in args or "-h" in args:
        _print_usage()
        return

    if "--version" in args or "-v" in args:
        print(f"exarp {__version__}")
        return

    if "--shell-setup" in args or "--zshrc" in args:
        _print_shell_setup("zsh")
        return

    if "--completions" in args:
        _print_completions("zsh")
        return

    if "--aliases" in args:
        _print_aliases()
        return

    # Check for explicit MCP mode or auto-detect
    if "--mcp" in args or _is_mcp_mode():
        # MCP server mode
        if not MCP_AVAILABLE:
            print("Error: MCP not available. Install with: pip install mcp", file=sys.stderr)
            sys.exit(1)
        
        if not USE_STDIO and mcp:
            # FastMCP mode
            _print_banner()
            mcp.run(show_banner=False)
        elif USE_STDIO and stdio_server_instance:
            # Stdio server mode
            _print_banner()
            import asyncio
            async def run():
                async with stdio_server() as (read_stream, write_stream):
                    init_options = stdio_server_instance.create_initialization_options()
                    await stdio_server_instance.run(read_stream, write_stream, init_options)
            try:
                asyncio.run(run())
            except KeyboardInterrupt:
                logger.info("Server stopped by user")
            except Exception as e:
                logger.error(f"Server error: {e}", exc_info=True)
                sys.exit(1)
        else:
            print("Error: MCP server not initialized properly", file=sys.stderr)
            sys.exit(1)
        return

    # Interactive terminal without args - show usage
    _print_usage()


if __name__ == "__main__":
    main()
elif stdio_server_instance:
    # Register resources for stdio server
    try:
        # Try relative imports first (when run as module)
        try:
            from .resources.cache import get_cache_status_resource
            from .resources.history import get_history_resource
            from .resources.list import get_tools_list_resource
            from .resources.status import get_status_resource
            from .resources.tasks import get_agent_tasks_resource, get_agents_resource, get_tasks_resource
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from resources.cache import get_cache_status_resource
            from resources.history import get_history_resource
            from resources.list import get_tools_list_resource
            from resources.status import get_status_resource
            from resources.tasks import get_agent_tasks_resource, get_agents_resource, get_tasks_resource

        @stdio_server_instance.list_resources()
        async def list_resources() -> list[str]:
            """List all available resources."""
            return [
                "automation://status",
                "automation://history",
                "automation://tools",
                "automation://tasks",
                "automation://agents",
                "automation://cache",
            ]

        @stdio_server_instance.read_resource()
        async def read_resource(uri: str) -> str:
            """Handle resource reads."""
            if uri == "automation://status":
                return get_status_resource()
            elif uri == "automation://history":
                return get_history_resource(limit=50)
            elif uri == "automation://tools":
                return get_tools_list_resource()
            elif uri == "automation://tasks":
                return get_tasks_resource()
            elif uri.startswith("automation://tasks/agent/"):
                agent_name = uri.replace("automation://tasks/agent/", "")
                return get_agent_tasks_resource(agent_name)
            elif uri.startswith("automation://tasks/status/"):
                status = uri.replace("automation://tasks/status/", "")
                return get_tasks_resource(status=status)
            elif uri == "automation://agents":
                return get_agents_resource()
            elif uri == "automation://cache":
                return get_cache_status_resource()
            else:
                return json.dumps({"error": f"Unknown resource: {uri}"})

        RESOURCES_AVAILABLE = True
        logger.info("Resource handlers loaded successfully")
    except ImportError as e:
        RESOURCES_AVAILABLE = False
        logger.warning(f"Resource handlers not available: {e}")

    # Main entry point for stdio server
    if __name__ == "__main__":
        logger.info("Starting stdio server...")
        logger.info(f"Server name: {stdio_server_instance.name}")
        logger.info(f"Tools available: {TOOLS_AVAILABLE}")
        logger.info(
            f"Resources available: {RESOURCES_AVAILABLE if 'RESOURCES_AVAILABLE' in globals() else 'Not registered'}"
        )

        # stdio_server provides stdin/stdout streams, Server.run() handles the protocol
        async def run():
            async with stdio_server() as (read_stream, write_stream):
                init_options = stdio_server_instance.create_initialization_options()
                logger.info(f"Initialization options: {init_options}")
                logger.info("Server ready, waiting for client connections...")
                await stdio_server_instance.run(read_stream, write_stream, init_options)

        try:
            asyncio.run(run())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            sys.exit(1)
