"""
Tests for Context Priming System

Tests the new context priming components:
- Context primer resource
- Hint registry with dynamic loading
- Auto-priming based on agent/time/mode
- Mode-aware prompt discovery
"""

import json
import os
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT PRIMER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestContextPrimer:
    """Tests for the unified context primer resource."""
    
    def test_tool_hints_registry_exists(self):
        """Test that TOOL_HINTS_REGISTRY is populated."""
        from project_management_automation.resources.context_primer import TOOL_HINTS_REGISTRY
        
        assert TOOL_HINTS_REGISTRY is not None
        assert len(TOOL_HINTS_REGISTRY) > 0
        assert "project_scorecard" in TOOL_HINTS_REGISTRY
        assert "scan_dependency_security" in TOOL_HINTS_REGISTRY
    
    def test_tool_hints_have_required_fields(self):
        """Test that each hint has required fields."""
        from project_management_automation.resources.context_primer import TOOL_HINTS_REGISTRY
        
        for name, data in TOOL_HINTS_REGISTRY.items():
            assert "hint" in data, f"{name} missing 'hint' field"
            assert "category" in data, f"{name} missing 'category' field"
            assert len(data["hint"]) > 0, f"{name} has empty hint"
    
    def test_workflow_mode_context_exists(self):
        """Test that WORKFLOW_MODE_CONTEXT is populated."""
        from project_management_automation.resources.context_primer import WORKFLOW_MODE_CONTEXT
        
        assert WORKFLOW_MODE_CONTEXT is not None
        assert len(WORKFLOW_MODE_CONTEXT) > 0
        assert "daily_checkin" in WORKFLOW_MODE_CONTEXT
        assert "security_review" in WORKFLOW_MODE_CONTEXT
        assert "development" in WORKFLOW_MODE_CONTEXT
    
    def test_workflow_modes_have_required_fields(self):
        """Test that each workflow mode has required fields."""
        from project_management_automation.resources.context_primer import WORKFLOW_MODE_CONTEXT
        
        for mode, data in WORKFLOW_MODE_CONTEXT.items():
            assert "description" in data, f"{mode} missing 'description'"
            assert "tool_groups" in data, f"{mode} missing 'tool_groups'"
            assert "prompts" in data, f"{mode} missing 'prompts'"
            assert "keywords" in data, f"{mode} missing 'keywords'"
    
    def test_get_context_primer_returns_json(self):
        """Test that get_context_primer returns valid JSON."""
        from project_management_automation.resources.context_primer import get_context_primer
        
        result = get_context_primer()
        
        # Should be valid JSON
        data = json.loads(result)
        
        assert "timestamp" in data
        assert "workflow" in data
    
    def test_get_context_primer_includes_hints(self):
        """Test that context primer includes hints when requested."""
        from project_management_automation.resources.context_primer import get_context_primer
        
        result = get_context_primer(include_hints=True)
        data = json.loads(result)
        
        assert "hints" in data
        assert "hints_count" in data
        assert data["hints_count"] > 0
    
    def test_get_context_primer_excludes_hints(self):
        """Test that context primer excludes hints when requested."""
        from project_management_automation.resources.context_primer import get_context_primer
        
        result = get_context_primer(include_hints=False)
        data = json.loads(result)
        
        assert "hints" not in data
    
    def test_get_context_primer_mode_override(self):
        """Test that mode can be overridden."""
        from project_management_automation.resources.context_primer import get_context_primer
        
        result = get_context_primer(mode="security_review")
        data = json.loads(result)
        
        assert data["workflow"]["mode"] == "security_review"
    
    def test_get_hints_for_mode(self):
        """Test getting hints filtered by mode."""
        from project_management_automation.resources.context_primer import get_hints_for_mode
        
        result = get_hints_for_mode("security_review")
        data = json.loads(result)
        
        assert data["mode"] == "security_review"
        assert "hints" in data
        assert data["count"] > 0
    
    def test_get_all_hints(self):
        """Test getting all hints."""
        from project_management_automation.resources.context_primer import get_all_hints
        
        result = get_all_hints()
        data = json.loads(result)
        
        assert "total_tools" in data
        assert "categories" in data
        assert "by_category" in data
        assert data["total_tools"] > 0


