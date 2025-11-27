"""
Unit Tests for Context Summarizer Tool

Tests for context summarization, batch processing, and token budget estimation.
"""

import pytest
import json
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from project_management_automation.tools.context_summarizer import (
    summarize_context,
    batch_summarize,
    estimate_context_budget,
    TOOL_PATTERNS,
    TOKENS_PER_CHAR,
)


class TestSummarizeContext:
    """Tests for summarize_context function."""

    def test_brief_level_health_data(self):
        """Test brief summarization of health data."""
        health_data = {
            "health_score": 85,
            "broken_links": 3,
            "stale_files": 2,
            "recommendations": ["Fix broken links", "Update stale docs"],
        }
        
        result = json.loads(summarize_context(health_data, level="brief"))
        
        assert "summary" in result
        assert result["level"] == "brief"
        assert result["tool_type"] == "health"
        assert "token_estimate" in result

    def test_detailed_level(self):
        """Test detailed summarization."""
        data = {
            "status": "success",
            "total_tasks": 50,
            "pending": 10,
            "completed": 35,
            "blocked": 5,
        }
        
        result = json.loads(summarize_context(data, level="detailed"))
        
        assert result["level"] == "detailed"
        assert "summary" in result

    def test_key_metrics_level(self):
        """Test key_metrics summarization."""
        security_data = {
            "status": "warning",
            "critical": 0,
            "high": 2,
            "medium": 5,
            "low": 10,
            "total_vulnerabilities": 17,
        }
        
        result = json.loads(summarize_context(security_data, level="key_metrics"))
        
        assert result["level"] == "key_metrics"
        assert "summary" in result

    def test_actionable_level(self):
        """Test actionable summarization."""
        data = {
            "status": "success",
            "recommendations": ["Update dependencies", "Add tests"],
            "tasks_created": 3,
        }
        
        result = json.loads(summarize_context(data, level="actionable"))
        
        assert result["level"] == "actionable"

    def test_explicit_tool_type(self):
        """Test with explicit tool_type parameter."""
        data = {"score": 75, "issues": 5}
        
        result = json.loads(summarize_context(data, tool_type="scorecard"))
        
        assert result["tool_type"] == "scorecard"

    def test_auto_detect_security_type(self):
        """Test auto-detection of security tool type."""
        data = {
            "vulnerabilities": [{"id": "CVE-123"}],
            "critical": 1,
            "high": 2,
        }
        
        result = json.loads(summarize_context(data))
        
        assert result["tool_type"] == "security"

    def test_auto_detect_task_type(self):
        """Test auto-detection of task tool type."""
        data = {
            "tasks": [{"id": "T-1"}],
            "pending": 5,
            "completed": 10,
        }
        
        result = json.loads(summarize_context(data))
        
        assert result["tool_type"] == "task"

    def test_json_string_input(self):
        """Test with JSON string input."""
        data = json.dumps({"status": "ok", "count": 5})
        
        result = json.loads(summarize_context(data))
        
        assert "summary" in result

    def test_plain_text_input(self):
        """Test with plain text (non-JSON) input."""
        data = "This is plain text, not JSON"
        
        result = json.loads(summarize_context(data))
        
        assert "summary" in result

    def test_token_estimation(self):
        """Test token estimation is included."""
        data = {"status": "ok", "items": list(range(100))}
        
        result = json.loads(summarize_context(data))
        
        assert "token_estimate" in result
        assert "original" in result["token_estimate"]
        assert "summarized" in result["token_estimate"]
        assert "reduction_percent" in result["token_estimate"]

    def test_include_raw(self):
        """Test include_raw parameter."""
        data = {"status": "success"}
        
        result = json.loads(summarize_context(data, include_raw=True))
        
        assert "raw_data" in result
        assert result["raw_data"] == data

    def test_max_tokens_truncation(self):
        """Test max_tokens truncation."""
        data = {"items": list(range(1000))}
        
        result = json.loads(summarize_context(data, max_tokens=50))
        
        # Should have truncated
        assert result["token_estimate"]["summarized"] <= 50

    def test_duration_included(self):
        """Test duration_ms is included in result."""
        data = {"status": "ok"}
        
        result = json.loads(summarize_context(data))
        
        assert "duration_ms" in result
        assert result["duration_ms"] >= 0


