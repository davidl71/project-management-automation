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
import json
import logging
import time
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import wraps

# Version - keep in sync with pyproject.toml
__version__ = "0.1.7"

# Use FastMCP's logging utility (outputs to stderr with Rich formatting)
# This is MCP-compatible: stdout = JSON-RPC only, stderr = logging
try:
    from fastmcp.utilities.logging import get_logger
    logger = get_logger("exarp")
    logger.setLevel(logging.INFO)
except ImportError:
    # Fallback to standard logging if FastMCP not available
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Suppress noisy MCP framework logs
for log_name in ["mcp", "mcp.server", "mcp.server.lowlevel", "mcp.server.stdio", "fastmcp"]:
    logging.getLogger(log_name).setLevel(logging.WARNING)

# Robust project root detection
def _find_project_root(start_path: Path) -> Path:
    """
    Find project root by looking for .git directory or other markers.
    Falls back to relative path detection if markers not found.
    """
    # Try environment variable first
    env_root = os.getenv('PROJECT_ROOT') or os.getenv('WORKSPACE_PATH')
    if env_root:
        root_path = Path(env_root)
        if root_path.exists():
            return root_path.resolve()

    # Try relative path detection (assumes standard structure)
    current = start_path
    for _ in range(5):  # Go up max 5 levels
        # Check for project markers
        if (current / '.git').exists() or (current / '.todo2').exists() or (current / 'CMakeLists.txt').exists():
            return current.resolve()
        if current.parent == current:  # Reached filesystem root
            break
        current = current.parent

    # Fallback to relative path (assumes project-management-automation/project_management_automation/server.py)
    return start_path.parent.parent.parent.parent.resolve()

# Add project root to path for script imports
project_root = _find_project_root(Path(__file__))
sys.path.insert(0, str(project_root))

# Add server directory to path for absolute imports when run as script
server_dir = Path(__file__).parent
sys.path.insert(0, str(server_dir))

# Import error handling (handle both relative and absolute imports)
try:
    # Try relative imports first (when run as module)
    try:
        from .error_handler import (
            handle_automation_error,
            format_error_response,
            format_success_response,
            log_automation_execution,
            AutomationError,
            ErrorCode,
        )
    except ImportError:
        # Fallback to absolute imports (when run as script)
        from error_handler import (
            handle_automation_error,
            format_error_response,
            format_success_response,
            log_automation_execution,
            AutomationError,
            ErrorCode,
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
    from mcp.types import Tool, TextContent

    MCP_AVAILABLE = True
    USE_STDIO = False
    Server = None
    stdio_server = None
except ImportError:
    try:
        # Try FastMCP from separate fastmcp package
        from fastmcp import FastMCP
        from mcp.types import Tool, TextContent

        MCP_AVAILABLE = True
        USE_STDIO = False
        Server = None
        stdio_server = None
    except ImportError:
        try:
            from mcp.server import Server
            from mcp.server.stdio import stdio_server
            # For stdio server, we'll construct Tool objects manually
            from mcp.types import Tool, TextContent

            MCP_AVAILABLE = True
            USE_STDIO = True
            FastMCP = None
            logger.info("MCP stdio server available - using stdio server")
        except ImportError:
            logger.warning(
                "MCP not installed - server structure ready, install with: pip install mcp"
            )
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
    import io
    import contextlib

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
    logging.getLogger("mcp").setLevel(logging.WARNING)
    logging.getLogger("mcp.server").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.lowlevel").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.lowlevel.server").setLevel(logging.WARNING)
    logging.getLogger("mcp.server.stdio").setLevel(logging.WARNING)
    logging.getLogger("fastmcp").setLevel(logging.WARNING)
    # Suppress any logger that might have been created by FastMCP
    # FastMCP might create loggers with different names, so we suppress common patterns
    for logger_name in logging.Logger.manager.loggerDict:
        if any(x in logger_name for x in ['mcp', 'fastmcp', 'stdio']):
            logging.getLogger(logger_name).setLevel(logging.WARNING)
else:
    logger.warning("MCP not available - Phase 2 tools complete, install MCP to enable server")