# ═══════════════════════════════════════════════════════════════════════════════
# HINT REGISTRY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestHintRegistry:
    """Tests for the centralized hint registry."""
    
    def test_tool_hint_dataclass(self):
        """Test ToolHint dataclass."""
        from project_management_automation.resources.hint_registry import ToolHint
        
        hint = ToolHint(
            tool_name="test_tool",
            hint="Test hint description",
            category="testing",
        )
        
        assert hint.tool_name == "test_tool"
        assert hint.hint == "Test hint description"
        assert hint.category == "testing"
    
    def test_tool_hint_to_dict(self):
        """Test ToolHint serialization."""
        from project_management_automation.resources.hint_registry import ToolHint
        
        hint = ToolHint(
            tool_name="test_tool",
            hint="Test hint",
            category="testing",
            outputs=["result"],
        )
        
        data = hint.to_dict()
        
        assert data["tool_name"] == "test_tool"
        assert data["hint"] == "Test hint"
        assert "result" in data["outputs"]
    
    def test_tool_hint_from_dict(self):
        """Test ToolHint deserialization."""
        from project_management_automation.resources.hint_registry import ToolHint
        
        data = {
            "tool_name": "test_tool",
            "hint": "Test hint",
            "category": "testing",
        }
        
        hint = ToolHint.from_dict(data)
        
        assert hint.tool_name == "test_tool"
        assert hint.hint == "Test hint"
    
    def test_get_hint_registry_singleton(self):
        """Test that get_hint_registry returns singleton."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry1 = get_hint_registry()
        registry2 = get_hint_registry()
        
        assert registry1 is registry2
    
    def test_registry_loads_builtin_hints(self):
        """Test that registry loads built-in hints."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        
        assert len(registry.get_all_hints()) > 0
    
    def test_registry_get_hint(self):
        """Test getting a specific hint."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        hint = registry.get_hint("project_scorecard")
        
        assert hint is not None
        assert "scorecard" in hint.hint.lower() or "score" in hint.hint.lower()
    
    def test_registry_get_hint_text(self):
        """Test getting hint text."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        text = registry.get_hint_text("project_scorecard")
        
        assert len(text) > 0
    
    def test_registry_get_hints_by_category(self):
        """Test filtering hints by category."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        security_hints = registry.get_hints_by_category("security")
        
        for name, hint in security_hints.items():
            assert hint.category == "security"
    
    def test_registry_get_compact_hints(self):
        """Test getting compact hints."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        compact = registry.get_compact_hints()
        
        assert isinstance(compact, dict)
        for name, text in compact.items():
            assert isinstance(text, str)
    
    def test_registry_status(self):
        """Test registry status."""
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        status = registry.status()
        
        assert "total_hints" in status
        assert "categories" in status
        assert status["total_hints"] > 0


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-PRIMER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAutoPrimer:
    """Tests for auto-priming functionality."""
    
    def test_detect_agent_type_default(self):
        """Test default agent type detection."""
        from project_management_automation.tools.auto_primer import detect_agent_type
        
        # Without any env vars or config files, should return default
        with patch.dict(os.environ, {}, clear=True):
            result = detect_agent_type()
            
            assert "agent" in result
            assert "source" in result
    
    def test_detect_agent_type_from_env(self):
        """Test agent type detection from environment."""
        from project_management_automation.tools.auto_primer import detect_agent_type
        
        with patch.dict(os.environ, {"EXARP_AGENT": "backend-agent"}):
            result = detect_agent_type()
            
            assert result["agent"] == "backend-agent"
            assert result["source"] == "environment"
    
    def test_suggest_mode_by_time(self):
        """Test time-based mode suggestion."""
        from project_management_automation.tools.auto_primer import suggest_mode_by_time
        
        result = suggest_mode_by_time()
        
        assert "mode" in result
        assert "reason" in result
        assert "confidence" in result
        assert result["mode"] in [
            "daily_checkin", "development", "task_management", "code_review"
        ]
    
    def test_get_agent_context(self):
        """Test getting agent-specific context."""
        from project_management_automation.tools.auto_primer import get_agent_context
        
        result = get_agent_context("backend")
        
        assert "agent" in result
        assert "recommended_mode" in result
        assert "focus_areas" in result
        assert "relevant_tools" in result
    
    def test_auto_prime_returns_json(self):
        """Test that auto_prime returns valid JSON."""
        from project_management_automation.tools.auto_primer import auto_prime
        
        result = auto_prime()
        
        # Should be valid JSON
        data = json.loads(result)
        
        assert "auto_primed" in data
        assert "detection" in data
    
    def test_auto_prime_includes_detection(self):
        """Test that auto_prime includes detection info."""
        from project_management_automation.tools.auto_primer import auto_prime
        
        result = auto_prime()
        data = json.loads(result)
        
        detection = data["detection"]
        assert "agent" in detection
        assert "mode" in detection
        assert "time_of_day" in detection
    
    def test_auto_prime_mode_override(self):
        """Test that mode can be overridden in auto_prime."""
        from project_management_automation.tools.auto_primer import auto_prime
        
        result = auto_prime(override_mode="security_review")
        data = json.loads(result)
        
        assert data["detection"]["mode"] == "security_review"
        assert data["detection"]["mode_source"] == "override"
    
    def test_prime_for_mode(self):
        """Test prime_for_mode helper."""
        from project_management_automation.tools.auto_primer import prime_for_mode
        
        result = prime_for_mode("task_management")
        data = json.loads(result)
        
        assert data["detection"]["mode"] == "task_management"


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT DISCOVERY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPromptDiscovery:
    """Tests for mode-aware prompt discovery."""
    
    def test_prompt_mode_mapping_exists(self):
        """Test that prompt mode mapping exists."""
        from project_management_automation.resources.prompt_discovery import PROMPT_MODE_MAPPING
        
        assert PROMPT_MODE_MAPPING is not None
        assert len(PROMPT_MODE_MAPPING) > 0
        assert "daily_checkin" in PROMPT_MODE_MAPPING
        assert "security_review" in PROMPT_MODE_MAPPING
    
    def test_prompt_persona_mapping_exists(self):
        """Test that prompt persona mapping exists."""
        from project_management_automation.resources.prompt_discovery import PROMPT_PERSONA_MAPPING
        
        assert PROMPT_PERSONA_MAPPING is not None
        assert len(PROMPT_PERSONA_MAPPING) > 0
        assert "developer" in PROMPT_PERSONA_MAPPING
        assert "project_manager" in PROMPT_PERSONA_MAPPING
    
    def test_prompt_descriptions_exist(self):
        """Test that prompt descriptions exist."""
        from project_management_automation.resources.prompt_discovery import PROMPT_DESCRIPTIONS
        
        assert PROMPT_DESCRIPTIONS is not None
        assert len(PROMPT_DESCRIPTIONS) > 0
    
    def test_get_prompts_for_mode(self):
        """Test getting prompts for a mode."""
        from project_management_automation.resources.prompt_discovery import get_prompts_for_mode
        
        result = get_prompts_for_mode("security_review")
        
        assert result["mode"] == "security_review"
        assert "prompts" in result
        assert result["count"] > 0
    
    def test_get_prompts_for_persona(self):
        """Test getting prompts for a persona."""
        from project_management_automation.resources.prompt_discovery import get_prompts_for_persona
        
        result = get_prompts_for_persona("developer")
        
        assert result["persona"] == "developer"
        assert "prompts" in result
        assert result["count"] > 0
    
    def test_get_prompts_for_category(self):
        """Test getting prompts for a category."""
        from project_management_automation.resources.prompt_discovery import get_prompts_for_category
        
        result = get_prompts_for_category("security")
        
        assert result["category"] == "security"
        assert "prompts" in result
    
    def test_get_all_prompts_compact(self):
        """Test getting all prompts in compact format."""
        from project_management_automation.resources.prompt_discovery import get_all_prompts_compact
        
        result = get_all_prompts_compact()
        
        assert "total_prompts" in result
        assert "categories" in result
        assert "by_category" in result
        assert result["total_prompts"] > 0
    
    def test_discover_prompts_with_mode_filter(self):
        """Test discovering prompts with mode filter."""
        from project_management_automation.resources.prompt_discovery import discover_prompts
        
        result = discover_prompts(mode="daily_checkin")
        
        assert "prompts" in result
        assert result["filters_applied"]["mode"] == "daily_checkin"
    
    def test_discover_prompts_with_keyword_filter(self):
        """Test discovering prompts with keyword filter."""
        from project_management_automation.resources.prompt_discovery import discover_prompts
        
        result = discover_prompts(keywords=["security", "scan"])
        
        assert "prompts" in result
        # Should find security-related prompts
        found_security = any("security" in p["name"].lower() for p in result["prompts"])
        assert found_security


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestContextPrimingIntegration:
    """Integration tests for context priming system."""
    
    def test_context_primer_and_hint_registry_sync(self):
        """Test that context primer and hint registry are synchronized."""
        from project_management_automation.resources.context_primer import TOOL_HINTS_REGISTRY
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        registry = get_hint_registry()
        
        # All hints from TOOL_HINTS_REGISTRY should be in registry
        for name in TOOL_HINTS_REGISTRY:
            hint = registry.get_hint(name)
            assert hint is not None, f"Hint {name} not found in registry"
    
    def test_auto_prime_uses_context_primer(self):
        """Test that auto_prime uses context primer."""
        from project_management_automation.tools.auto_primer import auto_prime
        
        result = auto_prime(include_hints=True)
        data = json.loads(result)
        
        # Should have hints from context primer
        assert "hints_count" in data or "top_hints" in data
    
    def test_prompt_discovery_modes_match_workflow_modes(self):
        """Test that prompt discovery modes match workflow modes."""
        from project_management_automation.resources.context_primer import WORKFLOW_MODE_CONTEXT
        from project_management_automation.resources.prompt_discovery import PROMPT_MODE_MAPPING
        
        # All workflow modes should have prompt mappings
        for mode in WORKFLOW_MODE_CONTEXT:
            assert mode in PROMPT_MODE_MAPPING, f"Mode {mode} missing from prompt mapping"
    
    def test_full_context_priming_workflow(self):
        """Test complete context priming workflow."""
        from project_management_automation.tools.auto_primer import auto_prime
        from project_management_automation.resources.prompt_discovery import get_prompts_for_mode
        from project_management_automation.resources.hint_registry import get_hint_registry
        
        # 1. Auto-prime at session start
        primer_result = auto_prime()
        primer_data = json.loads(primer_result)
        
        detected_mode = primer_data["detection"]["mode"]
        
        # 2. Get prompts for detected mode
        prompts = get_prompts_for_mode(detected_mode)
        
        assert prompts["mode"] == detected_mode
        
        # 3. Get hints from registry
        registry = get_hint_registry()
        hints = registry.get_compact_hints()
        
        assert len(hints) > 0
        
        # The workflow should complete without errors
        assert primer_data["auto_primed"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

