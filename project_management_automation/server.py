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

import json
import logging
import time
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import wraps

# Version - keep in sync with pyproject.toml
__version__ = "0.1.15"

# Import our MCP-aware logging utilities
from .utils.logging_config import configure_logging, suppress_noisy_loggers, is_mcp_mode

# Configure logging (quiet in MCP mode, verbose in CLI)
logger = configure_logging("exarp", level=logging.INFO)
suppress_noisy_loggers()

# Import security utilities
from .utils.security import (
    PathValidator,
    set_default_path_validator,
    get_access_controller,
    AccessController,
    set_access_controller,
)

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

# Initialize security controls
# Path boundary: only allow access within project root and common temp dirs
_path_validator = PathValidator(
    allowed_roots=[project_root, Path("/tmp"), Path("/var/tmp")],
    allow_symlinks=False,
    blocked_patterns=[
        r'\.git(?:/|$)',      # .git directory
        r'\.env',             # Environment files  
        r'\.ssh',             # SSH keys
        r'\.aws',             # AWS credentials
        r'id_rsa',            # SSH private keys
        r'\.pem$',            # Certificate files
        r'secrets?\.ya?ml',   # Secrets files
    ]
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
    suppress_noisy_loggers()
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
        from .tools.task_hierarchy_analyzer import analyze_task_hierarchy as _analyze_task_hierarchy
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
        from tools.task_hierarchy_analyzer import analyze_task_hierarchy as _analyze_task_hierarchy

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
                    "version": __version__,
                    "tools_available": TOOLS_AVAILABLE,
                    "total_tools": 27 if TOOLS_AVAILABLE else 1,
                    "project_root": str(project_root),
                },
                separators=(',', ':'),
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
                }, separators=(',', ':'))
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
            """[HINT: Docs health. Score 0-100, broken links, tasks created.]"""
            return _check_documentation_health(output_path, create_tasks)

        @mcp.tool()
        def analyze_todo2_alignment(
            create_followup_tasks: bool = True, output_path: Optional[str] = None
        ) -> str:
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
        def scan_dependency_security(
            languages: Optional[List[str]] = None, config_path: Optional[str] = None
        ) -> str:
            """[HINT: Security scan. Vulns by severity, language breakdown, remediation.]"""
            return _scan_dependency_security(languages, config_path)

        @mcp.tool()
        def find_automation_opportunities(
            min_value_score: float = 0.7, output_path: Optional[str] = None
        ) -> str:
            """[HINT: Automation discovery. Opportunities, value scores, recommendations.]"""
            return _find_automation_opportunities(min_value_score, output_path)

        @mcp.tool()
        def sync_todo_tasks(
            dry_run: bool = False, output_path: Optional[str] = None
        ) -> str:
            """[HINT: Task sync. Matches found, conflicts, new tasks created.]"""
            return _sync_todo_tasks(dry_run, output_path)

        @mcp.tool()
        def review_pwa_config(
            output_path: Optional[str] = None, config_path: Optional[str] = None
        ) -> str:
            """[HINT: PWA review. Config status, missing features, recommendations.]"""
            return _review_pwa_config(output_path, config_path)

        @mcp.tool()
        def add_external_tool_hints(
            dry_run: bool = False,
            output_path: Optional[str] = None,
            min_file_size: int = 50
        ) -> str:
            """[HINT: Tool hints. Files scanned, modified, hints added.]"""
            return _add_external_tool_hints(dry_run, output_path, min_file_size)

        @mcp.tool()
        def run_daily_automation(
            tasks: Optional[List[str]] = None,
            include_slow: bool = False,
            dry_run: bool = False,
            output_path: Optional[str] = None
        ) -> str:
            """[HINT: Daily automation. Tasks: docs_health, alignment, duplicates, security.]"""
            return _run_daily_automation(tasks, include_slow, dry_run, output_path)

        @mcp.tool()
        def validate_ci_cd_workflow(
            workflow_path: Optional[str] = None,
            check_runners: bool = True,
            output_path: Optional[str] = None
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
            dry_run: bool = False
        ) -> str:
            """[HINT: Batch approval. Approved count, task IDs, success status.]"""
            result = _batch_approve_tasks(
                status=status,
                new_status=new_status,
                clarification_none=clarification_none,
                filter_tag=filter_tag,
                task_ids=task_ids,
                dry_run=dry_run
            )
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def run_nightly_task_automation(
            max_tasks_per_host: int = 5,
            max_parallel_tasks: int = 10,
            priority_filter: Optional[str] = None,
            tag_filter: Optional[List[str]] = None,
            dry_run: bool = False
        ) -> str:
            """[HINT: Nightly automation. Assigned tasks, moved to review, background remaining.]"""
            result = _run_nightly_task_automation(
                max_tasks_per_host=max_tasks_per_host,
                max_parallel_tasks=max_parallel_tasks,
                priority_filter=priority_filter,
                tag_filter=tag_filter,
                dry_run=dry_run
            )
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def check_working_copy_health(
            agent_name: Optional[str] = None,
            check_remote: bool = True
        ) -> str:
            """[HINT: Working copy health. Agent status, uncommitted changes, sync status.]"""
            result = _check_working_copy_health(
                agent_name=agent_name,
                check_remote=check_remote
            )
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def resolve_task_clarification(
            task_id: str,
            clarification: str,
            decision: str,
            move_to_todo: bool = True,
            dry_run: bool = False
        ) -> str:
            """[HINT: Resolve clarification. Updates task description with decision.]"""
            result = _resolve_task_clarification(
                task_id=task_id,
                clarification=clarification,
                decision=decision,
                move_to_todo=move_to_todo,
                dry_run=dry_run
            )
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def resolve_multiple_clarifications(
            decisions: str,
            move_to_todo: bool = True,
            dry_run: bool = False
        ) -> str:
            """[HINT: Batch clarification. JSON decisions format: {"T-ID": {"clarification": "...", "decision": "..."}}]"""
            try:
                decisions_dict = json.loads(decisions)
            except json.JSONDecodeError as e:
                return json.dumps({
                    "status": "error",
                    "error": f"Invalid JSON: {str(e)}"
                }, separators=(',', ':'))

            result = _resolve_multiple_clarifications(
                decisions=decisions_dict,
                move_to_todo=move_to_todo,
                dry_run=dry_run
            )
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def list_tasks_awaiting_clarification() -> str:
            """[HINT: Tasks awaiting clarification. Review status tasks with questions.]"""
            result = _list_tasks_awaiting_clarification()
            return json.dumps(result, separators=(',', ':'))

        @mcp.tool()
        def setup_git_hooks(
            hooks: Optional[List[str]] = None,
            install: bool = True,
            dry_run: bool = False
        ) -> str:
            """[HINT: Git hooks. pre-commit/push/merge automation, installation status.]"""
            return _setup_git_hooks(hooks, install, dry_run)

        @mcp.tool()
        def setup_pattern_triggers(
            patterns: Optional[str] = None,
            config_path: Optional[str] = None,
            install: bool = True,
            dry_run: bool = False
        ) -> str:
            """[HINT: Pattern triggers. File/git/task-status automation, integration status.]"""
            parsed_patterns = None
            if patterns:
                try:
                    parsed_patterns = json.loads(patterns)
                except json.JSONDecodeError:
                    return json.dumps({
                        "status": "error",
                        "error": "Invalid JSON in patterns parameter"
                    }, separators=(',', ':'))

            return _setup_pattern_triggers(parsed_patterns, config_path, install, dry_run)

        @mcp.tool()
        def run_tests(
            test_path: Optional[str] = None,
            test_framework: str = "auto",
            verbose: bool = True,
            coverage: bool = False,
            output_path: Optional[str] = None
        ) -> str:
            """[HINT: Test runner. pytest/unittest/ctest, pass/fail counts, coverage.]"""
            return _run_tests(test_path, test_framework, verbose, coverage, output_path)

        @mcp.tool()
        def analyze_test_coverage(
            coverage_file: Optional[str] = None,
            min_coverage: int = 80,
            output_path: Optional[str] = None,
            format: str = "html"
        ) -> str:
            """[HINT: Coverage analysis. Percentage, gaps, threshold status, report path.]"""
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
            """[HINT: Sprint automation. Tasks processed, subtasks, blockers, wishlists.]"""
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
            """[HINT: Rule simplification. Files processed, changes count, auto-updates.]"""
            parsed_files = None
            if rule_files:
                try:
                    parsed_files = json.loads(rule_files)
                except json.JSONDecodeError:
                    return json.dumps({
                        "status": "error",
                        "error": "Invalid JSON in rule_files parameter"
                    }, separators=(',', ':'))

            return _simplify_rules(parsed_files, dry_run, output_dir)

        @mcp.tool()
        def project_scorecard(
            output_format: str = "text",
            include_recommendations: bool = True,
            output_path: Optional[str] = None
        ) -> str:
            """[HINT: Scorecard. Overall score, component scores, production readiness, recommendations.]"""
            result = _generate_project_scorecard(output_format, include_recommendations, output_path)
            return json.dumps({
                'overall_score': result['overall_score'],
                'production_ready': result['production_ready'],
                'blockers': result.get('blockers', []),
                'scores': result['scores'],
                'recommendations': result.get('recommendations', []),
                'formatted_output': result['formatted_output'],
            }, separators=(',', ':'))

        @mcp.tool()
        def project_overview(
            output_format: str = "text",
            output_path: Optional[str] = None
        ) -> str:
            """[HINT: Overview. One-page: info, scores, metrics, tasks, risks, roadmap.]"""
            result = _generate_project_overview(output_format, output_path)
            return json.dumps({
                'output_format': result['output_format'],
                'generated_at': result['generated_at'],
                'output_file': result.get('output_file'),
                'formatted_output': result['formatted_output'],
            }, separators=(',', ':'))

        @mcp.tool()
        def consolidate_tags(
            dry_run: bool = True,
            custom_rules: Optional[str] = None,
            remove_tags: Optional[str] = None,
            output_path: Optional[str] = None
        ) -> str:
            """[HINT: Tag consolidation. Renames, removals, stats, dry_run preview.]"""
            return _tag_consolidation(dry_run, custom_rules, remove_tags, output_path)

        @mcp.tool()
        def analyze_task_hierarchy(
            output_format: str = "text",
            output_path: Optional[str] = None,
            include_recommendations: bool = True
        ) -> str:
            """[HINT: Hierarchy analysis. Component groups, extraction candidates, decision matrix.]"""
            result = _analyze_task_hierarchy(output_format, output_path, include_recommendations)
            if output_format == "json":
                return json.dumps(result, separators=(',', ':'))
            return result.get("formatted_output", json.dumps(result, separators=(',', ':')))

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
            return json.dumps(result, separators=(',', ':'))

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
    
    # Fixed-width banner (56 chars inner width + 2 for borders = 58 total)
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
    banner = "\n".join(banner_lines)
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
