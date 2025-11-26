"""
Trusted Advisor System for Exarp

Assigns wisdom sources as "trusted advisors" for different metrics, tools,
and workflow stages. Tracks consultations for future podcast/video generation.

Usage:
    from project_management_automation.tools.wisdom.advisors import (
        get_advisor_for_metric,
        get_advisor_for_tool,
        get_advisor_for_stage,
        consult_advisor,
        get_consultation_log,
    )
    
    # Get advice for a metric
    advice = consult_advisor(metric="security", score=100.0, context="Reviewing controls")
    
    # Get advice for workflow stage
    advice = consult_advisor(stage="daily_checkin", overall_score=80.0)

Design Philosophy:
    Each advisor brings a unique perspective matching their source material:
    - BOFH: Paranoid security, expects user error
    - Stoics: Discipline through adversity
    - Tao: Balance and flow
    - Sun Tzu: Strategy and execution
    - Gracián: Pragmatic wisdom
    - Confucius: Teaching and ethics
    - Kybalion: Cause and effect, mental models
    - Murphy: Expect failure, plan for it
    - Shakespeare: Creativity and drama
    - Enochian: Mystical structure, hidden patterns
    - Bible: Timeless wisdom, patience
    - Pistis Sophia: Gnostic enlightenment journey
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from .sources import get_wisdom, WISDOM_SOURCES

# ═══════════════════════════════════════════════════════════════════════════════
# ADVISOR ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════════════════

# Metric → Advisor mapping with rationale
METRIC_ADVISORS = {
    "security": {
        "advisor": "bofh",
        "icon": "😈",
        "rationale": "BOFH is paranoid about security, expects users to break everything",
        "helps_with": "Finding vulnerabilities, defensive thinking, access control",
    },
    "testing": {
        "advisor": "stoic",
        "icon": "🏛️",
        "rationale": "Stoics teach discipline through adversity - tests reveal truth",
        "helps_with": "Persistence through failures, accepting harsh feedback",
    },
    "documentation": {
        "advisor": "confucius",
        "icon": "🎓",
        "rationale": "Confucius emphasized teaching and transmitting wisdom",
        "helps_with": "Clear explanations, teaching future maintainers",
    },
    "completion": {
        "advisor": "art_of_war",
        "icon": "⚔️",
        "rationale": "Sun Tzu teaches strategy and decisive execution",
        "helps_with": "Prioritization, knowing when to attack vs wait",
    },
    "alignment": {
        "advisor": "tao",
        "icon": "☯️",
        "rationale": "Tao emphasizes balance, flow, and purpose",
        "helps_with": "Ensuring work serves project goals, finding harmony",
    },
    "clarity": {
        "advisor": "gracian",
        "icon": "🎭",
        "rationale": "Gracián's maxims are models of clarity and pragmatism",
        "helps_with": "Simplifying complexity, clear communication",
    },
    "ci_cd": {
        "advisor": "kybalion",
        "icon": "⚗️",
        "rationale": "Kybalion teaches cause and effect - CI/CD is pure causation",
        "helps_with": "Understanding pipelines, automation philosophy",
    },
    "dogfooding": {
        "advisor": "murphy",
        "icon": "🔧",
        "rationale": "Murphy's Law: if it can break, it will - use your own tools!",
        "helps_with": "Finding edge cases, eating your own cooking",
    },
    "uniqueness": {
        "advisor": "shakespeare",
        "icon": "🎭",
        "rationale": "Shakespeare created unique works that transcended his time",
        "helps_with": "Creative differentiation, memorable design",
    },
    "codebase": {
        "advisor": "enochian",
        "icon": "🔮",
        "rationale": "Enochian mysticism reveals hidden structure and patterns",
        "helps_with": "Architecture, finding hidden connections",
    },
    "parallelizable": {
        "advisor": "tao_of_programming",
        "icon": "💻",
        "rationale": "The Tao of Programming teaches elegant parallel design",
        "helps_with": "Decomposition, independent task design",
    },
}

# Tool → Advisor mapping
TOOL_ADVISORS = {
    "project_scorecard": {"advisor": "pistis_sophia", "rationale": "Journey through aeons mirrors project health stages"},
    "project_overview": {"advisor": "kybalion", "rationale": "Hermetic principles for holistic understanding"},
    "sprint_automation": {"advisor": "art_of_war", "rationale": "Sprint is a campaign requiring strategy"},
    "check_documentation_health": {"advisor": "confucius", "rationale": "Teaching requires good documentation"},
    "analyze_todo2_alignment": {"advisor": "tao", "rationale": "Alignment is balance and flow"},
    "detect_duplicate_tasks": {"advisor": "bofh", "rationale": "Duplicates are user error manifested"},
    "scan_dependency_security": {"advisor": "bofh", "rationale": "Security paranoia is a feature"},
    "run_tests": {"advisor": "stoic", "rationale": "Tests teach through failure"},
    "validate_ci_cd_workflow": {"advisor": "kybalion", "rationale": "CI/CD is cause and effect"},
    "dev_reload": {"advisor": "murphy", "rationale": "Hot reload because Murphy says restarts will fail at the worst time"},
}

# Workflow Stage → Advisor mapping
STAGE_ADVISORS = {
    "daily_checkin": {
        "advisor": "pistis_sophia",
        "icon": "📜",
        "rationale": "Start each day with enlightenment journey wisdom",
        "consultation_depth": "brief",
    },
    "planning": {
        "advisor": "art_of_war",
        "icon": "⚔️",
        "rationale": "Planning is strategy - Sun Tzu is the master",
        "consultation_depth": "detailed",
    },
    "implementation": {
        "advisor": "tao_of_programming",
        "icon": "💻",
        "rationale": "During coding, let the code flow naturally",
        "consultation_depth": "brief",
    },
    "debugging": {
        "advisor": "bofh",
        "icon": "😈",
        "rationale": "BOFH knows all the ways things break",
        "consultation_depth": "detailed",
    },
    "review": {
        "advisor": "stoic",
        "icon": "🏛️",
        "rationale": "Review requires accepting harsh truths with equanimity",
        "consultation_depth": "detailed",
    },
    "retrospective": {
        "advisor": "confucius",
        "icon": "🎓",
        "rationale": "Retrospectives are about learning and teaching",
        "consultation_depth": "detailed",
    },
    "celebration": {
        "advisor": "shakespeare",
        "icon": "🎭",
        "rationale": "Celebrate with drama and poetry!",
        "consultation_depth": "brief",
    },
}

# Score-based consultation frequency
SCORE_CONSULTATION_FREQUENCY = {
    "chaos": {       # < 30%
        "min_score": 0,
        "max_score": 30,
        "frequency": "every_action",
        "description": "Chaos mode: Consult advisor before every significant action",
        "icon": "🔥",
    },
    "building": {    # 30-60%
        "min_score": 30,
        "max_score": 60,
        "frequency": "start_and_review",
        "description": "Building mode: Consult at start of work and during review",
        "icon": "🏗️",
    },
    "maturing": {    # 60-80%
        "min_score": 60,
        "max_score": 80,
        "frequency": "milestones",
        "description": "Maturing mode: Consult at planning and major milestones",
        "icon": "🌱",
    },
    "mastery": {     # > 80%
        "min_score": 80,
        "max_score": 100,
        "frequency": "weekly",
        "description": "Mastery mode: Weekly reflection with advisor",
        "icon": "🎯",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# CONSULTATION LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

def get_log_path() -> Path:
    """Get path to advisor consultation log."""
    from ...utils import find_project_root
    project_root = find_project_root()
    log_dir = project_root / '.exarp' / 'advisor_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"consultations_{datetime.now().strftime('%Y-%m')}.jsonl"


def log_consultation(consultation: Dict[str, Any]) -> None:
    """Append consultation to log file (JSONL format for easy parsing)."""
    log_path = get_log_path()
    with open(log_path, 'a') as f:
        f.write(json.dumps(consultation) + '\n')


def get_consultation_log(
    days: int = 30,
    advisor: Optional[str] = None,
    metric: Optional[str] = None,
    stage: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve consultation log entries.
    
    Args:
        days: Number of days to look back
        advisor: Filter by advisor
        metric: Filter by metric
        stage: Filter by stage
        
    Returns:
        List of consultation entries
    """
    from ...utils import find_project_root
    project_root = find_project_root()
    log_dir = project_root / '.exarp' / 'advisor_logs'
    
    if not log_dir.exists():
        return []
    
    consultations = []
    cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
    
    for log_file in sorted(log_dir.glob("consultations_*.jsonl")):
        with open(log_file) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # Parse timestamp
                    ts = datetime.fromisoformat(entry.get('timestamp', '')).timestamp()
                    if ts < cutoff:
                        continue
                    # Apply filters
                    if advisor and entry.get('advisor') != advisor:
                        continue
                    if metric and entry.get('metric') != metric:
                        continue
                    if stage and entry.get('stage') != stage:
                        continue
                    consultations.append(entry)
                except (json.JSONDecodeError, ValueError):
                    continue
    
    return consultations


