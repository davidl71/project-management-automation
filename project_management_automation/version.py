"""
Dynamic versioning for Exarp.

Version formats (PEP 440 compliant):
- Release:  X.Y.Z                    (from git tag vX.Y.Z)
- Dev:      X.Y.Z.devEPOCH+gCOMMIT   (dev version with epoch and commit)
- Nightly:  X.Y.Z.postEPOCH          (nightly/CI builds)

Version is determined by:
1. Git tag (if on a tag): exact version from tag
2. Environment variable EXARP_VERSION_TYPE: 'release', 'dev', 'nightly'
3. Default: dev version with epoch timestamp

Usage:
    from project_management_automation.version import __version__, get_version_info
    print(__version__)  # Dynamic version string
"""

import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# Base version - increment this for releases
# Format: MAJOR.MINOR.PATCH
BASE_VERSION = "0.1.17"


def get_epoch() -> int:
    """Get current Unix epoch timestamp."""
    return int(time.time())


def get_git_info() -> Dict[str, Optional[str]]:
    """
    Get git information for versioning.
    
    Returns:
        Dict with keys: tag, commit, branch, dirty
    """
    info = {
        'tag': None,
        'commit': None,
        'branch': None,
        'dirty': False,
        'commits_since_tag': 0,
    }
    
    try:
        # Check if we're in a git repo
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return info
        
        # Get current commit
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['commit'] = result.stdout.strip()
        
        # Get current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['branch'] = result.stdout.strip() or 'HEAD'
        
        # Check if dirty (uncommitted changes)
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['dirty'] = bool(result.stdout.strip())
        
        # Get tag on current commit (if any)
        result = subprocess.run(
            ['git', 'describe', '--tags', '--exact-match', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['tag'] = result.stdout.strip()
        
        # Get commits since last tag
        result = subprocess.run(
            ['git', 'describe', '--tags', '--long'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Format: v0.1.14-5-g1234567
            match = re.match(r'v?(\d+\.\d+\.\d+)-(\d+)-g([a-f0-9]+)', result.stdout.strip())
            if match:
                info['commits_since_tag'] = int(match.group(2))
        
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    
    return info


def parse_tag_version(tag: str) -> Optional[str]:
    """
    Parse version from git tag.
    
    Args:
        tag: Git tag (e.g., 'v0.1.15', '0.1.15')
        
    Returns:
        Version string or None if not a version tag
    """
    if not tag:
        return None
    
    # Strip 'v' prefix if present
    version = tag.lstrip('v')
    
    # Validate it's a proper version
    if re.match(r'^\d+\.\d+\.\d+$', version):
        return version
    
    return None


def get_version_type() -> str:
    """
    Determine version type from environment or git state.
    
    Returns:
        'release', 'dev', or 'nightly'
    """
    # Check environment variable first
    env_type = os.environ.get('EXARP_VERSION_TYPE', '').lower()
    if env_type in ('release', 'dev', 'nightly'):
        return env_type
    
    # Check if we're on a release tag
    git_info = get_git_info()
    if git_info['tag'] and not git_info['dirty']:
        tag_version = parse_tag_version(git_info['tag'])
        if tag_version:
            return 'release'
    
    # Check for CI/CD environment
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        # Nightly if scheduled, dev otherwise
        if os.environ.get('GITHUB_EVENT_NAME') == 'schedule':
            return 'nightly'
    
    # Default to dev
    return 'dev'


def get_version(version_type: Optional[str] = None) -> str:
    """
    Get the full version string.
    
    Args:
        version_type: Override version type ('release', 'dev', 'nightly')
        
    Returns:
        Full version string (PEP 440 compliant)
    """
    if version_type is None:
        version_type = get_version_type()
    
    git_info = get_git_info()
    
    # Release version: use tag or base version
    if version_type == 'release':
        if git_info['tag']:
            tag_version = parse_tag_version(git_info['tag'])
            if tag_version:
                return tag_version
        return BASE_VERSION
    
    # Dev version: base.devEPOCH
    if version_type == 'dev':
        epoch = get_epoch()
        version = f"{BASE_VERSION}.dev{epoch}"
        
        # Add commit hash if available
        if git_info['commit']:
            version = f"{version}+g{git_info['commit']}"
        
        # Add dirty marker
        if git_info['dirty']:
            version = f"{version}.dirty" if '+' in version else f"{version}+dirty"
        
        return version
    
    # Nightly version: base.nEPOCH (using 'n' for nightly, PEP 440 post-release)
    if version_type == 'nightly':
        epoch = get_epoch()
        # Use .post for nightly to be PEP 440 compliant
        return f"{BASE_VERSION}.post{epoch}"
    
    return BASE_VERSION


def get_version_info() -> Dict[str, any]:
    """
    Get comprehensive version information.
    
    Returns:
        Dict with version details
    """
    git_info = get_git_info()
    version_type = get_version_type()
    
    return {
        'version': get_version(version_type),
        'base_version': BASE_VERSION,
        'version_type': version_type,
        'epoch': get_epoch(),
        'timestamp': datetime.now().isoformat(),
        'git': {
            'tag': git_info['tag'],
            'commit': git_info['commit'],
            'branch': git_info['branch'],
            'dirty': git_info['dirty'],
            'commits_since_tag': git_info['commits_since_tag'],
        }
    }


def bump_version(part: str = 'patch') -> str:
    """
    Bump the base version.
    
    Args:
        part: 'major', 'minor', or 'patch'
        
    Returns:
        New version string
    """
    major, minor, patch = map(int, BASE_VERSION.split('.'))
    
    if part == 'major':
        return f"{major + 1}.0.0"
    elif part == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_base_version(new_version: str) -> bool:
    """
    Update BASE_VERSION in this file.
    
    Args:
        new_version: New version string (e.g., '0.1.16')
        
    Returns:
        True if successful
    """
    version_file = Path(__file__)
    content = version_file.read_text()
    
    # Replace BASE_VERSION
    new_content = re.sub(
        r'BASE_VERSION = "0.1.17"]+"',
        f'BASE_VERSION = "0.1.17"',
        content
    )
    
    if new_content != content:
        version_file.write_text(new_content)
        return True
    
    return False


# Module-level version (evaluated at import time)
__version__ = get_version()


# CLI interface
if __name__ == '__main__':
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Exarp version utility')
    parser.add_argument('--type', choices=['release', 'dev', 'nightly'],
                       help='Override version type')
    parser.add_argument('--info', action='store_true',
                       help='Show detailed version info as JSON')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'],
                       help='Bump and update BASE_VERSION')
    parser.add_argument('--base', action='store_true',
                       help='Show only base version')
    
    args = parser.parse_args()
    
    if args.bump:
        new_ver = bump_version(args.bump)
        if update_base_version(new_ver):
            print(f"Updated BASE_VERSION: {BASE_VERSION} -> {new_ver}")
        else:
            print(f"Failed to update BASE_VERSION")
    elif args.info:
        print(json.dumps(get_version_info(), indent=2))
    elif args.base:
        print(BASE_VERSION)
    else:
        print(get_version(args.type))

