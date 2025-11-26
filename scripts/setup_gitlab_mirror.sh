#!/bin/bash
# GitLab Mirror Setup Script
# Creates GitLab projects and configures GitHub secrets for mirroring
#
# Prerequisites:
# 1. GitLab Personal Access Token with: api, write_repository scopes
# 2. GitHub CLI (gh) authenticated
# 3. GitLab group: davidl71-group
#
# Usage:
#   export GITLAB_TOKEN="glpat-xxxxxxxxxxxx"
#   ./setup_gitlab_mirror.sh [repo_name]
#   ./setup_gitlab_mirror.sh --all  # Setup all repos

set -e

# Configuration
GITLAB_GROUP="davidl71-group"
GITLAB_API="https://gitlab.com/api/v4"
GITHUB_USER="davidl71"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repos to mirror (add more as needed)
REPOS=(
    "project-management-automation"
    "ib_box_spread_full_universal"
    "box-spread-cpp"
    "box-spread-python"
    "box-spread-notebooks"
    "trading-mcp-servers"
    "trading-setup-docs"
    "trading-tools-docs"
    "trading-automation-docs"
    "trading-architecture-docs"
    "trading-api-docs"
    "trading-automation-tools"
    "trading-build-tools"
    "homebrew-ib-box-spread"
)

# Check prerequisites
check_prerequisites() {
    if [[ -z "$GITLAB_TOKEN" ]]; then
        echo -e "${RED}Error: GITLAB_TOKEN environment variable not set${NC}"
        echo "Get a token from: https://gitlab.com/-/user_settings/personal_access_tokens"
        echo "Required scopes: api, write_repository"
        echo ""
        echo "Usage: export GITLAB_TOKEN='glpat-xxxx' && $0"
        exit 1
    fi
    
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}Error: GitHub CLI (gh) not installed${NC}"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}Error: GitHub CLI not authenticated${NC}"
        echo "Run: gh auth login"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}Error: jq not installed${NC}"
        echo "Run: brew install jq"
        exit 1
    fi
}

# Get GitLab group ID
get_group_id() {
    local group_id
    group_id=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$GITLAB_API/groups/$GITLAB_GROUP" | jq -r '.id')
    
    if [[ "$group_id" == "null" || -z "$group_id" ]]; then
        echo -e "${RED}Error: Could not find GitLab group: $GITLAB_GROUP${NC}"
        exit 1
    fi
    
    echo "$group_id"
}

# Create GitLab project
create_gitlab_project() {
    local repo_name="$1"
    local group_id="$2"
    local visibility="$3"
    
    echo -e "${YELLOW}Creating GitLab project: $repo_name${NC}"
    
    # Check if project already exists
    local existing
    existing=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$GITLAB_API/groups/$GITLAB_GROUP/projects?search=$repo_name" | \
        jq -r ".[] | select(.name == \"$repo_name\") | .id")
    
    if [[ -n "$existing" ]]; then
        echo -e "${GREEN}  ✓ Project already exists (ID: $existing)${NC}"
        return 0
    fi
    
    # Create project
    local response
    response=$(curl -s --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --header "Content-Type: application/json" \
        --data "{
            \"name\": \"$repo_name\",
            \"namespace_id\": $group_id,
            \"visibility\": \"$visibility\",
            \"initialize_with_readme\": false
        }" \
        "$GITLAB_API/projects")
    
    local project_id
    project_id=$(echo "$response" | jq -r '.id')
    
    if [[ "$project_id" == "null" || -z "$project_id" ]]; then
        echo -e "${RED}  ✗ Failed to create project${NC}"
        echo "$response" | jq .
        return 1
    fi
    
    echo -e "${GREEN}  ✓ Created project (ID: $project_id)${NC}"
}

# Add GitHub secret
add_github_secret() {
    local repo_name="$1"
    
    echo -e "${YELLOW}Adding GITLAB_TOKEN secret to GitHub: $repo_name${NC}"
    
    # Check if secret already exists
    if gh secret list --repo "$GITHUB_USER/$repo_name" 2>/dev/null | grep -q "GITLAB_TOKEN"; then
        echo -e "${GREEN}  ✓ Secret already exists${NC}"
        return 0
    fi
    
    # Add secret
    if echo "$GITLAB_TOKEN" | gh secret set GITLAB_TOKEN --repo "$GITHUB_USER/$repo_name"; then
        echo -e "${GREEN}  ✓ Secret added${NC}"
    else
        echo -e "${RED}  ✗ Failed to add secret${NC}"
        return 1
    fi
}

# Setup single repo
setup_repo() {
    local repo_name="$1"
    local group_id="$2"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Setting up: $repo_name${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    
    # Check if GitHub repo exists and get visibility
    local is_private
    is_private=$(gh repo view "$GITHUB_USER/$repo_name" --json isPrivate --jq '.isPrivate' 2>/dev/null)
    
    if [[ -z "$is_private" ]]; then
        echo -e "${RED}  ✗ GitHub repo not found: $GITHUB_USER/$repo_name${NC}"
        return 1
    fi
    
    local visibility="private"
    if [[ "$is_private" == "false" ]]; then
        visibility="public"
    fi
    
    echo "  GitHub visibility: $visibility"
    
    # Create GitLab project
    create_gitlab_project "$repo_name" "$group_id" "$visibility"
    
    # Add GitHub secret
    add_github_secret "$repo_name"
    
    echo -e "${GREEN}  ✓ Setup complete for $repo_name${NC}"
}

# Main
main() {
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║     GitLab Mirror Setup Script                    ║"
    echo "║     GitHub → GitLab (davidl71-group)              ║"
    echo "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    check_prerequisites
    
    local group_id
    group_id=$(get_group_id)
    echo -e "${GREEN}GitLab Group ID: $group_id${NC}"
    
    if [[ "$1" == "--all" ]]; then
        echo "Setting up all ${#REPOS[@]} repositories..."
        for repo in "${REPOS[@]}"; do
            setup_repo "$repo" "$group_id"
        done
    elif [[ -n "$1" ]]; then
        setup_repo "$1" "$group_id"
    else
        echo ""
        echo "Usage:"
        echo "  $0 <repo_name>   # Setup single repo"
        echo "  $0 --all         # Setup all repos"
        echo ""
        echo "Available repos:"
        for repo in "${REPOS[@]}"; do
            echo "  - $repo"
        done
    fi
    
    echo ""
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║  Next Steps:                                      ║"
    echo "║  1. Commit & push .github/workflows/mirror-to-    ║"
    echo "║     gitlab.yml and .gitlab-ci.yml to each repo    ║"
    echo "║  2. Check GitHub Actions for mirror sync          ║"
    echo "║  3. Check GitLab for security scan results        ║"
    echo "╚═══════════════════════════════════════════════════╝"
}

main "$@"