# ═══════════════════════════════════════════════════════════════════════════════
# ADVISOR CONSULTATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_consultation_mode(score: float) -> Dict[str, Any]:
    """Get consultation mode based on score."""
    for mode_name, mode in SCORE_CONSULTATION_FREQUENCY.items():
        if mode["min_score"] <= score < mode["max_score"]:
            return {"name": mode_name, **mode}
    return {"name": "mastery", **SCORE_CONSULTATION_FREQUENCY["mastery"]}


def get_advisor_for_metric(metric: str) -> Optional[Dict[str, Any]]:
    """Get the trusted advisor for a scorecard metric."""
    return METRIC_ADVISORS.get(metric)


def get_advisor_for_tool(tool: str) -> Optional[Dict[str, Any]]:
    """Get the trusted advisor for a tool."""
    return TOOL_ADVISORS.get(tool)


def get_advisor_for_stage(stage: str) -> Optional[Dict[str, Any]]:
    """Get the trusted advisor for a workflow stage."""
    return STAGE_ADVISORS.get(stage)


def consult_advisor(
    metric: Optional[str] = None,
    tool: Optional[str] = None,
    stage: Optional[str] = None,
    score: float = 50.0,
    context: str = "",
    log: bool = True,
) -> Dict[str, Any]:
    """
    Consult an advisor and get wisdom.
    
    Args:
        metric: Scorecard metric to get advice for
        tool: Tool to get advice for
        stage: Workflow stage to get advice for
        score: Current score (affects wisdom selection)
        context: What you're working on
        log: Whether to log this consultation
        
    Returns:
        Consultation result with wisdom and advice
    """
    # Determine which advisor to consult
    advisor_info = None
    consultation_type = None
    
    if metric:
        advisor_info = METRIC_ADVISORS.get(metric)
        consultation_type = "metric"
    elif tool:
        advisor_info = TOOL_ADVISORS.get(tool)
        consultation_type = "tool"
    elif stage:
        advisor_info = STAGE_ADVISORS.get(stage)
        consultation_type = "stage"
    
    if not advisor_info:
        # Default to random advisor
        import random
        advisor = random.choice(list(WISDOM_SOURCES.keys()))
        advisor_info = {"advisor": advisor, "rationale": "Random selection"}
        consultation_type = "random"
    
    advisor = advisor_info["advisor"]
    
    # Get wisdom from the advisor
    wisdom = get_wisdom(score, source=advisor, seed_date=False)
    
    if not wisdom:
        wisdom = {
            "quote": "Silence is also wisdom.",
            "source": "Unknown",
            "encouragement": "Sometimes reflection is the answer.",
        }
    
    # Get consultation mode
    mode = get_consultation_mode(score)
    
    # Build result
    result = {
        "timestamp": datetime.now().isoformat(),
        "consultation_type": consultation_type,
        "advisor": advisor,
        "advisor_icon": advisor_info.get("icon", wisdom.get("wisdom_icon", "📜")),
        "advisor_name": wisdom.get("wisdom_source", advisor.replace("_", " ").title()),
        "rationale": advisor_info.get("rationale", ""),
        "metric": metric,
        "tool": tool,
        "stage": stage,
        "score_at_time": score,
        "consultation_mode": mode["name"],
        "mode_icon": mode["icon"],
        "mode_frequency": mode["frequency"],
        "quote": wisdom.get("quote", ""),
        "quote_source": wisdom.get("source", ""),
        "encouragement": wisdom.get("encouragement", ""),
        "context": context,
    }
    
    # Log consultation
    if log:
        log_consultation(result)
    
    return result


