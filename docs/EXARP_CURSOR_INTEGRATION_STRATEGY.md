# Exarp Cursor IDE Integration Strategy

**Date**: 2025-01-27
**Status**: Analysis & Enhancement Proposal
**Purpose**: Enhance Exarp's integration with Cursor IDE for better project management and automation

---

## Overview

This document outlines Exarp's current Cursor IDE integration and opportunities to enhance it for better project management, automation, and developer experience.

---

## Current Cursor Integration

### MCP Server Configuration

Exarp is currently configured as an MCP (Model Context Protocol) server in Cursor:

**Configuration File**: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "exarp": {
      "command": "python3",
      "args": ["-m", "exarp_project_management.server"],
      "description": "Exarp - Project management automation tools (Enochian: Spirit of Air - Communication)"
    }
  }
}
```

### Current Capabilities

Exarp provides Cursor with:
- **18 Tools**: Documentation health, task alignment, duplicate detection, security scanning, etc.
- **14 Prompts**: Reusable workflow templates
- **8 Resources**: Status, history, tasks, agents, cache
- **stdio Transport**: Secure local execution

---

## Enhancement Opportunities

### 1. Cursor Project Context Awareness (High Priority)

**Problem**: Exarp doesn't leverage Cursor's project context

**Solution**: Integrate with Cursor's project structure and context

**Features**:
- **Project Detection**: Auto-detect Cursor workspace projects
- **File Context**: Understand current file/project context
- **Workspace Awareness**: Multi-workspace support
- **Cursor Rules Integration**: Read and analyze `.cursorrules` files

**Example Use Case**:
```python
def analyze_cursor_project_tool(
    workspace_path: Optional[str] = None,
    include_cursor_rules: bool = True,
    output_path: Optional[str] = None
) -> str:
    """
    Analyze Cursor project structure and context.

    Analysis:
    - Project structure detection
    - Cursor rules analysis
    - Workspace configuration
    - File context understanding
    """
    from pathlib import Path
    import json

    workspace = Path(workspace_path or Path.cwd())

    analysis = {
        'workspace_path': str(workspace),
        'cursor_config': {},
        'project_structure': {},
        'cursor_rules': {}
    }

    # Detect Cursor configuration
    cursor_dir = workspace / '.cursor'
    if cursor_dir.exists():
        # Read mcp.json
        mcp_config = cursor_dir / 'mcp.json'
        if mcp_config.exists():
            with open(mcp_config, 'r') as f:
                analysis['cursor_config']['mcp'] = json.load(f)

        # Read commands.json
        commands_config = cursor_dir / 'commands.json'
        if commands_config.exists():
            with open(commands_config, 'r') as f:
                analysis['cursor_config']['commands'] = json.load(f)

    # Analyze Cursor rules
    if include_cursor_rules:
        cursorrules = workspace / '.cursorrules'
        if cursorrules.exists():
            with open(cursorrules, 'r') as f:
                analysis['cursor_rules']['content'] = f.read()
                analysis['cursor_rules']['size'] = len(f.read())

    return json.dumps(analysis, indent=2)
```

**Benefits**:
- Better project understanding
- Cursor rules integration
- Workspace awareness
- Context-aware automation

---

### 2. Cursor Rules Analysis and Optimization (High Priority)

**Problem**: Cursor rules can become redundant or need optimization

**Solution**: Analyze and optimize `.cursorrules` files

**Features**:
- **Rules Analysis**: Analyze `.cursorrules` for redundancies
- **Optimization**: Suggest rule improvements
- **Integration Check**: Verify Exarp tool references
- **Auto-Update**: Update rules based on Exarp capabilities

**Example Use Case**:
```python
def analyze_cursor_rules_tool(
    cursorrules_path: Optional[str] = None,
    suggest_improvements: bool = True,
    output_path: Optional[str] = None
) -> str:
    """
    Analyze and optimize Cursor rules file.

    Analysis:
    - Redundancy detection
    - Exarp tool integration check
    - Rule optimization suggestions
    - Best practices compliance
    """
    from pathlib import Path
    import re

    rules_path = Path(cursorrules_path or Path.cwd() / '.cursorrules')

    if not rules_path.exists():
        return json.dumps({'error': 'No .cursorrules file found'}, indent=2)

    with open(rules_path, 'r') as f:
        rules_content = f.read()

    analysis = {
        'file_path': str(rules_path),
        'size': len(rules_content),
        'lines': len(rules_content.split('\n')),
        'redundancies': [],
        'exarp_references': [],
        'suggestions': []
    }

    # Check for Exarp tool references
    exarp_tools = [
        'check_documentation_health',
        'analyze_todo2_alignment',
        'detect_duplicate_tasks',
        'scan_dependency_security'
    ]

    for tool in exarp_tools:
        if tool in rules_content:
            analysis['exarp_references'].append(tool)

    # Suggest improvements
    if suggest_improvements:
        if 'exarp' in rules_content.lower():
            analysis['suggestions'].append('Replace "exarp" references with "Exarp"')

        if 'manual' in rules_content.lower() and 'exarp' not in rules_content.lower():
            analysis['suggestions'].append('Consider using Exarp automation instead of manual steps')

    return json.dumps(analysis, indent=2)
