"""
Workflow Mode Recommender Tool

Recommends AGENT vs ASK mode based on task complexity and type.
Based on Cursor IDE Best Practice #3.
"""

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Import error handler
try:
    from ..error_handler import (
        ErrorCode,
        format_error_response,
        format_success_response,
        log_automation_execution,
    )
except ImportError:

    def format_success_response(data, message=None):
        return {"success": True, "data": data, "timestamp": time.time()}

    def format_error_response(error, error_code, include_traceback=False):
        return {"success": False, "error": {"code": str(error_code), "message": str(error)}}

    def log_automation_execution(name, duration, success, error=None):
        logger.info(f"{name}: {duration:.2f}s, success={success}")

    class ErrorCode:
        AUTOMATION_ERROR = "AUTOMATION_ERROR"


# Complexity indicators for AGENT mode
AGENT_INDICATORS = {
    "keywords": [
        "implement", "create", "build", "develop", "refactor",
        "migrate", "upgrade", "integrate", "deploy", "configure",
        "setup", "install", "automate", "generate", "scaffold",
    ],
    "patterns": [
        r"multi.?file",
        r"cross.?module",
        r"end.?to.?end",
        r"full.?stack",
        r"complete\s+\w+",
    ],
    "tags": [
        "feature", "implementation", "infrastructure", "integration",
        "refactoring", "migration", "automation",
    ],
}

# Simplicity indicators for ASK mode
ASK_INDICATORS = {
    "keywords": [
        "explain", "what", "why", "how", "understand",
        "clarify", "review", "check", "validate", "analyze",
        "debug", "find", "locate", "show", "list",
    ],
    "patterns": [
        r"single\s+file",
        r"quick\s+\w+",
        r"simple\s+\w+",
        r"just\s+\w+",
    ],
    "tags": [
        "question", "documentation", "review", "analysis",
        "debugging", "research",
    ],
}


def recommend_workflow_mode(
    task_description: Optional[str] = None,
    task_id: Optional[str] = None,
    include_rationale: bool = True,
) -> str:
    """
    [HINT: Workflow mode. AGENT vs ASK recommendation based on task complexity.]

    📊 Output: Recommended mode (AGENT/ASK), confidence, rationale
    🔧 Side Effects: None (advisory only)
    📁 Analyzes: Task description, tags, complexity indicators
    ⏱️ Typical Runtime: <1 second

    Example Prompt:
    "Should I use AGENT or ASK mode for implementing user authentication?"

    Guidelines from Cursor Best Practices:
    - AGENT mode: Multi-file changes, implementation, refactoring
    - ASK mode: Questions, single-file edits, code review

    Args:
        task_description: Description of the task (or natural language query)
        task_id: Optional Todo2 task ID to analyze
        include_rationale: Whether to include detailed reasoning

    Returns:
        JSON with mode recommendation
    """
    start_time = time.time()

    try:
        content = task_description or ""
        tags = []

        # If task_id provided, load from Todo2
        if task_id and not task_description:
            from project_management_automation.utils import find_project_root

            project_root = find_project_root()
            todo2_path = project_root / ".todo2" / "state.todo2.json"

            if todo2_path.exists():
                state = json.loads(todo2_path.read_text())
                task = next(
                    (t for t in state.get("todos", []) if t.get("id") == task_id),
                    None,
                )
                if task:
                    content = f"{task.get('name', '')} {task.get('long_description', '')}"
                    tags = task.get("tags", [])

        content_lower = content.lower()

        # Score AGENT indicators
        agent_score = 0
        agent_reasons = []

        for kw in AGENT_INDICATORS["keywords"]:
            if kw in content_lower:
                agent_score += 2
                agent_reasons.append(f"Keyword: '{kw}'")

        for pattern in AGENT_INDICATORS["patterns"]:
            if re.search(pattern, content_lower):
                agent_score += 3
                agent_reasons.append(f"Pattern: '{pattern}'")

        for tag in tags:
            if tag.lower() in AGENT_INDICATORS["tags"]:
                agent_score += 2
                agent_reasons.append(f"Tag: '{tag}'")

        # Score ASK indicators
        ask_score = 0
        ask_reasons = []

        for kw in ASK_INDICATORS["keywords"]:
            if kw in content_lower:
                ask_score += 2
                ask_reasons.append(f"Keyword: '{kw}'")

        for pattern in ASK_INDICATORS["patterns"]:
            if re.search(pattern, content_lower):
                ask_score += 3
                ask_reasons.append(f"Pattern: '{pattern}'")

        for tag in tags:
            if tag.lower() in ASK_INDICATORS["tags"]:
                ask_score += 2
                ask_reasons.append(f"Tag: '{tag}'")

        # Determine recommendation
        if agent_score > ask_score:
            mode = "AGENT"
            confidence = min(agent_score / (agent_score + ask_score + 1) * 100, 95)
            reasons = agent_reasons
            description = "Use AGENT mode for autonomous multi-step implementation"
        elif ask_score > agent_score:
            mode = "ASK"
            confidence = min(ask_score / (agent_score + ask_score + 1) * 100, 95)
            reasons = ask_reasons
            description = "Use ASK mode for focused questions and single edits"
        else:
            mode = "ASK"  # Default to ASK when uncertain
            confidence = 50
            reasons = ["No strong indicators - defaulting to ASK for safety"]
            description = "Unclear complexity - start with ASK, escalate to AGENT if needed"

        result = {
            "recommended_mode": mode,
            "confidence": round(confidence, 1),
            "description": description,
            "agent_score": agent_score,
            "ask_score": ask_score,
        }

        if include_rationale:
            result["rationale"] = reasons[:5]  # Top 5 reasons
            result["guidelines"] = {
                "AGENT": "Best for: Multi-file changes, feature implementation, refactoring, scaffolding",
                "ASK": "Best for: Questions, code review, single-file edits, debugging help",
            }

        duration = time.time() - start_time
        log_automation_execution("recommend_workflow_mode", duration, True)

        return json.dumps(format_success_response(result), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution("recommend_workflow_mode", duration, False, e)
        error_response = format_error_response(e, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)

