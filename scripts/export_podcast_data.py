#!/usr/bin/env python3
"""
Export Advisor Consultation Data for NotebookLM Podcast Generation

This script exports advisor consultations to a format suitable for:
1. NotebookLM Audio Overviews (Google's AI podcast feature)
2. Manual podcast script generation
3. Video narration scripts

Usage:
    python scripts/export_podcast_data.py --days 7 --output podcast_data.md
    python scripts/export_podcast_data.py --days 30 --format json

The output can be uploaded to NotebookLM as a source document to generate
AI podcast-style discussions about your project progress.
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Migrated to devwisdom-go MCP server
# Use wisdom_client for MCP calls, fallback to old module if needed
try:
    from project_management_automation.utils.wisdom_client import call_wisdom_tool_sync, read_wisdom_resource_sync
    from project_management_automation.utils.project_root import find_project_root
    WISDOM_CLIENT_AVAILABLE = True
except ImportError:
    WISDOM_CLIENT_AVAILABLE = False

# For METRIC_ADVISORS, try to get from MCP server, fallback to old module
if WISDOM_CLIENT_AVAILABLE:
    try:
        project_root = find_project_root()
        advisors_json = read_wisdom_resource_sync("wisdom://advisors", project_root)
        if advisors_json:
            import json
            advisors_data = json.loads(advisors_json) if isinstance(advisors_json, str) else advisors_json
            METRIC_ADVISORS = advisors_data.get("by_metric", {})
        else:
            # Fallback
            from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS
    except Exception:
        from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS
else:
    from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS

# For export_for_podcast, use MCP client wrapper
def export_for_podcast(days: int = 7) -> dict:
    """Export consultations for podcast - calls devwisdom-go MCP server."""
    if WISDOM_CLIENT_AVAILABLE:
        try:
            project_root = find_project_root()
            result = call_wisdom_tool_sync("export_for_podcast", {"days": days}, project_root)
            return result if result else {}
        except Exception:
            pass
    # Fallback to old implementation
    from project_management_automation.tools.wisdom.advisors import export_for_podcast as _old_export
    return _old_export(days)


def generate_markdown_script(podcast_data: dict) -> str:
    """Generate a markdown document optimized for NotebookLM."""

    lines = [
        f"# {podcast_data['title']}",
        "",
        f"*Generated: {podcast_data['generated_at']}*",
        "",
        "## Project Overview",
        "",
        "This document summarizes the trusted advisor consultations for the Exarp project,",
        "a project management automation system. Each day, the team consults wisdom sources",
        "assigned to specific metrics to guide their work.",
        "",
        "## Trusted Advisors",
        "",
        "| Metric | Advisor | Philosophy |",
        "|--------|---------|------------|",
    ]

    for metric, info in METRIC_ADVISORS.items():
        icon = info.get("icon", "📜")
        advisor = info.get("advisor", "unknown").replace("_", " ").title()
        rationale = info.get("rationale", "")[:50]
        lines.append(f"| {metric.title()} | {icon} {advisor} | {rationale}... |")

    lines.extend([
        "",
        "## Daily Progress Episodes",
        "",
    ])

    for episode in podcast_data.get("episodes", []):
        date = episode.get("date", "Unknown")
        advisors = episode.get("advisors", [])
        metrics = episode.get("metrics", [])
        quotes = episode.get("notable_quotes", [])

        lines.extend([
            f"### Episode: {date}",
            "",
            f"**Advisors Consulted:** {', '.join(advisors) if advisors else 'None'}",
            "",
            f"**Metrics Reviewed:** {', '.join(metrics) if metrics else 'None'}",
            "",
        ])

        if quotes:
            lines.append("**Key Wisdom Received:**")
            lines.append("")
            for q in quotes[:3]:  # Top 3 quotes
                quote = q.get("quote", "")
                advisor = q.get("advisor", "Unknown")
                encouragement = q.get("encouragement", "")
                lines.extend([
                    f"> \"{quote}\"",
                    f"> — {advisor}",
                    f"> 💡 *{encouragement}*",
                    "",
                ])

        narrative = episode.get("narrative_prompt", "")
        if narrative:
            lines.extend([
                "**Narrative:**",
                "",
                narrative,
                "",
            ])

        lines.append("---")
        lines.append("")

    # Add summary section for NotebookLM to focus on
    lines.extend([
        "## Key Themes This Week",
        "",
        "Please generate a podcast discussing:",
        "1. The overall project health journey shown in these consultations",
        "2. The most impactful wisdom from our trusted advisors",
        "3. How the different philosophical perspectives complement each other",
        "4. Recommendations for the coming week based on patterns observed",
        "",
        "## Podcast Style Guide",
        "",
        "- Conversational tone between two hosts",
        "- Reference specific quotes and advisors by name",
        "- Discuss the practical application of ancient wisdom to software development",
        "- Include moments of humor (especially when discussing BOFH quotes)",
        "- End with actionable takeaways",
        "",
    ])

    return "\n".join(lines)


def generate_json_export(podcast_data: dict) -> str:
    """Generate JSON export with full details."""
    return json.dumps(podcast_data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Export advisor consultations for podcast generation"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days of history to include (default: 7)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown for NotebookLM)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)"
    )

    args = parser.parse_args()

    # Export podcast data
    podcast_data = export_for_podcast(days=args.days)

    # Generate output
    if args.format == "markdown":
        output = generate_markdown_script(podcast_data)
    else:
        output = generate_json_export(podcast_data)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output)
        print(f"✅ Exported to {output_path}", file=sys.stderr)
    else:
        print(output)

    # Print summary
    print("\n📻 Podcast Export Summary:", file=sys.stderr)
    print(f"   Days covered: {args.days}", file=sys.stderr)
    print(f"   Total consultations: {podcast_data['total_consultations']}", file=sys.stderr)
    print(f"   Episodes: {len(podcast_data.get('episodes', []))}", file=sys.stderr)
    print("\n💡 Upload the output to NotebookLM and click 'Audio Overview' to generate podcast!", file=sys.stderr)


if __name__ == "__main__":
    main()