```

**Benefits**:
- Rule optimization
- Exarp integration verification
- Best practices compliance
- Auto-improvement

---

### 3. Cursor Commands Integration (Medium Priority)

**Problem**: Exarp tools aren't exposed as Cursor commands

**Solution**: Create Cursor commands for Exarp tools

**Features**:
- **Command Generation**: Auto-generate Cursor commands
- **Tool Mapping**: Map Exarp tools to Cursor commands
- **Command Discovery**: Discover available commands
- **Command Execution**: Execute Exarp tools via commands

**Example Use Case**:
```python
def generate_cursor_commands_tool(
    output_path: Optional[str] = None,
    include_all_tools: bool = True
) -> str:
    """
    Generate Cursor commands.json for Exarp tools.

    Commands:
    - exarp:docs-health - Check documentation health
    - exarp:task-alignment - Analyze task alignment
    - exarp:duplicates - Detect duplicate tasks
    - exarp:security - Scan dependencies
    """
    from pathlib import Path
    import json

    commands = {
        "commands": {
            "exarp:docs-health": {
                "command": "python3 -m exarp_project_management.tools.docs_health",
                "description": "Check documentation health using Exarp"
            },
            "exarp:task-alignment": {
                "command": "python3 -m exarp_project_management.tools.todo2_alignment",
                "description": "Analyze Todo2 task alignment"
            },
            "exarp:duplicates": {
                "command": "python3 -m exarp_project_management.tools.duplicate_detection",
                "description": "Detect duplicate tasks"
            },
            "exarp:security": {
                "command": "python3 -m exarp_project_management.tools.dependency_security",
                "description": "Scan dependencies for security vulnerabilities"
            }
        }
    }

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(commands, f, indent=2)
        return json.dumps({'status': 'commands_generated', 'path': str(output_file)}, indent=2)

    return json.dumps(commands, indent=2)
```

**Benefits**:
- Easy tool access
- Command discovery
- Keyboard shortcuts
- Quick actions

---

### 4. Cursor Workspace Multi-Project Support (High Priority)

**Problem**: Cursor workspaces may contain multiple projects

**Solution**: Support multi-project Cursor workspaces

**Features**:
- **Workspace Detection**: Detect multiple projects in workspace
- **Project Isolation**: Isolate Exarp analysis per project
- **Workspace Aggregation**: Aggregate across workspace projects
- **Context Switching**: Switch between project contexts

**Example Use Case**:
```python
def analyze_cursor_workspace_tool(
    workspace_path: Optional[str] = None,
    aggregate: bool = True,
    output_path: Optional[str] = None
) -> str:
    """
    Analyze Cursor workspace with multiple projects.

    Analysis:
    - Detect projects in workspace
    - Analyze each project
    - Aggregate results
    - Generate workspace overview
    """
    from pathlib import Path
    import json

    workspace = Path(workspace_path or Path.cwd())

    # Detect projects (Git repositories)
    projects = []
    for git_dir in workspace.rglob('.git'):
        project_path = git_dir.parent
        projects.append({
            'name': project_path.name,
            'path': str(project_path),
            'type': 'git'
        })

    analysis = {
        'workspace_path': str(workspace),
        'projects': projects,
        'project_count': len(projects),
        'aggregated': {}
    }

    if aggregate:
        # Aggregate analysis across projects
        aggregated = {
            'total_tasks': 0,
            'total_docs': 0,
            'total_issues': 0
        }

        for project in projects:
            # Analyze each project
            project_analysis = analyze_project(Path(project['path']))
            aggregated['total_tasks'] += project_analysis.get('tasks', 0)
            aggregated['total_docs'] += project_analysis.get('docs', 0)
            aggregated['total_issues'] += project_analysis.get('issues', 0)

        analysis['aggregated'] = aggregated

    return json.dumps(analysis, indent=2)
