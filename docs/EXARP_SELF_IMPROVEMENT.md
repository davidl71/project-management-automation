# Exarp Self-Improvement Strategy

**Date**: 2025-11-26
**Status**: Proposal
**Concept**: "Eating Our Own Dog Food" - Using Exarp to Improve Exarp

---

## Overview

Exarp should use its own automation tools to continuously improve itself. This document outlines strategies for self-improvement, tool chaining, and automated workflows.

---

## Current Self-Improvement Opportunities

### 1. Documentation Health

**Tool**: `check_documentation_health_tool`

**Use Case**: Run on Exarp's own documentation
- Check `docs/` directory for broken links
- Validate documentation structure
- Identify missing documentation
- Create Todo2 tasks for documentation issues

**Workflow**:
```bash
# Manual: Use Exarp tool
check_documentation_health_tool(output_path="docs/EXARP_DOCS_HEALTH.json", create_tasks=True)

# Automated: GitHub Actions workflow
# Runs weekly, creates issues for documentation problems
```

---

### 2. Todo2 Task Management

**Tools**:
- `analyze_todo2_alignment_tool`
- `detect_duplicate_tasks_tool`
- `sync_todo_tasks_tool`

**Use Case**: Manage Exarp's own Todo2 tasks
- Analyze alignment of Exarp development tasks
- Detect duplicate tasks in Exarp project
- Sync Exarp tasks with project management system

**Workflow**:
```bash
# Weekly automation
1. analyze_todo2_alignment_tool() → Find misaligned tasks
2. detect_duplicate_tasks_tool() → Find duplicates
3. Create summary report
4. Create Todo2 tasks for fixes
```

---

### 3. Dependency Security

**Tool**: `scan_dependency_security_tool`

**Use Case**: Scan Exarp's own dependencies
- Check `pyproject.toml` for vulnerabilities
- Monitor FastMCP, Pydantic, and other dependencies
- Create alerts for security issues

**Workflow**:
```bash
# Automated: Weekly security scan
scan_dependency_security_tool(output_path="docs/EXARP_SECURITY_REPORT.json")

# Already implemented in security-scan.yml workflow
```

---

### 4. Automation Opportunities

**Tool**: `find_automation_opportunities_tool`

**Use Case**: Find automation opportunities in Exarp codebase
- Analyze Exarp's own scripts and workflows
- Identify repetitive tasks that could be automated
- Suggest new Exarp tools based on patterns

**Workflow**:
```bash
# Monthly automation discovery
find_automation_opportunities_tool(
    output_path="docs/EXARP_AUTOMATION_OPPORTUNITIES.json",
    create_tasks=True
)
```

---

### 5. Rule Simplification

**Tool**: `simplify_rules_tool`

**Use Case**: Simplify Exarp's own rules
- Analyze `.cursor/rules/*.mdc` files
- Identify redundant rules
- Simplify based on Exarp automation capabilities

**Workflow**:
```bash
# Quarterly rule review
simplify_rules_tool(
    rules_files=[".cursor/rules/*.mdc"],
    output_path="docs/EXARP_RULES_SIMPLIFICATION.json"
)
```

---

## Tool Chaining Strategy

### Current State

**Problem**: Tools return JSON strings, but don't easily chain together

**Example**:
```python
# Current: Manual chaining
result1 = check_documentation_health_tool()
# Parse JSON manually
issues = json.loads(result1)["issues"]
# Use in next tool manually
for issue in issues:
    # Create task manually
    ...
```

### Proposed Solution: Tool Piping

**Concept**: Allow tools to accept input from other tools

**Example**:
```python
# Proposed: Automatic chaining
check_documentation_health_tool(
    output_path="temp/docs_health.json"
) | analyze_todo2_alignment_tool(
    input_path="temp/docs_health.json",
    filter_issues=True
) | create_tasks_tool(
    input_path="temp/aligned_issues.json"
)
```

### Implementation Approaches

#### Option 1: MCP Tool Chaining

**How**: Tools accept `input_path` parameter to read previous tool output