def format_consultation(consultation: Dict[str, Any]) -> str:
    """Format a consultation for display."""
    icon = consultation.get("advisor_icon", "📜")
    name = consultation.get("advisor_name", "Unknown")
    quote = consultation.get("quote", "")
    source = consultation.get("quote_source", "")
    encouragement = consultation.get("encouragement", "")
    rationale = consultation.get("rationale", "")
    mode = consultation.get("consultation_mode", "")
    mode_icon = consultation.get("mode_icon", "")
    
    return f"""
╔══════════════════════════════════════════════════════════════════════╗
║  {icon} TRUSTED ADVISOR: {name:<45} ║
║  Mode: {mode_icon} {mode.upper():<56} ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  "{quote}"
║  
║  — {source}
║                                                                      ║
║  💡 {encouragement:<60} ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Why this advisor: {rationale[:47]:<47} ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def get_daily_briefing(overall_score: float, metric_scores: Dict[str, float]) -> str:
    """
    Get a daily briefing from advisors based on current scores.
    
    Args:
        overall_score: Overall project score
        metric_scores: Dict of metric name → score
        
    Returns:
        Formatted daily briefing with advisor wisdom
    """
    mode = get_consultation_mode(overall_score)
    
    # Find lowest scoring metrics (need most advice)
    sorted_metrics = sorted(metric_scores.items(), key=lambda x: x[1])
    
    briefing = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  🌅 DAILY ADVISOR BRIEFING                                           ║
║  Overall Score: {overall_score:.1f}% | Mode: {mode['icon']} {mode['name'].upper():<30} ║
╠══════════════════════════════════════════════════════════════════════╣
"""
    
    # Consult advisor for lowest 3 metrics
    for metric, score in sorted_metrics[:3]:
        advisor_info = METRIC_ADVISORS.get(metric, {})
        if not advisor_info:
            continue
            
        consultation = consult_advisor(metric=metric, score=score, log=False)
        
        briefing += f"""
║  {advisor_info.get('icon', '📜')} {metric.upper()}: {score:.0f}%
║     Advisor: {consultation['advisor_name']}
║     "{consultation['quote'][:55]}..."
║     💡 {consultation['encouragement'][:55]}
"""
    
    briefing += """
╚══════════════════════════════════════════════════════════════════════╝
"""
    return briefing


