# Exarp Multi-Project Aggregation Strategy

**Date**: 2025-01-27
**Status**: Proposal
**Purpose**: Aggregate tasks from multiple projects/repositories into unified overview with priorities and interactive digest

---

## Overview

This document outlines a comprehensive strategy for aggregating tasks from multiple projects/repositories, providing unified overview, priority analysis, and interactive digest capabilities.

---

## Problem Statement

**Current State**: Exarp works with a single project at a time
**Need**: Aggregate tasks from multiple projects/repositories
**Sources**: MD files, Todo2, Google Tasks, Sheets, CalDAV, etc.
**Output**: Unified overview, priorities, interactive digest

---

## Integration Opportunities

### 1. Multi-Project Task Discovery (High Priority)

**Problem**: Need to discover and scan multiple projects/repositories

**Solution**: Create project discovery and scanning system

**Features**:
- **Project Registry**: Configuration file listing all projects
- **Auto-Discovery**: Scan directories for Git repositories
- **Source Detection**: Identify task sources in each project (MD files, Todo2, etc.)
- **Repository Metadata**: Track project names, paths, priorities

**Example Use Case**:
```python
def discover_projects_tool(
    root_directory: Optional[str] = None,
    config_path: Optional[str] = None,
    auto_discover: bool = True,
    output_path: Optional[str] = None
) -> str:
    """
    Discover projects/repositories for task aggregation.
    
    Discovery:
    - Scan directories for Git repositories
    - Detect task sources (MD files, Todo2, etc.)
    - Read project metadata
    - Build project registry
    """
    from pathlib import Path
    import json
    
    projects = []
    
    if auto_discover:
        # Scan for Git repositories
        root = Path(root_directory or Path.cwd())
        for git_dir in root.rglob('.git'):
            project_path = git_dir.parent
            projects.append({
                'name': project_path.name,
                'path': str(project_path),
                'type': 'git',
                'sources': detect_task_sources(project_path)
            })
    
    # Load from config if provided
    if config_path:
        with open(config_path, 'r') as f:
            config_projects = json.load(f)
            projects.extend(config_projects)
    
    return json.dumps(projects, indent=2)
```

**Benefits**:
- Automatic project discovery
- Flexible configuration
- Source detection
- Project registry

---

### 2. Multi-Source Task Extraction (High Priority)

**Problem**: Tasks exist in various formats across projects

**Solution**: Unified task extraction from all supported sources

**Sources**:
- **Markdown Files**: TODO lists, task lists in MD
- **Todo2**: `.todo2/state.todo2.json`
- **Google Tasks**: Google Tasks API
- **Google Sheets**: Task management sheets
- **CalDAV**: CalDAV-compatible task managers
- **Jupyter Notebooks**: TODO/FIXME comments, markdown tasks
- **Code Comments**: TODO/FIXME in source code

**Example Use Case**:
```python
def extract_tasks_from_project_tool(
    project_path: str,
    sources: Optional[List[str]] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Extract tasks from a single project using all supported sources.
    
    Sources:
    - markdown: MD files with task lists
    - todo2: Todo2 state file
    - google_tasks: Google Tasks API
    - google_sheets: Google Sheets
    - caldav: CalDAV tasks
    - jupyter: Jupyter Notebooks
    - code: Source code comments
    """
    from pathlib import Path
    from exarp_project_management.scripts.multi_project_aggregator import TaskExtractor
    
    project = Path(project_path)
    extractor = TaskExtractor(project)
    
    # Extract from all sources
    tasks = extractor.extract_all(sources=sources)
    
    # Add project metadata
    for task in tasks:
        task['project'] = project.name
        task['project_path'] = str(project)
    
    return json.dumps(tasks, indent=2)
```

**Benefits**:
- Unified extraction
- Multiple source support
- Project metadata
- Flexible source selection

---

### 3. Task Aggregation and Deduplication (High Priority)

**Problem**: Tasks from multiple projects need aggregation and deduplication

**Solution**: Aggregate tasks with intelligent deduplication

**Features**:
- **Task Aggregation**: Combine tasks from all projects
- **Deduplication**: Detect duplicate tasks across projects
- **Priority Normalization**: Normalize priorities across systems
- **Tag Aggregation**: Combine tags from all sources