```python
def analyze_todo2_alignment_tool(
    input_path: Optional[str] = None,  # NEW: Accept input from previous tool
    output_path: Optional[str] = None,
    create_tasks: bool = True
) -> str:
    """
    Analyze Todo2 alignment.

    If input_path provided, reads issues from previous tool output.
    """
    if input_path:
        with open(input_path) as f:
            previous_output = json.load(f)
            # Extract relevant data
            issues = previous_output.get("issues", [])
    else:
        # Normal operation
        issues = analyze_todo2_tasks()

    # Process issues
    ...
```

#### Option 2: Workflow Orchestration Tool

**How**: Create a new tool that orchestrates multiple tools

```python
def run_automation_workflow_tool(
    workflow_name: str,
    tools: List[str],
    output_path: Optional[str] = None
) -> str:
    """
    Run a predefined workflow of Exarp tools.

    Workflows:
    - "self_improvement": docs_health → alignment → create_tasks
    - "security_audit": dependency_scan → create_tasks
    - "documentation_review": docs_health → external_hints → create_tasks
    """
    workflows = {
        "self_improvement": [
            "check_documentation_health_tool",
            "analyze_todo2_alignment_tool",
            "detect_duplicate_tasks_tool"
        ],
        "security_audit": [
            "scan_dependency_security_tool",
            "check_working_copy_health_tool"
        ],
        ...
    }

    results = []
    for tool_name in workflows[workflow_name]:
        tool_func = get_tool_function(tool_name)
        result = tool_func(...)
        results.append(result)
        # Pass output to next tool
        ...

    return json.dumps({"workflow": workflow_name, "results": results})
```

#### Option 3: Intermediate Data Format

**How**: Standardize tool output format for easy chaining

```python
# Standard output format
{
    "tool": "check_documentation_health_tool",
    "timestamp": "2025-01-27T10:00:00Z",
    "status": "success",
    "data": {
        "issues": [...],
        "metrics": {...}
    },
    "next_tools": [  # NEW: Suggest next tools
        "analyze_todo2_alignment_tool",
        "detect_duplicate_tasks_tool"
    ],
    "pipeline_data": {  # NEW: Data formatted for next tool
        "issues": [...],
        "tasks": [...]
    }
}
```

---

## Self-Improvement Workflows

### Workflow 1: Weekly Self-Health Check

**Purpose**: Comprehensive health check of Exarp itself

**Tools**:
1. `check_documentation_health_tool` - Check docs
2. `analyze_todo2_alignment_tool` - Check tasks
3. `detect_duplicate_tasks_tool` - Find duplicates
4. `scan_dependency_security_tool` - Check security
5. `find_automation_opportunities_tool` - Find new automation

**Implementation**:
```yaml
# .github/workflows/exarp-self-improvement.yml
name: Exarp Self-Improvement

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Mondays
  workflow_dispatch:

jobs:
  self-health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Exarp Self-Health Check
        run: |
          # Use Exarp MCP server to run tools on itself
          python -m exarp_project_management.scripts.self_improvement
```

---

### Workflow 2: Documentation Auto-Improvement

**Purpose**: Continuously improve Exarp documentation

**Tools**:
1. `check_documentation_health_tool` - Find issues
2. `add_external_tool_hints_tool` - Add Context7 hints
3. Create Todo2 tasks for fixes

**Implementation**:
```python
# exarp_project_management/scripts/self_improvement_docs.py
def improve_documentation():
    """Run documentation improvement workflow."""
    # Step 1: Check health
    health_result = check_documentation_health_tool(
        output_path="temp/docs_health.json"
    )

    # Step 2: Add external tool hints
    hints_result = add_external_tool_hints_tool(
        output_path="temp/external_hints.json"
    )

    # Step 3: Create tasks for issues
    issues = json.loads(health_result)["issues"]
    for issue in issues:
        create_todo2_task(
            title=f"Fix documentation: {issue['title']}",
            description=issue["description"]
        )
```

---

### Workflow 3: Rule Simplification

**Purpose**: Continuously simplify Exarp rules

**Tools**:
1. `simplify_rules_tool` - Analyze and simplify
2. Create PR with simplified rules

