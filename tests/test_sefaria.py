"""
Unit Tests for Sefaria Wisdom Integration

Tests for wisdom/sefaria.py module (9% coverage → target: 80%+).

NOTE: These tests currently test the Python wisdom module directly.
TODO: Update to mock wisdom_client and test MCP integration instead.
The old module is kept as fallback, so these tests still work.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import urllib.error

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestSefariaWisdom:
    """Tests for Sefaria wisdom integration."""

    def test_get_aeon_level_chaos(self):
        """Test aeon level determination for low scores."""
        from project_management_automation.tools.wisdom.sefaria import get_aeon_level

        assert get_aeon_level(0) == "chaos"
        assert get_aeon_level(15) == "chaos"
        assert get_aeon_level(30) == "chaos"

    def test_get_aeon_level_lower_aeons(self):
        """Test aeon level determination for lower scores."""
        from project_management_automation.tools.wisdom.sefaria import get_aeon_level

        assert get_aeon_level(31) == "lower_aeons"
        assert get_aeon_level(40) == "lower_aeons"
        assert get_aeon_level(50) == "lower_aeons"

    def test_get_aeon_level_middle_aeons(self):
        """Test aeon level determination for middle scores."""
        from project_management_automation.tools.wisdom.sefaria import get_aeon_level

        assert get_aeon_level(51) == "middle_aeons"
        assert get_aeon_level(60) == "middle_aeons"
        assert get_aeon_level(70) == "middle_aeons"

    def test_get_aeon_level_upper_aeons(self):
        """Test aeon level determination for upper scores."""
        from project_management_automation.tools.wisdom.sefaria import get_aeon_level

        assert get_aeon_level(71) == "upper_aeons"
        assert get_aeon_level(80) == "upper_aeons"
        assert get_aeon_level(85) == "upper_aeons"

    def test_get_aeon_level_treasury(self):
        """Test aeon level determination for highest scores."""
        from project_management_automation.tools.wisdom.sefaria import get_aeon_level

        assert get_aeon_level(86) == "treasury"
        assert get_aeon_level(95) == "treasury"
        assert get_aeon_level(100) == "treasury"

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_success(self, mock_urlopen):
        """Test successful Sefaria API fetch."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "text": "Test quote text",
            "ref": "Pirkei_Avot.1.14",
            "heRef": "פרקי אבות א:יד",
            "book": "Pirkei Avot"
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_sefaria_text("Pirkei_Avot.1.14")

        assert result is not None
        assert result['text'] == "Test quote text"
        assert result['ref'] == "Pirkei_Avot.1.14"
        assert result['book'] == "Pirkei Avot"

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_with_hebrew(self, mock_urlopen):
        """Test Sefaria API fetch with Hebrew text."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "text": "Test quote",
            "he": "ציטוט בדיקה",
            "ref": "Pirkei_Avot.1.14",
            "heRef": "פרקי אבות א:יד",
            "book": "Pirkei Avot"
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_sefaria_text("Pirkei_Avot.1.14", include_hebrew=True)

        assert result is not None
        assert 'hebrew' in result
        assert result['hebrew'] == "ציטוט בדיקה"

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_flattens_nested_lists(self, mock_urlopen):
        """Test that nested lists in API response are flattened."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "text": [["Part 1", "Part 2"], "Part 3"],
            "ref": "Test.1.1",
            "book": "Test"
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_sefaria_text("Test.1.1")

        assert result is not None
        assert isinstance(result['text'], str)
        assert "Part 1" in result['text']
        assert "Part 2" in result['text']
        assert "Part 3" in result['text']

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_handles_urlerror(self, mock_urlopen):
        """Test handling of URL errors."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        result = fetch_sefaria_text("Pirkei_Avot.1.14")

        assert result is None

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_handles_timeout(self, mock_urlopen):
        """Test handling of timeout errors."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_urlopen.side_effect = TimeoutError("Request timed out")

        result = fetch_sefaria_text("Pirkei_Avot.1.14")

        assert result is None

    @patch('urllib.request.urlopen')
    def test_fetch_sefaria_text_handles_json_decode_error(self, mock_urlopen):
        """Test handling of invalid JSON responses."""
        from project_management_automation.tools.wisdom.sefaria import fetch_sefaria_text

        mock_response = Mock()
        mock_response.read.return_value = b"invalid json"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = fetch_sefaria_text("Pirkei_Avot.1.14")

        assert result is None

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_success(self, mock_choice, mock_fetch):
        """Test successful wisdom retrieval."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"}
        mock_fetch.return_value = {
            "text": "Test quote",
            "ref": "Pirkei_Avot.1.14",
            "book": "Pirkei Avot"
        }

        result = get_sefaria_wisdom(health_score=25.0, source="pirkei_avot", fetch_live=True)

        assert result is not None
        assert result['quote'] == "Test quote"
        assert result['source'] == "Pirkei Avot.1.14"
        assert result['aeon_level'] == "Chaos"
        assert result['health_score'] == 25.0

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_fallback(self, mock_choice, mock_fetch):
        """Test fallback when API fetch fails."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"}
        mock_fetch.return_value = None

        result = get_sefaria_wisdom(health_score=25.0, source="pirkei_avot", fetch_live=True)

        assert result is not None
        assert "[Read:" in result['quote']  # Fallback format

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_with_hebrew(self, mock_choice, mock_fetch):
        """Test wisdom retrieval with Hebrew text."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"}
        mock_fetch.return_value = {
            "text": "Test quote",
            "hebrew": "ציטוט בדיקה",
            "ref": "Pirkei_Avot.1.14",
            "heRef": "פרקי אבות א:יד",
            "book": "Pirkei Avot"
        }

        result = get_sefaria_wisdom(
            health_score=25.0,
            source="pirkei_avot",
            fetch_live=True,
            include_hebrew=True
        )

        assert result is not None
        assert 'hebrew' in result
        assert result['bilingual'] is True

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_hebrew_only(self, mock_choice, mock_fetch):
        """Test Hebrew-only mode."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"}
        mock_fetch.return_value = {
            "text": "Test quote",
            "hebrew": "ציטוט בדיקה",
            "ref": "Pirkei_Avot.1.14",
            "heRef": "פרקי אבות א:יד",
            "book": "Pirkei Avot"
        }

        result = get_sefaria_wisdom(
            health_score=25.0,
            source="pirkei_avot",
            fetch_live=True,
            hebrew_only=True
        )

        assert result is not None
        assert result['quote'] == "ציטוט בדיקה"  # Hebrew becomes main quote

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_cleans_html(self, mock_choice, mock_fetch):
        """Test that HTML tags are cleaned from text."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "When overwhelmed"}
        mock_fetch.return_value = {
            "text": "<b>Bold</b> and <i>italic</i> text",
            "hebrew": "<b>טקסט</b> מודגש",
            "ref": "Pirkei_Avot.1.14",
            "book": "Pirkei Avot"
        }

        result = get_sefaria_wisdom(health_score=25.0, source="pirkei_avot", fetch_live=True)

        assert result is not None
        assert "<b>" not in result['quote']
        assert "<i>" not in result['quote']
        assert "Bold" in result['quote']
        assert "italic" in result['quote']

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_different_sources(self, mock_choice, mock_fetch):
        """Test wisdom retrieval from different sources."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Proverbs.1.1", "context": "Test"}
        mock_fetch.return_value = {"text": "Proverb quote", "ref": "Proverbs.1.1", "book": "Proverbs"}

        result = get_sefaria_wisdom(health_score=50.0, source="proverbs", fetch_live=True)

        assert result is not None
        assert result['wisdom_source'] == "Mishlei (Proverbs)"
        assert result['wisdom_icon'] == "📜"

    @patch('project_management_automation.tools.wisdom.sefaria.fetch_sefaria_text')
    @patch('random.choice')
    def test_get_sefaria_wisdom_invalid_source(self, mock_choice, mock_fetch):
        """Test that invalid source defaults to pirkei_avot."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "Test"}
        mock_fetch.return_value = {"text": "Quote", "ref": "Pirkei_Avot.1.14", "book": "Pirkei Avot"}

        result = get_sefaria_wisdom(health_score=50.0, source="invalid_source", fetch_live=True)

        assert result is not None
        assert result['wisdom_source'] == "Pirkei Avot (Ethics of the Fathers)"

    @patch('random.seed')
    @patch('random.choice')
    def test_get_sefaria_wisdom_seed_date(self, mock_choice, mock_seed):
        """Test that seed_date parameter uses date-based seeding."""
        from project_management_automation.tools.wisdom.sefaria import get_sefaria_wisdom

        mock_choice.return_value = {"ref": "Pirkei_Avot.1.14", "context": "Test"}

        get_sefaria_wisdom(health_score=50.0, seed_date=True, fetch_live=False)

        # Verify seed was called
        assert mock_seed.called

    def test_format_rtl_text(self):
        """Test RTL text formatting."""
        from project_management_automation.tools.wisdom.sefaria import format_rtl_text

        hebrew_text = "זה טקסט בעברית ארוך מאוד שצריך להיות מעוצב"
        lines = format_rtl_text(hebrew_text, width=20)

        assert len(lines) > 1
        # Check RTL marker is present
        assert "\u200F" in lines[0]  # Right-to-Left Mark

    def test_format_rtl_text_empty(self):
        """Test RTL formatting with empty text."""
        from project_management_automation.tools.wisdom.sefaria import format_rtl_text

        lines = format_rtl_text("", width=20)
        assert lines == []

    def test_format_sefaria_wisdom(self):
        """Test wisdom formatting for display."""
        from project_management_automation.tools.wisdom.sefaria import format_sefaria_wisdom

        wisdom = {
            "quote": "Test quote text",
            "source": "Pirkei Avot.1.14",
            "context": "When overwhelmed",
            "wisdom_source": "Pirkei Avot",
            "wisdom_icon": "🕎",
            "aeon_level": "Chaos",
            "sefaria_link": "https://www.sefaria.org/Pirkei_Avot.1.14"
        }

        formatted = format_sefaria_wisdom(wisdom)

        assert "Test quote text" in formatted
        assert "Pirkei Avot" in formatted
        assert "🕎" in formatted
        assert "When overwhelmed" in formatted

    def test_format_sefaria_wisdom_none(self):
        """Test formatting with None input."""
        from project_management_automation.tools.wisdom.sefaria import format_sefaria_wisdom

        formatted = format_sefaria_wisdom(None)
        assert formatted == ""

    def test_format_sefaria_wisdom_truncates_long_quotes(self):
        """Test that long quotes are truncated."""
        from project_management_automation.tools.wisdom.sefaria import format_sefaria_wisdom

        long_quote = "A" * 250
        wisdom = {
            "quote": long_quote,
            "source": "Test.1.1",
            "context": "Test",
            "wisdom_source": "Test",
            "wisdom_icon": "📜",
            "aeon_level": "Middle",
            "sefaria_link": "https://test.com"
        }

        formatted = format_sefaria_wisdom(wisdom)
        # Should be truncated to ~200 chars
        assert len([line for line in formatted.split('\n') if 'A' * 200 in line]) == 0

    def test_format_hebrew_only_wisdom(self):
        """Test Hebrew-only formatting."""
        from project_management_automation.tools.wisdom.sefaria import format_hebrew_only_wisdom

        wisdom = {
            "quote": "ציטוט בעברית",
            "source": "Pirkei Avot.1.14",
            "hebrew_ref": "פרקי אבות א:יד",
            "context": "When overwhelmed",
            "wisdom_source": "Pirkei Avot",
            "wisdom_icon": "🕎",
            "aeon_level": "Chaos",
            "sefaria_link": "https://www.sefaria.org/Pirkei_Avot.1.14"
        }

        formatted = format_hebrew_only_wisdom(wisdom)

        assert "ציטוט בעברית" in formatted
        assert "עברית" in formatted  # Hebrew indicator

    def test_format_hebrew_only_wisdom_none(self):
        """Test Hebrew-only formatting with None."""
        from project_management_automation.tools.wisdom.sefaria import format_hebrew_only_wisdom

        formatted = format_hebrew_only_wisdom(None)
        assert formatted == ""