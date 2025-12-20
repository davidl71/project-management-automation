# Ollama Integration Guide for Exarp PMA

This guide shows how to use Ollama/CodeLlama within the exarp_pma project for enhanced code analysis, documentation generation, and intelligent automation.

## Table of Contents

1. [Use Cases](#use-cases)
2. [Integration Examples](#integration-examples)
3. [Enhanced Tools](#enhanced-tools)
4. [Workflow Integration](#workflow-integration)

---

## Use Cases

### 1. **Code Analysis & Documentation**

**Use Case**: Generate code documentation, explain complex code, analyze code patterns

**Example**:
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Analyze a code file and generate documentation
code_content = """
def analyze_todo2_alignment(project_root, threshold=0.7):
    # Complex function logic here...
    pass
"""

prompt = f"""
Analyze this Python function and generate:
1. A clear docstring
2. Parameter descriptions
3. Return value documentation
4. Usage examples

Code:
{code_content}
"""

docs = generate_with_ollama(prompt, model="codellama")
```

### 2. **Context Summarization Enhancement**

**Use Case**: Use LLM to create intelligent summaries of tool outputs

**Current**: Pattern-based summarization
**Enhanced**: LLM-powered semantic summarization

**Example**:
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama
from project_management_automation.tools.context_summarizer import summarize_context

def summarize_with_llm(data, level="brief"):
    """Enhanced summarization using CodeLlama."""
    # First, get pattern-based summary
    pattern_summary = summarize_context(data, level=level)
    
    # Then enhance with LLM for better semantic understanding
    prompt = f"""
Summarize this project management data in a {level} format.
Focus on actionable insights and key metrics.

Data:
{pattern_summary}

Provide a concise, actionable summary.
"""
    
    llm_summary = generate_with_ollama(prompt, model="codellama")
    return llm_summary
```

### 3. **PRD Generation Enhancement**

**Use Case**: Generate Product Requirements Documents from codebase analysis

**Example**:
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama
from project_management_automation.tools.prd_generator import generate_prd

def generate_prd_with_llm(project_root):
    """Generate PRD with LLM enhancement."""
    # Get base PRD structure
    base_prd = generate_prd(project_root)
    
    # Enhance with LLM analysis
    prompt = f"""
Analyze this PRD and enhance it with:
1. Clearer user stories
2. Better acceptance criteria
3. Technical requirements
4. Success metrics

PRD:
{base_prd}
"""
    
    enhanced_prd = generate_with_ollama(prompt, model="codellama")
    return enhanced_prd
```

### 4. **Task Analysis & Recommendations**

**Use Case**: Analyze tasks and provide intelligent recommendations

**Example**:
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

def analyze_task_with_llm(task_description, code_context=None):
    """Analyze a task and provide recommendations."""
    prompt = f"""
Analyze this development task and provide:
1. Complexity assessment (low/medium/high)
2. Estimated effort
3. Dependencies to check
4. Recommended approach
5. Potential risks

Task: {task_description}
"""
    
    if code_context:
        prompt += f"\n\nRelevant code context:\n{code_context}"
    
    analysis = generate_with_ollama(prompt, model="codellama")
    return analysis
```

### 5. **Code Review & Suggestions**

**Use Case**: Automated code review and improvement suggestions

**Example**:
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

def review_code_with_llm(code, file_path):
    """Review code and suggest improvements."""
    prompt = f"""
Review this Python code and provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance improvements
4. Best practice suggestions
5. Security concerns

File: {file_path}
Code:
{code}
"""
    
    review = generate_with_ollama(prompt, model="codellama")
    return review
```

---

## Integration Examples

### Example 1: Enhanced Documentation Health Check

Create a new tool that uses Ollama to generate documentation improvements:

```python
# project_management_automation/tools/docs_health_llm.py

from project_management_automation.tools.ollama_integration import generate_with_ollama
from project_management_automation.tools.docs_health import check_documentation_health
import json

def check_documentation_health_with_suggestions(output_path=None, create_tasks=True):
    """Check docs health and get LLM-powered improvement suggestions."""
    # Run standard health check
    health_result = check_documentation_health(output_path, create_tasks)
    health_data = json.loads(health_result)
    
    if not health_data.get("success"):
        return health_result
    
    # Get LLM suggestions
    prompt = f"""
Based on this documentation health report, provide:
1. Top 3 priority improvements
2. Quick wins (easy fixes)
3. Long-term recommendations
4. Documentation structure suggestions

Health Report:
{json.dumps(health_data.get("data", {}), indent=2)}
"""
    
    suggestions = generate_with_ollama(prompt, model="codellama")
    suggestions_data = json.loads(suggestions)
    
    # Combine results
    enhanced_result = {
        "health_check": health_data.get("data", {}),
        "llm_suggestions": suggestions_data.get("data", {}).get("response", "")
    }
    
    return json.dumps({"success": True, "data": enhanced_result}, indent=2)
```

### Example 2: Code-Aware Task Analysis

Enhance task analysis with code context:

```python
# project_management_automation/tools/task_analysis_llm.py

from project_management_automation.tools.ollama_integration import generate_with_ollama
from project_management_automation.tools.duplicate_detection import detect_duplicate_tasks
import json
from pathlib import Path

def analyze_task_with_code_context(task_id, project_root):
    """Analyze a task with relevant code context."""
    # Get task details (from Todo2)
    # ... fetch task ...
    
    # Find relevant code files
    # ... search codebase for task keywords ...
    
    # Get code context
    relevant_files = find_relevant_code(task_description, project_root)
    code_context = "\n\n".join([
        f"File: {f}\n{read_file(f)}" 
        for f in relevant_files[:3]  # Limit to 3 files
    ])
    
    # Analyze with LLM
    prompt = f"""
Task: {task_description}

Relevant code:
{code_context}

Analyze:
1. Is this task feasible given the codebase?
2. What files need to be modified?
3. Are there similar implementations to reference?
4. Potential blockers or dependencies?
"""
    
    analysis = generate_with_ollama(prompt, model="codellama")
    return analysis
```

### Example 3: Intelligent Context Summarization

Enhance the existing context summarizer:

```python
# Enhancement to context_summarizer.py

from project_management_automation.tools.ollama_integration import generate_with_ollama

def summarize_context_with_llm(
    data: Union[str, dict, list],
    level: str = "brief",
    use_llm: bool = False,
) -> str:
    """Summarize with optional LLM enhancement."""
    # Get pattern-based summary first (fast)
    pattern_summary = summarize_context(data, level=level)
    
    if not use_llm:
        return pattern_summary
    
    # Enhance with LLM for better semantic understanding
    prompt = f"""
Summarize this project management data in a {level} format.
Focus on:
- Key metrics and numbers
- Actionable items
- Critical issues
- Next steps

Data:
{pattern_summary}

Provide a concise, well-structured summary.
"""
    
    llm_summary = generate_with_ollama(prompt, model="codellama", max_tokens=500)
    return llm_summary
```

---

## Enhanced Tools

### Tool: `generate_code_documentation`

```python
# project_management_automation/tools/code_documentation.py

from project_management_automation.tools.ollama_integration import generate_with_ollama
import json
from pathlib import Path

def generate_code_documentation(
    file_path: str,
    output_path: Optional[str] = None,
    style: str = "google",  # google, numpy, sphinx
) -> str:
    """
    Generate documentation for a code file using CodeLlama.
    
    Args:
        file_path: Path to Python file
        output_path: Optional output path for docs
        style: Documentation style (google, numpy, sphinx)
    
    Returns:
        JSON with generated documentation
    """
    file = Path(file_path)
    if not file.exists():
        return json.dumps({
            "success": False,
            "error": f"File not found: {file_path}"
        })
    
    code = file.read_text()
    
    prompt = f"""
Generate comprehensive documentation for this Python code.
Use {style} docstring style.

Requirements:
1. Module-level docstring
2. Function/class docstrings with:
   - Description
   - Parameters (Args)
   - Returns
   - Raises (if applicable)
   - Examples (if helpful)
3. Inline comments for complex logic

Code:
{code}
"""
    
    docs = generate_with_ollama(prompt, model="codellama")
    docs_data = json.loads(docs)
    
    if output_path:
        output_file = Path(output_path)
        output_file.write_text(docs_data.get("data", {}).get("response", ""))
    
    return docs
```

### Tool: `analyze_code_quality`

```python
# project_management_automation/tools/code_quality_llm.py

from project_management_automation.tools.ollama_integration import generate_with_ollama
import json
from pathlib import Path

def analyze_code_quality(
    file_path: str,
    include_suggestions: bool = True,
) -> str:
    """
    Analyze code quality using CodeLlama.
    
    Returns:
        JSON with quality metrics and suggestions
    """
    file = Path(file_path)
    code = file.read_text()
    
    prompt = f"""
Analyze this Python code for quality and provide:
1. Overall quality score (0-100)
2. Code smells detected
3. Performance issues
4. Security concerns
5. Best practice violations
6. Refactoring suggestions

Code:
{code}
"""
    
    analysis = generate_with_ollama(prompt, model="codellama")
    return analysis
```

---

## Workflow Integration

### Workflow 1: Daily Code Review

```python
# Automated daily code review using Ollama

def daily_code_review(project_root):
    """Run daily code review with LLM analysis."""
    # 1. Find recently modified files
    recent_files = get_recent_files(project_root, days=1)
    
    # 2. Review each file
    reviews = []
    for file_path in recent_files:
        if file_path.suffix == ".py":
            review = analyze_code_quality(str(file_path))
            reviews.append(review)
    
    # 3. Generate summary
    summary_prompt = f"""
Summarize these code reviews:
{json.dumps(reviews, indent=2)}

Provide:
1. Overall quality trends
2. Common issues
3. Priority fixes
"""
    
    summary = generate_with_ollama(summary_prompt, model="codellama")
    return summary
```

### Workflow 2: Sprint Planning Enhancement

```python
# Enhance sprint planning with code-aware task analysis

def enhanced_sprint_planning(sprint_tasks, project_root):
    """Plan sprint with code context awareness."""
    analyses = []
    
    for task in sprint_tasks:
        # Find relevant code
        code_context = find_relevant_code(task.description, project_root)
        
        # Analyze task feasibility
        prompt = f"""
Task: {task.description}

Relevant code:
{code_context}

Assess:
1. Complexity (1-5)
2. Estimated effort (hours)
3. Dependencies
4. Risk level
5. Recommended approach
"""
        
        analysis = generate_with_ollama(prompt, model="codellama")
        analyses.append(analysis)
    
    # Generate sprint summary
    summary_prompt = f"""
Based on these task analyses, provide:
1. Sprint capacity estimate
2. Risk assessment
3. Recommended task order
4. Potential blockers

Analyses:
{json.dumps(analyses, indent=2)}
"""
    
    sprint_plan = generate_with_ollama(summary_prompt, model="codellama")
    return sprint_plan
```

---

## Best Practices

### 1. **Use Ollama for Semantic Understanding**

- ✅ Code analysis and explanation
- ✅ Documentation generation
- ✅ Task analysis with context
- ✅ Code review and suggestions

### 2. **Use Pattern-Based Tools for Speed**

- ✅ Simple summarization (use existing `summarize_context`)
- ✅ Structured data extraction
- ✅ Quick metrics calculation

### 3. **Combine Both Approaches**

```python
# Fast pattern-based summary
quick_summary = summarize_context(data, level="brief")

# Enhanced with LLM for insights
enhanced = generate_with_ollama(
    f"Provide insights on: {quick_summary}",
    model="codellama"
)
```

### 4. **Cache LLM Results**

For repeated queries, cache results to save time and resources.

---

## Performance Considerations

- **CodeLlama**: ~3-10 seconds per request (depends on prompt length)
- **Use for**: Complex analysis, documentation, code review
- **Skip for**: Simple metrics, pattern matching, quick summaries

---

## Next Steps

1. **Integrate into existing tools**: Add LLM enhancement to `context_summarizer`, `prd_generator`
2. **Create new LLM-powered tools**: `generate_code_documentation`, `analyze_code_quality`
3. **Workflow automation**: Daily code review, sprint planning enhancement
4. **Caching layer**: Cache LLM results for repeated queries

---

## Example: Complete Integration

See `project_management_automation/tools/ollama_enhanced_tools.py` for complete examples of enhanced tools using Ollama.

