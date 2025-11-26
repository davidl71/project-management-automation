#!/bin/bash
# ==============================================================================
# Batch Uninstall Unwanted Cursor Extensions
# ==============================================================================
# Generated: 2025-11-26
# Purpose: Remove extensions that are redundant, unused, or replaced by Exarp
#
# Usage:
#   ./scripts/uninstall_unwanted_extensions.sh        # Uninstall all
#   ./scripts/uninstall_unwanted_extensions.sh --dry-run  # Show what would be uninstalled
#
# Categories:
#   - REPLACED BY EXARP: Security/dependency scanning
#   - MAINFRAME: IBM i, COBOL, Zowe (not used)
#   - ANSIBLE: Full extension suite (CLI sufficient)
#   - UNUSED LANGUAGES: Go, Java, .NET, PHP, Ruby, etc.
#   - REDUNDANT: Multiple AI assistants, duplicate tools
# ==============================================================================

set -e

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
    echo ""
fi

# Extensions to uninstall
EXTENSIONS=(
    # REPLACED BY EXARP
    "redhat.fabric8-analytics"
    "fill-labs.dependi"
    
    # MAINFRAME/ENTERPRISE
    "halcyontechltd.code-for-ibmi"
    "halcyontechltd.vscode-ibmi-walkthroughs"
    "barrettotte.ibmi-languages"
    "ibm.zopendebug"
    "broadcommfd.cobol-language-support"
    "zowe.vscode-extension-for-zowe"
    
    # ANSIBLE
    "redhat.ansible"
    "mattiasbaake.vscode-snippets-for-ansible"
    "jborean.ansibug"
    
    # UNUSED LANGUAGES
    "13xforever.language-x86-64-assembly"
    "guyskk.language-cython"
    "aliasadidev.nugetpackagemanagergui"
    
    # REDUNDANT TOOLS
    "firefox-devtools.vscode-firefox-debug"
    "ms-edgedevtools.vscode-edge-devtools"
    "yeshan333.jenkins-pipeline-linter-connector-fork"
    "quantconnect.quantconnect"
    "labring.open-remote-ssh-for-trae"
    "formulahendry.code-runner"
    "franneck94.vscode-c-cpp-dev-extension-pack"
    "kylinideteam.cmake-intellisence"
    
    # REDUNDANT AI (Keep Copilot only)
    "tabnine.tabnine-vscode"
    "amazonwebservices.codewhisperer-for-command-line-companion"
)

echo "===================================================================="
echo "🧹 Cursor Extension Cleanup"
echo "===================================================================="
echo ""
echo "Extensions to process: ${#EXTENSIONS[@]}"
echo ""

SUCCESS=0
SKIPPED=0
FAILED=0

for ext in "${EXTENSIONS[@]}"; do
    if $DRY_RUN; then
        echo "  Would uninstall: $ext"
    else
        if cursor --uninstall-extension "$ext" 2>/dev/null; then
            echo "  ✅ Uninstalled: $ext"
            ((SUCCESS++))
        else
            # Check if it was already not installed
            if ! ls ~/.cursor/extensions/ 2>/dev/null | grep -q "^${ext}-"; then
                echo "  ⏭️  Skipped (not installed): $ext"
                ((SKIPPED++))
            else
                echo "  ❌ Failed: $ext"
                ((FAILED++))
            fi
        fi
    fi
done

echo ""
echo "===================================================================="
echo "📊 Summary"
echo "===================================================================="
if $DRY_RUN; then
    echo "  Would uninstall: ${#EXTENSIONS[@]} extensions"
    echo ""
    echo "  Run without --dry-run to apply changes"
else
    echo "  ✅ Uninstalled: $SUCCESS"
    echo "  ⏭️  Skipped:     $SKIPPED"
    echo "  ❌ Failed:      $FAILED"
    echo ""
    echo "  Restart Cursor to complete cleanup"
fi
echo "===================================================================="

