# Pre-Commit Check

Before I commit, verify my changes are ready.

## Steps
1. Check what files changed (git status)
2. Run `/exarp/check_documentation_health` if docs changed
3. Run `/exarp/project_scorecard` tier="quick" for metrics
4. Flag any complexity or security concerns

## Checklist
- [ ] Tests pass
- [ ] No linter errors
- [ ] Documentation updated (if needed)
- [ ] No security issues introduced
