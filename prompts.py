"""
MCP Prompts for Project Management Automation

Reusable prompt templates that guide users through common workflows
using the project management automation tools.
"""

# Documentation Health Prompts

DOCUMENTATION_HEALTH_CHECK = """Analyze the project documentation health and identify issues.

This prompt will:
1. Check documentation structure and organization
2. Validate internal and external links
3. Identify broken references and formatting issues
4. Generate a health score (0-100)
5. Optionally create Todo2 tasks for issues found

Use the check_documentation_health_tool with create_tasks=True to automatically create tasks for issues."""

DOCUMENTATION_QUICK_CHECK = """Quick documentation health check without creating tasks.

Use check_documentation_health_tool with create_tasks=False for a report-only analysis."""

# Task Management Prompts

TASK_ALIGNMENT_ANALYSIS = """Analyze Todo2 task alignment with project goals and investment strategy framework.

This prompt will:
1. Evaluate task alignment with project objectives
2. Identify misaligned or out-of-scope tasks
3. Calculate alignment scores for each task
4. Optionally create follow-up tasks for misaligned items

Use analyze_todo2_alignment_tool with create_followup_tasks=True to automatically create tasks for misaligned items."""

DUPLICATE_TASK_CLEANUP = """Find and consolidate duplicate Todo2 tasks.

This prompt will:
1. Detect duplicate tasks using similarity analysis
2. Group similar tasks together
3. Provide recommendations for consolidation
4. Optionally auto-fix duplicates (merge/delete)

Use detect_duplicate_tasks_tool with:
- similarity_threshold=0.85 (default) for standard detection
- auto_fix=True to automatically consolidate duplicates
- auto_fix=False (default) to review before fixing"""

TASK_SYNC = """Synchronize tasks between shared TODO table and Todo2.

This prompt will:
1. Compare tasks across systems
2. Identify missing or out-of-sync tasks
3. Optionally sync tasks (dry_run=False) or preview changes (dry_run=True)

Use sync_todo_tasks_tool with dry_run=True first to preview changes, then dry_run=False to apply."""

# Security & Dependencies Prompts

SECURITY_SCAN_ALL = """Scan all project dependencies for security vulnerabilities.

This prompt will:
1. Scan Python, Rust, and npm dependencies
2. Identify known vulnerabilities
3. Prioritize by severity (critical, high, medium, low)
4. Provide remediation recommendations

Use scan_dependency_security_tool with languages=None to scan all languages, or specify ['python', 'rust', 'npm']."""

SECURITY_SCAN_PYTHON = """Scan Python dependencies for security vulnerabilities.

Use scan_dependency_security_tool with languages=['python']."""

SECURITY_SCAN_RUST = """Scan Rust dependencies for security vulnerabilities.

Use scan_dependency_security_tool with languages=['rust']."""

# Automation Discovery Prompts

AUTOMATION_DISCOVERY = """Discover new automation opportunities in the codebase.

This prompt will:
1. Analyze codebase for repetitive patterns
2. Identify high-value automation opportunities
3. Score opportunities by value and effort
4. Generate recommendations for automation

Use find_automation_opportunities_tool with min_value_score=0.7 to find high-value opportunities."""

AUTOMATION_HIGH_VALUE = """Find only high-value automation opportunities (score >= 0.8).

Use find_automation_opportunities_tool with min_value_score=0.8."""

# PWA Configuration Prompts

PWA_REVIEW = """Review PWA configuration and generate improvement recommendations.

This prompt will:
1. Analyze PWA manifest and service worker configuration
2. Check for best practices compliance
3. Identify missing features or optimizations
4. Provide actionable improvement recommendations

Use review_pwa_config_tool to analyze the current PWA setup."""

# Workflow Prompts

PRE_SPRINT_CLEANUP = """Pre-sprint cleanup workflow.

Run these tools in sequence:
1. detect_duplicate_tasks_tool - Find and consolidate duplicates
2. analyze_todo2_alignment_tool - Check task alignment
3. check_documentation_health_tool - Ensure docs are up to date

This ensures a clean task list and aligned goals before starting new work."""

POST_IMPLEMENTATION_REVIEW = """Post-implementation review workflow.

Run these tools after completing a feature:
1. check_documentation_health_tool - Update documentation
2. scan_dependency_security_tool - Check for new vulnerabilities
3. find_automation_opportunities_tool - Discover new automation needs

This ensures quality and identifies follow-up work."""

WEEKLY_MAINTENANCE = """Weekly maintenance workflow.

Run these tools weekly:
1. check_documentation_health_tool - Keep docs healthy
2. detect_duplicate_tasks_tool - Clean up duplicates
3. scan_dependency_security_tool - Check security
4. sync_todo_tasks_tool - Sync across systems

This maintains project health and keeps systems in sync."""

# Daily Workflow Prompts

DAILY_CHECKIN = """Daily check-in workflow for project health monitoring.

Run these tools every morning (5 min):
1. server_status - Verify server is operational
2. list_tasks_awaiting_clarification - Identify any blockers needing decisions
3. check_working_copy_health - Verify Git status across agents

This gives you a quick overview of project state before starting work.

For automated daily maintenance, use run_daily_automation_tool which handles:
- Documentation health checks
- Task alignment verification
- Duplicate detection"""

# Sprint Workflow Prompts

SPRINT_START = """Sprint start workflow for preparing a clean backlog.

Run these tools at the beginning of each sprint:
1. detect_duplicate_tasks_tool - Clean up duplicate tasks
2. analyze_todo2_alignment_tool - Ensure tasks align with goals
3. batch_approve_tasks_tool - Queue ready tasks for automation
4. list_tasks_awaiting_clarification - Identify blocked tasks

This ensures a clean, prioritized backlog before starting sprint work."""

