# Exarp ZSH Plugin (uvx version)
# Source this file in your .zshrc:
#   source /path/to/exarp-uvx.plugin.zsh
#
# Or download directly:
#   curl -o ~/.exarp.zsh https://raw.githubusercontent.com/davidl71/project-management-automation/main/shell/exarp-uvx.plugin.zsh
#   echo 'source ~/.exarp.zsh' >> ~/.zshrc
#
# Features:
#   - Context-aware project detection
#   - MOTD with project health + wisdom
#   - Prompt indicator showing project score
#   - Shell-only lite mode (no Python startup time)
#   - iTerm2 integration

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# EXARP_MOTD=1           # Show MOTD on shell start (score|overview|wisdom)
# EXARP_PROMPT=1         # Show project health in prompt
# EXARP_CACHE_TTL=300    # Cache TTL in seconds (default: 5 min)

EXARP_CACHE_DIR="${EXARP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/exarp}"
mkdir -p "$EXARP_CACHE_DIR" 2>/dev/null

# ═══════════════════════════════════════════════════════════════
# CORE ALIASES (using uvx)
# ═══════════════════════════════════════════════════════════════

alias exarp="uvx exarp"
alias pma="uvx exarp"

# ═══════════════════════════════════════════════════════════════
# SHELL-ONLY FUNCTIONS (no Python/uvx required - FAST)
# ═══════════════════════════════════════════════════════════════

# Fast task count using only shell (no Python)
_exarp_tasks_fast() {
    local dir="${1:-.}"
    local todo_file="$dir/.todo2/state.todo2.json"
    
    if [[ ! -f "$todo_file" ]]; then
        echo "0/0"
        return
    fi
    
    # Use grep for speed (no Python startup time)
    local total=$(grep -c '"id"' "$todo_file" 2>/dev/null || echo 0)
    local done=$(grep -c '"status".*[Dd]one\|[Cc]ompleted' "$todo_file" 2>/dev/null || echo 0)
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
        grep -m1 '"name"' "$dir/package.json" 2>/dev/null | sed 's/.*": *"\([^"]*\)".*/\1/'
    elif [[ -f "$dir/Cargo.toml" ]]; then
        grep -m1 'name.*=' "$dir/Cargo.toml" 2>/dev/null | sed 's/.*"\([^"]*\)".*/\1/' | head -1
    else
        basename "$(cd "$dir" 2>/dev/null && pwd || echo "$dir")"
    fi
}

# Git stats (shell only)
_exarp_git_stats() {
    local dir="${1:-.}"
    if [[ ! -d "$dir/.git" ]]; then
        echo "no-git"
        return
    fi
    
    (
        cd "$dir" 2>/dev/null || return
        local branch=$(git branch --show-current 2>/dev/null)
        local dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        
        if (( dirty > 0 )); then
            echo "$branch+$dirty"
        else
            echo "$branch"
        fi
    )
}

# Lightweight context (NO Python required) - FAST
exarp-lite() {
    local dir="${1:-.}"
    
    if ! _exarp_detect_fast "$dir"; then
        echo "📁 Not a project directory"
        return 1
    fi
    
    local name=$(_exarp_name_fast "$dir")
    local tasks=$(_exarp_tasks_fast "$dir")
    local git=$(_exarp_git_stats "$dir")
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    echo "│  ⚡ EXARP LITE (shell-only, instant)                      │"
    echo "├───────────────────────────────────────────────────────────┤"
    printf "│  %-56s │\n" "Project: ${name:0:47}"
    printf "│  %-56s │\n" "Tasks: $tasks (pending/total)"
    printf "│  %-56s │\n" "Git: ${git:0:50}"
    echo "└───────────────────────────────────────────────────────────┘"
    echo ""
}

alias xl="exarp-lite"