```

**Benefits**:
- Multi-project support
- Workspace awareness
- Context isolation
- Aggregated insights

---

### 5. Cursor AI Assistant Integration (Medium Priority)

**Problem**: Exarp tools aren't easily discoverable by Cursor AI

**Solution**: Enhance Exarp's AI discoverability in Cursor

**Features**:
- **Tool Descriptions**: Comprehensive tool descriptions with hints
- **Prompt Templates**: Cursor-specific prompt templates
- **Context Hints**: Provide context hints for AI assistant
- **Usage Examples**: Examples for AI assistant

**Example Use Case**:
```python
def generate_cursor_ai_hints_tool(
    output_path: Optional[str] = None
) -> str:
    """
    Generate AI hints for Cursor AI assistant.

    Hints:
    - Tool descriptions with [HINT: ...] format
    - Usage examples
    - Context information
    - Best practices
    """
    from pathlib import Path
    import json

    hints = {
        'tools': [
            {
                'name': 'check_documentation_health_tool',
                'hint': '[HINT: Documentation health check. Returns health score, broken links, issues.]',
                'example': 'Check documentation health for this project',
                'when_to_use': 'Before commits, after documentation changes'
            },
            {
                'name': 'analyze_todo2_alignment_tool',
                'hint': '[HINT: Todo2 alignment analysis. Returns alignment score, misaligned tasks.]',
                'example': 'Analyze task alignment with project goals',
                'when_to_use': 'During task review, before sprint planning'
            }
        ],
        'prompts': [
            {
                'name': 'doc_check',
                'hint': '[HINT: Quick documentation health check without creating tasks.]',
                'example': 'Run doc_check prompt',
                'when_to_use': 'Quick documentation review'
            }
        ]
    }

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(hints, f, indent=2)
        return json.dumps({'status': 'hints_generated', 'path': str(output_file)}, indent=2)

    return json.dumps(hints, indent=2)
```

**Benefits**:
- Better AI discoverability
- Improved tool usage
- Context awareness
- Usage guidance

---

## Integration Strategy

### Phase 1: Cursor Project Context (High Priority)

**Goal**: Understand Cursor project structure

**Implementation**:
1. Create `analyze_cursor_project_tool`
2. Detect Cursor configuration
3. Analyze project structure
4. Read Cursor rules

**Benefits**:
- Project awareness
- Context understanding
- Rules integration

---

### Phase 2: Cursor Rules Optimization (High Priority)

**Goal**: Optimize Cursor rules with Exarp

**Implementation**:
1. Create `analyze_cursor_rules_tool`
2. Detect redundancies
3. Suggest improvements
4. Auto-update rules

**Benefits**:
- Rule optimization
- Exarp integration
- Best practices

---

### Phase 3: Cursor Commands (Medium Priority)

**Goal**: Expose Exarp tools as Cursor commands

**Implementation**:
1. Create `generate_cursor_commands_tool`
2. Map Exarp tools to commands
3. Generate commands.json
4. Test command execution

**Benefits**:
- Easy tool access
- Command discovery
- Quick actions

---

### Phase 4: Workspace Multi-Project (High Priority)

**Goal**: Support multi-project Cursor workspaces

**Implementation**:
1. Create `analyze_cursor_workspace_tool`
2. Detect multiple projects
3. Aggregate analysis
4. Context switching

**Benefits**:
- Multi-project support
- Workspace awareness
- Aggregated insights

---

## Use Cases

### Use Case 1: Cursor Project Analysis

**Problem**: Need to understand Cursor project structure

**Solution**: Analyze Cursor project

```python
# User: "Analyze this Cursor project"
# Exarp: Analyzes project structure, Cursor config, rules, etc.

def analyze_cursor_project_workflow():
    """Workflow for analyzing Cursor project."""
    # 1. Detect Cursor workspace
    # 2. Read Cursor configuration
    # 3. Analyze project structure
    # 4. Read Cursor rules
    # 5. Generate analysis report
    ...
```

---

### Use Case 2: Cursor Rules Optimization

**Problem**: Cursor rules need optimization

**Solution**: Analyze and optimize rules

```python
# User: "Optimize my Cursor rules"
# Exarp: Analyzes rules, suggests improvements, updates with Exarp references

def optimize_cursor_rules_workflow():
    """Workflow for optimizing Cursor rules."""
    # 1. Read .cursorrules
    # 2. Analyze for redundancies
    # 3. Check Exarp integration
    # 4. Suggest improvements
    # 5. Auto-update if approved
    ...
```

---

### Use Case 3: Multi-Project Workspace

**Problem**: Cursor workspace has multiple projects

**Solution**: Analyze and aggregate across projects

```python
# User: "Analyze all projects in this workspace"
# Exarp: Detects projects, analyzes each, aggregates results

def multi_project_workspace_workflow():
    """Workflow for multi-project workspace."""
    # 1. Detect projects in workspace
    # 2. Analyze each project
    # 3. Aggregate results
    # 4. Generate workspace overview
    ...
