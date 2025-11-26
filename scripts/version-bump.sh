#!/bin/bash
# Version bump and tag script for Exarp
#
# Usage:
#   ./scripts/version-bump.sh patch    # 0.1.15 -> 0.1.16
#   ./scripts/version-bump.sh minor    # 0.1.15 -> 0.2.0
#   ./scripts/version-bump.sh major    # 0.1.15 -> 1.0.0
#   ./scripts/version-bump.sh          # Show current version

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="$PROJECT_ROOT/project_management_automation/version.py"

# Get current version
get_current_version() {
    grep 'BASE_VERSION = "' "$VERSION_FILE" | head -1 | sed 's/.*BASE_VERSION = "\([0-9.]*\)".*/\1/'
}

# Parse version into components
parse_version() {
    local version="$1"
    echo "$version" | sed 's/\./ /g'
}

# Bump version
bump_version() {
    local current="$1"
    local part="$2"
    
    read -r major minor patch <<< "$(parse_version "$current")"
    
    case "$part" in
        major)
            echo "$((major + 1)).0.0"
            ;;
        minor)
            echo "$major.$((minor + 1)).0"
            ;;
        patch)
            echo "$major.$minor.$((patch + 1))"
            ;;
        *)
            echo "Invalid part: $part" >&2
            exit 1
            ;;
    esac
}

# Update version in version.py
update_version_file() {
    local new_version="$1"
    sed -i.bak "s/BASE_VERSION = \"[^\"]*\"/BASE_VERSION = \"$new_version\"/" "$VERSION_FILE"
    rm -f "$VERSION_FILE.bak"
}

# Main
main() {
    local part="${1:-}"
    local current_version
    current_version="$(get_current_version)"
    
    if [ -z "$part" ]; then
        echo "Current version: $current_version"
        echo ""
        echo "Usage: $0 [patch|minor|major]"
        echo ""
        echo "Examples:"
        echo "  $0 patch  # $current_version -> $(bump_version "$current_version" patch)"
        echo "  $0 minor  # $current_version -> $(bump_version "$current_version" minor)"
        echo "  $0 major  # $current_version -> $(bump_version "$current_version" major)"
        exit 0
    fi
    
    local new_version
    new_version="$(bump_version "$current_version" "$part")"
    
    echo "Bumping version: $current_version -> $new_version"
    
    # Update version file
    update_version_file "$new_version"
    echo "✅ Updated $VERSION_FILE"
    
    # Stage the change
    git add "$VERSION_FILE"
    
    # Commit
    git commit -m "chore: bump version to $new_version"
    echo "✅ Committed version bump"
    
    # Create tag
    git tag -a "v$new_version" -m "Release v$new_version"
    echo "✅ Created tag v$new_version"
    
    echo ""
    echo "Next steps:"
    echo "  git push origin main"
    echo "  git push origin v$new_version"
    echo ""
    echo "Or push both:"
    echo "  git push origin main --tags"
}

main "$@"