# Quick task list (shell + minimal Python for JSON parsing)
exarp-tasks-lite() {
    local dir="${1:-.}"
    local todo_file="$dir/.todo2/state.todo2.json"
    local limit="${2:-10}"
    
    if [[ ! -f "$todo_file" ]]; then
        echo "No .todo2/state.todo2.json found"
        return 1
    fi
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    printf "│  📋 PENDING TASKS (top %-2s)                               │\n" "$limit"
    echo "├───────────────────────────────────────────────────────────┤"
    
    # Use Python one-liner for reliable JSON parsing
    local output
    output=$(python3 -c "
import json
with open('$todo_file') as f:
    data = json.load(f)
count = 0
for t in data.get('todos', []):
    status = t.get('status', '').lower()
    if status in ['pending', 'in_progress', 'todo', 'in progress']:
        content = t.get('content', 'No content')[:52]
        tid = t.get('id', '?')
        print(f'{tid}: {content}')
        count += 1
        if count >= $limit:
            break
" 2>/dev/null)
    
    if [[ -z "$output" ]]; then
        echo "│  ✅ No pending tasks!                                     │"
    else
        echo "$output" | while read -r task; do
            printf "│  • %-54s │\n" "${task:0:54}"
        done
    fi
    
    echo "└───────────────────────────────────────────────────────────┘"
    echo ""
}

alias xt="exarp-tasks-lite"

# Multi-project scan (shell only) - FAST
exarp-projects-lite() {
    local dir="${1:-.}"
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    echo "│  🗂️  PROJECTS (lite scan)                                 │"
    echo "├───────────────────────────────────────────────────────────┤"
    echo "│  Name                        Tasks     Git                │"
    echo "├───────────────────────────────────────────────────────────┤"
    
    local count=0
    for subdir in "$dir"/*/; do
        if _exarp_detect_fast "$subdir"; then
            local name=$(_exarp_name_fast "$subdir")
            local tasks=$(_exarp_tasks_fast "$subdir")
            local git=$(_exarp_git_stats "$subdir")
            printf "│  %-26s %-9s %-16s │\n" "${name:0:26}" "$tasks" "${git:0:16}"
            ((count++))
        fi
    done
    
    if (( count == 0 )); then
        echo "│  No projects found                                       │"
    fi
    
    echo "└───────────────────────────────────────────────────────────┘"
    echo "  Found $count project(s)"
    echo ""
}

alias xpl="exarp-projects-lite"

# ═══════════════════════════════════════════════════════════════
# UVX-POWERED FUNCTIONS (full features, uses uvx)
# ═══════════════════════════════════════════════════════════════

# Get cached score or compute new one (via uvx)
_exarp_get_score() {
    local dir="${1:-.}"
    local cache_file="$EXARP_CACHE_DIR/score_$(echo "$dir" | shasum | cut -c1-8)"
    local cache_ttl="${EXARP_CACHE_TTL:-300}"
    
    # Check cache
    if [[ -f "$cache_file" ]]; then
        local now=$(date +%s)
        local mtime=$(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file" 2>/dev/null || echo 0)
        local age=$((now - mtime))
        if (( age < cache_ttl )); then
            cat "$cache_file"
            return
        fi
    fi
    
    # Compute score via uvx (runs in background, returns cached or 0)
    local score=0
    if [[ -f "$dir/.todo2/state.todo2.json" ]]; then
        score=$(cd "$dir" && uvx exarp 2>/dev/null <<< '{"method":"tools/call","params":{"name":"project_scorecard","arguments":{"output_format":"json","include_recommendations":false}}}' 2>/dev/null | python3 -c "
import sys, json
try:
    for line in sys.stdin:
        if 'overall_score' in line:
            data = json.loads(line)
            print(int(data.get('result', {}).get('overall_score', 0)))
            break
except: pass
" 2>/dev/null || echo 0)
    fi
    
    score="${score:-0}"
    echo "$score" > "$cache_file" 2>/dev/null
    echo "$score"
}

# Full context with score (uses cache for speed)
exarp-context() {
    local dir="${1:-.}"
    
    if ! _exarp_detect_fast "$dir"; then
        # Check for projects in subdirectories
        local projects_count=0
        for subdir in "$dir"/*/; do
            _exarp_detect_fast "$subdir" && ((projects_count++))
        done
        
        if (( projects_count > 0 )); then
            echo ""
            echo "📁 Not a project directory, but found $projects_count project(s) below."
            echo "   Use 'xpl' for quick scan or 'xp' for full analysis."
            echo ""
        else
            echo ""
            echo "📁 No exarp project detected in current directory."
            echo ""
        fi
        return 1
    fi
    
    local name=$(_exarp_name_fast "$dir")
    local tasks=$(_exarp_tasks_fast "$dir")
    local git=$(_exarp_git_stats "$dir")
    local score=$(_exarp_get_score "$dir")
    
    # Color based on score
    local score_icon
    if (( score >= 80 )); then score_icon="🟢"
    elif (( score >= 60 )); then score_icon="🟡"
    elif (( score > 0 )); then score_icon="🔴"
    else score_icon="⚪"
    fi
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    echo "│  📁 PROJECT CONTEXT                                       │"
    echo "├───────────────────────────────────────────────────────────┤"
    printf "│  %-56s │\n" "Project: ${name:0:47}"
    printf "│  %-56s │\n" "Score: ${score}% ${score_icon}"
    printf "│  %-56s │\n" "Tasks: $tasks (pending/total)"
    printf "│  %-56s │\n" "Git: ${git:0:50}"
    echo "└───────────────────────────────────────────────────────────┘"
    echo ""
    echo "  Quick: xl (lite) | xs (scorecard) | xo (overview) | xw (wisdom)"
    echo ""
}

alias xc="exarp-context"

# Full project scan (uses uvx for scores)
exarp-projects() {
    local dir="${1:-.}"
    local dir_name=$(basename "$(cd "$dir" && pwd)")
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    printf "│  🗂️  PROJECT SUMMARY - %-34s │\n" "${dir_name:0:34}"
    echo "├───────────────────────────────────────────────────────────┤"
    echo "│  Name                      Score   Tasks    Status       │"
    echo "├───────────────────────────────────────────────────────────┤"
    
    local count=0
    for subdir in "$dir"/*/; do
        if _exarp_detect_fast "$subdir"; then
            local name=$(_exarp_name_fast "$subdir")
            local tasks=$(_exarp_tasks_fast "$subdir")
            local score=$(_exarp_get_score "$subdir")
            
            local status
            if (( score >= 80 )); then status="🟢 Healthy"
            elif (( score >= 60 )); then status="🟡 Okay"
            elif (( score > 0 )); then status="🔴 Needs"
            else status="⚪ Unknown"
            fi
            
            printf "│  %-24s %5s%%  %-8s %-12s │\n" "${name:0:24}" "$score" "$tasks" "$status"
            ((count++))
        fi
    done
    
    if (( count == 0 )); then
        echo "│  No projects found                                       │"
    fi
    
    echo "└───────────────────────────────────────────────────────────┘"
    echo "  Found $count project(s)"
    echo ""
}

alias xp="exarp-projects"

# ═══════════════════════════════════════════════════════════════
# FULL SCORECARD/OVERVIEW (via uvx - slower but complete)
# ═══════════════════════════════════════════════════════════════

# Full scorecard
exarp-score() {
    if ! _exarp_detect_fast "."; then
        echo "Not in a project directory"
        return 1
    fi
    
    echo "Running full scorecard via uvx..."
    uvx --from exarp python -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
result = generate_project_scorecard(output_format='text', include_recommendations=True)
print(result.get('formatted_output', 'Unable to generate scorecard'))
"
}

alias xs="exarp-score"

# Full overview
exarp-overview() {
    if ! _exarp_detect_fast "."; then
        echo "Not in a project directory"
        return 1
    fi
    
    echo "Running project overview via uvx..."
    uvx --from exarp python -c "
from project_management_automation.tools.project_overview import generate_project_overview
result = generate_project_overview(output_format='text')
print(result.get('formatted_output', 'Unable to generate overview'))
"
}

alias xo="exarp-overview"

# Wisdom only
exarp-wisdom() {
    uvx --from exarp python -c "
from project_management_automation.tools.wisdom import get_wisdom, format_text
import os

# Get score from cache or use default
score = 50
try:
    from project_management_automation.tools.project_scorecard import generate_project_scorecard
    result = generate_project_scorecard(output_format='json', include_recommendations=False)
    score = result.get('overall_score', 50)
except: pass

source = os.environ.get('EXARP_WISDOM_SOURCE', 'random')
wisdom = get_wisdom(score, source=source)
print(format_text(wisdom))
"
}

alias xw="exarp-wisdom"

# ═══════════════════════════════════════════════════════════════
# MOTD (Message of the Day)
# ═══════════════════════════════════════════════════════════════

exarp-motd() {
    local mode="${1:-lite}"
    
    echo ""
    echo "┌───────────────────────────────────────────────────────────┐"
    echo "│  🌟 EXARP - Project Health & Wisdom                       │"
    echo "└───────────────────────────────────────────────────────────┘"
    
    case "$mode" in
        lite|l)
            # Fast shell-only mode
            if _exarp_detect_fast "."; then
                exarp-lite
            else
                exarp-projects-lite
            fi
            ;;
        context|c)
            exarp-context
            ;;
        score|s)
            exarp-score
            ;;
        overview|o)
            exarp-overview
            ;;
        wisdom|w)
            exarp-wisdom
            ;;
        full|f)
            # Full: context + wisdom
            exarp-context
            echo "─────────────────────────────────────────────────────────────"
            exarp-wisdom
            ;;
        *)
            exarp-lite
            ;;
    esac
}

alias motd="exarp-motd"

# ═══════════════════════════════════════════════════════════════
# PROMPT INTEGRATION
# ═══════════════════════════════════════════════════════════════

# Fast prompt indicator (uses cache, shell-only fallback)
exarp_prompt_info() {
    if [[ "${EXARP_PROMPT:-0}" == "0" ]]; then
        return
    fi
    
    if ! _exarp_detect_fast "."; then
        return
    fi
    
    # Use cached score if available, otherwise show tasks
    local cache_file="$EXARP_CACHE_DIR/score_$(echo "$PWD" | shasum | cut -c1-8)"
    local score=0
    
    if [[ -f "$cache_file" ]]; then
        score=$(cat "$cache_file")
    fi
    
    local tasks=$(_exarp_tasks_fast ".")
    local pending=$(echo "$tasks" | cut -d'/' -f1)
    
    if (( score >= 80 )); then
        echo "%F{green}⬢${score}%f"
    elif (( score >= 60 )); then
        echo "%F{yellow}⬡${score}%f"
    elif (( score > 0 )); then
        echo "%F{red}⬡${score}%f"
    elif (( pending > 0 )); then
        echo "%F{blue}◇${pending}%f"
    fi
}

# Detailed prompt (name + score + tasks)
exarp_prompt_full() {
    if ! _exarp_detect_fast "."; then
        return
    fi
    
    local name=$(_exarp_name_fast ".")
    local tasks=$(_exarp_tasks_fast ".")
    local cache_file="$EXARP_CACHE_DIR/score_$(echo "$PWD" | shasum | cut -c1-8)"
    local score=0
    
    if [[ -f "$cache_file" ]]; then
        score=$(cat "$cache_file")
    fi
    
    if (( score >= 80 )); then
        echo "%F{green}[${name:0:12}:${score}%|$tasks]%f"
    elif (( score >= 60 )); then
        echo "%F{yellow}[${name:0:12}:${score}%|$tasks]%f"
    elif (( score > 0 )); then
        echo "%F{red}[${name:0:12}:${score}%|$tasks]%f"
    else
        echo "%F{blue}[${name:0:12}|$tasks]%f"
    fi
}

# ═══════════════════════════════════════════════════════════════
# iTERM2 INTEGRATION
# ═══════════════════════════════════════════════════════════════

_exarp_iterm2_available() {
    [[ "$TERM_PROGRAM" == "iTerm.app" ]] && \
    typeset -f iterm2_set_user_var > /dev/null 2>&1
}

# Set iTerm2 user variables (for status bar)
_exarp_iterm2_update() {
    if ! _exarp_iterm2_available; then
        return
    fi
    
    if _exarp_detect_fast "."; then
        local name=$(_exarp_name_fast ".")
        local tasks=$(_exarp_tasks_fast ".")
        local pending=$(echo "$tasks" | cut -d'/' -f1)
        
        local cache_file="$EXARP_CACHE_DIR/score_$(echo "$PWD" | shasum | cut -c1-8)"
        local score=0
        [[ -f "$cache_file" ]] && score=$(cat "$cache_file")
        
        iterm2_set_user_var exarpProject "$name"
        iterm2_set_user_var exarpScore "$score"
        iterm2_set_user_var exarpTasks "$pending"
        
        local health
        if (( score >= 80 )); then health="🟢"
        elif (( score >= 60 )); then health="🟡"
        elif (( score > 0 )); then health="🔴"
        else health="⚪"
        fi
        iterm2_set_user_var exarpHealth "$health"
        
        # Set tab title
        echo -ne "\e]1;${name} (${score}%)\a"
    else
        iterm2_set_user_var exarpProject ""
        iterm2_set_user_var exarpScore ""
        iterm2_set_user_var exarpTasks ""
        iterm2_set_user_var exarpHealth ""
    fi
}

# Hook for directory changes
if _exarp_iterm2_available; then
    autoload -Uz add-zsh-hook
    add-zsh-hook chpwd _exarp_iterm2_update
    _exarp_iterm2_update
fi

# ═══════════════════════════════════════════════════════════════
# COMPLETIONS
# ═══════════════════════════════════════════════════════════════

_exarp_commands() {
    local commands=(
        "xl:Lite context (instant, shell-only)"
        "xc:Full context with score"
        "xt:Task list"
        "xp:Projects summary"
        "xpl:Projects lite (instant)"
        "xs:Full scorecard"
        "xo:Full overview"
        "xw:Daily wisdom"
        "motd:Message of the day"
    )
    _describe 'exarp commands' commands
}

# ═══════════════════════════════════════════════════════════════
# AUTO-INIT
# ═══════════════════════════════════════════════════════════════

# Show MOTD on shell start if enabled
if [[ "${EXARP_MOTD:-0}" != "0" ]]; then
    local today=$(date +%Y%m%d)
    if [[ ! -f "$EXARP_CACHE_DIR/motd_${today}_shown" ]]; then
        exarp-motd "${EXARP_MOTD}"
        touch "$EXARP_CACHE_DIR/motd_${today}_shown"
    fi
fi

# Status message
echo "✅ Exarp (uvx) loaded"
echo "   Instant: xl (context)  xpl (projects)  xt (tasks)"
echo "   Full:    xc (context)  xp (projects)   xs (score)  xo (overview)  xw (wisdom)"
echo ""
echo "   Enable prompt: export EXARP_PROMPT=1"
echo "   Enable MOTD:   export EXARP_MOTD=lite  (or: context|score|wisdom|full)"

if _exarp_iterm2_available; then
    echo "   🍎 iTerm2: Add status bar with \(user.exarpProject) \(user.exarpHealth)\(user.exarpScore)%"
fi

