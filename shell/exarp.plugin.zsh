# Exarp ZSH Plugin
# Source this file or add to your .zshrc:
#   source /path/to/exarp.plugin.zsh
# Or symlink to ~/.oh-my-zsh/custom/plugins/exarp/exarp.plugin.zsh

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

echo "✅ Exarp plugin loaded. Try: exarp, xs (score), xh (health), xo (overview)"