# ═══════════════════════════════════════════════════════════════════════════════
# PODCAST/VIDEO DATA EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_for_podcast(
    days: int = 7,
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Export consultation data formatted for AI podcast/video generation.
    
    Args:
        days: Days of history to include
        output_path: Optional path to write JSON output
        
    Returns:
        Structured data for podcast generation
    """
    consultations = get_consultation_log(days=days)
    
    # Group by day
    by_day = {}
    for c in consultations:
        day = c.get("timestamp", "")[:10]
        if day not in by_day:
            by_day[day] = []
        by_day[day].append(c)
    
    # Build narrative structure
    podcast_data = {
        "title": f"Exarp Project Progress - Week of {datetime.now().strftime('%Y-%m-%d')}",
        "generated_at": datetime.now().isoformat(),
        "days_covered": days,
        "total_consultations": len(consultations),
        "episodes": [],
    }
    
    for day, day_consultations in sorted(by_day.items()):
        # Summarize the day
        advisors_consulted = list(set(c.get("advisor") for c in day_consultations))
        metrics_worked = list(set(c.get("metric") for c in day_consultations if c.get("metric")))
        stages_visited = list(set(c.get("stage") for c in day_consultations if c.get("stage")))
        
        # Find best quotes of the day
        quotes = [
            {
                "quote": c.get("quote"),
                "advisor": c.get("advisor_name"),
                "context": c.get("context"),
                "encouragement": c.get("encouragement"),
            }
            for c in day_consultations if c.get("quote")
        ]
        
        episode = {
            "date": day,
            "summary": f"Consulted {len(advisors_consulted)} advisors on {len(metrics_worked)} metrics",
            "advisors": advisors_consulted,
            "metrics": metrics_worked,
            "stages": stages_visited,
            "consultation_count": len(day_consultations),
            "notable_quotes": quotes[:5],  # Top 5 quotes
            "narrative_prompt": f"""
On {day}, the team consulted {len(advisors_consulted)} trusted advisors 
({', '.join(advisors_consulted)}) while working on {', '.join(metrics_worked) if metrics_worked else 'various tasks'}.
Key wisdom received: "{quotes[0]['quote'] if quotes else 'No quotes recorded'}"
            """.strip(),
        }
        
        podcast_data["episodes"].append(episode)
    
    # Save if path provided
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(podcast_data, f, indent=2)
    
    return podcast_data


__all__ = [
    'METRIC_ADVISORS',
    'TOOL_ADVISORS',
    'STAGE_ADVISORS',
    'SCORE_CONSULTATION_FREQUENCY',
    'get_advisor_for_metric',
    'get_advisor_for_tool',
    'get_advisor_for_stage',
    'get_consultation_mode',
    'consult_advisor',
    'format_consultation',
    'get_daily_briefing',
    'get_consultation_log',
    'export_for_podcast',
]

