"""
Consolidated MCP Tools

Combines related tools into unified interfaces with action parameters.
Reduces tool count while maintaining all functionality.

All tools use 'action' as the dispatcher parameter for consistency.

Consolidated tools:
- analyze_alignment(action=todo2|prd) ← analyze_todo2_alignment, analyze_prd_alignment
- security(action=scan|alerts|report) ← scan_dependency_security, fetch_dependabot_alerts, generate_security_report
- generate_config(action=rules|ignore|simplify) ← generate_cursor_rules, generate_cursorignore, simplify_rules
- setup_hooks(action=git|patterns) ← setup_git_hooks, setup_pattern_triggers
- prompt_tracking(action=log|analyze) ← log_prompt_iteration, analyze_prompt_iterations
- health(action=server|git|docs|dod|cicd) ← server_status, check_working_copy_health, check_documentation_health, check_definition_of_done, validate_ci_cd_workflow
- report(action=overview|scorecard|briefing|prd) ← generate_project_overview, generate_project_scorecard, get_advisor_briefing, generate_prd
- advisor_audio(action=quote|podcast|export) ← synthesize_advisor_quote, generate_podcast_audio, export_advisor_podcast
- task_analysis(action=duplicates|tags|hierarchy) ← detect_duplicate_tasks, consolidate_tags, analyze_task_hierarchy
- testing(action=run|coverage) ← run_tests, analyze_test_coverage
- lint(action=run|analyze) ← run_linter, analyze_problems
- memory(action=save|recall|search) ← save_memory, recall_context, search_memories
- task_discovery(action=comments|markdown|orphans|all) ← NEW: find tasks from various sources
- task_workflow(action=sync|approve|clarify, sub_action for clarify) ← sync_todo_tasks, batch_approve_tasks, clarification
"""

