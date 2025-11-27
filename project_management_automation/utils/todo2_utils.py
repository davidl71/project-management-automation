"""
Todo2 utilities for project-scoped automation.

Encapsulates helpers that:
- infer the git-backed project ID (owner/repo) for Todo2 ownership metadata,
- filter task lists to the current project ID, and
- annotate tasks with ownership metadata.
"""

import logging
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional

# Remove circular import
# from . import find_project_root

logger = logging.getLogger(__name__)


def _normalize_git_remote(url: str) -> Optional[str]:
    """Normalize git remote to owner/repo format."""
    if not url:
        return None

    url = url.strip()
    if url.endswith(".git"):
        url = url[: -len(".git")]

    if url.startswith("git@"):
        # git@github.com:owner/repo
        parts = url.split(":", 1)
        if len(parts) == 2:
            return parts[1]
    elif "://" in url:
        # https://github.com/owner/repo
        parts = url.split("://", 1)[1].split("/")
        if len(parts) >= 2:
            return "/".join(parts[1:3])

    # Fallback for other formats
    if "/" in url:
        return "/".join(url.split("/")[-2:])
    return None


def get_repo_project_id(project_root: Optional[Path] = None) -> Optional[str]:
    """Return the git owner/repo identifier for the current project."""
    # Local import to avoid circular dependency
    from . import find_project_root
    root = find_project_root(project_root)
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        return _normalize_git_remote(result.stdout)
    except subprocess.CalledProcessError as exc:
        logger.debug("Could not read git remote: %s", exc)
        return None
    except FileNotFoundError:
        logger.debug("Git executable not found while determining project ID")
        return None


def task_belongs_to_project(task: dict, project_id: Optional[str]) -> bool:
    """Return True if the task is owned by the given project_id."""
    if not project_id:
        return True

    task_project = task.get("project_id")
    if not task_project:
        return True

    return task_project == project_id


def filter_tasks_by_project(
    tasks: Iterable[dict],
    project_id: Optional[str],
    include_unassigned: bool = True,
    logger: Optional[logging.Logger] = None,
) -> List[dict]:
    """Return only the tasks that belong to the requested project."""
    filtered = []
    for task in tasks:
        task_project = task.get("project_id")
        if task_project:
            if project_id and task_project != project_id:
                if logger:
                    logger.debug("Skipping task %s owned by %s", task.get("id"), task_project)
                continue
        elif not include_unassigned and project_id:
            if logger:
                logger.debug("Skipping unassigned task %s", task.get("id"))
            continue
        filtered.append(task)
    return filtered


def annotate_task_project(task: dict, project_id: Optional[str]) -> dict:
    """Ensure the task has ownership metadata."""
    if project_id:
        task["project_id"] = project_id
    return task


__all__ = [
    "get_repo_project_id",
    "task_belongs_to_project",
    "filter_tasks_by_project",
    "annotate_task_project",
]

