# Exarp ZSH Plugin
# Source this file or add to your .zshrc:
#   source /path/to/exarp.plugin.zsh
# Or symlink to ~/.oh-my-zsh/custom/plugins/exarp/exarp.plugin.zsh
#
# MOTD: Set EXARP_MOTD=1 to show project health + wisdom on shell start
# Disable: Set EXARP_MOTD=0 or unset EXARP_MOTD

# ═══════════════════════════════════════════════════════════════
# ALIASES
# ═══════════════════════════════════════════════════════════════

# Main command (shorter than project-management-automation)
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

# ═══════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════

# Quick health check
exarp-quick() {
    echo "🔍 Running quick health check..."
    python -m project_management_automation.tools.project_scorecard output_format=text include_recommendations=false
}

# Daily routine
exarp-daily() {
    echo "📅 Running daily automation..."
    python -m project_management_automation.scripts.automate_daily
}

# Sprint start
exarp-sprint() {
    echo "🏃 Running sprint automation..."
    python -m project_management_automation.scripts.automate_sprint
}

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
        "daily:Daily automation"
        "sprint:Sprint automation"
    )
    _describe 'exarp tools' tools
}

compdef _exarp_tools exarp

# ═══════════════════════════════════════════════════════════════
# PROMPT INTEGRATION (optional)
# ═══════════════════════════════════════════════════════════════

# Add project health to prompt (uncomment to enable)
# exarp_prompt_info() {
#     local score=$(python -c "from project_management_automation.tools.project_scorecard import generate_project_scorecard; print(generate_project_scorecard()['overall_score'])" 2>/dev/null)
#     if [[ -n "$score" ]]; then
#         if (( score >= 80 )); then echo "%F{green}⬢${score}%f"
#         elif (( score >= 60 )); then echo "%F{yellow}⬡${score}%f"
#         else echo "%F{red}⬡${score}%f"
#         fi
#     fi
# }
# RPROMPT='$(exarp_prompt_info)'

# ═══════════════════════════════════════════════════════════════
# MOTD (Message of the Day)
# ═══════════════════════════════════════════════════════════════

# Show project health + wisdom on shell start
# Enable: export EXARP_MOTD=1 (or EXARP_MOTD=score|overview|wisdom)
# Disable: export EXARP_MOTD=0 or unset

exarp-motd() {
    local mode="${1:-score}"
    
    # Check if we're in a project with exarp
    if [[ ! -f "pyproject.toml" ]] && [[ ! -f ".todo2/state.todo2.json" ]]; then
        return 0
    fi
    
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│  🌟 EXARP - Project Health & Wisdom                         │"
    echo "└─────────────────────────────────────────────────────────────┘"
    echo ""
    
    case "$mode" in
        overview|o)
            python -m project_management_automation.tools.project_overview output_format=text 2>/dev/null | head -40
            ;;
        wisdom|w)
            python -c "
from project_management_automation.tools.project_scorecard import generate_project_scorecard
result = generate_project_scorecard(output_format='text', include_recommendations=False)
# Extract just the wisdom section
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

# Shorter aliases for MOTD modes
alias motd="exarp-motd"
alias motd-score="exarp-motd score"
alias motd-overview="exarp-motd overview"
alias motd-wisdom="exarp-motd wisdom"

# Auto-show MOTD on shell start if enabled
if [[ "${EXARP_MOTD:-0}" != "0" ]]; then
    # Only show once per day (cache in /tmp)
    local today=$(date +%Y%m%d)
    local cache_file="/tmp/exarp_motd_${today}"
    
    if [[ ! -f "$cache_file" ]]; then
        exarp-motd "${EXARP_MOTD}"
        touch "$cache_file"
    fi
fi

echo "✅ Exarp plugin loaded. Try: exarp, xs, xh, xo, motd"
echo "   Enable MOTD: export EXARP_MOTD=1 (or score|overview|wisdom)"

