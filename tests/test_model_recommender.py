"""
Unit Tests for Model Recommender Tool

Tests for model_recommender.py module (0% coverage → target: 80%+).
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestModelRecommender:
    """Tests for AI model recommendation."""

    def test_recommend_model_by_task_description(self):
        """Test model recommendation based on task description."""
        from project_management_automation.tools.model_recommender import recommend_model

        # Test architecture task
        result_str = recommend_model(task_description="architecture design", optimize_for="quality")
        result = json.loads(result_str)
        assert result['success'] is True
        assert 'recommended_model' in result['data']
        assert 'confidence' in result['data']

    def test_recommend_model_by_keywords(self):
        """Test model recommendation based on keywords in description."""
        from project_management_automation.tools.model_recommender import recommend_model

        # Test with keywords in description
        result_str = recommend_model(task_description="refactor multi-file complex codebase")
        result = json.loads(result_str)
        assert result['success'] is True
        assert 'recommended_model' in result['data']

    def test_recommend_model_optimize_for(self):
        """Test model recommendation with different optimization goals."""
        from project_management_automation.tools.model_recommender import recommend_model

        # Test speed optimization
        result_str = recommend_model(task_description="quick fix", optimize_for="speed")
        result = json.loads(result_str)
        assert result['success'] is True
        assert result['data']['optimization'] == "speed"
        
        # Test cost optimization
        result_str_cost = recommend_model(task_description="simple task", optimize_for="cost")
        result_cost = json.loads(result_str_cost)
        assert result_cost['success'] is True

    def test_recommend_model_with_alternatives(self):
        """Test model recommendation includes alternatives."""
        from project_management_automation.tools.model_recommender import recommend_model

        result_str = recommend_model(task_description="complex task", include_alternatives=True)
        result = json.loads(result_str)
        assert result['success'] is True
        assert 'alternatives' in result['data']

    def test_list_available_models(self):
        """Test listing all available models."""
        from project_management_automation.tools.model_recommender import list_available_models

        result_str = list_available_models()
        result = json.loads(result_str)
        assert result['success'] is True
        assert 'models' in result['data']
        assert len(result['data']['models']) > 0

    def test_model_recommendations_structure(self):
        """Test MODEL_RECOMMENDATIONS structure."""
        from project_management_automation.tools.model_recommender import MODEL_RECOMMENDATIONS

        assert isinstance(MODEL_RECOMMENDATIONS, dict)
        assert len(MODEL_RECOMMENDATIONS) > 0
        
        # Check structure of first model
        first_model = list(MODEL_RECOMMENDATIONS.values())[0]
        assert 'name' in first_model
        assert 'best_for' in first_model
        assert 'keywords' in first_model
