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
# SHELL-ONLY FUNCTIONS (no Python/MCP required)
# ═══════════════════════════════════════════════════════════════

# Fast task count using only shell (no Python)
_exarp_tasks_fast() {
    local dir="${1:-.}"
    local todo_file="$dir/.todo2/state.todo2.json"
    
    if [[ ! -f "$todo_file" ]]; then
        echo "0/0"
        return
    fi
    
    # Use grep/awk for speed (no Python startup time)
    local total=$(grep -c '"id"' "$todo_file" 2>/dev/null || echo 0)
    local done=$(grep -c '"status":\s*"done\|completed"' "$todo_file" 2>/dev/null || echo 0)
    local pending=$((total - done))
    echo "$pending/$total"
}

# Fast project detection (shell only)
_exarp_detect_fast() {
    local dir="${1:-.}"
    [[ -d "$dir/.todo2" ]] || [[ -d "$dir/.git" ]] || \
    [[ -f "$dir/pyproject.toml" ]] || [[ -f "$dir/package.json" ]] || \
    [[ -f "$dir/Cargo.toml" ]] || [[ -f "$dir/go.mod" ]]
}

# Fast project name (shell only)
_exarp_name_fast() {
    local dir="${1:-.}"
    
    if [[ -f "$dir/pyproject.toml" ]]; then
        grep -m1 'name.*=' "$dir/pyproject.toml" 2>/dev/null | sed 's/.*"\([^"]*\)".*/\1/' | head -1
    elif [[ -f "$dir/package.json" ]]; then
        grep -m1 '"name"' "$dir/package.json" 2>/dev/null | sed 's/.*"\([^"]*\)"[^"]*$/\1/'
    elif [[ -f "$dir/Cargo.toml" ]]; then
        grep -m1 'name.*=' "$dir/Cargo.toml" 2>/dev/null | sed 's/.*"\([^"]*\)".*/\1/' | head -1
    else
        basename "$(realpath "$dir" 2>/dev/null || echo "$dir")"
    fi
}

# Git stats (shell only)
_exarp_git_stats() {
    local dir="${1:-.}"
    if [[ ! -d "$dir/.git" ]]; then
        echo "no-git"
        return
    fi
    
    cd "$dir" 2>/dev/null || return
    local branch=$(git branch --show-current 2>/dev/null)
    local commits=$(git rev-list --count HEAD 2>/dev/null || echo 0)
    local dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    
    if (( dirty > 0 )); then
        echo "$branch+$dirty"
    else
        echo "$branch"
    fi
}