class TestBatchSummarize:
    """Tests for batch_summarize function."""

    def test_batch_multiple_items(self):
        """Test batch summarization of multiple items."""
        items = [
            {"data": {"health_score": 85}, "tool_type": "health"},
            {"data": {"critical": 0, "high": 1}, "tool_type": "security"},
            {"data": {"pending": 5, "completed": 10}, "tool_type": "task"},
        ]
        
        result = json.loads(batch_summarize(items))
        
        assert "combined_summary" in result
        assert result["total_items"] == 3
        assert "token_estimate" in result

    def test_batch_without_combine(self):
        """Test batch summarization without combining."""
        items = [
            {"data": {"status": "ok"}},
            {"data": {"status": "error"}},
        ]
        
        result = json.loads(batch_summarize(items, combine=False))
        
        assert "summaries" in result
        assert len(result["summaries"]) == 2

    def test_batch_with_level(self):
        """Test batch summarization with specific level."""
        items = [
            {"data": {"score": 80}},
            {"data": {"score": 90}},
        ]
        
        result = json.loads(batch_summarize(items, level="key_metrics"))
        
        assert "combined_summary" in result

    def test_batch_token_totals(self):
        """Test batch summarization calculates token totals."""
        items = [
            {"data": {"items": list(range(50))}},
            {"data": {"items": list(range(100))}},
        ]
        
        result = json.loads(batch_summarize(items))
        
        assert result["token_estimate"]["original"] > 0
        assert "reduction_percent" in result["token_estimate"]


class TestEstimateContextBudget:
    """Tests for estimate_context_budget function."""

    def test_under_budget(self):
        """Test budget analysis when under budget."""
        items = [
            {"status": "ok"},
            {"count": 5},
        ]
        
        result = json.loads(estimate_context_budget(items, budget_tokens=1000))
        
        assert result["over_budget"] is False
        assert result["reduction_needed"] == 0
        assert "items" in result

    def test_over_budget(self):
        """Test budget analysis when over budget."""
        items = [
            {"items": list(range(500))},
            {"items": list(range(500))},
        ]
        
        result = json.loads(estimate_context_budget(items, budget_tokens=100))
        
        assert result["over_budget"] is True
        assert result["reduction_needed"] > 0

    def test_items_sorted_by_size(self):
        """Test items are sorted by token size descending."""
        items = [
            {"small": 1},
            {"large": list(range(100))},
            {"medium": list(range(10))},
        ]
        
        result = json.loads(estimate_context_budget(items))
        
        # Should be sorted descending by tokens
        tokens = [item["tokens"] for item in result["items"]]
        assert tokens == sorted(tokens, reverse=True)

    def test_percent_of_budget(self):
        """Test percent_of_budget is calculated."""
        items = [{"data": list(range(100))}]
        
        result = json.loads(estimate_context_budget(items, budget_tokens=1000))
        
        assert "percent_of_budget" in result["items"][0]

    def test_strategy_included(self):
        """Test reduction strategy is included."""
        items = [
            {"items": list(range(500))},
        ]
        
        result = json.loads(estimate_context_budget(items, budget_tokens=100))
        
        assert "strategy" in result


class TestToolPatterns:
    """Tests for TOOL_PATTERNS configuration."""

    def test_health_pattern_exists(self):
        """Test health pattern is defined."""
        assert "health" in TOOL_PATTERNS
        assert "key_fields" in TOOL_PATTERNS["health"]
        assert "brief_template" in TOOL_PATTERNS["health"]

    def test_security_pattern_exists(self):
        """Test security pattern is defined."""
        assert "security" in TOOL_PATTERNS
        assert "count_fields" in TOOL_PATTERNS["security"]

    def test_task_pattern_exists(self):
        """Test task pattern is defined."""
        assert "task" in TOOL_PATTERNS

    def test_testing_pattern_exists(self):
        """Test testing pattern is defined."""
        assert "testing" in TOOL_PATTERNS

    def test_generic_fallback_exists(self):
        """Test generic fallback pattern exists."""
        assert "generic" in TOOL_PATTERNS

    def test_all_patterns_have_required_fields(self):
        """Test all patterns have required fields."""
        required_fields = ["key_fields", "count_fields", "action_fields", "brief_template"]
        
        for tool_type, pattern in TOOL_PATTERNS.items():
            for field in required_fields:
                assert field in pattern, f"Pattern '{tool_type}' missing '{field}'"


class TestTokenEstimation:
    """Tests for token estimation constants."""

    def test_tokens_per_char_defined(self):
        """Test TOKENS_PER_CHAR constant is defined."""
        assert TOKENS_PER_CHAR > 0
        assert TOKENS_PER_CHAR < 1  # Should be a fraction

    def test_tokens_per_char_reasonable(self):
        """Test TOKENS_PER_CHAR is a reasonable value."""
        # Typical tokenizers produce ~0.2-0.3 tokens per character
        assert 0.1 <= TOKENS_PER_CHAR <= 0.5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