```

---

## Library Recommendations

### Cursor Configuration

**JSON Parsing**: `json` (built-in)
- Parse Cursor configuration files
- Read commands.json, mcp.json

**Path Handling**: `pathlib` (built-in)
- Workspace path detection
- File discovery

### Project Analysis

**GitPython**: `GitPython>=3.1.0` (already in multi-project dependencies)
- Repository detection
- Git metadata

**File Parsing**: `markdown>=3.4.0` (already in multi-project dependencies)
- Parse Cursor rules
- Analyze documentation

---

## Dependencies

### Required

- **GitPython**: `GitPython>=3.1.0` (project detection)
- **markdown**: `markdown>=3.4.0` (rules parsing)

### Optional

- **pyyaml**: `pyyaml>=6.0.0` (YAML config support)

### Installation

```bash
# Core Cursor integration (already in multi-project dependencies)
pip install GitPython markdown
```

---

## Implementation Examples

### Example 1: Cursor Project Analyzer

```python
from pathlib import Path
import json
from typing import Dict, Optional

class CursorProjectAnalyzer:
    """Analyze Cursor project structure and configuration."""

    def __init__(self, workspace_path: Optional[Path] = None):
        self.workspace = workspace_path or Path.cwd()
        self.cursor_dir = self.workspace / '.cursor'

    def analyze(self) -> Dict:
        """Analyze Cursor project."""
        analysis = {
            'workspace_path': str(self.workspace),
            'cursor_config': self._analyze_config(),
            'cursor_rules': self._analyze_rules(),
            'project_structure': self._analyze_structure()
        }
        return analysis

    def _analyze_config(self) -> Dict:
        """Analyze Cursor configuration."""
        config = {}

        if not self.cursor_dir.exists():
            return config

        # Read mcp.json
        mcp_config = self.cursor_dir / 'mcp.json'
        if mcp_config.exists():
            with open(mcp_config, 'r') as f:
                config['mcp'] = json.load(f)

        # Read commands.json
        commands_config = self.cursor_dir / 'commands.json'
        if commands_config.exists():
            with open(commands_config, 'r') as f:
                config['commands'] = json.load(f)

        return config

    def _analyze_rules(self) -> Dict:
        """Analyze Cursor rules."""
        rules_path = self.workspace / '.cursorrules'

        if not rules_path.exists():
            return {'exists': False}

        with open(rules_path, 'r') as f:
            content = f.read()

        return {
            'exists': True,
            'size': len(content),
            'lines': len(content.split('\n')),
            'exarp_references': self._count_exarp_references(content)
        }

    def _count_exarp_references(self, content: str) -> int:
        """Count Exarp tool references in rules."""
        exarp_keywords = ['exarp', 'check_documentation_health', 'analyze_todo2_alignment']
        return sum(1 for keyword in exarp_keywords if keyword.lower() in content.lower())

    def _analyze_structure(self) -> Dict:
        """Analyze project structure."""
        structure = {
            'has_git': (self.workspace / '.git').exists(),
            'has_docs': (self.workspace / 'docs').exists(),
            'has_tests': (self.workspace / 'tests').exists()
        }
        return structure
```

---

## Benefits for Exarp

### 1. Cursor Integration

- **Project Awareness**: Understand Cursor project structure
- **Rules Optimization**: Optimize Cursor rules with Exarp
- **Command Integration**: Expose Exarp tools as commands
- **Workspace Support**: Multi-project workspace support

### 2. Developer Experience

- **Easy Access**: Quick access to Exarp tools
- **Context Awareness**: Understand project context
- **Automation**: Auto-optimize Cursor rules
- **Discovery**: Better tool discovery

### 3. AI Assistant

- **Discoverability**: Better AI assistant integration
- **Context Hints**: Provide context for AI
- **Usage Examples**: Examples for AI assistant
- **Best Practices**: Guide AI assistant usage

---

## Next Steps

1. **Research**: Analyze Cursor configuration format and structure
2. **Implement**: Create Cursor integration tools
3. **Test**: Validate with real Cursor projects
4. **Document**: Add usage examples and setup guides

---

## Related Documentation

- [Multi-Project Aggregation](EXARP_MULTI_PROJECT_AGGREGATION.md) - Multi-project support
- [Chatbot Integration](EXARP_CHATBOT_INTEGRATION_STRATEGY.md) - Conversational interfaces
- [MCP Specification Compliance](EXARP_MCP_SPECIFICATION_COMPLIANCE.md) - MCP protocol

---

## References

- [Cursor IDE Documentation](https://cursor.sh/docs)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Cursor Rules Format](https://cursor.sh/docs/cursor-rules)

---

**Status**: Analysis & Enhancement Proposal - Ready for Implementation
**Priority**: High - Cursor integration is core to Exarp's usage
**Effort**: Medium - Requires Cursor configuration analysis and tool creation