# Lightweight context (NO Python required)
exarp-lite() {
    local dir="${1:-.}"
    
    if ! _exarp_detect_fast "$dir"; then
        echo "📁 Not a project directory"
        return 1
    fi
    
    local name=$(_exarp_name_fast "$dir")
    local tasks=$(_exarp_tasks_fast "$dir")
    local git=$(_exarp_git_stats "$dir")
    
    # File counts
    local py_files=$(find "$dir" -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')
    local js_files=$(find "$dir" -name "*.js" -o -name "*.ts" -type f 2>/dev/null | wc -l | tr -d ' ')
    local total_files=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│  ⚡ EXARP LITE (shell-only, no MCP)                         │"
    echo "├─────────────────────────────────────────────────────────────┤"
    printf "│  %-58s│\n" "Project: $name"
    printf "│  %-58s│\n" "Tasks: $tasks (pending/total)"
    printf "│  %-58s│\n" "Git: $git"
    printf "│  %-58s│\n" "Files: $total_files total ($py_files py, $js_files js/ts)"
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
}

# Alias for lite mode
alias xl="exarp-lite"

# Quick task list (shell only, reads JSON directly)
exarp-tasks-lite() {
    local dir="${1:-.}"
    local todo_file="$dir/.todo2/state.todo2.json"
    local limit="${2:-10}"
    
    if [[ ! -f "$todo_file" ]]; then
        echo "No .todo2/state.todo2.json found"
        return 1
    fi
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    printf "│  📋 PENDING TASKS (top %-2s)                                 │\n" "$limit"
    echo "├─────────────────────────────────────────────────────────────┤"
    
    # Use Python one-liner for reliable JSON parsing (still fast, no imports)
    local output
    output=$(python3 -c "
import json
with open('$todo_file') as f:
    data = json.load(f)
count = 0
for t in data.get('todos', []):
    status = t.get('status', '')
    if status in ['pending', 'in_progress', 'Todo', 'In Progress']:
        content = t.get('content', 'No content')[:54]
        print(content)
        count += 1
        if count >= $limit:
            break
" 2>/dev/null)
    
    if [[ -z "$output" ]]; then
        echo "│  No pending tasks found                                     │"
    else
        echo "$output" | while read -r task; do
            printf "│  • %-56s│\n" "$task"
        done
    fi
    
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
}

alias xt="exarp-tasks-lite"

# Multi-project scan (shell only)
exarp-projects-lite() {
    local dir="${1:-.}"
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│  🗂️  PROJECTS (lite scan)                                   │"
    echo "├─────────────────────────────────────────────────────────────┤"
    echo "│  Name                          Tasks     Git               │"
    echo "├─────────────────────────────────────────────────────────────┤"
    
    local count=0
    for subdir in "$dir"/*/; do
        if _exarp_detect_fast "$subdir"; then
            local name=$(_exarp_name_fast "$subdir")
            local tasks=$(_exarp_tasks_fast "$subdir")
            local git=$(_exarp_git_stats "$subdir")
            printf "│  %-28s %-9s %-17s│\n" "${name:0:28}" "$tasks" "${git:0:17}"
            ((count++))
        fi
    done
    
    if (( count == 0 )); then
        echo "│  No projects found                                          │"
    fi
    
    echo "└─────────────────────────────────────────────────────────────┘"
    echo "  Found $count project(s)"
    echo ""
}

alias xpl="exarp-projects-lite"

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
# iTERM2 INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Detect iTerm2 shell integration
_exarp_iterm2_available() {
    [[ "$TERM_PROGRAM" == "iTerm.app" ]] && \
    typeset -f iterm2_set_user_var > /dev/null 2>&1
}

# Set iTerm2 badge (background text)
exarp_iterm2_badge() {
    if ! _exarp_iterm2_available; then
        return
    fi
    
    local badge_text=""
    if _exarp_is_project "."; then
        local name=$(_exarp_project_name ".")
        local score=$(_exarp_get_score ".")
        local tasks=$(_exarp_get_tasks ".")
        badge_text="${name}\n${score}% | ${tasks}"
    fi
    
    # Set badge using iTerm2 escape sequence
    printf "\e]1337;SetBadgeFormat=%s\a" "$(echo -n "$badge_text" | base64)"
}

# Set iTerm2 user variables (for status bar)
exarp_iterm2_vars() {
    if ! _exarp_iterm2_available; then
        return
    fi
    
    if _exarp_is_project "."; then
        local name=$(_exarp_project_name ".")
        local score=$(_exarp_get_score ".")
        local tasks=$(_exarp_get_tasks ".")
        local pending=$(echo "$tasks" | cut -d'/' -f1)
        
        # Set user variables for iTerm2 status bar
        iterm2_set_user_var exarpProject "$name"
        iterm2_set_user_var exarpScore "$score"
        iterm2_set_user_var exarpTasks "$pending"
        
        # Health indicator
        local health
        if (( score >= 80 )); then health="🟢"
        elif (( score >= 60 )); then health="🟡"
        elif (( score > 0 )); then health="🔴"
        else health="⚪"
        fi
        iterm2_set_user_var exarpHealth "$health"
    else
        iterm2_set_user_var exarpProject ""
        iterm2_set_user_var exarpScore ""
        iterm2_set_user_var exarpTasks ""
        iterm2_set_user_var exarpHealth ""
    fi
}

# Set iTerm2 tab title and window title
exarp_iterm2_title() {
    if [[ "$TERM_PROGRAM" != "iTerm.app" ]]; then
        return
    fi
    
    if _exarp_is_project "."; then
        local name=$(_exarp_project_name ".")
        local score=$(_exarp_get_score ".")
        
        # Tab title: project name + score
        echo -ne "\e]1;${name} (${score}%)\a"
        # Window title: full path
        echo -ne "\e]2;${PWD}\a"
    fi
}

# iTerm2 marks for command output (mark start of exarp output)
exarp_iterm2_mark() {
    if _exarp_iterm2_available; then
        printf "\e]1337;SetMark\a"
    fi
}

# iTerm2 annotation (highlight important output)
exarp_iterm2_annotate() {
    local message="$1"
    if _exarp_iterm2_available; then
        printf "\e]1337;AddAnnotation=%s\a" "$message"
    fi
}

# Hook to update iTerm2 on directory change
_exarp_iterm2_chpwd() {
    if _exarp_iterm2_available; then
        exarp_iterm2_vars
        exarp_iterm2_badge
        exarp_iterm2_title
    fi
}

# Register chpwd hook for iTerm2 updates
if _exarp_iterm2_available; then
    autoload -Uz add-zsh-hook
    add-zsh-hook chpwd _exarp_iterm2_chpwd
    
    # Initial update
    _exarp_iterm2_chpwd
fi

# iTerm2-enhanced context display
exarp-context-iterm() {
    exarp_iterm2_mark
    exarp-context "$@"
    
    if _exarp_is_project "." && _exarp_iterm2_available; then
        local score=$(_exarp_get_score ".")
        if (( score < 60 )); then
            exarp_iterm2_annotate "⚠️ Project health is low ($score%)"
        fi
    fi
}

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
echo "   Full:  xc - context   xp - projects   xs - score   xo - overview"
echo "   Lite:  xl - context   xpl - projects  xt - tasks   (no Python needed)"
echo "   Enable prompt: export EXARP_PROMPT=1 && RPROMPT='\$(exarp_prompt_info)'"

# iTerm2 integration status
if _exarp_iterm2_available; then
    echo "   🍎 iTerm2 integration active (badge, status bar, titles)"
    echo "      Status bar: Add 'Interpolated String' with \(user.exarpProject) \(user.exarpHealth)\(user.exarpScore)%"
fi
