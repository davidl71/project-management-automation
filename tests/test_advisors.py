"""
Unit tests for the Trusted Advisor System.

Tests cover:
- Advisor assignments (metrics, tools, stages)
- Consultation functionality
- Score-based frequency determination
- Daily briefing generation
- Podcast export functionality
- Consultation logging
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch


class TestAdvisorAssignments:
    """Test that all advisors are properly assigned."""

    def test_metric_advisors_complete(self):
        """All expected metrics should have advisors."""
        from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS

        expected_metrics = [
            "security",
            "testing",
            "documentation",
            "completion",
            "alignment",
            "clarity",
            "ci_cd",
            "dogfooding",
            "uniqueness",
            "codebase",
            "parallelizable",
        ]

        for metric in expected_metrics:
            assert metric in METRIC_ADVISORS, f"Missing advisor for metric: {metric}"
            assert "advisor" in METRIC_ADVISORS[metric], f"Missing 'advisor' key for {metric}"
            assert "rationale" in METRIC_ADVISORS[metric], f"Missing 'rationale' key for {metric}"

    def test_tool_advisors_complete(self):
        """Key tools should have advisors."""
        from project_management_automation.tools.wisdom.advisors import TOOL_ADVISORS

        expected_tools = ["project_scorecard", "sprint_automation", "run_tests", "scan_dependency_security"]

        for tool in expected_tools:
            assert tool in TOOL_ADVISORS, f"Missing advisor for tool: {tool}"

    def test_stage_advisors_complete(self):
        """All workflow stages should have advisors."""
        from project_management_automation.tools.wisdom.advisors import STAGE_ADVISORS

        expected_stages = [
            "daily_checkin",
            "planning",
            "implementation",
            "debugging",
            "review",
            "retrospective",
            "celebration",
        ]

        for stage in expected_stages:
            assert stage in STAGE_ADVISORS, f"Missing advisor for stage: {stage}"
            assert "advisor" in STAGE_ADVISORS[stage], f"Missing 'advisor' key for {stage}"

    def test_advisor_has_icon(self):
        """Metric advisors should have icons."""
        from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS

        for metric, info in METRIC_ADVISORS.items():
            assert "icon" in info, f"Missing 'icon' for metric: {metric}"


class TestConsultationFrequency:
    """Test score-based consultation frequency."""

    def test_chaos_mode(self):
        """Scores < 30 should trigger chaos mode."""
        from project_management_automation.tools.wisdom.advisors import get_consultation_mode

        import json
        for score in [0, 10, 20, 29]:
            mode_json = get_consultation_mode(score)
            mode = json.loads(mode_json)
            assert mode["name"] == "chaos", f"Score {score} should be chaos mode"
            assert mode["frequency"] == "every_action"

    def test_building_mode(self):
        """Scores 30-60 should trigger building mode."""
        from project_management_automation.tools.wisdom.advisors import get_consultation_mode

        import json
        for score in [30, 40, 50, 59]:
            mode_json = get_consultation_mode(score)
            mode = json.loads(mode_json)
            assert mode["name"] == "building", f"Score {score} should be building mode"

    def test_maturing_mode(self):
        """Scores 60-80 should trigger maturing mode."""
        from project_management_automation.tools.wisdom.advisors import get_consultation_mode

        import json
        for score in [60, 70, 79]:
            mode_json = get_consultation_mode(score)
            mode = json.loads(mode_json)
            assert mode["name"] == "maturing", f"Score {score} should be maturing mode"

    def test_mastery_mode(self):
        """Scores >= 80 should trigger mastery mode."""
        from project_management_automation.tools.wisdom.advisors import get_consultation_mode

        import json
        for score in [80, 90, 100]:
            mode_json = get_consultation_mode(score)
            mode = json.loads(mode_json)
            assert mode["name"] == "mastery", f"Score {score} should be mastery mode"


class TestConsultAdvisor:
    """Test the consult_advisor function."""

    def test_consult_metric_advisor(self):
        """Consulting a metric advisor should return wisdom."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(metric="security", score=80.0, context="Test", log=False)
        result = json.loads(result_json)

        assert "advisor" in result
        assert "quote" in result
        assert "encouragement" in result
        assert result["metric"] == "security"
        assert result["consultation_type"] == "metric"

    def test_consult_stage_advisor(self):
        """Consulting a stage advisor should return wisdom."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(stage="daily_checkin", score=70.0, context="Morning", log=False)
        result = json.loads(result_json)

        assert "advisor" in result
        assert result["stage"] == "daily_checkin"
        assert result["consultation_type"] == "stage"

    def test_consult_tool_advisor(self):
        """Consulting a tool advisor should return wisdom."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(tool="project_scorecard", score=75.0, context="Review", log=False)
        result = json.loads(result_json)

        assert "advisor" in result
        assert result["tool"] == "project_scorecard"
        assert result["consultation_type"] == "tool"

    def test_consult_with_no_params_uses_random(self):
        """Consulting without params should use random advisor."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(score=50.0, log=False)
        result = json.loads(result_json)

        assert "advisor" in result
        assert result["consultation_type"] == "random"

    def test_consultation_includes_mode(self):
        """Consultation result should include mode based on score."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        # Low score = chaos
        result_chaos_json = consult_advisor(metric="testing", score=20.0, log=False)
        result_chaos = json.loads(result_chaos_json)
        assert result_chaos["consultation_mode"] == "chaos"

        # High score = mastery
        result_mastery_json = consult_advisor(metric="testing", score=90.0, log=False)
        result_mastery = json.loads(result_mastery_json)
        assert result_mastery["consultation_mode"] == "mastery"

    def test_consultation_includes_timestamp(self):
        """Consultation result should include timestamp."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(metric="security", score=80.0, log=False)
        result = json.loads(result_json)

        assert "timestamp" in result
        # Should be ISO format
        datetime.fromisoformat(result["timestamp"])


class TestConsultationLogging:
    """Test consultation logging functionality."""

    def test_logging_creates_file(self):
        """Logging should create a JSONL file."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("project_management_automation.tools.wisdom.advisors.get_log_path") as mock_path:
                log_file = Path(tmpdir) / "consultations_test.jsonl"
                mock_path.return_value = log_file

                # Consult with logging enabled
                consult_advisor(metric="security", score=80.0, context="Test log", log=True)

                # Check file was created
                assert log_file.exists()

                # Check content
                with open(log_file) as f:
                    line = f.readline()
                    entry = json.loads(line)
                    assert entry["metric"] == "security"
                    assert entry["context"] == "Test log"

    def test_get_consultation_log_filters(self):
        """get_consultation_log should filter by advisor/metric/stage."""
        from project_management_automation.tools.wisdom.advisors import get_consultation_log

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create proper directory structure
            log_dir = Path(tmpdir) / ".exarp" / "advisor_logs"
            log_dir.mkdir(parents=True)
            log_file = log_dir / f"consultations_{datetime.now().strftime('%Y-%m')}.jsonl"

            # Create test log entries with current timestamps
            now = datetime.now()
            entries = [
                {"timestamp": now.isoformat(), "advisor": "bofh", "metric": "security"},
                {"timestamp": now.isoformat(), "advisor": "stoic", "metric": "testing"},
                {"timestamp": now.isoformat(), "advisor": "bofh", "stage": "debugging"},
            ]

            with open(log_file, "w") as f:
                for e in entries:
                    f.write(json.dumps(e) + "\n")

            # Patch find_project_root at its source (imported inside function)
            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                # Filter by advisor
                bofh_logs = get_consultation_log(days=30, advisor="bofh")
                assert len(bofh_logs) == 2, f"Expected 2, got {len(bofh_logs)}: {bofh_logs}"

                # Filter by metric
                security_logs = get_consultation_log(days=30, metric="security")
                assert len(security_logs) == 1, f"Expected 1, got {len(security_logs)}"


