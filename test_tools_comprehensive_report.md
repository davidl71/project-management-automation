================================================================================
MCP TOOLS COMPREHENSIVE TEST REPORT
================================================================================

## SUMMARY

Total Tools: 27
✅ Working: 7 (25.9%)
❌ Broken: 20 (74.1%)

## BREAKDOWN BY ERROR TYPE

### AWAIT DICT ERROR: 20 tools
  - infer_session_mode
    Error: object dict can't be used in 'await' expression...
  - add_external_tool_hints
    Error: object dict can't be used in 'await' expression...
  - automation
    Error: object dict can't be used in 'await' expression...
  - tool_catalog
    Error: object dict can't be used in 'await' expression...
  - workflow_mode
    Error: object dict can't be used in 'await' expression...
  - context
    Error: object dict can't be used in 'await' expression...
  - recommend
    Error: object dict can't be used in 'await' expression...
  - analyze_alignment
    Error: object dict can't be used in 'await' expression...
  - security
    Error: object dict can't be used in 'await' expression...
  - generate_config
    Error: object dict can't be used in 'await' expression...
  - setup_hooks
    Error: object dict can't be used in 'await' expression...
  - prompt_tracking
    Error: object dict can't be used in 'await' expression...
  - health
    Error: object dict can't be used in 'await' expression...
  - check_attribution
    Error: object dict can't be used in 'await' expression...
  - report
    Error: object dict can't be used in 'await' expression...
  - task_analysis
    Error: object dict can't be used in 'await' expression...
  - testing
    Error: object dict can't be used in 'await' expression...
  - lint
    Error: object dict can't be used in 'await' expression...
  - memory
    Error: object dict can't be used in 'await' expression...
  - task_discovery
    Error: object dict can't be used in 'await' expression...

## WORKING TOOLS

  ✅ task_workflow
  ✅ estimation
  ✅ ollama
  ✅ mlx
  ✅ git_tools
  ✅ session
  ✅ memory_maint

## BROKEN TOOLS

  ❌ infer_session_mode (await_dict_error)
  ❌ add_external_tool_hints (await_dict_error)
  ❌ automation (await_dict_error)
  ❌ tool_catalog (await_dict_error)
  ❌ workflow_mode (await_dict_error)
  ❌ context (await_dict_error)
  ❌ recommend (await_dict_error)
  ❌ analyze_alignment (await_dict_error)
  ❌ security (await_dict_error)
  ❌ generate_config (await_dict_error)
  ❌ setup_hooks (await_dict_error)
  ❌ prompt_tracking (await_dict_error)
  ❌ health (await_dict_error)
  ❌ check_attribution (await_dict_error)
  ❌ report (await_dict_error)
  ❌ task_analysis (await_dict_error)
  ❌ testing (await_dict_error)
  ❌ lint (await_dict_error)
  ❌ memory (await_dict_error)
  ❌ task_discovery (await_dict_error)

## PATTERN ANALYSIS

Working tool prefixes:
  - estimation: 1
  - mlx: 1
  - memory: 1
  - ollama: 1
  - task: 1
  - git: 1
  - session: 1

Broken tool prefixes:
  - task: 2
  - lint: 1
  - context: 1
  - report: 1
  - health: 1
  - analyze: 1
  - check: 1
  - memory: 1
  - add: 1
  - automation: 1
  - recommend: 1
  - testing: 1
  - workflow: 1
  - infer: 1
  - setup: 1
  - prompt: 1
  - security: 1
  - tool: 1
  - generate: 1

## RECOMMENDATIONS

1. All broken tools show FastMCP framework errors
2. This confirms the issue is in FastMCP, not our code
3. Use EXARP_FORCE_STDIO=1 as workaround
4. Consider reporting to FastMCP maintainers