**Implementation**:
```python
# Quarterly rule simplification
def simplify_exarp_rules():
    """Simplify Exarp's own rules."""
    result = simplify_rules_tool(
        rules_files=[
            ".cursor/rules/project-automation.mdc",
            ".cursor/rules/todo2.mdc",
            ...
        ],
        output_path="temp/rules_simplification.json",
        dry_run=False
    )

    # Create PR with changes
    create_pr(
        title="Simplify Exarp rules using Exarp",
        body="Auto-generated by Exarp self-improvement workflow"
    )
```

---

## Implementation Plan

### Phase 1: Basic Self-Improvement (Current)

**Status**: ✅ Partially Implemented

- ✅ `run_daily_automation_tool` - Can run on Exarp
- ✅ `security-scan.yml` - Scans Exarp dependencies
- ⚠️ Manual execution required

**Next Steps**:
1. Create `self_improvement.py` script
2. Add GitHub Actions workflow for weekly self-check
3. Document self-improvement workflows

---

### Phase 2: Tool Chaining (Proposed)

**Status**: 🟡 Design Phase

**Requirements**:
1. Standardize tool output format
2. Add `input_path` parameter to tools
3. Create workflow orchestration tool
4. Add tool chaining examples

**Implementation**:
1. Update tool signatures to accept `input_path`
2. Create `run_automation_workflow_tool`
3. Add chaining examples to documentation
4. Test with self-improvement workflows

---

### Phase 3: Advanced Self-Improvement (Future)

**Status**: 🔮 Future Enhancement

**Features**:
1. Automatic PR creation from self-improvement
2. Self-healing documentation
3. Automatic rule optimization
4. Predictive automation discovery

---

## Benefits

### 1. Continuous Improvement

- Exarp improves itself automatically
- No manual intervention needed
- Always up-to-date documentation and rules

### 2. Tool Validation

- Using Exarp on itself validates tools work correctly
- Real-world testing of automation capabilities
- Identifies tool improvements needed

### 3. Demonstration

- Shows Exarp's capabilities in action
- Provides examples for users
- Proves tool effectiveness

### 4. Efficiency

- Automated workflows reduce manual work
- Tool chaining reduces redundant operations
- Standardized formats enable reuse

---

## Examples

### Example 1: Self-Documentation Health

```bash
# Run Exarp on itself
exarp check_documentation_health_tool \
  --output-path docs/EXARP_DOCS_HEALTH.json \
  --create-tasks

# Result: Creates Todo2 tasks for documentation issues
```

### Example 2: Chained Workflow

```python
# Proposed: Tool chaining
workflow_result = run_automation_workflow_tool(
    workflow_name="self_improvement",
    output_path="docs/SELF_IMPROVEMENT_REPORT.json"
)

# Executes:
# 1. check_documentation_health_tool
# 2. analyze_todo2_alignment_tool (uses docs health output)
# 3. detect_duplicate_tasks_tool (uses alignment output)
# 4. Creates combined report
```

### Example 3: GitHub Actions Integration

```yaml
# .github/workflows/exarp-self-improvement.yml
- name: Run Exarp Self-Improvement
  run: |
    python -m exarp_project_management.scripts.self_improvement \
      --workflow weekly_health_check \
      --create-tasks \
      --output-path reports/self-improvement-$(date +%Y%m%d).json
```

---

## Next Steps

1. **Create Self-Improvement Script** (`scripts/self_improvement.py`)
   - Run Exarp tools on Exarp repository
   - Generate reports
   - Create Todo2 tasks

2. **Add Tool Chaining Support**
   - Update tool signatures
   - Create workflow orchestration tool
   - Add chaining examples

3. **Create GitHub Actions Workflow**
   - Weekly self-improvement check
   - Automated documentation improvement
   - Rule simplification

4. **Document Self-Improvement**
   - Add to README.md
   - Create usage examples
   - Document workflows

---

## Related Documentation

- GitHub Workflows - CI/CD workflows
- Tool Status - Available tools
- Usage Guide - How to use Exarp tools
- Contributing Guide - Development guidelines

---

**Status**: Proposal - Ready for Implementation
**Priority**: High - Demonstrates Exarp's capabilities
**Effort**: Medium - Requires tool chaining implementation
