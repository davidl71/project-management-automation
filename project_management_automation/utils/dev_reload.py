"""
Development hot-reload utility for Exarp MCP server.

Allows reloading Python modules without restarting Cursor.
Only available when EXARP_DEV_MODE=1 is set.

Usage:
    # Enable dev mode in MCP config:
    "env": {"EXARP_DEV_MODE": "1"}
    
    # Then call the reload tool:
    /exarp/dev_reload
"""

import importlib
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .logging_config import get_logger

logger = get_logger(__name__)


def is_dev_mode() -> bool:
    """Check if development mode is enabled."""
    return os.environ.get("EXARP_DEV_MODE", "").lower() in ("1", "true", "yes")


def get_package_modules(package_name: str = "project_management_automation") -> List[str]:
    """
    Get all loaded modules from a package.
    
    Args:
        package_name: Name of the package to find modules for
        
    Returns:
        List of module names that are part of the package
    """
    return [
        name for name in sys.modules.keys()
        if name.startswith(package_name)
    ]


def reload_module(module_name: str) -> Dict[str, Any]:
    """
    Reload a single module.
    
    Args:
        module_name: Full module name to reload
        
    Returns:
        Dict with reload status
    """
    try:
        if module_name not in sys.modules:
            return {
                "module": module_name,
                "status": "skipped",
                "reason": "not loaded"
            }
        
        module = sys.modules[module_name]
        importlib.reload(module)
        
        return {
            "module": module_name,
            "status": "reloaded",
            "file": getattr(module, "__file__", None)
        }
        
    except Exception as e:
        return {
            "module": module_name,
            "status": "error",
            "error": str(e)
        }


def reload_all_modules(package_name: str = "project_management_automation") -> Dict[str, Any]:
    """
    Reload all modules from a package in dependency order.
    
    This function:
    1. Finds all loaded modules from the package
    2. Sorts them by depth (deepest first) to handle dependencies
    3. Reloads each module
    
    Args:
        package_name: Package to reload
        
    Returns:
        Dict with reload results
    """
    if not is_dev_mode():
        return {
            "success": False,
            "error": "Dev mode not enabled. Set EXARP_DEV_MODE=1 in environment.",
            "hint": "Add to MCP config: \"env\": {\"EXARP_DEV_MODE\": \"1\"}"
        }
    
    start_time = datetime.now()
    
    # Get all package modules
    modules = get_package_modules(package_name)
    
    if not modules:
        return {
            "success": False,
            "error": f"No modules found for package: {package_name}"
        }
    
    # Sort by depth (deepest first) to handle dependencies correctly
    # e.g., reload project_management_automation.tools.wisdom.sources
    # before project_management_automation.tools.wisdom
    modules_sorted = sorted(modules, key=lambda x: x.count('.'), reverse=True)
    
    results = []
    reloaded = 0
    errors = 0
    skipped = 0
    
    for module_name in modules_sorted:
        result = reload_module(module_name)
        results.append(result)
        
        if result["status"] == "reloaded":
            reloaded += 1
        elif result["status"] == "error":
            errors += 1
            logger.warning(f"Failed to reload {module_name}: {result.get('error')}")
        else:
            skipped += 1
    
    duration = (datetime.now() - start_time).total_seconds()
    
    return {
        "success": errors == 0,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration,
        "summary": {
            "total_modules": len(modules),
            "reloaded": reloaded,
            "errors": errors,
            "skipped": skipped
        },
        "modules": results if errors > 0 else None,  # Only show details if errors
        "message": f"Reloaded {reloaded} modules in {duration:.2f}s" + (
            f" ({errors} errors)" if errors else ""
        )
    }


def reload_specific_modules(module_names: List[str]) -> Dict[str, Any]:
    """
    Reload specific modules by name.
    
    Args:
        module_names: List of module names to reload
        
    Returns:
        Dict with reload results
    """
    if not is_dev_mode():
        return {
            "success": False,
            "error": "Dev mode not enabled. Set EXARP_DEV_MODE=1 in environment."
        }
    
    results = []
    for name in module_names:
        # Allow shorthand names
        if not name.startswith("project_management_automation"):
            name = f"project_management_automation.{name}"
        
        result = reload_module(name)
        results.append(result)
    
    reloaded = sum(1 for r in results if r["status"] == "reloaded")
    errors = sum(1 for r in results if r["status"] == "error")
    
    return {
        "success": errors == 0,
        "summary": {
            "requested": len(module_names),
            "reloaded": reloaded,
            "errors": errors
        },
        "modules": results
    }


def get_module_info() -> Dict[str, Any]:
    """
    Get information about loaded package modules.
    
    Returns:
        Dict with module information
    """
    modules = get_package_modules()
    
    module_info = []
    for name in sorted(modules):
        module = sys.modules.get(name)
        if module:
            file_path = getattr(module, "__file__", None)
            mtime = None
            if file_path and Path(file_path).exists():
                mtime = datetime.fromtimestamp(
                    Path(file_path).stat().st_mtime
                ).isoformat()
            
            module_info.append({
                "name": name,
                "file": file_path,
                "modified": mtime
            })
    
    return {
        "dev_mode": is_dev_mode(),
        "total_modules": len(modules),
        "modules": module_info
    }


__all__ = [
    'is_dev_mode',
    'reload_all_modules',
    'reload_specific_modules',
    'reload_module',
    'get_module_info',
]