**Example Use Case**:
```python
def aggregate_tasks_tool(
    project_paths: List[str],
    sources: Optional[List[str]] = None,
    deduplicate: bool = True,
    priority_normalization: bool = True,
    output_path: Optional[str] = None
) -> str:
    """
    Aggregate tasks from multiple projects.
    
    Aggregation:
    - Extract tasks from all projects
    - Deduplicate across projects
    - Normalize priorities
    - Combine tags
    - Generate unified overview
    """
    from exarp_project_management.scripts.multi_project_aggregator import TaskAggregator
    
    aggregator = TaskAggregator()
    
    # Extract from all projects
    all_tasks = []
    for project_path in project_paths:
        tasks = extract_tasks_from_project(project_path, sources)
        all_tasks.extend(tasks)
    
    # Aggregate and deduplicate
    aggregated = aggregator.aggregate(all_tasks, deduplicate, priority_normalization)
    
    return json.dumps(aggregated, indent=2)
```

**Benefits**:
- Unified task view
- Duplicate detection
- Priority normalization
- Tag aggregation

---

### 4. Priority Analysis Across Projects (High Priority)

**Problem**: Need to understand priorities across all projects

**Solution**: Cross-project priority analysis

**Features**:
- **Priority Distribution**: Analyze priority distribution across projects
- **High-Priority Tasks**: Identify high-priority tasks across all projects
- **Project Priority Ranking**: Rank projects by task priorities
- **Priority Conflicts**: Detect conflicting priorities

**Example Use Case**:
```python
def analyze_priorities_tool(
    aggregated_tasks: List[Dict],
    output_path: Optional[str] = None
) -> str:
    """
    Analyze priorities across all projects.
    
    Analysis:
    - Priority distribution by project
    - High-priority task identification
    - Project priority ranking
    - Priority conflict detection
    """
    from exarp_project_management.scripts.multi_project_aggregator import PriorityAnalyzer
    
    analyzer = PriorityAnalyzer()
    
    analysis = {
        'priority_distribution': analyzer.distribution(aggregated_tasks),
        'high_priority_tasks': analyzer.high_priority(aggregated_tasks),
        'project_ranking': analyzer.rank_projects(aggregated_tasks),
        'conflicts': analyzer.detect_conflicts(aggregated_tasks)
    }
    
    return json.dumps(analysis, indent=2)
```

**Benefits**:
- Cross-project insights
- Priority visibility
- Project ranking
- Conflict detection

---

### 5. Interactive Digest Generation (High Priority)

**Problem**: Need interactive overview and digest of all tasks

**Solution**: Generate interactive HTML/CLI digest

**Features**:
- **HTML Dashboard**: Interactive web dashboard
- **CLI Interface**: Command-line interactive interface
- **Filtering**: Filter by project, priority, status, tags
- **Sorting**: Sort by priority, due date, project
- **Search**: Search tasks across all projects
- **Export**: Export to various formats (JSON, CSV, Markdown)

**Example Use Case**:
```python
def generate_interactive_digest_tool(
    aggregated_tasks: List[Dict],
    format: str = "html",  # html, cli, json, csv, markdown
    output_path: Optional[str] = None,
    filters: Optional[Dict] = None,
    sort_by: Optional[str] = None
) -> str:
    """
    Generate interactive digest of aggregated tasks.
    
    Formats:
    - html: Interactive web dashboard
    - cli: Command-line interface
    - json: JSON export
    - csv: CSV export
    - markdown: Markdown report
    
    Features:
    - Filtering (project, priority, status, tags)
    - Sorting (priority, due date, project)
    - Search across all tasks
    - Export to various formats
    """
    from exarp_project_management.scripts.multi_project_aggregator import DigestGenerator
    
    generator = DigestGenerator(format)
    
    # Apply filters
    if filters:
        aggregated_tasks = generator.filter(aggregated_tasks, filters)
    
    # Sort
    if sort_by:
        aggregated_tasks = generator.sort(aggregated_tasks, sort_by)
    
    # Generate digest
    digest = generator.generate(aggregated_tasks, output_path)
    
    return json.dumps({'digest_path': digest, 'format': format}, indent=2)
```

**Benefits**:
- Interactive overview
- Flexible filtering
- Multiple export formats
- Search capabilities

---

### 6. Project Registry Management (Medium Priority)

**Problem**: Need to manage project registry configuration

**Solution**: Create project registry management system

**Features**:
- **Registry Configuration**: JSON/YAML configuration file
- **Project Metadata**: Name, path, priority, tags
- **Source Configuration**: Which sources to use per project
- **Update Management**: Add/remove/update projects

