#!/usr/bin/env python3
"""
MCP Client Wrapper

Provides Python interface to MCP servers (Tractatus Thinking, Sequential Thinking).
Uses lazy connection pattern - only connects when actually needed.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # Base delay in seconds (exponential backoff)


class MCPClient:
    """Client for communicating with MCP servers using lazy connection."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.mcp_config_path = project_root / '.cursor' / 'mcp.json'
        # Lazy loading - don't load config until needed
        self._mcp_config: Optional[dict] = None
        self._config_loaded = False

    @property
    def mcp_config(self) -> dict:
        """Lazy load MCP config on first access."""
        if not self._config_loaded:
            self._mcp_config = self._load_mcp_config_with_retry()
            self._config_loaded = True
        return self._mcp_config or {}

    def _load_mcp_config_with_retry(self) -> dict:
        """Load MCP server configuration with retry logic."""
        for attempt in range(MAX_RETRIES):
            if not self.mcp_config_path.exists():
                if attempt < MAX_RETRIES - 1:
                    logger.debug(f"MCP config not found, retry {attempt + 1}/{MAX_RETRIES}")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                logger.info("MCP config not found, using fallback mode")
                return {}

            try:
                with open(self.mcp_config_path) as f:
                    config = json.load(f)
                    return config.get('mcpServers', {})
            except json.JSONDecodeError as e:
                # File might be partially written - retry
                if attempt < MAX_RETRIES - 1:
                    logger.debug(f"MCP config parse error, retry {attempt + 1}/{MAX_RETRIES}: {e}")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    logger.warning(f"Failed to parse MCP config after {MAX_RETRIES} attempts: {e}")
                    return {}
            except Exception as e:
                logger.warning(f"Failed to load MCP config: {e}")
                return {}
        return {}

    def call_tractatus_thinking(self, operation: str, **kwargs) -> Optional[dict]:
        """Call Tractatus Thinking MCP server."""
        if 'tractatus_thinking' not in self.mcp_config:
            logger.warning("Tractatus Thinking MCP server not configured")
            return None

        try:
            # For now, return a simplified response
            # In a full implementation, this would communicate with the MCP server
            # via stdio or HTTP
            logger.info(f"Tractatus Thinking: {operation}")

            # Simplified response structure
            if operation == "start":
                concept = kwargs.get('concept', '')
                return {
                    'session_id': f"tractatus_{hash(concept)}",
                    'concept': concept,
                    'components': self._extract_components_simple(concept)
                }

            return None
        except Exception as e:
            logger.warning(f"Tractatus Thinking call failed: {e}")
            return None

    def call_sequential_thinking(self, operation: str, **kwargs) -> Optional[dict]:
        """Call Sequential Thinking MCP server."""
        if 'sequential_thinking' not in self.mcp_config:
            logger.warning("Sequential Thinking MCP server not configured")
            return None

        try:
            logger.info(f"Sequential Thinking: {operation}")

            # Simplified response structure
            if operation == "start":
                problem = kwargs.get('problem', '')
                return {
                    'session_id': f"sequential_{hash(problem)}",
                    'problem': problem,
                    'steps': self._plan_steps_simple(problem)
                }

            return None
        except Exception as e:
            logger.warning(f"Sequential Thinking call failed: {e}")
            return None

    def _extract_components_simple(self, concept: str) -> list[str]:
        """Simple component extraction (fallback)."""
        # Look for × or * patterns indicating components
        components = []

        if '×' in concept or '*' in concept:
            # Split by × or *
            parts = concept.replace('×', '*').split('*')
            components = [p.strip() for p in parts if p.strip()]
        else:
            # Extract keywords
            keywords = ['automation', 'analysis', 'validation', 'monitoring',
                       'tracking', 'synchronization', 'health', 'alignment']
            components = [kw for kw in keywords if kw in concept.lower()]

        return components if components else ['general']

    def _plan_steps_simple(self, problem: str) -> list[str]:
        """Simple step planning (fallback)."""
        steps = [
            "Load and analyze data",
            "Identify patterns and opportunities",
            "Generate recommendations",
            "Create follow-up tasks"
        ]

        # Customize based on problem keywords
        if 'find' in problem.lower() or 'discover' in problem.lower():
            steps = [
                "Search for opportunities",
                "Analyze and score findings",
                "Prioritize recommendations",
                "Create implementation tasks"
            ]
        elif 'check' in problem.lower() or 'validate' in problem.lower():
            steps = [
                "Load data to validate",
                "Run validation checks",
                "Identify issues",
                "Generate fix recommendations"
            ]

        return steps


# Global MCP client instance
_mcp_client = None

def get_mcp_client(project_root: Path) -> MCPClient:
    """Get or create MCP client instance."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient(project_root)
    return _mcp_client


def load_json_with_retry(
    file_path: Path,
    max_retries: int = MAX_RETRIES,
    retry_delay: float = RETRY_DELAY,
    default: Any = None
) -> Any:
    """
    Load JSON file with retry logic for race conditions.

    Handles cases where file is being written by another process
    (e.g., another MCP server updating its state file).

    Args:
        file_path: Path to JSON file
        max_retries: Maximum number of retry attempts
        retry_delay: Base delay between retries (exponential backoff)
        default: Default value if file cannot be loaded

    Returns:
        Parsed JSON data or default value
    """
    for attempt in range(max_retries):
        if not file_path.exists():
            if attempt < max_retries - 1:
                logger.debug(f"File not found, retry {attempt + 1}/{max_retries}: {file_path}")
                time.sleep(retry_delay * (attempt + 1))
                continue
            logger.debug(f"File not found after {max_retries} attempts: {file_path}")
            return default

        try:
            with open(file_path) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # File might be partially written - retry
            if attempt < max_retries - 1:
                logger.debug(f"JSON parse error, retry {attempt + 1}/{max_retries}: {e}")
                time.sleep(retry_delay * (attempt + 1))
            else:
                logger.warning(f"Failed to parse JSON after {max_retries} attempts: {file_path}")
                return default
        except PermissionError as e:
            # File might be locked by another process - retry
            if attempt < max_retries - 1:
                logger.debug(f"File locked, retry {attempt + 1}/{max_retries}: {e}")
                time.sleep(retry_delay * (attempt + 1))
            else:
                logger.warning(f"File permission error after {max_retries} attempts: {file_path}")
                return default
        except Exception as e:
            logger.warning(f"Unexpected error loading {file_path}: {e}")
            return default

    return default