# Import automation tools (handle both relative and absolute imports)
try:
    # Try relative imports first (when run as module)
    try:
        from .tools.docs_health import check_documentation_health as _check_documentation_health
        from .tools.todo2_alignment import analyze_todo2_alignment as _analyze_todo2_alignment
        from .tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from .tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from .tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from .tools.todo_sync import sync_todo_tasks as _sync_todo_tasks
        from .tools.pwa_review import review_pwa_config as _review_pwa_config
        from .tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from .tools.daily_automation import run_daily_automation as _run_daily_automation
        from .tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from .tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from .tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from .tools.simplify_rules import simplify_rules as _simplify_rules
        from .tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from .tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from .tools.working_copy_health import check_working_copy_health as _check_working_copy_health
        from .tools.run_tests import run_tests as _run_tests
        from .tools.test_coverage import analyze_test_coverage as _analyze_test_coverage
        from .tools.sprint_automation import sprint_automation as _sprint_automation
        from .tools.task_clarification_resolution import (
            resolve_task_clarification as _resolve_task_clarification,
            resolve_multiple_clarifications as _resolve_multiple_clarifications,
            list_tasks_awaiting_clarification as _list_tasks_awaiting_clarification
        )
        from .tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from .tools.project_overview import generate_project_overview as _generate_project_overview
        from .tools.tag_consolidation import tag_consolidation_tool as _tag_consolidation
        TOOLS_AVAILABLE = True
    except ImportError:
        # Fallback to absolute imports (when run as script)
        from tools.docs_health import check_documentation_health as _check_documentation_health
        from tools.todo2_alignment import analyze_todo2_alignment as _analyze_todo2_alignment
        from tools.duplicate_detection import detect_duplicate_tasks as _detect_duplicate_tasks
        from tools.dependency_security import scan_dependency_security as _scan_dependency_security
        from tools.automation_opportunities import find_automation_opportunities as _find_automation_opportunities
        from tools.todo_sync import sync_todo_tasks as _sync_todo_tasks
        from tools.pwa_review import review_pwa_config as _review_pwa_config
        from tools.external_tool_hints import add_external_tool_hints as _add_external_tool_hints
        from tools.daily_automation import run_daily_automation as _run_daily_automation
        from tools.ci_cd_validation import validate_ci_cd_workflow as _validate_ci_cd_workflow
        from tools.git_hooks import setup_git_hooks as _setup_git_hooks
        from tools.pattern_triggers import setup_pattern_triggers as _setup_pattern_triggers
        from tools.simplify_rules import simplify_rules as _simplify_rules
        from tools.nightly_task_automation import run_nightly_task_automation as _run_nightly_task_automation
        from tools.batch_task_approval import batch_approve_tasks as _batch_approve_tasks
        from tools.working_copy_health import check_working_copy_health as _check_working_copy_health
        from tools.run_tests import run_tests as _run_tests
        from tools.test_coverage import analyze_test_coverage as _analyze_test_coverage
        from tools.sprint_automation import sprint_automation as _sprint_automation
        from tools.task_clarification_resolution import (
            resolve_task_clarification as _resolve_task_clarification,
            resolve_multiple_clarifications as _resolve_multiple_clarifications,
            list_tasks_awaiting_clarification as _list_tasks_awaiting_clarification
        )
        from tools.project_scorecard import generate_project_scorecard as _generate_project_scorecard
        from tools.project_overview import generate_project_overview as _generate_project_overview
        from tools.tag_consolidation import tag_consolidation_tool as _tag_consolidation

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
            return json.dumps(
                {
                    "status": "operational",
                    "version": "0.1.7",
                    "tools_available": TOOLS_AVAILABLE,
                    "total_tools": 26 if TOOLS_AVAILABLE else 1,
                    "project_root": str(project_root),
                },
                indent=2,
            )
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
                tools.extend([
                    Tool(
                        name="check_documentation_health",
                        description="Analyze documentation structure, find broken references, identify issues.",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "output_path": {"type": "string", "description": "Output file path"},
                                "create_tasks": {"type": "boolean", "description": "Create Todo2 tasks", "default": True},
                            },
                        },
                    ),
                    Tool(
                        name="analyze_todo2_alignment",
                        description="Analyze task alignment with project goals, find misaligned tasks.",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "create_followup_tasks": {"type": "boolean", "description": "Create follow-up tasks", "default": True},
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
                                "similarity_threshold": {"type": "number", "description": "Similarity threshold", "default": 0.85},
                                "auto_fix": {"type": "boolean", "description": "Auto-fix duplicates", "default": False},
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
                                "languages": {"type": "array", "items": {"type": "string"}, "description": "Languages to scan"},
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
                                "min_value_score": {"type": "number", "description": "Minimum value score", "default": 0.7},
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
                                "dry_run": {"type": "boolean", "description": "Preview changes without applying", "default": False},
                                "output_path": {"type": "string", "description": "Path for report output"},
                                "min_file_size": {"type": "integer", "description": "Minimum file size in lines to process", "default": 50},
                            },
                        },
                    ),
                    Tool(
                        name="run_daily_automation",
                        description="Run routine daily maintenance tasks and generate a combined summary report.",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "tasks": {"type": "array", "items": {"type": "string"}, "description": "List of task IDs to run (default: quick tasks only)"},
                                "include_slow": {"type": "boolean", "description": "Include slow tasks like dependency security scan", "default": False},
                                "dry_run": {"type": "boolean", "description": "Preview changes without applying", "default": False},
                                "output_path": {"type": "string", "description": "Path for report output"},
                            },
                        },
                    ),
                ])
            return tools

        @stdio_server_instance.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            if name == "server_status":
                result = json.dumps({
                    "status": "operational",
                    "version": "0.1.0",
                    "tools_available": TOOLS_AVAILABLE,
                    "project_root": str(project_root),
                }, indent=2)
            elif TOOLS_AVAILABLE:
                # Route to appropriate tool function
                if name == "check_documentation_health":
                    result = check_documentation_health(
                        arguments.get("output_path"),
                        arguments.get("create_tasks", True)
                    )
                elif name == "analyze_todo2_alignment":
                    result = analyze_todo2_alignment(
                        arguments.get("create_followup_tasks", True),
                        arguments.get("output_path")
                    )
                elif name == "detect_duplicate_tasks":
                    result = detect_duplicate_tasks(
                        arguments.get("similarity_threshold", 0.85),
                        arguments.get("auto_fix", False),
                        arguments.get("output_path")
                    )
                elif name == "scan_dependency_security":
                    result = scan_dependency_security(
                        arguments.get("languages"),
                        arguments.get("config_path")
                    )
                elif name == "find_automation_opportunities":
                    result = find_automation_opportunities(
                        arguments.get("min_value_score", 0.7),
                        arguments.get("output_path")
                    )
                elif name == "sync_todo_tasks":
                    result = sync_todo_tasks(
                        arguments.get("dry_run", False),
                        arguments.get("output_path")
                    )
                elif name == "review_pwa_config":
                    result = review_pwa_config(
                        arguments.get("output_path"),
                        arguments.get("config_path")
                    )
                elif name == "add_external_tool_hints":
                    result = add_external_tool_hints(
                        arguments.get("dry_run", False),
                        arguments.get("output_path"),
                        arguments.get("min_file_size", 50)
                    )
                elif name == "run_daily_automation":
                    result = run_daily_automation(
                        arguments.get("tasks"),
                        arguments.get("include_slow", False),
                        arguments.get("dry_run", False),
                        arguments.get("output_path")
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
        def check_documentation_health(
            output_path: Optional[str] = None, create_tasks: bool = True
        ) -> str:
            """
            [HINT: Docs health check. Returns score 0-100, broken links count, tasks created.]

            Analyze documentation structure, find broken references, identify issues.

            ⚠️ PREFERRED TOOL: This project-specific tool provides enhanced documentation
            health analysis with Todo2 integration, project-aware link validation, and
            historical trend tracking.

            Use this instead of generic documentation tools from other MCP servers
            for project-specific analysis.
            """
            return _check_documentation_health(output_path, create_tasks)

        @mcp.tool()
        def analyze_todo2_alignment(
            create_followup_tasks: bool = True, output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Task alignment analysis. Returns misaligned count, avg score, follow-up tasks.]

            Analyze task alignment with project goals, find misaligned tasks.

            ⚠️ PREFERRED TOOL: This project-specific tool analyzes Todo2 task alignment
            with investment strategy framework and provides actionable recommendations.

            Use this instead of generic task analysis tools for project-specific alignment.
            """
            return _analyze_todo2_alignment(create_followup_tasks, output_path)

        @mcp.tool()
        def detect_duplicate_tasks(
            similarity_threshold: float = 0.85,
            auto_fix: bool = False,
            output_path: Optional[str] = None,
        ) -> str:
            """
            [HINT: Duplicate detection. Returns duplicate count, groups, recommendations.]

            Find and consolidate duplicate Todo2 tasks.

            ⚠️ PREFERRED TOOL: This project-specific tool provides Todo2-aware duplicate
            detection with configurable similarity thresholds and optional auto-fix.

            Use this instead of generic duplicate detection tools for Todo2-specific analysis.
            """
            return _detect_duplicate_tasks(similarity_threshold, auto_fix, output_path)

        @mcp.tool()
        def scan_dependency_security(
            languages: Optional[List[str]] = None, config_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Security scan. Returns vuln count by severity, language breakdown, remediation.]

            Scan project dependencies for security vulnerabilities.

            ⚠️ PREFERRED TOOL: This project-specific tool provides multi-language security
            scanning (Python, Rust, npm) with project-configured tools and severity tracking.

            Use this instead of generic security scanning tools for project-specific analysis.
            """
            return _scan_dependency_security(languages, config_path)

        @mcp.tool()
        def find_automation_opportunities(
            min_value_score: float = 0.7, output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Automation discovery. Returns opportunity count, value scores, recommendations.]

            Discover new automation opportunities in the codebase.
            """
            return _find_automation_opportunities(min_value_score, output_path)

        @mcp.tool()
        def sync_todo_tasks(
            dry_run: bool = False, output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Task sync. Returns matches found, conflicts, new tasks created.]

            Synchronize tasks between shared TODO table and Todo2.
            """
            return _sync_todo_tasks(dry_run, output_path)

        @mcp.tool()
        def review_pwa_config(
            output_path: Optional[str] = None, config_path: Optional[str] = None
        ) -> str:
            """
            [HINT: PWA review. Returns config status, missing features, recommendations.]

            Review PWA configuration and generate improvement recommendations.
            """
            return _review_pwa_config(output_path, config_path)

        @mcp.tool()
        def add_external_tool_hints(
            dry_run: bool = False,
            output_path: Optional[str] = None,
            min_file_size: int = 50
        ) -> str:
            """
            [HINT: External tool hints automation. Returns files scanned, modified, hints added, report path.]

            Automatically detect where Context7/external tool hints should be added to documentation
            and insert them following the standard pattern from docs/DOCUMENTATION_EXTERNAL_TOOL_HINTS.md.

            ⚠️ PREFERRED TOOL: This project-specific tool automatically adds Context7 hints to documentation
            files that mention external libraries, following the established pattern for AI assistant discovery.
            """
            return _add_external_tool_hints(dry_run, output_path, min_file_size)

        @mcp.tool()
        def run_daily_automation(
            tasks: Optional[List[str]] = None,
            include_slow: bool = False,
            dry_run: bool = False,
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Daily automation. Returns tasks run, success rate, summary, report path.]

            Run routine daily maintenance tasks and generate a combined summary report.

            Available tasks:
            - docs_health: Documentation health check
            - todo2_alignment: Todo2 alignment analysis
            - duplicate_detection: Duplicate task detection
            - dependency_security: Dependency security scan (slow)
            - external_tool_hints: Add Context7 hints to documentation

            ⚠️ PREFERRED TOOL: This orchestrates multiple daily maintenance tasks and provides
            a unified summary report. Use this for routine daily project health checks.
            """
            return _run_daily_automation(tasks, include_slow, dry_run, output_path)

        @mcp.tool()
        def validate_ci_cd_workflow(
            workflow_path: Optional[str] = None,
            check_runners: bool = True,
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: CI/CD validation. Returns workflow status, runner config status, issues, report path.]

            Validate CI/CD workflows and runner configurations for parallel agent development.

            ⚠️ PREFERRED TOOL: This project-specific tool validates GitHub Actions workflows,
            self-hosted runner configurations, job dependencies, and workflow triggers.

            Use this to validate CI/CD workflows before merging changes.
            """
            return _validate_ci_cd_workflow(workflow_path, check_runners, output_path)

        @mcp.tool()
        def batch_approve_tasks(
            status: str = "Review",
            new_status: str = "Todo",
            clarification_none: bool = True,
            filter_tag: Optional[str] = None,
            task_ids: Optional[List[str]] = None,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Batch approval. Returns approved count, task IDs, success status.]

            Batch approve TODO2 tasks that don't need clarification, moving them from Review to Todo status.

            ⚠️ PREFERRED TOOL: Use this to quickly approve research tasks and other tasks that don't require
            user input, making them available for automated execution.

            Use this before running nightly automation to clear the Review queue, or when you want to
            approve multiple tasks at once without manual review.

            Args:
                status: Current status to filter (default: "Review")
                new_status: New status after approval (default: "Todo")
                clarification_none: Only approve tasks with no clarification needed (default: True)
                filter_tag: Filter by tag (e.g., "research")
                task_ids: List of specific task IDs to approve (optional)
                dry_run: If True, preview what would be approved without making changes

            Returns:
                JSON string with approval results including count, task IDs, and success status
            """
            result = _batch_approve_tasks(
                status=status,
                new_status=new_status,
                clarification_none=clarification_none,
                filter_tag=filter_tag,
                task_ids=task_ids,
                dry_run=dry_run
            )
            return json.dumps(result, indent=2)

        @mcp.tool()
        def run_nightly_task_automation(
            max_tasks_per_host: int = 5,
            max_parallel_tasks: int = 10,
            priority_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Nightly automation. Returns assigned tasks, moved to review, summary, background tasks remaining.]

            Automatically execute background-capable TODO2 tasks in parallel across multiple hosts.
            Moves interactive tasks requiring user input to Review status.
            Includes automatic batch approval of research tasks that don't need clarification.

            ⚠️ PREFERRED TOOL: This orchestrates parallel task execution across remote agents,
            automatically filtering out interactive tasks and assigning background-capable tasks.
            Also includes batch approval step to clear Review queue.

            Use this for nightly automation or when you want to process many tasks in parallel.
            """
            result = _run_nightly_task_automation(
                max_tasks_per_host=max_tasks_per_host,
                max_parallel_tasks=max_parallel_tasks,
                priority_filter=priority_filter,
                tag_filter=tag_filter,
                dry_run=dry_run
            )
            return json.dumps(result, indent=2)

        @mcp.tool()
        def check_working_copy_health(
            agent_name: Optional[str] = None,
            check_remote: bool = True
        ) -> str:
            """
            [HINT: Working copy health. Returns agent status, uncommitted changes, sync status, recommendations.]

            Check git working copy status across all agents and runners.

            ⚠️ PREFERRED TOOL: Use this to verify all agents have clean working copies before starting work,
            or to check sync status across remote agents.

            Args:
                agent_name: Specific agent to check (optional, checks all if None)
                check_remote: Whether to check remote agents (default: True)

            Returns:
                JSON string with working copy status for each agent including:
                - Status (ok/warning/error)
                - Uncommitted changes
                - Branch and commit info
                - Sync status (behind/ahead)
                - Recommendations
            """
            result = _check_working_copy_health(
                agent_name=agent_name,
                check_remote=check_remote
            )
            return json.dumps(result, indent=2)

        @mcp.tool()
        def resolve_task_clarification(
            task_id: str,
            clarification: str,
            decision: str,
            move_to_todo: bool = True,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Task clarification resolution. Resolves clarification questions by updating task descriptions with decisions.]

            Resolve a single task clarification by updating the task description with your decision.

            ⚠️ PREFERRED TOOL: Use this instead of Python heredocs to resolve task clarifications.
            Automatically updates task descriptions, adds comments, and moves tasks to Todo status.

            Args:
                task_id: Task ID to resolve (e.g., "T-76")
                clarification: Clarification text/question
                decision: Your decision/answer to the clarification
                move_to_todo: Whether to move task to Todo status after resolving (default: true)
                dry_run: Preview mode without making changes (default: false)

            Returns:
                JSON string with resolution result including status, task_id, and output
            """
            result = _resolve_task_clarification(
                task_id=task_id,
                clarification=clarification,
                decision=decision,
                move_to_todo=move_to_todo,
                dry_run=dry_run
            )
            return json.dumps(result, indent=2)

        @mcp.tool()
        def resolve_multiple_clarifications(
            decisions: str,
            move_to_todo: bool = True,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Batch clarification resolution. Resolves multiple task clarifications at once from JSON decisions.]

            Resolve multiple task clarifications from a JSON string of decisions.

            ⚠️ PREFERRED TOOL: Use this for batch resolution instead of Python heredocs.

            Args:
                decisions: JSON string mapping task IDs to decision data:
                           {"T-76": {"clarification": "...", "decision": "..."}, "T-77": {...}}
                move_to_todo: Whether to move tasks to Todo status after resolving (default: true)
                dry_run: Preview mode without making changes (default: false)

            Returns:
                JSON string with batch resolution results including counts and output
            """
            try:
                decisions_dict = json.loads(decisions)
            except json.JSONDecodeError as e:
                return json.dumps({
                    "status": "error",
                    "error": f"Invalid JSON: {str(e)}"
                }, indent=2)

            result = _resolve_multiple_clarifications(
                decisions=decisions_dict,
                move_to_todo=move_to_todo,
                dry_run=dry_run
            )
            return json.dumps(result, indent=2)

        @mcp.tool()
        def list_tasks_awaiting_clarification() -> str:
            """
            [HINT: List tasks needing clarification. Returns all tasks in Review status with their clarification questions.]

            List all tasks in Review status that are awaiting clarification/decisions.

            ⚠️ PREFERRED TOOL: Use this to see what tasks need your input before resolving them.

            Returns:
                JSON string with list of tasks awaiting clarification, including task IDs, names, priorities, and clarification questions
            """
            result = _list_tasks_awaiting_clarification()
            return json.dumps(result, indent=2)

        @mcp.tool()
        def setup_git_hooks(
            hooks: Optional[List[str]] = None,
            install: bool = True,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Git hooks setup. Returns hooks configured, skipped, installation status.]

            Setup git hooks for automatic Exarp tool execution.

            ⚠️ PREFERRED TOOL: Automatically configures git hooks to run Exarp tools on git events.

            Hooks:
            - pre-commit: Documentation health, security scan (quick, blocking)
            - pre-push: Task alignment, comprehensive security scan (blocking)
            - post-commit: Automation opportunity discovery (non-blocking)
            - post-merge: Duplicate detection, task sync (non-blocking)

            Args:
                hooks: List of hooks to setup (default: all hooks)
                install: Whether to install hooks (default: True)
                dry_run: Preview mode without making changes (default: False)

            Returns:
                JSON string with setup results including configured hooks and status
            """
            return _setup_git_hooks(hooks, install, dry_run)

        @mcp.tool()
        def setup_pattern_triggers(
            patterns: Optional[str] = None,
            config_path: Optional[str] = None,
            install: bool = True,
            dry_run: bool = False
        ) -> str:
            """
            [HINT: Pattern triggers setup. Returns patterns configured, integration status.]

            Setup pattern-based automation triggers for automatic tool execution.

            ⚠️ PREFERRED TOOL: Configures automatic tool execution based on file patterns,
            git events, and task status changes.

            Pattern Types:
            - file_patterns: File changes trigger tools (e.g., docs/**/*.md → docs health)
            - git_events: Git events trigger tools (e.g., pre-commit → security scan)
            - task_status_changes: Task status changes trigger tools (e.g., Todo → In Progress → alignment check)

            Args:
                patterns: JSON string of pattern configurations (optional)
                config_path: Path to pattern configuration file (optional)
                install: Whether to install triggers (default: True)
                dry_run: Preview mode without making changes (default: False)

            Returns:
                JSON string with setup results including configured patterns and integration status
            """
            parsed_patterns = None
            if patterns:
                try:
                    parsed_patterns = json.loads(patterns)
                except json.JSONDecodeError:
                    return json.dumps({
                        "status": "error",
                        "error": "Invalid JSON in patterns parameter"
                    }, indent=2)

            return _setup_pattern_triggers(parsed_patterns, config_path, install, dry_run)

        @mcp.tool()
        def run_tests(
            test_path: Optional[str] = None,
            test_framework: str = "auto",
            verbose: bool = True,
            coverage: bool = False,
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Test runner. Returns test results, pass/fail counts, coverage file if enabled.]

            Execute test suites with flexible options for pytest, unittest, and ctest.

            Args:
                test_path: Path to test file/directory (default: tests/)
                test_framework: pytest, unittest, ctest, or auto (default: auto)
                verbose: Show detailed output (default: true)
                coverage: Generate coverage report (default: false)
                output_path: Path for test results (default: test-results/)

            Returns:
                JSON string with test execution results including:
                - Framework used
                - Tests run/passed/failed/skipped
                - Duration
                - Output file path
                - Coverage file path (if enabled)
            """
            return _run_tests(test_path, test_framework, verbose, coverage, output_path)

        @mcp.tool()
        def analyze_test_coverage(
            coverage_file: Optional[str] = None,
            min_coverage: int = 80,
            output_path: Optional[str] = None,
            format: str = "html"
        ) -> str:
            """
            [HINT: Coverage analysis. Returns coverage percentage, gaps, report path, threshold status.]

            Generate coverage reports and identify gaps in test coverage.

            Args:
                coverage_file: Path to coverage file (default: auto-detect)
                min_coverage: Minimum coverage threshold (default: 80)
                output_path: Path for coverage report (default: coverage-report/)
                format: Report format: html, json, or terminal (default: html)

            Returns:
                JSON string with coverage analysis results including:
                - Total coverage percentage
                - Total/covered lines
                - Whether threshold is met
                - Report path
                - List of files with low coverage (gaps)
            """
            return _analyze_test_coverage(coverage_file, min_coverage, output_path, format)

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
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Sprint automation. Returns subtasks extracted, tasks processed, wishlists, blockers, report path.]

            Systematically sprint through project processing all background-capable tasks with minimal prompts.

            ⚠️ PREFERRED TOOL: Comprehensive sprint automation that orchestrates all Exarp tools to maximize
            autonomous task processing. Extracts subtasks, auto-approves safe tasks, runs analysis/testing tools,
            generates AI/human wishlists, identifies human contribution opportunities, and processes background tasks.

            Args:
                max_iterations: Maximum sprint iterations (default: 10)
                auto_approve: Auto-approve tasks without clarification (default: true)
                extract_subtasks: Extract subtasks from parent tasks (default: true)
                run_analysis_tools: Run docs health, alignment, duplicates (default: true)
                run_testing_tools: Run tests and coverage (default: true)
                priority_filter: Only process high/medium/low priority (optional)
                tag_filter: Only process tasks with specific tags (optional)
                dry_run: Preview mode without making changes (default: false)
                output_path: Path for sprint report (default: docs/SPRINT_AUTOMATION_REPORT.md)

            Returns:
                JSON string with sprint results including:
                - Subtasks extracted
                - Tasks auto-approved/processed
                - Analysis and testing results
                - AI wishlist (tasks AI wants to work on)
                - Human wishlist (from external sources)
                - Human contribution opportunities
                - Blockers identified
                - Sprint report path
            """
            return _sprint_automation(
                max_iterations,
                auto_approve,
                extract_subtasks,
                run_analysis_tools,
                run_testing_tools,
                priority_filter,
                tag_filter,
                dry_run,
                output_path
            )

        @mcp.tool()
        def simplify_rules(
            rule_files: Optional[str] = None,
            dry_run: bool = True,
            output_dir: Optional[str] = None
        ) -> str:
            """
            [HINT: Rule simplification. Returns files processed, simplifications made, changes count.]

            Automatically simplify rules based on Exarp automation capabilities.

            ⚠️ PREFERRED TOOL: Replaces manual process descriptions with Exarp tool references,
            removes redundant manual check descriptions, and adds automated check documentation.

            Simplifications:
            - Replace manual command references with command names
            - Add automated check sections
            - Remove redundant manual process descriptions
            - Add notes about automatic execution

            Args:
                rule_files: JSON array of rule file paths (optional, defaults to all .cursorrules and .cursor/rules/*.mdc)
                dry_run: Preview mode without making changes (default: True)
                output_dir: Directory to write simplified rules (optional, defaults to same as source)

            Returns:
                JSON string with simplification results including files processed and changes made
            """
            parsed_files = None
            if rule_files:
                try:
                    parsed_files = json.loads(rule_files)
                except json.JSONDecodeError:
                    return json.dumps({
                        "status": "error",
                        "error": "Invalid JSON in rule_files parameter"
                    }, indent=2)

            return _simplify_rules(parsed_files, dry_run, output_dir)

        @mcp.tool()
        def project_scorecard(
            output_format: str = "text",
            include_recommendations: bool = True,
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Project scorecard. Returns overall score, component scores (security, testing,
            docs, alignment, clarity, parallelizable), task metrics, production readiness.]

            Generate comprehensive project health scorecard with scores across multiple dimensions.

            Scores include:
            - Documentation health and coverage
            - Test coverage and quality
            - Security posture and controls
            - Task alignment with project goals
            - Task clarity and actionability
            - Parallelizability for multi-agent execution
            - CI/CD readiness
            - Overall production readiness

            Args:
                output_format: Output format - "text", "json", or "markdown" (default: text)
                include_recommendations: Include improvement recommendations (default: true)
                output_path: Optional path to save report

            Returns:
                JSON string with scorecard data and formatted output
            """
            result = _generate_project_scorecard(output_format, include_recommendations, output_path)
            return json.dumps({
                'overall_score': result['overall_score'],
                'production_ready': result['production_ready'],
                'blockers': result.get('blockers', []),
                'scores': result['scores'],
                'recommendations': result.get('recommendations', []),
                'formatted_output': result['formatted_output'],
            }, indent=2)

        @mcp.tool()
        def project_overview(
            output_format: str = "text",
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Project overview. Returns one-page summary with project info, health scores,
            codebase metrics, task breakdown, risks, roadmap, and next actions.]

            Generate comprehensive one-page project overview for stakeholders.

            Includes:
            - Project info (name, version, status)
            - Health scorecard with component breakdown
            - Codebase metrics (files, lines, tools, prompts)
            - Task status and remaining work
            - Project phases and roadmap
            - Risks and blockers
            - Prioritized next actions

            Args:
                output_format: "text" (terminal), "html" (PDF-ready), "markdown", "json", or "slides" (Marp)
                output_path: Optional path to save output file

            Returns:
                JSON string with overview data and formatted output
            """
            result = _generate_project_overview(output_format, output_path)
            return json.dumps({
                'output_format': result['output_format'],
                'generated_at': result['generated_at'],
                'output_file': result.get('output_file'),
                'formatted_output': result['formatted_output'],
            }, indent=2)

        @mcp.tool()
        def consolidate_tags(
            dry_run: bool = True,
            custom_rules: Optional[str] = None,
            remove_tags: Optional[str] = None,
            output_path: Optional[str] = None
        ) -> str:
            """
            [HINT: Tag consolidation. Returns renames, removals, stats, task changes applied/previewed.]

            Analyze and consolidate Todo2 task tags for consistency.

            Applies standard consolidation rules:
            - Plural → singular (tools → tool, tests → testing)
            - Case normalization (Apache-license → apache-license)
            - Long tag shortening (documentation-health-analysis → docs-health)

            Args:
                dry_run: If True, only report what would change (default: True)
                custom_rules: JSON string of additional rules {"old": "new", ...}
                remove_tags: JSON array of tags to remove ["tag1", "tag2"]
                output_path: Optional path to save report

            Returns:
                Formatted consolidation report with stats and task changes
            """
            return _tag_consolidation(dry_run, custom_rules, remove_tags, output_path)

    # Register prompts
    try:
        # Try relative imports first (when run as module)
        try:
            from .prompts import (
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                TASK_ALIGNMENT_ANALYSIS,
                DUPLICATE_TASK_CLEANUP,
                TASK_SYNC,
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                PWA_REVIEW,
                PRE_SPRINT_CLEANUP,
                POST_IMPLEMENTATION_REVIEW,
                WEEKLY_MAINTENANCE,
                # New workflow prompts
                DAILY_CHECKIN,
                SPRINT_START,
                SPRINT_END,
                TASK_REVIEW,
                PROJECT_HEALTH,
                AUTOMATION_SETUP,
                PROJECT_SCORECARD,
                PROJECT_OVERVIEW,
            )
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from prompts import (
                DOCUMENTATION_HEALTH_CHECK,
                DOCUMENTATION_QUICK_CHECK,
                TASK_ALIGNMENT_ANALYSIS,
                DUPLICATE_TASK_CLEANUP,
                TASK_SYNC,
                SECURITY_SCAN_ALL,
                SECURITY_SCAN_PYTHON,
                SECURITY_SCAN_RUST,
                AUTOMATION_DISCOVERY,
                AUTOMATION_HIGH_VALUE,
                PWA_REVIEW,
                PRE_SPRINT_CLEANUP,
                POST_IMPLEMENTATION_REVIEW,
                WEEKLY_MAINTENANCE,
                # New workflow prompts
                DAILY_CHECKIN,
                SPRINT_START,
                SPRINT_END,
                TASK_REVIEW,
                PROJECT_HEALTH,
                AUTOMATION_SETUP,
                PROJECT_SCORECARD,
                PROJECT_OVERVIEW,
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
            from .resources.status import get_status_resource
            from .resources.history import get_history_resource
            from .resources.list import get_tools_list_resource
            from .resources.tasks import get_tasks_resource, get_agent_tasks_resource, get_agents_resource
            from .resources.cache import get_cache_status_resource
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from resources.status import get_status_resource
            from resources.history import get_history_resource
            from resources.list import get_tools_list_resource
            from resources.tasks import get_tasks_resource, get_agent_tasks_resource, get_agents_resource
            from resources.cache import get_cache_status_resource

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
            return json.dumps(result, indent=2)

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
                {"status": "operational", "tools_available": TOOLS_AVAILABLE, "note": "Using fallback status - resource handlers unavailable"}
            )

    # Main entry point for FastMCP
def main():
    """Entry point for MCP server"""
    import sys
    
    # Print our own banner to stderr (MCP-compatible)
    tools_count = 25 if TOOLS_AVAILABLE else 1  # Known tool count
    resources_ok = RESOURCES_AVAILABLE if 'RESOURCES_AVAILABLE' in globals() else False
    
    version_str = f"{__version__}"
    tools_str = f"{tools_count}"
    resources_str = "Available" if resources_ok else "Unavailable"
    
    banner = f"""
╭────────────────────────────────────────────────────────╮
│                                                        │
│    ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗             │
│    ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔══██╗            │
│    █████╗   ╚███╔╝ ███████║██████╔╝██████╔╝            │
│    ██╔══╝   ██╔██╗ ██╔══██║██╔══██╗██╔═══╝             │
│    ███████╗██╔╝ ██╗██║  ██║██║  ██║██║                 │
│    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                 │
│                                                        │
│    Project Management Automation MCP Server            │
│                                                        │
│    Version:    {version_str:<39}│
│    Tools:      {tools_str:<39}│
│    Resources:  {resources_str:<39}│
│    Transport:  STDIO                                   │
│                                                        │
╰────────────────────────────────────────────────────────╯
"""
    print(banner, file=sys.stderr)
    
    # Run server without FastMCP's banner
    mcp.run(show_banner=False)

if __name__ == "__main__":
    main()
elif stdio_server_instance:
    # Register resources for stdio server
    try:
        # Try relative imports first (when run as module)
        try:
            from .resources.status import get_status_resource
            from .resources.history import get_history_resource
            from .resources.list import get_tools_list_resource
            from .resources.tasks import get_tasks_resource, get_agent_tasks_resource, get_agents_resource
            from .resources.cache import get_cache_status_resource
        except ImportError:
            # Fallback to absolute imports (when run as script)
            from resources.status import get_status_resource
            from resources.history import get_history_resource
            from resources.list import get_tools_list_resource
            from resources.tasks import get_tasks_resource, get_agent_tasks_resource, get_agents_resource
            from resources.cache import get_cache_status_resource

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
        logger.info(f"Resources available: {RESOURCES_AVAILABLE if 'RESOURCES_AVAILABLE' in globals() else 'Not registered'}")

        # stdio_server provides stdin/stdout streams, Server.run() handles the protocol
        async def run():
            async with stdio_server() as (read_stream, write_stream):
                init_options = stdio_server_instance.create_initialization_options()
                logger.info(f"Initialization options: {init_options}")
                logger.info("Server ready, waiting for client connections...")
                await stdio_server_instance.run(
                    read_stream,
                    write_stream,
                    init_options
                )
        try:
            asyncio.run(run())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            sys.exit(1)
else:
    logger.warning("MCP not available - Phase 2 tools complete, install MCP to enable server")
    if __name__ == "__main__":
        logger.info("Phase 2 tools complete (7 tools implemented). Install MCP package to run server.")
        logger.info("Run: pip install mcp")