**Example Use Case**:
```python
def manage_project_registry_tool(
    action: str,  # add, remove, update, list
    project_name: Optional[str] = None,
    project_path: Optional[str] = None,
    config_path: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> str:
    """
    Manage project registry configuration.
    
    Actions:
    - add: Add new project to registry
    - remove: Remove project from registry
    - update: Update project metadata
    - list: List all projects in registry
    """
    from exarp_project_management.scripts.multi_project_aggregator import ProjectRegistry
    
    registry = ProjectRegistry(config_path)
    
    if action == 'add':
        registry.add(project_name, project_path, metadata)
    elif action == 'remove':
        registry.remove(project_name)
    elif action == 'update':
        registry.update(project_name, metadata)
    elif action == 'list':
        return json.dumps(registry.list_all(), indent=2)
    
    return json.dumps({'status': 'success', 'action': action}, indent=2)
```

**Benefits**:
- Centralized configuration
- Easy project management
- Metadata tracking
- Source configuration

---

## Integration Strategy

### Phase 1: Multi-Project Discovery and Extraction (High Priority)

**Goal**: Discover projects and extract tasks

**Implementation**:
1. Create `discover_projects_tool`
2. Create `extract_tasks_from_project_tool`
3. Support multiple task sources
4. Build project registry

**Benefits**:
- Project discovery
- Task extraction
- Source support
- Registry management

---

### Phase 2: Task Aggregation and Analysis (High Priority)

**Goal**: Aggregate tasks and analyze priorities

**Implementation**:
1. Create `aggregate_tasks_tool`
2. Create `analyze_priorities_tool`
3. Implement deduplication
4. Normalize priorities

**Benefits**:
- Unified task view
- Priority analysis
- Duplicate detection
- Cross-project insights

---

### Phase 3: Interactive Digest (High Priority)

**Goal**: Generate interactive digest

**Implementation**:
1. Create `generate_interactive_digest_tool`
2. Build HTML dashboard
3. Create CLI interface
4. Add filtering and sorting

**Benefits**:
- Interactive overview
- Flexible filtering
- Multiple formats
- Search capabilities

---

### Phase 4: Advanced Features (Medium Priority)

**Goal**: Advanced aggregation features

**Implementation**:
1. Real-time updates
2. Webhook integration
3. Scheduled aggregation
4. Notification system

**Benefits**:
- Real-time sync
- Automated updates
- Notifications
- Webhook support

---

## Use Cases

### Use Case 1: Multi-Project Overview

**Problem**: Need overview of all tasks across projects

**Solution**: Generate unified overview

```python
def generate_multi_project_overview_tool(
    project_registry_path: str,
    output_path: Optional[str] = None,
    format: str = "html"
) -> str:
    """
    Generate unified overview of all tasks across projects.
    
    Overview includes:
    - Total tasks by project
    - Priority distribution
    - High-priority tasks
    - Project rankings
    - Interactive dashboard
    """
    # Discover projects
    projects = discover_projects(project_registry_path)
    
    # Extract tasks
    all_tasks = []
    for project in projects:
        tasks = extract_tasks_from_project(project['path'])
        all_tasks.extend(tasks)
    
    # Aggregate
    aggregated = aggregate_tasks(all_tasks)
    
    # Analyze priorities
    priorities = analyze_priorities(aggregated)
    
    # Generate digest
    digest = generate_interactive_digest(aggregated, format, output_path)
    
    return json.dumps({
        'overview': {
            'total_tasks': len(aggregated),
            'projects': len(projects),
            'priorities': priorities,
            'digest_path': digest
        }
    }, indent=2)
```

---

### Use Case 2: Priority-Based Filtering

**Problem**: Need to see high-priority tasks across all projects

**Solution**: Filter by priority

```python
def filter_high_priority_tasks_tool(
    project_registry_path: str,
    priority_threshold: str = "high",
    output_path: Optional[str] = None
) -> str:
    """
    Filter high-priority tasks across all projects.
    
    Filters:
    - Priority threshold (high, medium, low)
    - Project selection
    - Status filtering
    """
    # Aggregate tasks
    aggregated = aggregate_tasks_from_registry(project_registry_path)
    
    # Filter by priority
    high_priority = [
        task for task in aggregated
        if task.get('priority') == priority_threshold
    ]
    
    # Generate digest
    digest = generate_interactive_digest(
        high_priority,
        format='html',
        output_path=output_path
    )
    
    return json.dumps({
        'high_priority_tasks': len(high_priority),
        'digest_path': digest
    }, indent=2)
```

---

### Use Case 3: Interactive CLI Dashboard

**Problem**: Need interactive CLI for task management

**Solution**: Create CLI dashboard

```python
def interactive_cli_dashboard_tool(
    project_registry_path: str
) -> str:
    """
    Launch interactive CLI dashboard for multi-project tasks.
    
    Features:
    - Browse tasks by project
    - Filter by priority, status, tags
    - Search tasks
    - Update task status
    - Export tasks
    """
    from exarp_project_management.scripts.multi_project_aggregator import CLIDashboard
    
    dashboard = CLIDashboard(project_registry_path)
    dashboard.launch()
    
    return json.dumps({'status': 'dashboard_closed'}, indent=2)
```

