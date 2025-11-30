#!/usr/bin/env python3
"""
MCP Client Wrapper

Provides Python interface to MCP servers (Tractatus Thinking, Sequential Thinking, Agentic-Tools).
Uses lazy connection pattern - only connects when actually needed.
"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # Base delay in seconds (exponential backoff)

# Try to import MCP client library
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    logger.warning("MCP client library not available. Install with: pip install mcp>=1.0.0")


class MCPClient:
    """Client for communicating with MCP servers using lazy connection."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.mcp_config_path = project_root / '.cursor' / 'mcp.json'
        # Lazy loading - don't load config until needed
        self._mcp_config: Optional[dict] = None
        self._config_loaded = False
        # Agentic-tools session management
        self.agentic_tools_session = None
        self._agentic_tools_lock = asyncio.Lock() if MCP_CLIENT_AVAILABLE else None

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

    # Agentic-Tools MCP Support
    async def _get_agentic_tools_session(self) -> Optional["ClientSession"]:
        """Get or create agentic-tools MCP session."""
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return None

        if 'agentic-tools' not in self.mcp_config:
            logger.warning("Agentic-tools MCP server not configured in .cursor/mcp.json")
            return None

        # Use lock to ensure thread-safe session creation
        if self._agentic_tools_lock:
            async with self._agentic_tools_lock:
                if self.agentic_tools_session is None:
                    try:
                        # Get agentic-tools config
                        agentic_config = self.mcp_config.get('agentic-tools', {})
                        command = agentic_config.get('command', 'npx')
                        args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

                        # Create stdio client connection
                        server_params = StdioServerParameters(
                            command=command,
                            args=args
                        )

                        # Create session (will be managed by context manager in methods)
                        # Note: We'll create a new session for each operation to avoid connection issues
                        # In production, you might want to implement connection pooling
                        logger.info("Creating agentic-tools MCP session")
                        return None  # Will create session in each method call
                    except Exception as e:
                        logger.error(f"Failed to create agentic-tools session: {e}")
                        return None
                return self.agentic_tools_session
        return None

    async def list_todos(self, project_id: str, working_directory: str) -> List[Dict]:
        """
        List todos using agentic-tools MCP.
        
        Args:
            project_id: The project ID to list todos for
            working_directory: The working directory for the project
            
        Returns:
            List of task dictionaries
        """
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return []

        try:
            # Get agentic-tools config
            agentic_config = self.mcp_config.get('agentic-tools', {})
            command = agentic_config.get('command', 'npx')
            args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

            # Create stdio client connection
            server_params = StdioServerParameters(
                command=command,
                args=args
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call list_todos tool
                    result = await session.call_tool("list_todos", {
                        "workingDirectory": working_directory,
                        "projectId": project_id
                    })

                    # Parse JSON response
                    if result.content and len(result.content) > 0:
                        response_text = result.content[0].text
                        # The response should be JSON, parse it
                        try:
                            response_data = json.loads(response_text)
                            # Extract tasks from response (structure may vary)
                            if isinstance(response_data, list):
                                return response_data
                            elif isinstance(response_data, dict):
                                # Try common response formats
                                return response_data.get('todos', response_data.get('tasks', []))
                            return []
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse agentic-tools response: {response_text}")
                            return []
                    return []
        except Exception as e:
            logger.error(f"Failed to list todos via agentic-tools MCP: {e}", exc_info=True)
            return []

    async def create_task(
        self,
        project_id: str,
        working_directory: str,
        name: str,
        details: str,
        **kwargs
    ) -> Optional[Dict]:
        """
        Create task using agentic-tools MCP.
        
        Args:
            project_id: The project ID
            working_directory: The working directory for the project
            name: Task name
            details: Task details/description
            **kwargs: Additional task parameters (priority, tags, etc.)
            
        Returns:
            Created task dictionary or None on failure
        """
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return None

        try:
            # Get agentic-tools config
            agentic_config = self.mcp_config.get('agentic-tools', {})
            command = agentic_config.get('command', 'npx')
            args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

            # Create stdio client connection
            server_params = StdioServerParameters(
                command=command,
                args=args
            )

            # Prepare task data
            task_data = {
                "workingDirectory": working_directory,
                "projectId": project_id,
                "name": name,
                "details": details,
                **kwargs
            }

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call create_task tool
                    result = await session.call_tool("create_task", task_data)

                    # Parse JSON response
                    if result.content and len(result.content) > 0:
                        response_text = result.content[0].text
                        try:
                            return json.loads(response_text)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse create_task response: {response_text}")
                            return None
                    return None
        except Exception as e:
            logger.error(f"Failed to create task via agentic-tools MCP: {e}", exc_info=True)
            return None

    async def update_task(
        self,
        task_id: str,
        working_directory: str,
        **updates
    ) -> Optional[Dict]:
        """
        Update task using agentic-tools MCP.
        
        Args:
            task_id: The task ID to update
            working_directory: The working directory for the project
            **updates: Task fields to update (name, details, status, priority, etc.)
            
        Returns:
            Updated task dictionary or None on failure
        """
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return None

        try:
            # Get agentic-tools config
            agentic_config = self.mcp_config.get('agentic-tools', {})
            command = agentic_config.get('command', 'npx')
            args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

            # Create stdio client connection
            server_params = StdioServerParameters(
                command=command,
                args=args
            )

            # Prepare update data
            update_data = {
                "workingDirectory": working_directory,
                "id": task_id,
                **updates
            }

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call update_task tool
                    result = await session.call_tool("update_task", update_data)

                    # Parse JSON response
                    if result.content and len(result.content) > 0:
                        response_text = result.content[0].text
                        try:
                            return json.loads(response_text)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse update_task response: {response_text}")
                            return None
                    return None
        except Exception as e:
            logger.error(f"Failed to update task via agentic-tools MCP: {e}", exc_info=True)
            return None

    async def get_task(self, task_id: str, working_directory: str) -> Optional[Dict]:
        """
        Get task details using agentic-tools MCP.
        
        Args:
            task_id: The task ID
            working_directory: The working directory for the project
            
        Returns:
            Task dictionary or None on failure
        """
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return None

        try:
            # Get agentic-tools config
            agentic_config = self.mcp_config.get('agentic-tools', {})
            command = agentic_config.get('command', 'npx')
            args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

            # Create stdio client connection
            server_params = StdioServerParameters(
                command=command,
                args=args
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call get_task tool
                    result = await session.call_tool("get_task", {
                        "workingDirectory": working_directory,
                        "id": task_id
                    })

                    # Parse JSON response
                    if result.content and len(result.content) > 0:
                        response_text = result.content[0].text
                        try:
                            return json.loads(response_text)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse get_task response: {response_text}")
                            return None
                    return None
        except Exception as e:
            logger.error(f"Failed to get task via agentic-tools MCP: {e}", exc_info=True)
            return None

    async def delete_task(self, task_id: str, working_directory: str) -> bool:
        """
        Delete task using agentic-tools MCP.
        
        Args:
            task_id: The task ID to delete
            working_directory: The working directory for the project
            
        Returns:
            True if successful, False otherwise
        """
        if not MCP_CLIENT_AVAILABLE:
            logger.warning("MCP client library not available")
            return False

        try:
            # Get agentic-tools config
            agentic_config = self.mcp_config.get('agentic-tools', {})
            command = agentic_config.get('command', 'npx')
            args = agentic_config.get('args', ['-y', '@modelcontextprotocol/server-agentic-tools'])

            # Create stdio client connection
            server_params = StdioServerParameters(
                command=command,
                args=args
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call delete_task tool
                    result = await session.call_tool("delete_task", {
                        "workingDirectory": working_directory,
                        "id": task_id
                    })

                    # Check if successful (response format may vary)
                    return result.content is not None and len(result.content) > 0
        except Exception as e:
            logger.error(f"Failed to delete task via agentic-tools MCP: {e}", exc_info=True)
            return False


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