SPRINT_END = """Sprint end workflow for quality assurance and documentation.

Run these tools at the end of each sprint:
1. run_tests_tool with coverage=true - Verify test coverage
2. analyze_test_coverage_tool - Identify coverage gaps
3. check_documentation_health_tool - Ensure docs are updated
4. scan_dependency_security_tool - Security check before release

This ensures quality standards are met before sprint completion."""

# Task Review Workflow

TASK_REVIEW = """Comprehensive task review workflow for backlog hygiene.

Run monthly or after major project changes:
1. detect_duplicate_tasks_tool - Find and merge duplicates
2. analyze_todo2_alignment_tool - Check task-goal alignment  
3. list_tasks_awaiting_clarification - Review blocked tasks
4. Review manually for obsolete/stale tasks
5. batch_approve_tasks_tool - Queue reviewed tasks

Categories to evaluate:
- Duplicates → Merge or remove
- Misaligned → Re-scope or cancel
- Obsolete → Cancel if work already done
- Stale (>30 days) → Review priority or cancel
- Blocked → Resolve dependencies

Future: review_task_relevance_tool and infer_task_completion_tool will automate steps 4."""

# Project Health Prompt

PROJECT_HEALTH = """Comprehensive project health assessment.

Run these tools for a full health check:
1. server_status - Server operational status
2. check_documentation_health_tool - Documentation score
3. run_tests_tool coverage=true - Test results and coverage
4. analyze_test_coverage_tool - Coverage gap analysis
5. scan_dependency_security_tool - Security vulnerabilities
6. validate_ci_cd_workflow_tool - CI/CD pipeline status
7. analyze_todo2_alignment_tool - Task alignment with goals

This provides a complete picture of:
- Code quality (tests, coverage)
- Documentation health
- Security posture
- CI/CD reliability
- Project management state

Use this before major releases or quarterly reviews."""

# Automation Setup Prompt

AUTOMATION_SETUP = """One-time automation setup workflow.

Run these tools to enable automated project management:

1. setup_git_hooks_tool - Configure automatic checks on commits
   - pre-commit: docs health, security scan (blocking)
   - pre-push: task alignment, comprehensive security (blocking)
   - post-commit: automation discovery (non-blocking)
   - post-merge: duplicate detection, task sync (non-blocking)

2. setup_pattern_triggers_tool - Configure file change triggers
   - docs/**/*.md → documentation health check
   - src/**/*.py → run tests
   - requirements.txt → security scan

3. Configure cron jobs (manual):
   - Daily: run_daily_automation
   - Weekly: scan_dependency_security
   - See scripts/cron/*.sh for examples

After setup, Exarp will automatically maintain project health."""

# Prompt Metadata

PROMPTS = {
    "doc_health_check": {
        "name": "Documentation Health Check",
        "description": DOCUMENTATION_HEALTH_CHECK,
        "arguments": []
    },
    "doc_quick_check": {
        "name": "Quick Documentation Check",
        "description": DOCUMENTATION_QUICK_CHECK,
        "arguments": []
    },
    "task_alignment": {
        "name": "Task Alignment Analysis",
        "description": TASK_ALIGNMENT_ANALYSIS,
        "arguments": []
    },
    "duplicate_cleanup": {
        "name": "Duplicate Task Cleanup",
        "description": DUPLICATE_TASK_CLEANUP,
        "arguments": []
    },
    "task_sync": {
        "name": "Task Synchronization",
        "description": TASK_SYNC,
        "arguments": []
    },
    "security_scan_all": {
        "name": "Security Scan (All Languages)",
        "description": SECURITY_SCAN_ALL,
        "arguments": []
    },
    "security_scan_python": {
        "name": "Security Scan (Python)",
        "description": SECURITY_SCAN_PYTHON,
        "arguments": []
    },
    "security_scan_rust": {
        "name": "Security Scan (Rust)",
        "description": SECURITY_SCAN_RUST,
        "arguments": []
    },
    "automation_discovery": {
        "name": "Automation Discovery",
        "description": AUTOMATION_DISCOVERY,
        "arguments": []
    },
    "automation_high_value": {
        "name": "High-Value Automation Discovery",
        "description": AUTOMATION_HIGH_VALUE,
        "arguments": []
    },
    "pwa_review": {
        "name": "PWA Configuration Review",
        "description": PWA_REVIEW,
        "arguments": []
    },
    "pre_sprint_cleanup": {
        "name": "Pre-Sprint Cleanup Workflow",
        "description": PRE_SPRINT_CLEANUP,
        "arguments": []
    },
    "post_implementation_review": {
        "name": "Post-Implementation Review Workflow",
        "description": POST_IMPLEMENTATION_REVIEW,
        "arguments": []
    },
    "weekly_maintenance": {
        "name": "Weekly Maintenance Workflow",
        "description": WEEKLY_MAINTENANCE,
        "arguments": []
    },
    # New workflow prompts
    "daily_checkin": {
        "name": "Daily Check-in Workflow",
        "description": DAILY_CHECKIN,
        "arguments": []
    },
    "sprint_start": {
        "name": "Sprint Start Workflow",
        "description": SPRINT_START,
        "arguments": []
    },
    "sprint_end": {
        "name": "Sprint End Workflow",
        "description": SPRINT_END,
        "arguments": []
    },
    "task_review": {
        "name": "Task Review Workflow",
        "description": TASK_REVIEW,
        "arguments": []
    },
    "project_health": {
        "name": "Project Health Assessment",
        "description": PROJECT_HEALTH,
        "arguments": []
    },
    "automation_setup": {
        "name": "Automation Setup Workflow",
        "description": AUTOMATION_SETUP,
        "arguments": []
    },
}