---

## Library Recommendations

### Task Extraction

**Markdown Parsing**: `markdown>=3.4.0` or `mistune>=3.0.0`
- Parse markdown task lists
- Extract TODO items

**Git Integration**: `GitPython>=3.1.0`
- Repository discovery
- Git metadata

**YAML/JSON Parsing**: `pyyaml>=6.0.0`, `json` (built-in)
- Configuration files
- Task data

### Aggregation and Analysis

**Pandas**: `pandas>=2.0.0` (optional)
- Task data analysis
- Aggregation operations
- Export to CSV/Excel

**NetworkX**: `networkx>=3.0.0` (already in Exarp)
- Task dependency graphs
- Project relationships

### Interactive Dashboard

**Rich**: `rich>=13.0.0`
- CLI dashboard
- Terminal formatting
- Interactive tables

**Jinja2**: `jinja2>=3.1.0`
- HTML template rendering
- Dashboard generation

**Flask/FastAPI**: `flask>=3.0.0` or `fastapi>=0.100.0` (optional)
- Web dashboard
- API endpoints

---

## Dependencies

### Required

- **GitPython**: `GitPython>=3.1.0` (repository discovery)
- **markdown**: `markdown>=3.4.0` (markdown parsing)
- **pyyaml**: `pyyaml>=6.0.0` (configuration files)
- **rich**: `rich>=13.0.0` (CLI dashboard)

### Optional

- **pandas**: `pandas>=2.0.0` (data analysis)
- **jinja2**: `jinja2>=3.1.0` (HTML templates)
- **flask**: `flask>=3.0.0` (web dashboard)

### Installation

```bash
# Core multi-project support
pip install GitPython markdown pyyaml rich

# Optional: Advanced features
pip install pandas jinja2 flask
```

---

## Implementation Examples

### Example 1: Project Registry

```python
import json
from pathlib import Path
from typing import List, Dict, Optional

class ProjectRegistry:
    """Manage project registry configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / '.exarp' / 'projects.json'
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.projects = self._load()
    
    def _load(self) -> List[Dict]:
        """Load project registry."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save(self):
        """Save project registry."""
        with open(self.config_path, 'w') as f:
            json.dump(self.projects, f, indent=2)
    
    def add(self, name: str, path: str, metadata: Optional[Dict] = None):
        """Add project to registry."""
        project = {
            'name': name,
            'path': str(Path(path).absolute()),
            'metadata': metadata or {},
            'sources': self._detect_sources(Path(path))
        }
        self.projects.append(project)
        self._save()
    
    def _detect_sources(self, project_path: Path) -> List[str]:
        """Detect task sources in project."""
        sources = []
        
        # Check for Todo2
        if (project_path / '.todo2' / 'state.todo2.json').exists():
            sources.append('todo2')
        
        # Check for markdown files
        md_files = list(project_path.rglob('*.md'))
        if md_files:
            sources.append('markdown')
        
        # Check for Jupyter notebooks
        if list(project_path.rglob('*.ipynb')):
            sources.append('jupyter')
        
        return sources
```

### Example 2: Task Aggregator

```python
from typing import List, Dict
from collections import defaultdict

class TaskAggregator:
    """Aggregate tasks from multiple projects."""
    
    def aggregate(self, tasks: List[Dict], deduplicate: bool = True, 
                  normalize_priorities: bool = True) -> List[Dict]:
        """Aggregate tasks with optional deduplication."""
        # Normalize priorities
        if normalize_priorities:
            tasks = self._normalize_priorities(tasks)
        
        # Deduplicate
        if deduplicate:
            tasks = self._deduplicate(tasks)
        
        # Add aggregation metadata
        for task in tasks:
            task['aggregated'] = True
            task['source_count'] = len(task.get('sources', []))
        
        return tasks
    
    def _normalize_priorities(self, tasks: List[Dict]) -> List[Dict]:
        """Normalize priorities across different systems."""
        priority_map = {
            'critical': 5,
            'high': 4,
            'medium': 3,
            'low': 2,
            'lowest': 1
        }
        
        for task in tasks:
            priority = task.get('priority', 'medium').lower()
            task['priority_normalized'] = priority_map.get(priority, 3)
            task['priority_original'] = priority
        
        return tasks
    
    def _deduplicate(self, tasks: List[Dict]) -> List[Dict]:
        """Deduplicate tasks across projects."""
        seen = {}
        deduplicated = []
        
        for task in tasks:
            # Create signature from title and description
            signature = self._create_signature(task)
            
            if signature in seen:
                # Merge with existing task
                existing = seen[signature]
                existing['sources'].append(task.get('source'))
                existing['projects'].append(task.get('project'))
            else:
                # New task
                task['sources'] = [task.get('source')]
                task['projects'] = [task.get('project')]
                seen[signature] = task
                deduplicated.append(task)
        
        return deduplicated
    
    def _create_signature(self, task: Dict) -> str:
        """Create signature for deduplication."""
        title = task.get('title', '').lower().strip()
        description = task.get('description', '').lower().strip()[:100]
        return f"{title}:{description}"
```

