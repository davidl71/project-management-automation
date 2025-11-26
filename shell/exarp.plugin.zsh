# Exarp ZSH Plugin
# Source this file or add to your .zshrc:
#   source /path/to/exarp.plugin.zsh
# Or symlink to ~/.oh-my-zsh/custom/plugins/exarp/exarp.plugin.zsh
#
# Features:
#   - Context-aware project detection
#   - MOTD with project health + wisdom
#   - Prompt indicator showing project score
#   - Multi-project summary for parent directories

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# EXARP_MOTD=1           # Show MOTD on shell start (score|overview|wisdom)
# EXARP_PROMPT=1         # Show project health in prompt
# EXARP_CACHE_TTL=300    # Cache TTL in seconds (default: 5 min)

EXARP_CACHE_DIR="${EXARP_CACHE_DIR:-/tmp/exarp_cache}"
mkdir -p "$EXARP_CACHE_DIR" 2>/dev/null

# ═══════════════════════════════════════════════════════════════
# ALIASES
# ═══════════════════════════════════════════════════════════════

alias exarp="python -m project_management_automation.server"
alias pma="python -m project_management_automation.server"

# Quick tools
alias exarp-score="python -m project_management_automation.tools.project_scorecard"
alias exarp-health="python -m project_management_automation.tools.docs_health"
alias exarp-align="python -m project_management_automation.tools.todo2_alignment"
alias exarp-dups="python -m project_management_automation.tools.duplicate_detection"
alias exarp-sec="python -m project_management_automation.tools.dependency_security"
alias exarp-tags="python -m project_management_automation.tools.tag_consolidation"
alias exarp-overview="python -m project_management_automation.tools.project_overview"

# Even shorter
alias xs="exarp-score"
alias xh="exarp-health"
alias xo="exarp-overview"
alias xc="exarp-context"
alias xp="exarp-projects"

# ═══════════════════════════════════════════════════════════════
# CONTEXT DETECTION
# ═══════════════════════════════════════════════════════════════

# Check if directory is an exarp-compatible project
_exarp_is_project() {
    local dir="${1:-.}"
    [[ -f "$dir/.todo2/state.todo2.json" ]] || \
    [[ -f "$dir/pyproject.toml" && -d "$dir/project_management_automation" ]] || \
    [[ -f "$dir/.git" || -d "$dir/.git" ]] && [[ -f "$dir/pyproject.toml" || -f "$dir/package.json" || -f "$dir/Cargo.toml" ]]
}

