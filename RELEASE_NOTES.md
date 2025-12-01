## What's Changed

### ✨ Features

- Consolidate context and discovery tools (Phase 2B & 2C) (058fc951) @David Lowes
- Complete status standardization and portability improvements (d27ceb13) @David Lowes
- Standardize task status handling across codebase (3f3cb9bc) @David Lowes
- Implement session mode inference from tool patterns (e74768bb) @David Lowes
- implement project scorecard recommendations (75ff3229) @David Lowes
- Add Memory Management System with GC, pruning, consolidation, and dreaming (d13c5a6c) @David Lowes
- Add context summarization, mode suggestions, and async bug fix (7cfc3601) @David Lowes
- Add progress reporting to security scan and test runner (d6ea8c1b) @David Lowes
- Add elicitation, roots, and notification helpers for FastMCP (3172a3c3) @David Lowes
- Add FastMCP 2 advanced features (bcabf369) @David Lowes
- Add prompt tracking, model recommendations, and enhanced HINT catalog (583b4ad8) @David Lowes
- Add 5 new Cursor IDE best practice tools (67ce024f) @David Lowes
- Add PRD generator with persona-advisor alignment (34abf696) @David Lowes

### 🐛 Bug Fixes

- Correct update_base_version to use dynamic version replacement (8a0980fc) @David Lowes
- Correct update_base_version regex pattern in version.py (0776d13a) @David Lowes
- FastMCP return type for analyze_alignment tool (376be222) @David Lowes
- Resolve exarp version and MCP configuration issues (c9ac364b) @David Lowes
- Update MCP server to use local code version (6d57b199) @David Lowes
- scorecard completion score now recognizes done/Done status (daaf4319) @David Lowes
- lint cleanup - fix 2172 issues (cae0247c) @David Lowes
- correct briefing function call in consolidated.py (aed60a62) @David Lowes
- use try/except/else pattern for async context detection in run_tests (8c5bb4ae) @David Lowes
- Async wrapper bugs in security/testing/run_tests tools (4da92aba) @David Lowes
- accept exarp_pma as valid MCP server name (00b03ff2) @David Lowes
- Prevent duplicate task creation and cleanup existing duplicates (137c271d) @David Lowes

### 📚 Documentation

- Add release preparation files for v0.2.0 (a7711843) @David Lowes
- Add comprehensive MCP frameworks and tools comparison (a135c8f4) @David Lowes

### ♻️ Refactoring

- use toggle pattern for async context detection (30fec0c0) @David Lowes

### ⚡ Performance

- remove redundant inline asyncio imports (799bbfec) @David Lowes

### 🧪 Tests

- Add expanded test coverage and utils (0f72e9bf) @David Lowes

### 🔧 Maintenance

- Final state update (aa604f83) @David Lowes
- Update state files from pre-commit hooks (db40cf6e) @David Lowes
- Update project state, dependencies, and reports (46859873) @David Lowes
- mark more implemented tool tasks as Done (e3533491) @David Lowes
- mark implemented tool tasks as Done (62a6a8c9) @David Lowes
- session cleanup - exarp naming, cursorignore, docs index, lint fixes (48858de6) @David Lowes
- remove dead code (unused imports and variables) (3200ac07) @David Lowes
- Update todo2 state and session data (51e3fe5b) @David Lowes
- update task state (9c25228f) @David Lowes

### 📝 Other Changes

- Fix MCP tools: Split run_automation and add validation system (cc1e8a3c) @David Lowes
- Split analyze_alignment tool into separate tools to fix FastMCP issue (348bfd74) @David Lowes
- Update Todo2 task: Fix FastMCP return type issues - completed (59666a3c) @David Lowes
- Fix FastMCP return type issues and add automation (053a172e) @David Lowes
- Fix FastMCP return type issues and update cursor rules (2931d5a3) @David Lowes
- Normalize todo2 task statuses (e77e112a) @David Lowes
- Update Cursor MCP config to use exarp-uvx-wrapper.sh with --with-editable (f5ea9ebb) @David Lowes
- Merge branch 'main' of github.com:davidl71/project-management-automation (8ab10470) @David Lowes
- Update todo2 state (automation) (c40235cc) @David Lowes
- Update todo2 state and docs health history (04122ad6) @David Lowes
- Update todo2 state, memory tools, and docs health history (9e3a6cae) @David Lowes
- Merge branch 'main' of github.com:davidl71/project-management-automation (a66cb2c6) @David Lowes
- Add FastMCP workaround: direct access wrapper for session handoff (5948f551) @David Lowes
- Mark Phase 2B and Phase 2C consolidation tasks as completed (37bbf8b0) @David Lowes
- Complete consolidation verification and documentation (0510a509) @David Lowes
- Add sync action to session_handoff for automatic Todo2 state synchronization (402a4139) @David Lowes
- Phase 2D: Consolidate Model/Advisor Tools (3→1) - FINAL PHASE (85563fe0) @David Lowes
- Phase 2A: Consolidate Dynamic Tools (3→1) (7461e130) @David Lowes
- Phase 1: Extend testing tool with suggest and validate actions (46b67585) @David Lowes
- Add tool consolidation plan and assign tasks to remote agent (29328b3e) @David Lowes
- Apply MCP configuration improvements and merge latest changes (020cf17c) @David Lowes
- Complete parallel task execution: Interactive MCP, mode-aware features, and Cursor extension (29a75ab8) @David Lowes
- Update project files and configurations (fba64927) @David Lowes
- Add session handoff: completion score improvements (82862430) @David Lowes
- Improve completion score: 51.9% → 78.8% (fc87f14b) @David Lowes
- Remove PWA test class from test_tools_expanded.py (bc575cbd) @David Lowes
- Remove remaining PWA references from test files (3cb11213) @David Lowes
- Remove PWA functionality from Exarp (2bb72688) @David Lowes
- Fix test mock paths and assertions (5cb7d4bb) @David Lowes
- Add tests for daily_automation, task_clarification_resolution, pattern_triggers, and simplify_rules (8f36d4a3) @David Lowes
- Add tests for ci_cd_validation, nightly_task_automation, and working_copy_health tools (4999278b) @David Lowes
- Add tests for external_tool_hints, git_hooks, and batch_task_approval tools (4efccf70) @David Lowes
- Add tests for automation_opportunities, todo_sync, and pwa_review tools (a1af99cc) @David Lowes
- Add tests for linter.py (13% → 80%+ coverage target) (350fa645) @David Lowes
- Fix import mismatches and add tests for 0% coverage modules (efcabecc) @David Lowes
- Implement Exarp improvements from ib_box_spread_full_universal (cf9d1fa9) @David Lowes
- Enhance context primer and auto_primer tools (a0e18c1d) @David Lowes
- Add capabilities resource, context priming system, companion MCP hints (55dac8a5) @David Lowes
- Add uv.lock to .gitignore (0df5aa77) @David Lowes
- Add agentic-tools MCP integration to MCPClient (91bc13ac) @David Lowes


**Full Changelog**: `v0.1.18...v0.1.18`