### Example 3: Interactive Digest Generator

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from jinja2 import Template

class DigestGenerator:
    """Generate interactive digest of aggregated tasks."""
    
    def __init__(self, format: str = "html"):
        self.format = format
        self.console = Console()
    
    def generate(self, tasks: List[Dict], output_path: Optional[Path] = None) -> str:
        """Generate digest in specified format."""
        if self.format == "html":
            return self._generate_html(tasks, output_path)
        elif self.format == "cli":
            return self._generate_cli(tasks)
        elif self.format == "json":
            return self._generate_json(tasks, output_path)
        elif self.format == "markdown":
            return self._generate_markdown(tasks, output_path)
        else:
            raise ValueError(f"Unsupported format: {self.format}")
    
    def _generate_html(self, tasks: List[Dict], output_path: Optional[Path]) -> str:
        """Generate HTML dashboard."""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Multi-Project Task Overview</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .task { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }
                .priority-high { border-left: 4px solid red; }
                .priority-medium { border-left: 4px solid orange; }
                .priority-low { border-left: 4px solid green; }
            </style>
        </head>
        <body>
            <h1>Multi-Project Task Overview</h1>
            <p>Total Tasks: {{ tasks|length }}</p>
            {% for task in tasks %}
            <div class="task priority-{{ task.priority }}">
                <h3>{{ task.title }}</h3>
                <p>Project: {{ task.project }}</p>
                <p>Priority: {{ task.priority }}</p>
            </div>
            {% endfor %}
        </body>
        </html>
        """)
        
        html = template.render(tasks=tasks)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(html)
            return str(output_path)
        
        return html
    
    def _generate_cli(self, tasks: List[Dict]) -> str:
        """Generate CLI dashboard."""
        table = Table(title="Multi-Project Tasks")
        table.add_column("Project")
        table.add_column("Title")
        table.add_column("Priority")
        table.add_column("Status")
        
        for task in tasks:
            table.add_row(
                task.get('project', 'Unknown'),
                task.get('title', '')[:50],
                task.get('priority', 'medium'),
                task.get('status', 'todo')
            )
        
        self.console.print(table)
        return "CLI dashboard displayed"
```

---

## Benefits for Exarp

### 1. Multi-Project Visibility

- **Unified Overview**: See all tasks across projects
- **Priority Analysis**: Understand priorities across projects
- **Project Ranking**: Identify high-priority projects
- **Cross-Project Insights**: Find patterns across projects

### 2. Task Management

- **Deduplication**: Avoid duplicate work
- **Priority Normalization**: Consistent priority handling
- **Source Flexibility**: Support multiple task sources
- **Aggregation**: Combine tasks from all sources

### 3. User Convenience

- **Interactive Dashboard**: Easy task browsing
- **Flexible Filtering**: Filter by project, priority, status
- **Multiple Formats**: HTML, CLI, JSON, CSV, Markdown
- **Search**: Search across all projects

---

## Next Steps

1. **Research**: Evaluate multi-project aggregation patterns
2. **Design**: Design project registry format
3. **Implement**: Create aggregation tools
4. **Test**: Validate with real multi-project setups
5. **Document**: Add usage examples and setup guides

---

## Related Documentation

- [Task Management Integration](EXARP_TASK_MANAGEMENT_INTEGRATION.md) - Task source integrations
- [Jupyter Notebook Integration](EXARP_JUPYTER_NOTEBOOK_INTEGRATION.md) - Notebook task extraction
- [Google Workspace Integration](EXARP_GOOGLE_WORKSPACE_INTEGRATION.md) - Google Tasks/Sheets

---

## References

- [GitPython Documentation](https://gitpython.readthedocs.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

---

**Status**: Proposal - Ready for Research and Implementation
**Priority**: High - Multi-project aggregation is a key feature for managing multiple repositories
**Effort**: High - Requires significant implementation for aggregation, deduplication, and interactive digest