import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def analyze_alignment(
    action: str = "todo2",
    create_followup_tasks: bool = True,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Unified alignment analysis tool.
    
    Args:
        action: "todo2" for task alignment, "prd" for PRD persona mapping
        create_followup_tasks: Create tasks for misaligned items (todo2 only)
        output_path: Optional file to save results
    
    Returns:
        Alignment analysis results
    """
    if action == "todo2":
        from .todo2_alignment import analyze_todo2_alignment
        return analyze_todo2_alignment(create_followup_tasks, output_path)
    elif action == "prd":
        from .prd_generator import analyze_prd_alignment
        return analyze_prd_alignment(output_path)
    else:
        return {
            "status": "error",
            "error": f"Unknown alignment action: {action}. Use 'todo2' or 'prd'.",
        }


async def security_async(
    action: str = "report",
    repo: str = "davidl71/project-management-automation",
    languages: Optional[list[str]] = None,
    config_path: Optional[str] = None,
    state: str = "open",
    include_dismissed: bool = False,
    ctx: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Unified security analysis tool (async with progress).
    
    Args:
        action: "scan" for local pip-audit, "alerts" for Dependabot, "report" for combined
        repo: GitHub repo for alerts/report (owner/repo format)
        languages: Languages to scan (scan action)
        config_path: Config file path (scan action)
        state: Alert state filter (alerts action)
        include_dismissed: Include dismissed alerts (report action)
        ctx: FastMCP Context for progress reporting (optional)
    
    Returns:
        Security scan/report results
    """
    if action == "scan":
        from .dependency_security import scan_dependency_security_async
        result = await scan_dependency_security_async(languages, config_path, ctx)
        return json.loads(result) if isinstance(result, str) else result
    elif action == "alerts":
        from .dependabot_integration import fetch_dependabot_alerts
        return fetch_dependabot_alerts(repo, state)
    elif action == "report":
        from .dependabot_integration import get_unified_security_report
        return get_unified_security_report(repo, include_dismissed)
    else:
        return {
            "status": "error",
            "error": f"Unknown security action: {action}. Use 'scan', 'alerts', or 'report'.",
        }


def security(
    action: str = "report",
    repo: str = "davidl71/project-management-automation",
    languages: Optional[list[str]] = None,
    config_path: Optional[str] = None,
    state: str = "open",
    include_dismissed: bool = False,
    ctx: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Unified security analysis tool (sync wrapper).
    
    Args:
        action: "scan" for local pip-audit, "alerts" for Dependabot, "report" for combined
        repo: GitHub repo for alerts/report (owner/repo format)
        languages: Languages to scan (scan action)
        config_path: Config file path (scan action)
        state: Alert state filter (alerts action)
        include_dismissed: Include dismissed alerts (report action)
        ctx: FastMCP Context for progress reporting (optional)
    
    Returns:
        Security scan/report results
    """
    import asyncio
    try:
        # Check if we're in an async context
        asyncio.get_running_loop()
        # In async context - caller must await this or use security_async directly
        # For sync callers, fall through to RuntimeError path
        raise RuntimeError("Use security_async() in async context")
    except RuntimeError:
        # No running loop - run synchronously
        return asyncio.run(security_async(action, repo, languages, config_path, state, include_dismissed, ctx))


def generate_config(
    action: str = "rules",
    # rules params
    rules: Optional[str] = None,
    overwrite: bool = False,
    analyze_only: bool = False,
    # ignore params
    include_indexing: bool = True,
    analyze_project: bool = True,
    # simplify params
    rule_files: Optional[str] = None,
    output_dir: Optional[str] = None,
    # common
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Unified config generation tool.
    
    Args:
        action: "rules" for .mdc files, "ignore" for .cursorignore, "simplify" for rule simplification
        rules: Specific rules to generate (rules action)
        overwrite: Overwrite existing rules (rules action)
        analyze_only: Only analyze, don't generate (rules action)
        include_indexing: Include indexing ignore (ignore action)
        analyze_project: Analyze project structure (ignore action)
        rule_files: Rule files to simplify (simplify action)
        output_dir: Output directory (simplify action)
        dry_run: Preview changes without writing
    
    Returns:
        Config generation results
    """
    if action == "rules":
        from .cursor_rules_generator import generate_cursor_rules
        return generate_cursor_rules(rules, overwrite, analyze_only)
    elif action == "ignore":
        from .cursorignore_generator import generate_cursorignore
        return generate_cursorignore(include_indexing, analyze_project, dry_run)
    elif action == "simplify":
        from .rule_simplifier import simplify_rules
        parsed_files = None
        if rule_files:
            try:
                parsed_files = json.loads(rule_files)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid JSON in rule_files parameter"}
        return simplify_rules(parsed_files, dry_run, output_dir)
    else:
        return {
            "status": "error",
            "error": f"Unknown config action: {action}. Use 'rules', 'ignore', or 'simplify'.",
        }


def setup_hooks(
    action: str = "git",
    # git hooks params
    hooks: Optional[list[str]] = None,
    # pattern params
    patterns: Optional[str] = None,
    config_path: Optional[str] = None,
    # common
    install: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Unified hooks setup tool.
    
    Args:
        action: "git" for git hooks, "patterns" for pattern triggers
        hooks: Specific git hooks to install (git action)
        patterns: Pattern trigger definitions as JSON (patterns action)
        config_path: Config file path (patterns action)
        install: Install hooks (vs uninstall)
        dry_run: Preview changes without writing
    
    Returns:
        Hook setup results
    """
    if action == "git":
        from .git_hooks import setup_git_hooks
        return setup_git_hooks(hooks, install, dry_run)
    elif action == "patterns":
        from .pattern_triggers import setup_pattern_triggers
        parsed_patterns = None
        if patterns:
            try:
                parsed_patterns = json.loads(patterns)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid JSON in patterns parameter"}
        return setup_pattern_triggers(parsed_patterns, config_path, install, dry_run)
    else:
        return {
            "status": "error",
            "error": f"Unknown hooks action: {action}. Use 'git' or 'patterns'.",
        }


def prompt_tracking(
    action: str = "analyze",
    # log params
    prompt: Optional[str] = None,
    task_id: Optional[str] = None,
    mode: Optional[str] = None,
    outcome: Optional[str] = None,
    iteration: int = 1,
    # analyze params
    days: int = 7,
) -> dict[str, Any]:
    """
    Unified prompt tracking tool.
    
    Args:
        action: "log" to record a prompt, "analyze" to view patterns
        prompt: Prompt text to log (log action, required)
        task_id: Associated task ID (log action)
        mode: Workflow mode used (log action)
        outcome: Result of prompt (log action)
        iteration: Iteration number (log action)
        days: Days of history to analyze (analyze action)
    
    Returns:
        Log confirmation or analysis results
    """
    if action == "log":
        if not prompt:
            return {"status": "error", "error": "prompt parameter required for log action"}
        from .prompt_tracker import log_prompt_iteration
        return log_prompt_iteration(prompt, task_id, mode, outcome, iteration)
    elif action == "analyze":
        from .prompt_tracker import analyze_prompt_iterations
        return analyze_prompt_iterations(days)
    else:
        return {
            "status": "error",
            "error": f"Unknown prompt tracking action: {action}. Use 'log' or 'analyze'.",
        }


def health(
    action: str = "server",
    # git params
    agent_name: Optional[str] = None,
    check_remote: bool = True,
    # docs params
    output_path: Optional[str] = None,
    create_tasks: bool = True,
    # dod params
    task_id: Optional[str] = None,
    changed_files: Optional[str] = None,
    auto_check: bool = True,
    # cicd params
    workflow_path: Optional[str] = None,
    check_runners: bool = True,
) -> dict[str, Any]:
    """
    Unified health check tool.
    
    Args:
        action: "server" for server status, "git" for working copy, "docs" for documentation, "dod" for definition of done, "cicd" for CI/CD validation
        agent_name: Agent name filter (git action)
        check_remote: Check remote sync status (git action)
        output_path: Save results to file (docs, cicd actions)
        create_tasks: Create tasks for issues (docs action)
        task_id: Task to check completion for (dod action)
        changed_files: Files changed as JSON (dod action)
        auto_check: Auto-run checks (dod action)
        workflow_path: Path to workflow file (cicd action)
        check_runners: Validate runner configs (cicd action)
    
    Returns:
        Health check results
    """
    if action == "server":
        from ..utils.dev_reload import is_dev_mode
        from ..utils import find_project_root
        import time
        
        project_root = find_project_root()
        version = "unknown"
        pyproject = project_root / "pyproject.toml"
        if pyproject.exists():
            import re
            content = pyproject.read_text()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                version = match.group(1)
        
        return {
            "status": "operational",
            "version": version,
            "dev_mode": is_dev_mode(),
            "project_root": str(project_root),
            "timestamp": time.time(),
        }
    elif action == "git":
        from .working_copy_health import check_working_copy_health
        return check_working_copy_health(agent_name=agent_name, check_remote=check_remote)
    elif action == "docs":
        from .docs_health import check_documentation_health
        return check_documentation_health(output_path, create_tasks)
    elif action == "dod":
        from .definition_of_done import check_definition_of_done
        return check_definition_of_done(task_id, changed_files, auto_check, output_path)
    elif action == "cicd":
        from .ci_cd_validation import validate_ci_cd_workflow
        import json
        result = validate_ci_cd_workflow(workflow_path, check_runners, output_path)
        return json.loads(result) if isinstance(result, str) else result
    else:
        return {
            "status": "error",
            "error": f"Unknown health action: {action}. Use 'server', 'git', 'docs', 'dod', or 'cicd'.",
        }


def report(
    action: str = "overview",
    # common params
    output_format: str = "text",
    output_path: Optional[str] = None,
    # scorecard params
    include_recommendations: bool = True,
    # briefing params
    overall_score: float = 50.0,
    security_score: float = 50.0,
    testing_score: float = 50.0,
    documentation_score: float = 50.0,
    completion_score: float = 50.0,
    alignment_score: float = 50.0,
    # prd params
    project_name: Optional[str] = None,
    include_architecture: bool = True,
    include_metrics: bool = True,
    include_tasks: bool = True,
) -> dict[str, Any]:
    """
    Unified report generation tool.
    
    Args:
        action: "overview" for project overview, "scorecard" for health metrics, "briefing" for advisor wisdom, "prd" for requirements doc
        output_format: Output format (text, json, markdown)
        output_path: Save results to file
        include_recommendations: Include recommendations (scorecard action)
        overall_score: Overall project score (briefing action)
        security_score: Security metric score (briefing action)
        testing_score: Testing metric score (briefing action)
        documentation_score: Documentation score (briefing action)
        completion_score: Completion score (briefing action)
        alignment_score: Alignment score (briefing action)
        project_name: Project name override (prd action)
        include_architecture: Include architecture section (prd action)
        include_metrics: Include metrics section (prd action)
        include_tasks: Include tasks section (prd action)
    
    Returns:
        Generated report
    """
    if action == "overview":
        from .project_overview import generate_project_overview
        return generate_project_overview(output_format, output_path)
    elif action == "scorecard":
        from .project_scorecard import generate_project_scorecard
        return generate_project_scorecard(output_format, include_recommendations, output_path)
    elif action == "briefing":
        from .wisdom.advisors import get_advisor_briefing
        return get_advisor_briefing(
            overall_score, security_score, testing_score,
            documentation_score, completion_score, alignment_score
        )
    elif action == "prd":
        from .prd_generator import generate_prd
        return generate_prd(project_name, include_architecture, include_metrics, include_tasks, output_path)
    else:
        return {
            "status": "error",
            "error": f"Unknown report action: {action}. Use 'overview', 'scorecard', 'briefing', or 'prd'.",
        }


def advisor_audio(
    action: str = "podcast",
    # quote params
    text: Optional[str] = None,
    advisor: str = "default",
    # podcast/export params
    days: int = 7,
    # common
    output_path: Optional[str] = None,
    backend: str = "auto",
) -> dict[str, Any]:
    """
    Unified advisor audio tool.
    
    Args:
        action: "quote" to synthesize single quote, "podcast" to generate full audio, "export" for JSON export
        text: Quote text to synthesize (quote action, required)
        advisor: Advisor ID for voice selection (quote action)
        days: Days of history to include (podcast/export actions)
        output_path: Output file path
        backend: TTS backend (auto, elevenlabs, edge-tts, pyttsx3)
    
    Returns:
        Audio generation results or export data
    """
    if action == "quote":
        if not text:
            return {"status": "error", "error": "text parameter required for quote action"}
        from .wisdom.voice import synthesize_advisor_quote
        return synthesize_advisor_quote(text, advisor, output_path, backend)
    elif action == "podcast":
        from .wisdom.advisors import get_consultation_log
        from .wisdom.voice import generate_podcast_audio
        consultations = get_consultation_log(days=days)
        return generate_podcast_audio(consultations, output_path, backend)
    elif action == "export":
        from .wisdom.advisors import export_for_podcast
        from pathlib import Path
        path = Path(output_path) if output_path else None
        return export_for_podcast(days=days, output_path=path)
    else:
        return {
            "status": "error",
            "error": f"Unknown advisor_audio action: {action}. Use 'quote', 'podcast', or 'export'.",
        }


def task_analysis(
    action: str = "duplicates",
    # duplicates params
    similarity_threshold: float = 0.85,
    auto_fix: bool = False,
    # tags params
    dry_run: bool = True,
    custom_rules: Optional[str] = None,
    remove_tags: Optional[str] = None,
    # hierarchy params
    output_format: str = "text",
    include_recommendations: bool = True,
    # common
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Unified task analysis tool.
    
    Args:
        action: "duplicates" to find duplicates, "tags" for tag cleanup, "hierarchy" for structure analysis
        similarity_threshold: Threshold for duplicate detection (duplicates action)
        auto_fix: Auto-merge duplicates (duplicates action)
        dry_run: Preview changes without applying (tags action)
        custom_rules: Custom tag rename rules as JSON (tags action)
        remove_tags: Tags to remove as JSON list (tags action)
        output_format: Output format - text or json (hierarchy action)
        include_recommendations: Include recommendations (hierarchy action)
        output_path: Save results to file
    
    Returns:
        Analysis results
    """
    if action == "duplicates":
        from .duplicate_detection import detect_duplicate_tasks
        return detect_duplicate_tasks(similarity_threshold, auto_fix, output_path)
    elif action == "tags":
        from .tag_consolidation import consolidate_tags
        return consolidate_tags(dry_run, custom_rules, remove_tags, output_path)
    elif action == "hierarchy":
        from .task_hierarchy import analyze_task_hierarchy
        return analyze_task_hierarchy(output_format, output_path, include_recommendations)
    else:
        return {
            "status": "error",
            "error": f"Unknown task_analysis action: {action}. Use 'duplicates', 'tags', or 'hierarchy'.",
        }


async def testing_async(
    action: str = "run",
    # run params
    test_path: Optional[str] = None,
    test_framework: str = "auto",
    verbose: bool = True,
    coverage: bool = False,
    # coverage params
    coverage_file: Optional[str] = None,
    min_coverage: int = 80,
    format: str = "html",
    # common
    output_path: Optional[str] = None,
    ctx: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Unified testing tool (async with progress).
    
    Args:
        action: "run" to execute tests, "coverage" to analyze coverage
        test_path: Path to test file/directory (run action)
        test_framework: pytest, unittest, ctest, or auto (run action)
        verbose: Show detailed output (run action)
        coverage: Generate coverage during test run (run action)
        coverage_file: Path to coverage file (coverage action)
        min_coverage: Minimum coverage threshold (coverage action)
        format: Report format - html, json, terminal (coverage action)
        output_path: Save results to file
        ctx: FastMCP Context for progress reporting (optional)
    
    Returns:
        Test or coverage results as JSON string
    """
    if action == "run":
        from .run_tests import run_tests_async
        result = await run_tests_async(test_path, test_framework, verbose, coverage, output_path, ctx)
        return json.loads(result) if isinstance(result, str) else result
    elif action == "coverage":
        from .test_coverage import analyze_test_coverage
        result = analyze_test_coverage(coverage_file, min_coverage, output_path, format)
        return json.loads(result) if isinstance(result, str) else result
    else:
        return {
            "status": "error",
            "error": f"Unknown testing action: {action}. Use 'run' or 'coverage'.",
        }


def testing(
    action: str = "run",
    # run params
    test_path: Optional[str] = None,
    test_framework: str = "auto",
    verbose: bool = True,
    coverage: bool = False,
    # coverage params
    coverage_file: Optional[str] = None,
    min_coverage: int = 80,
    format: str = "html",
    # common
    output_path: Optional[str] = None,
    ctx: Optional[Any] = None,
) -> dict[str, Any]:
    """
    Unified testing tool (sync wrapper).
    
    Args:
        action: "run" to execute tests, "coverage" to analyze coverage
        test_path: Path to test file/directory (run action)
        test_framework: pytest, unittest, ctest, or auto (run action)
        verbose: Show detailed output (run action)
        coverage: Generate coverage during test run (run action)
        coverage_file: Path to coverage file (coverage action)
        min_coverage: Minimum coverage threshold (coverage action)
        format: Report format - html, json, terminal (coverage action)
        output_path: Save results to file
        ctx: FastMCP Context for progress reporting (optional)
    
    Returns:
        Test or coverage results as dict
    """
    import asyncio
    try:
        # Check if we're in an async context
        asyncio.get_running_loop()
        # In async context - caller must await this or use testing_async directly
        raise RuntimeError("Use testing_async() in async context")
    except RuntimeError:
        # No running loop - run synchronously
        return asyncio.run(testing_async(action, test_path, test_framework, verbose, coverage, coverage_file, min_coverage, format, output_path, ctx))


def lint(
    action: str = "run",
    # run params
    path: Optional[str] = None,
    linter: str = "ruff",
    fix: bool = False,
    analyze: bool = True,
    select: Optional[str] = None,
    ignore: Optional[str] = None,
    # analyze params
    problems_json: Optional[str] = None,
    include_hints: bool = True,
    # common
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Unified linting tool.
    
    Args:
        action: "run" to execute linter, "analyze" to analyze problems
        path: File or directory to lint (run action)
        linter: "ruff" or "flake8" (run action)
        fix: Auto-fix issues (run action)
        analyze: Run analyze_problems on results (run action)
        select: Rule codes to enable (run action)
        ignore: Rule codes to ignore (run action)
        problems_json: JSON string of problems to analyze (analyze action)
        include_hints: Include resolution hints (analyze action)
        output_path: Save results to file
    
    Returns:
        Linting or analysis results as JSON string
    """
    if action == "run":
        from .linter import run_linter
        result = run_linter(path, linter, fix, analyze, select, ignore)
        return json.loads(result) if isinstance(result, str) else result
    elif action == "analyze":
        if not problems_json:
            return {
                "status": "error",
                "error": "problems_json is required for analyze action",
            }
        from .problems_advisor import analyze_problems_tool
        result = analyze_problems_tool(problems_json, include_hints, output_path)
        return json.loads(result) if isinstance(result, str) else result
    else:
        return {
            "status": "error",
            "error": f"Unknown lint action: {action}. Use 'run' or 'analyze'.",
        }


def memory(
    action: str = "search",
    # save params
    title: Optional[str] = None,
    content: Optional[str] = None,
    category: str = "insight",
    task_id: Optional[str] = None,
    metadata: Optional[str] = None,  # JSON string
    # recall params
    include_related: bool = True,
    # search params
    query: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """
    Unified memory management tool.
    
    Args:
        action: "save" to store insight, "recall" to get task context, "search" to find memories
        title: Memory title (save action, required)
        content: Memory content (save action, required)
        category: One of: debug, research, architecture, preference, insight (save action)
        task_id: Task ID to link memory to (save action) or recall context for (recall action)
        metadata: Additional metadata as JSON string (save action)
        include_related: Include related task memories (recall action)
        query: Search query text (search action)
        limit: Maximum results (search action)
    
    Returns:
        Memory operation results
    """
    if action == "save":
        if not title or not content:
            return {
                "success": False,
                "error": "title and content are required for save action",
            }
        from .session_memory import save_session_insight
        meta = None
        if metadata:
            try:
                meta = json.loads(metadata)
            except json.JSONDecodeError:
                return {"success": False, "error": "Invalid metadata JSON"}
        return save_session_insight(title, content, category, task_id, meta)
    elif action == "recall":
        if not task_id:
            return {
                "success": False,
                "error": "task_id is required for recall action",
            }
        from .session_memory import recall_task_context
        return recall_task_context(task_id, include_related)
    elif action == "search":
        if not query:
            return {
                "success": False,
                "error": "query is required for search action",
            }
        from .session_memory import search_session_memories
        return search_session_memories(query, category if category != "insight" else None, limit)
    else:
        return {
            "success": False,
            "error": f"Unknown memory action: {action}. Use 'save', 'recall', or 'search'.",
        }


def task_discovery(
    action: str = "all",
    # comments params
    file_patterns: Optional[str] = None,  # JSON list of glob patterns
    include_fixme: bool = True,
    # markdown params
    doc_path: Optional[str] = None,
    # orphans params (uses task_analysis internally)
    # common
    output_path: Optional[str] = None,
    create_tasks: bool = False,
) -> dict[str, Any]:
    """
    Unified task discovery tool.
    
    Finds tasks from various sources in the codebase.
    
    Args:
        action: "comments" for TODO/FIXME in code, "markdown" for task lists in docs,
                "orphans" for orphaned Todo2 tasks, "all" for everything
        file_patterns: JSON list of glob patterns for code scanning (comments action)
        include_fixme: Include FIXME comments (comments action)
        doc_path: Path to scan for markdown tasks (markdown action)
        output_path: Save results to file
        create_tasks: Auto-create Todo2 tasks from discoveries
    
    Returns:
        Discovery results with found tasks
    """
    import re
    from pathlib import Path
    from ..utils import find_project_root
    
    project_root = find_project_root()
    results = {
        "action": action,
        "discoveries": [],
        "summary": {},
    }
    
    def scan_comments():
        """Scan code for TODO/FIXME comments."""
        discoveries = []
        patterns = ["**/*.py", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx"]
        if file_patterns:
            try:
                patterns = json.loads(file_patterns)
            except json.JSONDecodeError:
                pass
        
        todo_pattern = re.compile(r'#\s*(TODO|FIXME)[\s:]+(.+)', re.IGNORECASE) if include_fixme else re.compile(r'#\s*TODO[\s:]+(.+)', re.IGNORECASE)
        
        for pattern in patterns:
            for file_path in project_root.glob(pattern):
                if any(skip in str(file_path) for skip in ['.git', 'node_modules', '__pycache__', '.venv', 'build']):
                    continue
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for line_num, line in enumerate(content.split('\n'), 1):
                        match = todo_pattern.search(line)
                        if match:
                            discoveries.append({
                                "type": match.group(1).upper() if include_fixme else "TODO",
                                "text": match.group(2).strip() if include_fixme else match.group(1).strip(),
                                "file": str(file_path.relative_to(project_root)),
                                "line": line_num,
                                "source": "comment",
                            })
                except Exception:
                    continue
        return discoveries
    
    def scan_markdown():
        """Scan markdown files for task lists."""
        discoveries = []
        search_path = Path(doc_path) if doc_path else project_root / "docs"
        if not search_path.exists():
            search_path = project_root
        
        task_pattern = re.compile(r'^[\s]*[-*]\s*\[([ xX])\]\s*(.+)', re.MULTILINE)
        
        for md_file in search_path.rglob("*.md"):
            if any(skip in str(md_file) for skip in ['.git', 'node_modules']):
                continue
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                for match in task_pattern.finditer(content):
                    is_done = match.group(1).lower() == 'x'
                    if not is_done:  # Only uncompleted tasks
                        discoveries.append({
                            "type": "MARKDOWN_TASK",
                            "text": match.group(2).strip(),
                            "file": str(md_file.relative_to(project_root)),
                            "completed": is_done,
                            "source": "markdown",
                        })
            except Exception:
                continue
        return discoveries
    
    def find_orphans():
        """Find orphaned Todo2 tasks."""
        from .task_hierarchy import analyze_task_hierarchy
        result = analyze_task_hierarchy(output_format="json", include_recommendations=False)
        orphans = result.get("networkx_analysis", {}).get("orphans", [])
        return [{"type": "ORPHAN", "task_id": o, "source": "todo2"} for o in orphans]
    
    # Execute based on source
    if action in ["comments", "all"]:
        results["discoveries"].extend(scan_comments())
    if action in ["markdown", "all"]:
        results["discoveries"].extend(scan_markdown())
    if action in ["orphans", "all"]:
        results["discoveries"].extend(find_orphans())
    
    # Summary
    results["summary"] = {
        "total": len(results["discoveries"]),
        "by_source": {},
        "by_type": {},
    }
    for d in results["discoveries"]:
        src = d.get("source", "unknown")
        typ = d.get("type", "unknown")
        results["summary"]["by_source"][src] = results["summary"]["by_source"].get(src, 0) + 1
        results["summary"]["by_type"][typ] = results["summary"]["by_type"].get(typ, 0) + 1
    
    # Save if requested
    if output_path:
        Path(output_path).write_text(json.dumps(results, indent=2))
    
    return results


def task_workflow(
    action: str = "sync",
    # sync params
    dry_run: bool = False,
    # approve params
    status: str = "Review",
    new_status: str = "Todo",
    clarification_none: bool = True,
    filter_tag: Optional[str] = None,
    task_ids: Optional[str] = None,  # JSON list
    # clarify params
    sub_action: str = "list",  # list, resolve, batch (for clarify action)
    task_id: Optional[str] = None,
    clarification_text: Optional[str] = None,
    decision: Optional[str] = None,
    decisions_json: Optional[str] = None,
    move_to_todo: bool = True,
    # common
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Unified task workflow management tool.
    
    Args:
        action: "sync" for TODO↔Todo2 sync, "approve" for bulk approval, "clarify" for clarifications
        dry_run: Preview changes without applying (sync, approve)
        status: Filter tasks by status (approve)
        new_status: Target status (approve)
        clarification_none: Only tasks without clarification (approve)
        filter_tag: Filter by tag (approve)
        task_ids: JSON list of task IDs (approve)
        sub_action: "list", "resolve", or "batch" (clarify action)
        task_id: Task to resolve (clarify)
        clarification_text: Clarification response (clarify)
        decision: Decision made (clarify)
        decisions_json: Batch decisions as JSON (clarify)
        move_to_todo: Move resolved tasks to Todo (clarify)
        output_path: Save results to file
    
    Returns:
        Workflow operation results
    """
    if action == "sync":
        from .todo_sync import sync_todo_tasks
        result = sync_todo_tasks(dry_run, output_path)
        return json.loads(result) if isinstance(result, str) else result
    
    elif action == "approve":
        from .batch_task_approval import batch_approve_tasks
        ids = None
        if task_ids:
            try:
                ids = json.loads(task_ids)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid task_ids JSON"}
        result = batch_approve_tasks(
            status=status,
            new_status=new_status,
            clarification_none=clarification_none,
            filter_tag=filter_tag,
            task_ids=ids,
            dry_run=dry_run,
        )
        return json.loads(result) if isinstance(result, str) else result
    
    elif action == "clarify":
        from .task_clarification_resolution import (
            list_tasks_awaiting_clarification,
            resolve_task_clarification,
            resolve_multiple_clarifications,
        )
        
        if sub_action == "list":
            result = list_tasks_awaiting_clarification()
        elif sub_action == "resolve":
            if not task_id:
                return {"status": "error", "error": "task_id required for resolve"}
            result = resolve_task_clarification(
                task_id, clarification_text, decision, move_to_todo, dry_run
            )
        elif sub_action == "batch":
            if not decisions_json:
                return {"status": "error", "error": "decisions_json required for batch"}
            try:
                decisions = json.loads(decisions_json)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid decisions_json"}
            result = resolve_multiple_clarifications(decisions, move_to_todo, dry_run)
        else:
            return {"status": "error", "error": f"Unknown sub_action: {sub_action}. Use 'list', 'resolve', or 'batch'."}
        
        return result if isinstance(result, dict) else json.loads(result)
    
    else:
        return {
            "status": "error",
            "error": f"Unknown task_workflow action: {action}. Use 'sync', 'approve', or 'clarify'.",
        }

