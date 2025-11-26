"""
MCP Resource Handlers for Project Management Automation

These modules provide resource access for automation status, history, and metadata.

Resources:
- Static: status, tasks, cache, catalog, history, memories
- Dynamic (templates): tasks://{id}, advisor://{id}, memory://{id}
"""

from .templates import (
    register_resource_templates,
    get_task_by_id,
    get_tasks_by_status,
    get_tasks_by_tag,
    get_tasks_by_priority,
    get_advisor_consultations,
    get_advisor_info,
    get_memory_by_id,
    get_memories_by_category,
)

__all__ = [
    # Registration
    "register_resource_templates",
    # Task resources
    "get_task_by_id",
    "get_tasks_by_status",
    "get_tasks_by_tag",
    "get_tasks_by_priority",
    # Advisor resources
    "get_advisor_consultations",
    "get_advisor_info",
    # Memory resources
    "get_memory_by_id",
    "get_memories_by_category",
]
