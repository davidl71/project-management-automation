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

    # Suppress FastMCP output during initialization (banner, startup messages)
    with suppress_fastmcp_output():
        if not USE_STDIO and FastMCP:
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
# Import automation tools (handle both relative and absolute imports)
try:
    # Try relative imports first (when run as module)
    try:
        from .tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from .tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from .tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from .tools.daily_automation import run_daily_automation as _run_daily_automation
        from .tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from .tools.docs_health import check_documentation_health as _check_documentation_health
        from .tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from .tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from .tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from .tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from .tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from .tools.problems_advisor import analyze_problems_tool as _analyze_problems
        from .tools.problems_advisor import list_problem_categories as _list_problem_categories
        from .tools.project_overview import generate_project_overview as _generate_project_overview
        from .tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from .tools.pwa_review import review_pwa_config as _review_pwa_config
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
        from .tools.working_copy_health import check_working_copy_health as _check_working_copy_health

        TOOLS_AVAILABLE = True
    except ImportError:
        # Fallback to absolute imports (when run as script)
        from tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from tools.daily_automation import run_daily_automation as _run_daily_automation
        from tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from tools.docs_health import check_documentation_health as _check_documentation_health
        from tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from tools.problems_advisor import analyze_problems_tool as _analyze_problems
        from tools.problems_advisor import list_problem_categories as _list_problem_categories
        from tools.project_overview import generate_project_overview as _generate_project_overview
        from tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from tools.pwa_review import review_pwa_config as _review_pwa_config
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
        from tools.working_copy_health import check_working_copy_health as _check_working_copy_health

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
        @mcp.tool()
        def server_status() -> str:
            """
            [HINT: Server status. Returns operational status, version, tools available.]

            Get the current status of the project management automation server.
            """
            from .utils.dev_reload import is_dev_mode

            return json.dumps(
                {
                    "status": "operational",
                    "version": __version__,
                    "tools_available": TOOLS_AVAILABLE,
                    "total_tools": 28 if TOOLS_AVAILABLE else 2,
                    "project_root": str(project_root),
                    "dev_mode": is_dev_mode(),
                },
                separators=(",", ":"),
            )

        @mcp.tool()
        def dev_reload(modules: Optional[List[str]] = None) -> str:
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

        return server_status
    elif stdio_server_instance:
        # Stdio Server registration (handler-based)
        @stdio_server_instance.list_tools()
        async def list_tools() -> List[Tool]:
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
                            name="review_pwa_config",
                            description="Review PWA configuration and generate improvement recommendations.",
                            inputSchema={
                                "type": "object",
                                "properties": {
                                    "output_path": {"type": "string", "description": "Output file path"},
                                    "config_path": {"type": "string", "description": "Config file path"},
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
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
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
                    result = check_documentation_health(
                        arguments.get("output_path"), arguments.get("create_tasks", True)
                    )
                elif name == "analyze_todo2_alignment":
                    result = analyze_todo2_alignment(
                        arguments.get("create_followup_tasks", True), arguments.get("output_path")
                    )
                elif name == "detect_duplicate_tasks":
                    result = detect_duplicate_tasks(
                        arguments.get("similarity_threshold", 0.85),
                        arguments.get("auto_fix", False),
                        arguments.get("output_path"),
                    )
                elif name == "scan_dependency_security":
                    result = scan_dependency_security(arguments.get("languages"), arguments.get("config_path"))
                elif name == "find_automation_opportunities":
                    result = find_automation_opportunities(
                        arguments.get("min_value_score", 0.7), arguments.get("output_path")
                    )
                elif name == "sync_todo_tasks":
                    result = sync_todo_tasks(arguments.get("dry_run", False), arguments.get("output_path"))
                elif name == "review_pwa_config":
                    result = review_pwa_config(arguments.get("output_path"), arguments.get("config_path"))
                elif name == "add_external_tool_hints":
                    result = add_external_tool_hints(
                        arguments.get("dry_run", False),
                        arguments.get("output_path"),
                        arguments.get("min_file_size", 50),
                    )
                elif name == "run_daily_automation":
                    result = run_daily_automation(
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

        @mcp.tool()
        def check_documentation_health(output_path: Optional[str] = None, create_tasks: bool = True) -> str:
            """[HINT: Docs health. Score 0-100, broken links, tasks created.]"""
            return _check_documentation_health(output_path, create_tasks)

        @mcp.tool()
        def analyze_todo2_alignment(create_followup_tasks: bool = True, output_path: Optional[str] = None) -> str:
            """[HINT: Task alignment. Misaligned count, avg score, follow-up tasks.]"""
            return _analyze_todo2_alignment(create_followup_tasks, output_path)

        @mcp.tool()
        def detect_duplicate_tasks(
            similarity_threshold: float = 0.85,
            auto_fix: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Duplicate tasks. Count, groups, auto_fix available.]"""
            return _detect_duplicate_tasks(similarity_threshold, auto_fix, output_path)

        @mcp.tool()
        def scan_dependency_security(languages: Optional[List[str]] = None, config_path: Optional[str] = None) -> str:
            """[HINT: Security scan. Vulns by severity, language breakdown, remediation.]"""
            return _scan_dependency_security(languages, config_path)

        @mcp.tool()
        def find_automation_opportunities(min_value_score: float = 0.7, output_path: Optional[str] = None) -> str:
            """[HINT: Automation discovery. Opportunities, value scores, recommendations.]"""
            return _find_automation_opportunities(min_value_score, output_path)

        @mcp.tool()
        def sync_todo_tasks(dry_run: bool = False, output_path: Optional[str] = None) -> str:
            """[HINT: Task sync. Matches found, conflicts, new tasks created.]"""
            return _sync_todo_tasks(dry_run, output_path)

        @mcp.tool()
        def review_pwa_config(output_path: Optional[str] = None, config_path: Optional[str] = None) -> str:
            """[HINT: PWA review. Config status, missing features, recommendations.]"""
            return _review_pwa_config(output_path, config_path)

        @mcp.tool()
        def add_external_tool_hints(
            dry_run: bool = False, output_path: Optional[str] = None, min_file_size: int = 50
        ) -> str:
            """[HINT: Tool hints. Files scanned, modified, hints added.]"""
            return _add_external_tool_hints(dry_run, output_path, min_file_size)

        @mcp.tool()
        def analyze_problems(problems_json: str, include_hints: bool = True, output_path: Optional[str] = None) -> str:
            """[HINT: Problems advisor. Analyzes linter errors, provides resolution hints, metrics.]"""
            return _analyze_problems(problems_json, include_hints, output_path)

        @mcp.tool()
        def list_problem_categories() -> str:
            """[HINT: Problem categories. Shows all recognized categories with resolution strategies.]"""
            return _list_problem_categories()

        @mcp.tool()
        def run_daily_automation(
            tasks: Optional[List[str]] = None,
            include_slow: bool = False,
            dry_run: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Daily automation. Tasks: docs_health, alignment, duplicates, security.]"""
            return _run_daily_automation(tasks, include_slow, dry_run, output_path)

        @mcp.tool()
        def validate_ci_cd_workflow(
            workflow_path: Optional[str] = None, check_runners: bool = True, output_path: Optional[str] = None
        ) -> str:
            """[HINT: CI/CD validation. Workflow status, runner config, issues.]"""
            return _validate_ci_cd_workflow(workflow_path, check_runners, output_path)

        @mcp.tool()
        def batch_approve_tasks(
            status: str = "Review",
            new_status: str = "Todo",
            clarification_none: bool = True,
            filter_tag: Optional[str] = None,
            task_ids: Optional[List[str]] = None,
            dry_run: bool = False,
        ) -> str:
            """[HINT: Batch approval. Approved count, task IDs, success status.]"""
            result = _batch_approve_tasks(
                status=status,
                new_status=new_status,
                clarification_none=clarification_none,
                filter_tag=filter_tag,
                task_ids=task_ids,
                dry_run=dry_run,
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def run_nightly_task_automation(
            max_tasks_per_host: int = 5,
            max_parallel_tasks: int = 10,
            priority_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            dry_run: bool = False,
        ) -> str:
            """[HINT: Nightly automation. Assigned tasks, moved to review, background remaining.]"""
            result = _run_nightly_task_automation(
                max_tasks_per_host=max_tasks_per_host,
                max_parallel_tasks=max_parallel_tasks,
                priority_filter=priority_filter,
                tag_filter=tag_filter,
                dry_run=dry_run,
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def check_working_copy_health(agent_name: Optional[str] = None, check_remote: bool = True) -> str:
            """[HINT: Working copy health. Agent status, uncommitted changes, sync status.]"""
            result = _check_working_copy_health(agent_name=agent_name, check_remote=check_remote)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def resolve_task_clarification(
            task_id: str, clarification: str, decision: str, move_to_todo: bool = True, dry_run: bool = False
        ) -> str:
            """[HINT: Resolve clarification. Updates task description with decision.]"""
            result = _resolve_task_clarification(
                task_id=task_id,
                clarification=clarification,
                decision=decision,
                move_to_todo=move_to_todo,
                dry_run=dry_run,
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def resolve_multiple_clarifications(decisions: str, move_to_todo: bool = True, dry_run: bool = False) -> str:
            """[HINT: Batch clarification. JSON decisions format: {"T-ID": {"clarification": "...", "decision": "..."}}]"""
            try:
                decisions_dict = json.loads(decisions)
            except json.JSONDecodeError as e:
                return json.dumps({"status": "error", "error": f"Invalid JSON: {str(e)}"}, separators=(",", ":"))

            result = _resolve_multiple_clarifications(
                decisions=decisions_dict, move_to_todo=move_to_todo, dry_run=dry_run
            )
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def list_tasks_awaiting_clarification() -> str:
            """[HINT: Tasks awaiting clarification. Review status tasks with questions.]"""
            result = _list_tasks_awaiting_clarification()
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def setup_git_hooks(hooks: Optional[List[str]] = None, install: bool = True, dry_run: bool = False) -> str:
            """[HINT: Git hooks. pre-commit/push/merge automation, installation status.]"""
            return _setup_git_hooks(hooks, install, dry_run)

        @mcp.tool()
        def setup_pattern_triggers(
            patterns: Optional[str] = None,
            config_path: Optional[str] = None,
            install: bool = True,
            dry_run: bool = False,
        ) -> str:
            """[HINT: Pattern triggers. File/git/task-status automation, integration status.]"""
            parsed_patterns = None
            if patterns:
                try:
                    parsed_patterns = json.loads(patterns)
                except json.JSONDecodeError:
                    return json.dumps(
                        {"status": "error", "error": "Invalid JSON in patterns parameter"}, separators=(",", ":")
                    )

            return _setup_pattern_triggers(parsed_patterns, config_path, install, dry_run)

        @mcp.tool()
        def run_tests(
            test_path: Optional[str] = None,
            test_framework: str = "auto",
            verbose: bool = True,
            coverage: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Test runner. pytest/unittest/ctest, pass/fail counts, coverage.]"""
            return _run_tests(test_path, test_framework, verbose, coverage, output_path)

        @mcp.tool()
        def analyze_test_coverage(
            coverage_file: Optional[str] = None,
            min_coverage: int = 80,
            output_path: Optional[str] = None,
            format: str = "html",
        ) -> str:
            """[HINT: Coverage analysis. Percentage, gaps, threshold status, report path.]"""
            return _analyze_test_coverage(coverage_file, min_coverage, output_path, format)

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

        @mcp.tool()
        def run_sprint_automation(
            max_iterations: int = 10,
            auto_approve: bool = True,
            extract_subtasks: bool = True,
            run_analysis_tools: bool = True,
            run_testing_tools: bool = True,
            priority_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            dry_run: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Sprint automation. Tasks processed, subtasks, blockers, wishlists.]

            Run automated sprint workflow processing tasks.
            """
            return _sprint_automation_impl(
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

        @mcp.tool()
        def sprint_automation(
            max_iterations: int = 10,
            auto_approve: bool = True,
            extract_subtasks: bool = True,
            run_analysis_tools: bool = True,
            run_testing_tools: bool = True,
            priority_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            dry_run: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """[DEPRECATED: Use run_sprint_automation] Alias for backward compatibility."""
            return _sprint_automation_impl(
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

        @mcp.tool()
        def simplify_rules(
            rule_files: Optional[str] = None, dry_run: bool = True, output_dir: Optional[str] = None
        ) -> str:
            """[HINT: Rule simplification. Files processed, changes count, auto-updates.]"""
            parsed_files = None
            if rule_files:
                try:
                    parsed_files = json.loads(rule_files)
                except json.JSONDecodeError:
                    return json.dumps(
                        {"status": "error", "error": "Invalid JSON in rule_files parameter"}, separators=(",", ":")
                    )

            return _simplify_rules(parsed_files, dry_run, output_dir)

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

        @mcp.tool()
        def generate_project_scorecard(
            output_format: str = "text", include_recommendations: bool = True, output_path: Optional[str] = None
        ) -> str:
            """[HINT: Scorecard. Overall score, component scores, production readiness, recommendations.]

            Generate comprehensive project health scorecard with all metrics.
            """
            return _scorecard_impl(output_format, include_recommendations, output_path)

        @mcp.tool()
        def project_scorecard(
            output_format: str = "text", include_recommendations: bool = True, output_path: Optional[str] = None
        ) -> str:
            """[DEPRECATED: Use generate_project_scorecard] Alias for backward compatibility."""
            return _scorecard_impl(output_format, include_recommendations, output_path)

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

        @mcp.tool()
        def generate_project_overview(output_format: str = "text", output_path: Optional[str] = None) -> str:
            """[HINT: Overview. One-page: info, scores, metrics, tasks, risks, roadmap.]

            Generate one-page project overview for stakeholders.
            """
            return _overview_impl(output_format, output_path)

        @mcp.tool()
        def project_overview(output_format: str = "text", output_path: Optional[str] = None) -> str:
            """[DEPRECATED: Use generate_project_overview] Alias for backward compatibility."""
            return _overview_impl(output_format, output_path)

        @mcp.tool()
        def consolidate_tags(
            dry_run: bool = True,
            custom_rules: Optional[str] = None,
            remove_tags: Optional[str] = None,
            output_path: Optional[str] = None,
        ) -> str:
            """[HINT: Tag consolidation. Renames, removals, stats, dry_run preview.]"""
            return _tag_consolidation(dry_run, custom_rules, remove_tags, output_path)

        @mcp.tool()
        def analyze_task_hierarchy(
            output_format: str = "text", output_path: Optional[str] = None, include_recommendations: bool = True
        ) -> str:
            """[HINT: Hierarchy analysis. Component groups, extraction candidates, decision matrix.]"""
            result = _analyze_task_hierarchy(output_format, output_path, include_recommendations)
            if output_format == "json":
                return json.dumps(result, separators=(",", ":"))
            return result.get("formatted_output", json.dumps(result, separators=(",", ":")))

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

        @mcp.tool()
        def get_advisor_briefing(
            overall_score: float = 50.0,
            security_score: float = 50.0,
            testing_score: float = 50.0,
            documentation_score: float = 50.0,
            completion_score: float = 50.0,
            alignment_score: float = 50.0,
        ) -> str:
            """
            [HINT: Daily briefing. Advisor wisdom for lowest-scoring metrics.]

            Get a daily briefing from trusted advisors based on current scores.
            Focuses on the metrics needing the most attention.

            Args:
                overall_score: Overall project score (0-100)
                security_score: Security metric score
                testing_score: Testing metric score
                documentation_score: Documentation metric score
                completion_score: Completion metric score
                alignment_score: Alignment metric score
            """
            from .tools.wisdom.advisors import get_daily_briefing

            metric_scores = {
                "security": security_score,
                "testing": testing_score,
                "documentation": documentation_score,
                "completion": completion_score,
                "alignment": alignment_score,
            }
            briefing = get_daily_briefing(overall_score, metric_scores)
            return briefing

        @mcp.tool()
        def export_advisor_podcast(days: int = 7, output_file: Optional[str] = None) -> str:
            """
            [HINT: Podcast export. Consultation logs formatted for AI video/podcast generation.]

            Export advisor consultation data for AI-generated podcast or video.
            Creates structured narrative data from consultation logs.

            Args:
                days: Days of history to include (default: 7)
                output_file: Optional path to save JSON export
            """
            from .tools.wisdom.advisors import export_for_podcast

            output_path = Path(output_file) if output_file else None
            result = export_for_podcast(days=days, output_path=output_path)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def list_advisors() -> str:
            """
            [HINT: List advisors. All metric/tool/stage advisor assignments with rationale.]

            List all trusted advisor assignments showing which advisor
            is assigned to each metric, tool, and workflow stage.
            """
            from .tools.wisdom.advisors import (
                METRIC_ADVISORS,
                SCORE_CONSULTATION_FREQUENCY,
                STAGE_ADVISORS,
                TOOL_ADVISORS,
            )

            return json.dumps(
                {
                    "metric_advisors": METRIC_ADVISORS,
                    "tool_advisors": TOOL_ADVISORS,
                    "stage_advisors": STAGE_ADVISORS,
                    "consultation_frequency": SCORE_CONSULTATION_FREQUENCY,
                },
                separators=(",", ":"),
            )

        @mcp.tool()
        def check_tts_backends() -> str:
            """
            [HINT: TTS status. Available backends, recommended, installation status.]

            Check which text-to-speech backends are available for voice synthesis.
            """
            from .tools.wisdom.voice import check_tts_backends as _check_backends

            return json.dumps(_check_backends(), separators=(",", ":"))

        @mcp.tool()
        def synthesize_advisor_quote(
            text: str,
            advisor: str = "default",
            output_path: str | None = None,
            backend: str = "auto",
        ) -> str:
            """
            [HINT: Voice synthesis. Generate audio from advisor quote. Backends: elevenlabs/edge-tts/pyttsx3.]

            Synthesize an advisor quote to audio file.

            Args:
                text: The quote text to synthesize
                advisor: Advisor ID (bofh, stoic, zen, mystic, sage, etc.)
                output_path: Output file path (default: auto-generated in .exarp/audio/)
                backend: TTS backend (auto, elevenlabs, edge-tts, pyttsx3)
            """
            from .tools.wisdom.voice import synthesize_advisor_quote as _synthesize

            return json.dumps(_synthesize(text, advisor, output_path, backend), separators=(",", ":"))

        @mcp.tool()
        def generate_podcast_audio(
            days: int = 7,
            output_path: str | None = None,
            backend: str = "auto",
        ) -> str:
            """
            [HINT: Podcast audio. Generate audio from recent advisor consultations.]

            Generate podcast-style audio from recent advisor consultations.

            Args:
                days: Number of days of consultations to include
                output_path: Output file path (default: auto-generated in .exarp/podcasts/)
                backend: TTS backend (auto, elevenlabs, edge-tts, pyttsx3)
            """
            from .tools.wisdom.advisors import get_consultation_log
            from .tools.wisdom.voice import generate_podcast_audio as _generate

            consultations = get_consultation_log(days=days)
            return json.dumps(_generate(consultations, output_path, backend), separators=(",", ":"))

        # ═══════════════════════════════════════════════════════════════════
        # DEPENDABOT INTEGRATION TOOLS
        # ═══════════════════════════════════════════════════════════════════

        @mcp.tool()
        def fetch_dependabot_alerts(
            repo: str = "davidl71/project-management-automation",
            state: str = "open",
        ) -> str:
            """
            [HINT: Dependabot alerts. Fetch GitHub security alerts via API.]

            Fetch Dependabot vulnerability alerts from GitHub.
            Requires: gh CLI installed and authenticated.

            Args:
                repo: GitHub repo in owner/repo format
                state: Alert state (open, fixed, dismissed, all)
            """
            from .tools.dependabot_integration import fetch_dependabot_alerts as _fetch

            return json.dumps(_fetch(repo, state), separators=(",", ":"))

        @mcp.tool()
        def generate_security_report(
            repo: str = "davidl71/project-management-automation",
            include_dismissed: bool = False,
        ) -> str:
            """
            [HINT: Unified security. Combines Dependabot + pip-audit findings.]

            Generate comprehensive security report combining:
            - GitHub Dependabot alerts
            - Local pip-audit scan
            - Comparison and recommendations

            Args:
                repo: GitHub repo in owner/repo format
                include_dismissed: Include dismissed alerts
            """
            from .tools.dependabot_integration import get_unified_security_report

            return json.dumps(get_unified_security_report(repo, include_dismissed), separators=(",", ":"))

        @mcp.tool()
        def unified_security_report(
            repo: str = "davidl71/project-management-automation",
            include_dismissed: bool = False,
        ) -> str:
            """[DEPRECATED: Use generate_security_report] Alias for backward compatibility."""
            from .tools.dependabot_integration import get_unified_security_report

            return json.dumps(get_unified_security_report(repo, include_dismissed), separators=(",", ":"))

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

        @mcp.tool()
        def save_memory(
            title: str,
            content: str,
            category: str = "insight",
            task_id: Optional[str] = None,
        ) -> str:
            """
            [HINT: Save memory. Persist AI discoveries for session continuity.]

            Save a session insight/discovery to persistent memory.

            Categories:
            - debug: Error solutions, workarounds, root causes
            - research: Pre-implementation findings, approach comparisons
            - architecture: Component relationships, hidden dependencies
            - preference: User coding style, workflow preferences
            - insight: Sprint patterns, blockers, optimizations

            Args:
                title: Short descriptive title (max 100 chars)
                content: Full insight content (detailed description)
                category: One of: debug, research, architecture, preference, insight
                task_id: Optional task ID to link this memory to
            """
            result = save_session_insight(title, content, category, task_id)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def recall_context(task_id: str, include_related: bool = True) -> str:
            """
            [HINT: Recall context. Get memories related to a task before starting work.]

            Recall all memories related to a task.

            Use this before starting work on a task to:
            - See what was previously discovered
            - Review past approaches tried
            - Understand decisions already made
            - Find related debug solutions

            Args:
                task_id: Task ID to get context for
                include_related: Whether to include memories from related tasks
            """
            result = recall_task_context(task_id, include_related)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def search_memories(
            query: str,
            category: Optional[str] = None,
            limit: int = 10,
        ) -> str:
            """
            [HINT: Search memories. Find past insights by text search.]

            Search past session memories.

            Use this to find:
            - Similar problems and their solutions
            - Past research on a topic
            - Previous decisions about similar features

            Args:
                query: Search query text
                category: Optional category filter (debug, research, architecture, preference, insight)
                limit: Maximum results to return
            """
            result = search_session_memories(query, category, limit)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def get_session_summary(
            date: Optional[str] = None,
            include_consultations: bool = True,
        ) -> str:
            """
            [HINT: Session summary. End-of-session learnings and wisdom review.]

            Generate a summary of a session's learnings.

            Use this at end of session to:
            - Review what was learned
            - See all insights captured
            - Get combined wisdom (memories + advisor consultations)

            Args:
                date: Session date in YYYY-MM-DD format (default: today)
                include_consultations: Whether to include advisor consultations
            """
            result = generate_session_summary(date, include_consultations)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def session_summary(
            date: Optional[str] = None,
            include_consultations: bool = True,
        ) -> str:
            """[DEPRECATED: Use get_session_summary] Alias for backward compatibility."""
            result = generate_session_summary(date, include_consultations)
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def get_sprint_memories() -> str:
            """
            [HINT: Sprint memories. Recent insights for sprint planning/review.]

            Get memories useful for sprint planning/review.

            Returns recent insights, debug solutions, and patterns
            that could inform sprint decisions.
            """
            result = get_memories_for_sprint()
            return json.dumps(result, separators=(",", ":"))

        @mcp.tool()
        def sprint_memories() -> str:
            """[DEPRECATED: Use get_sprint_memories] Alias for backward compatibility."""
            result = get_memories_for_sprint()
            return json.dumps(result, separators=(",", ":"))

        logger.info("Memory tools loaded successfully")

    # Register prompts
    try:
        # Try relative imports first (when run as module)
        try:
            from .prompts import (
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                AUTOMATION_SETUP,
                # New workflow prompts
                DAILY_CHECKIN,
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                DUPLICATE_TASK_CLEANUP,
                POST_IMPLEMENTATION_REVIEW,
                PRE_SPRINT_CLEANUP,
                PROJECT_HEALTH,
                PROJECT_OVERVIEW,
                PROJECT_SCORECARD,
                PWA_REVIEW,
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                SPRINT_END,
                SPRINT_START,
                TASK_ALIGNMENT_ANALYSIS,
                TASK_REVIEW,
                TASK_SYNC,
                WEEKLY_MAINTENANCE,
            )
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from prompts import (
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                AUTOMATION_SETUP,
                # New workflow prompts
                DAILY_CHECKIN,
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                DUPLICATE_TASK_CLEANUP,
                POST_IMPLEMENTATION_REVIEW,
                PRE_SPRINT_CLEANUP,
                PROJECT_HEALTH,
                PROJECT_OVERVIEW,
                PROJECT_SCORECARD,
                PWA_REVIEW,
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                SPRINT_END,
                SPRINT_START,
                TASK_ALIGNMENT_ANALYSIS,
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
        def pwa() -> str:
            """Review PWA configuration and generate improvement recommendations."""
            return PWA_REVIEW

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

        PROMPTS_AVAILABLE = True
        logger.info("Registered 22 prompts successfully")
    except ImportError as e:
        PROMPTS_AVAILABLE = False
        logger.warning(f"Prompts not available: {e}")

    # Resource handlers (Phase 3)
    try:
        # Try relative imports first (when run as module)
        try:
            from .resources.cache import get_cache_status_resource
            from .resources.history import get_history_resource
            from .resources.list import get_tools_list_resource
            from .resources.memories import (
                get_memories_by_category_resource,
                get_memories_by_task_resource,
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
            from resources.history import get_history_resource
            from resources.list import get_tools_list_resource
            from resources.status import get_status_resource
            from resources.tasks import get_agent_tasks_resource, get_agents_resource, get_tasks_resource

            try:
                from resources.memories import (
                    get_memories_by_category_resource,
                    get_memories_by_task_resource,
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
        _print_banner()
        mcp.run(show_banner=False)
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
        async def list_resources() -> List[str]:
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