class TestDailyBriefing:
    """Test daily briefing generation."""

    def test_daily_briefing_returns_string(self):
        """get_daily_briefing should return formatted string."""
        from project_management_automation.tools.wisdom.advisors import get_daily_briefing

        briefing = get_daily_briefing(
            overall_score=72.0,
            metric_scores={
                "security": 100.0,
                "testing": 45.0,
                "documentation": 60.0,
            },
        )

        assert isinstance(briefing, str)
        assert "DAILY ADVISOR BRIEFING" in briefing
        assert "72.0%" in briefing

    def test_daily_briefing_focuses_on_lowest_scores(self):
        """Briefing should prioritize lowest-scoring metrics."""
        from project_management_automation.tools.wisdom.advisors import get_daily_briefing

        briefing = get_daily_briefing(
            overall_score=60.0,
            metric_scores={
                "security": 100.0,  # High - should not appear first
                "testing": 20.0,  # Lowest - should appear
                "documentation": 80.0,
            },
        )

        # Testing should be mentioned (lowest score)
        assert "TESTING" in briefing or "testing" in briefing.lower()


class TestPodcastExport:
    """Test podcast export functionality."""

    def test_export_for_podcast_returns_structure(self):
        """export_for_podcast should return proper structure."""
        from project_management_automation.tools.wisdom.advisors import export_for_podcast

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                # Create empty log directory
                log_dir = Path(tmpdir) / ".exarp" / "advisor_logs"
                log_dir.mkdir(parents=True)

                result = export_for_podcast(days=7)

                assert "title" in result
                assert "generated_at" in result
                assert "days_covered" in result
                assert "total_consultations" in result
                assert "episodes" in result
                assert isinstance(result["episodes"], list)

    def test_export_for_podcast_includes_consultations(self):
        """export_for_podcast should include logged consultations."""
        from project_management_automation.tools.wisdom.advisors import export_for_podcast

        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / ".exarp" / "advisor_logs"
            log_dir.mkdir(parents=True)

            # Create test consultation log
            log_file = log_dir / f"consultations_{datetime.now().strftime('%Y-%m')}.jsonl"
            entry = {
                "timestamp": datetime.now().isoformat(),
                "advisor": "bofh",
                "advisor_name": "BOFH",
                "metric": "security",
                "quote": "Test quote",
                "context": "Test context",
            }
            with open(log_file, "w") as f:
                f.write(json.dumps(entry) + "\n")

            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                result = export_for_podcast(days=7)

                assert result["total_consultations"] >= 1

    def test_export_for_podcast_writes_file(self):
        """export_for_podcast should write to file when path provided."""
        from project_management_automation.tools.wisdom.advisors import export_for_podcast

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("project_management_automation.utils.find_project_root") as mock_root:
                mock_root.return_value = Path(tmpdir)

                log_dir = Path(tmpdir) / ".exarp" / "advisor_logs"
                log_dir.mkdir(parents=True)

                output_file = Path(tmpdir) / "podcast.json"
                export_for_podcast(days=7, output_path=output_file)

                assert output_file.exists()
                with open(output_file) as f:
                    data = json.load(f)
                    assert "title" in data


