# Tool Conditional Logic Analysis

*Generated: 1764632037.4297311*

> **See Also:**
> - `docs/FASTMCP_TOOL_CONSTRAINTS.md` - Constraint rules and validation guidelines
> - `docs/TOOL_VALIDATION_REPORT.md` - Current validation status
> - `project_management_automation/utils/tool_validator.py` - Validation utility

## Summary

- Total tools: 23
- Tools with conditional logic: 3
- Tools without issues: 20

## Tools with Conditional Logic

### dev_reload (line 680)

- If statements: 3
- Elif statements: 2
- Else statements: 2
- Has 'action' parameter: False
- Conditional on action: False
- Multiple returns: True
- Function length: 44 lines

```python
        def dev_reload(modules: Optional[list[str]] = None) -> str:

            """

            [HINT: Dev reload. Hot-reload modules without restart. Requires EXARP_DEV_MODE=1.]



            Reload Python modules without restarting Cursor.

            Only available when EXARP_DEV_MODE=1 is set in environment.



            Args:

                modules: Optional list of specific modules to reload (e.g., ["tools.project_scorecard"]).

                        If not provided, reloads all package modules.



            To enable dev mode, add to your MCP config:

                "env": {"EXARP_DEV_MODE": "1"}

            """

            from .utils.dev_reload import is_dev_mode, reload_all_modules, reload_specific_modules



            if not is_dev_mode():

                return json.dumps(

                    {

                        "success": False,

```

### run_automation (line 1660)

- If statements: 2
- Elif statements: 4
- Else statements: 2
- Has 'action' parameter: True
- Conditional on action: True
- Multiple returns: True
- Function length: 70 lines

```python
        def run_automation(

            action: str = "daily",

            # Daily action params

            tasks: Optional[list[str]] = None,

            include_slow: bool = False,

            # Nightly action params

            max_tasks_per_host: int = 5,

            max_parallel_tasks: int = 10,

            # Sprint action params

            max_iterations: int = 10,

            auto_approve: bool = True,

            extract_subtasks: bool = True,

            run_analysis_tools: bool = True,

            run_testing_tools: bool = True,

            # Discover action params

            min_value_score: float = 0.7,

            # Shared params

            priority_filter: Optional[str] = None,

            tag_filter: Optional[list[str]] = None,

            dry_run: bool = False,

```

### recommend (line 1982)

- If statements: 3
- Elif statements: 1
- Else statements: 1
- Has 'action' parameter: True
- Conditional on action: False
- Multiple returns: True
- Function length: 106 lines

```python
        def recommend(

            action: str = "model",

            task_description: Optional[str] = None,

            task_type: Optional[str] = None,

            optimize_for: str = "quality",

            include_alternatives: bool = True,

            task_id: Optional[str] = None,

            include_rationale: bool = True,

            metric: Optional[str] = None,

            tool: Optional[str] = None,

            stage: Optional[str] = None,

            score: float = 50.0,

            context: str = "",

            log: bool = True,

        ) -> str:

            """

            [HINT: Recommendations. action=model|workflow|advisor. Unified recommendation system.]



            Unified recommendation tool consolidating model selection, workflow mode suggestions, and advisor consultations.



```

## Tools Without Issues

- ✅ add_external_tool_hints
- ✅ advisor_audio
- ✅ analyze_prd_alignment
- ✅ analyze_todo2_alignment
- ✅ check_attribution
- ✅ context
- ✅ discovery
- ✅ generate_config
- ✅ health
- ✅ lint
- ✅ memory
- ✅ memory_maint
- ✅ prompt_tracking
- ✅ report
- ✅ security
- ✅ setup_hooks
- ✅ task_analysis
- ✅ task_discovery
- ✅ task_workflow
- ✅ testing