# Get project name from directory
_exarp_project_name() {
    local dir="${1:-.}"
    local name=""
    if [[ -f "$dir/pyproject.toml" ]]; then
        name=$(python3 -c "
import re
with open('$dir/pyproject.toml') as f:
    content = f.read()
match = re.search(r'^name\s*=\s*[\"\\']([^\"\\']+)[\"\\']', content, re.MULTILINE)
print(match.group(1) if match else '')
" 2>/dev/null)
    elif [[ -f "$dir/package.json" ]]; then
        name=$(python3 -c "import json; print(json.load(open('$dir/package.json')).get('name',''))" 2>/dev/null)
    elif [[ -f "$dir/Cargo.toml" ]]; then
        name=$(python3 -c "
import re
with open('$dir/Cargo.toml') as f:
    content = f.read()
match = re.search(r'^name\s*=\s*[\"\\']([^\"\\']+)[\"\\']', content, re.MULTILINE)
print(match.group(1) if match else '')
" 2>/dev/null)
    fi
    
    if [[ -z "$name" ]]; then
        basename "$(realpath "$dir")"
    else
        echo "$name"
    fi
}

# Get cached score or compute new one
_exarp_get_score() {
    local dir="${1:-.}"
    local cache_file="$EXARP_CACHE_DIR/score_$(echo "$dir" | md5sum | cut -c1-8)"
    local cache_ttl="${EXARP_CACHE_TTL:-300}"
    
    # Check cache
    if [[ -f "$cache_file" ]]; then
        local cache_age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file" 2>/dev/null)))
        if (( cache_age < cache_ttl )); then
            cat "$cache_file"
            return
        fi
    fi
    
    # Compute score
    local score
    if [[ -f "$dir/.todo2/state.todo2.json" ]]; then
        score=$(cd "$dir" && python3 -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
try:
    result = generate_project_scorecard(output_format='json', include_recommendations=False)
    print(int(result.get('overall_score', 0)))
except:
    print(0)
" 2>/dev/null)
    fi
    
    score="${score:-0}"
    echo "$score" > "$cache_file"
    echo "$score"
}

# Get task counts from todo2
_exarp_get_tasks() {
    local dir="${1:-.}"
    if [[ -f "$dir/.todo2/state.todo2.json" ]]; then
        python3 -c "
import json
try:
    with open('$dir/.todo2/state.todo2.json') as f:
        data = json.load(f)
    todos = data.get('todos', [])
    pending = len([t for t in todos if t.get('status') in ['pending', 'in_progress', 'Todo', 'In Progress']])
    done = len([t for t in todos if t.get('status') in ['completed', 'done', 'Done']])
    print(f'{pending}/{pending+done}')
except:
    print('0/0')
" 2>/dev/null
    else
        echo "0/0"
    fi
}

# ═══════════════════════════════════════════════════════════════
# CONTEXT-AWARE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

# Show context for current directory
exarp-context() {
    local dir="${1:-.}"
    
    if _exarp_is_project "$dir"; then
        local name=$(_exarp_project_name "$dir")
        local score=$(_exarp_get_score "$dir")
        local tasks=$(_exarp_get_tasks "$dir")
        
        # Color based on score
        local color score_icon
        if (( score >= 80 )); then
            color="\033[32m"; score_icon="🟢"
        elif (( score >= 60 )); then
            color="\033[33m"; score_icon="🟡"
        else
            color="\033[31m"; score_icon="🔴"
        fi
        
        echo ""
        echo "┌─────────────────────────────────────────────────────────────┐"
        echo "│  📁 PROJECT CONTEXT                                         │"
        echo "├─────────────────────────────────────────────────────────────┤"
        printf "│  %-58s│\n" "Name: $name"
        printf "│  %-58s│\n" "Score: ${score}% $score_icon"
        printf "│  %-58s│\n" "Tasks: $tasks pending/total"
        printf "│  %-58s│\n" "Path: ${dir:0:50}"
        echo "└─────────────────────────────────────────────────────────────┘"
        echo ""
        
        # Show quick actions
        echo "  Quick actions:"
        echo "    xs  - Full scorecard    xh  - Docs health"
        echo "    xo  - Overview          motd - MOTD with wisdom"
        echo ""
    else
        # Check for projects in subdirectories
        local projects=()
        for subdir in "$dir"/*/; do
            if _exarp_is_project "$subdir"; then
                projects+=("$subdir")
            fi
        done
        
        if (( ${#projects[@]} > 0 )); then
            echo ""
            echo "📁 Not a project directory, but found ${#projects[@]} project(s) below."
            echo "   Use 'xp' or 'exarp-projects' to see summary."
            echo ""
        else
            echo ""
            echo "📁 No exarp project detected in current directory."
            echo "   Looking for: .todo2/, pyproject.toml, package.json, Cargo.toml"
            echo ""
        fi
    fi
}

# Scan subdirectories for projects and show summary
exarp-projects() {
    local dir="${1:-.}"
    local projects=()
    local max_depth="${2:-2}"
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│  🗂️  PROJECT SUMMARY - $(basename "$(realpath "$dir")")      "
    echo "├─────────────────────────────────────────────────────────────┤"
    echo "│  Name                        Score    Tasks    Status      │"
    echo "├─────────────────────────────────────────────────────────────┤"
    
    # Find projects (max 2 levels deep)
    while IFS= read -r -d '' subdir; do
        if _exarp_is_project "$subdir"; then
            local name=$(_exarp_project_name "$subdir")
            local score=$(_exarp_get_score "$subdir")
            local tasks=$(_exarp_get_tasks "$subdir")
            
            # Status indicator
            local status
            if (( score >= 80 )); then status="🟢 Healthy"
            elif (( score >= 60 )); then status="🟡 Okay"
            elif (( score > 0 )); then status="🔴 Needs work"
            else status="⚪ Unknown"
            fi
            
            printf "│  %-26s %5s%%   %-8s %-11s│\n" "${name:0:26}" "$score" "$tasks" "$status"
            projects+=("$subdir")
        fi
    done < <(find "$dir" -maxdepth "$max_depth" -type d -print0 2>/dev/null)
    
    if (( ${#projects[@]} == 0 )); then
        echo "│  No projects found                                          │"
    fi
    
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
    echo "  Found ${#projects[@]} project(s). Use 'cd <project>' then 'xc' for details."
    echo ""
}

# ═══════════════════════════════════════════════════════════════
# PROMPT INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Fast prompt indicator (uses cache)
exarp_prompt_info() {
    if [[ "${EXARP_PROMPT:-0}" == "0" ]]; then
        return
    fi
    
    if ! _exarp_is_project "."; then
        return
    fi
    
    local score=$(_exarp_get_score ".")
    local tasks=$(_exarp_get_tasks ".")
    
    if (( score >= 80 )); then
        echo "%F{green}⬢${score}%f"
    elif (( score >= 60 )); then
        echo "%F{yellow}⬡${score}%f"
    elif (( score > 0 )); then
        echo "%F{red}⬡${score}%f"
    fi
}

# Detailed prompt info
exarp_prompt_full() {
    if ! _exarp_is_project "."; then
        return
    fi
    
    local name=$(_exarp_project_name ".")
    local score=$(_exarp_get_score ".")
    local tasks=$(_exarp_get_tasks ".")
    
    if (( score >= 80 )); then
        echo "%F{green}[$name:${score}%|$tasks]%f"
    elif (( score >= 60 )); then
        echo "%F{yellow}[$name:${score}%|$tasks]%f"
    elif (( score > 0 )); then
        echo "%F{red}[$name:${score}%|$tasks]%f"
    fi
}

# Hook to update on directory change (optional, can be slow)
# exarp_chpwd() {
#     # Clear cache for this directory to force refresh
#     local cache_file="$EXARP_CACHE_DIR/score_$(echo "$PWD" | md5sum | cut -c1-8)"
#     rm -f "$cache_file" 2>/dev/null
# }
# add-zsh-hook chpwd exarp_chpwd

# ═══════════════════════════════════════════════════════════════
# MOTD (Message of the Day)
# ═══════════════════════════════════════════════════════════════

exarp-motd() {
    local mode="${1:-score}"
    
    # Check if we're in a project with exarp
    if ! _exarp_is_project "."; then
        # Maybe show projects summary instead
        local projects_count=$(find . -maxdepth 2 -name ".todo2" -type d 2>/dev/null | wc -l)
        if (( projects_count > 0 )); then
            exarp-projects "." 2
        fi
        return 0
    fi
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│  🌟 EXARP - Project Health & Wisdom                         │"
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
    
    case "$mode" in
        context|c)
            exarp-context
            ;;
        overview|o)
            python -m project_management_automation.tools.project_overview output_format=text 2>/dev/null | head -40
            ;;
        wisdom|w)
            python -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
result = generate_project_scorecard(output_format='text', include_recommendations=False)
output = result.get('formatted_output', '')
if 'DAILY WISDOM' in output:
    print(output[output.find('DAILY WISDOM')-5:])
else:
    print(output[-500:] if len(output) > 500 else output)
" 2>/dev/null
            ;;
        score|s|*)
            python -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
result = generate_project_scorecard(output_format='text', include_recommendations=False)
print(result.get('formatted_output', 'Unable to generate scorecard')[:1500])
" 2>/dev/null
            ;;
    esac
    echo ""
}

# Aliases for MOTD modes
alias motd="exarp-motd"
alias motd-score="exarp-motd score"
alias motd-overview="exarp-motd overview"
alias motd-wisdom="exarp-motd wisdom"
alias motd-context="exarp-motd context"

# ═══════════════════════════════════════════════════════════════
# COMPLETIONS
# ═══════════════════════════════════════════════════════════════

_exarp_tools() {
    local tools=(
        "score:Project scorecard"
        "health:Documentation health"
        "align:Task alignment analysis"
        "dups:Duplicate detection"
        "sec:Security scan"
        "tags:Tag consolidation"
        "overview:Project overview"
        "context:Current project context"
        "projects:Scan for projects"
        "daily:Daily automation"
        "sprint:Sprint automation"
    )
    _describe 'exarp tools' tools
}

compdef _exarp_tools exarp 2>/dev/null

# ═══════════════════════════════════════════════════════════════
# AUTO-INIT
# ═══════════════════════════════════════════════════════════════

# Auto-show MOTD on shell start if enabled
if [[ "${EXARP_MOTD:-0}" != "0" ]]; then
    local today=$(date +%Y%m%d)
    local cache_file="$EXARP_CACHE_DIR/motd_${today}_$$"
    
    if [[ ! -f "$EXARP_CACHE_DIR/motd_${today}_shown" ]]; then
        exarp-motd "${EXARP_MOTD}"
        touch "$EXARP_CACHE_DIR/motd_${today}_shown"
    fi
fi

# Enable prompt integration example:
# RPROMPT='$(exarp_prompt_info) '$RPROMPT

echo "✅ Exarp plugin loaded"
echo "   xc - context  xp - projects  xs - score  xo - overview  motd - wisdom"
echo "   Enable prompt: export EXARP_PROMPT=1 && RPROMPT='\$(exarp_prompt_info)'"