class TestFormatConsultation:
    """Test consultation formatting."""

    def test_format_consultation_returns_string(self):
        """format_consultation should return formatted string."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor, format_consultation
        import json

        consultation_json = consult_advisor(metric="security", score=80.0, log=False)
        consultation = json.loads(consultation_json)
        formatted = format_consultation(consultation)

        assert isinstance(formatted, str)
        assert "TRUSTED ADVISOR" in formatted

    def test_format_consultation_includes_quote(self):
        """Formatted consultation should include the quote."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor, format_consultation
        import json

        consultation_json = consult_advisor(metric="security", score=80.0, log=False)
        consultation = json.loads(consultation_json)
        formatted = format_consultation(consultation)

        # Quote should be in the output
        assert consultation["quote"][:20] in formatted or '"' in formatted


class TestGetAdvisorFunctions:
    """Test advisor getter functions."""

    def test_get_advisor_for_metric(self):
        """get_advisor_for_metric should return advisor info."""
        from project_management_automation.tools.wisdom.advisors import get_advisor_for_metric

        result = get_advisor_for_metric("security")

        assert result is not None
        assert "advisor" in result
        assert result["advisor"] == "bofh"

    def test_get_advisor_for_unknown_metric(self):
        """get_advisor_for_metric should return None for unknown metric."""
        from project_management_automation.tools.wisdom.advisors import get_advisor_for_metric

        result = get_advisor_for_metric("unknown_metric")

        assert result is None

    def test_get_advisor_for_tool(self):
        """get_advisor_for_tool should return advisor info."""
        from project_management_automation.tools.wisdom.advisors import get_advisor_for_tool

        result = get_advisor_for_tool("project_scorecard")

        assert result is not None
        assert "advisor" in result

    def test_get_advisor_for_stage(self):
        """get_advisor_for_stage should return advisor info."""
        from project_management_automation.tools.wisdom.advisors import get_advisor_for_stage

        result = get_advisor_for_stage("daily_checkin")

        assert result is not None
        assert "advisor" in result


class TestIntegrationWithWisdomSources:
    """Test integration with wisdom sources."""

    def test_advisor_sources_exist_in_wisdom(self):
        """All advisors should reference valid wisdom sources."""
        from project_management_automation.tools.wisdom.advisors import METRIC_ADVISORS
        from project_management_automation.tools.wisdom.sources import WISDOM_SOURCES

        for metric, info in METRIC_ADVISORS.items():
            advisor = info["advisor"]
            # Check if advisor exists in WISDOM_SOURCES
            assert advisor in WISDOM_SOURCES, f"Advisor '{advisor}' for metric '{metric}' not in WISDOM_SOURCES"

    def test_consultation_returns_valid_wisdom(self):
        """Consultation should return valid wisdom from the source."""
        from project_management_automation.tools.wisdom.advisors import consult_advisor
        import json

        result_json = consult_advisor(metric="security", score=80.0, log=False)
        result = json.loads(result_json)

        # Should have actual quote content
        assert len(result.get("quote", "")) > 0
        assert len(result.get("encouragement", "")) > 0

