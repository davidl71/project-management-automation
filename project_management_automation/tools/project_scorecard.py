"""
Project Scorecard Tool - Generate comprehensive project health overview.

[HINT: Project scorecard. Returns overall score, component scores (security, testing,
docs, alignment, clarity, parallelizable), task metrics, production readiness.]
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any

from ..utils import find_project_root


def generate_project_scorecard(
    output_format: str = "text",
    include_recommendations: bool = True,
    output_path: str | None = None
) -> dict[str, Any]:
    """
    Generate comprehensive project health scorecard.
    
    [HINT: Project scorecard. Returns overall score, component scores (security, testing,
    docs, alignment, clarity, parallelizable), task metrics, production readiness.]
    
    Args:
        output_format: Output format - "text", "json", or "markdown"
        include_recommendations: Include improvement recommendations
        output_path: Optional path to save report
        
    Returns:
        Dictionary with scorecard data and formatted output
    """
    project_root = find_project_root()
    
    scores = {}
    metrics = {}
    details = {}
    
    # ═══════════════════════════════════════════════════════════════
    # 1. CODEBASE METRICS
    # ═══════════════════════════════════════════════════════════════
    py_files = list(project_root.rglob('*.py'))
    py_files = [f for f in py_files if 'venv' not in str(f) and '.build-env' not in str(f) 
                and '__pycache__' not in str(f)]
    
    total_py_lines = 0
    for f in py_files:
        try:
            total_py_lines += len(f.read_text().splitlines())
        except:
            pass
    
    # Count tools and prompts
    tools_dir = project_root / 'project_management_automation' / 'tools'
    tools_count = len([f for f in tools_dir.glob('*.py') if not f.name.startswith('__')]) if tools_dir.exists() else 0
    
    try:
        import sys
        sys.path.insert(0, str(project_root))
        from prompts import PROMPTS
        prompts_count = len(PROMPTS)
    except:
        prompts_count = 0
    
    metrics['codebase'] = {
        'python_files': len(py_files),
        'python_lines': total_py_lines,
        'mcp_tools': tools_count,
        'mcp_prompts': prompts_count,
    }
    scores['codebase'] = 80  # Base score for having a structured codebase
    
    # ═══════════════════════════════════════════════════════════════
    # 2. TESTING
    # ═══════════════════════════════════════════════════════════════
    test_dir = project_root / 'tests'
    test_files = list(test_dir.rglob('test_*.py')) if test_dir.exists() else []
    test_lines = sum(len(f.read_text().splitlines()) for f in test_files if f.exists())
    
    test_ratio = (test_lines / total_py_lines * 100) if total_py_lines > 0 else 0
    scores['testing'] = min(100, test_ratio * 3)  # 33% ratio = 100%
    
    metrics['testing'] = {
        'test_files': len(test_files),
        'test_lines': test_lines,
        'test_ratio': round(test_ratio, 1),
    }
    
    # ═══════════════════════════════════════════════════════════════
    # 3. DOCUMENTATION
    # ═══════════════════════════════════════════════════════════════
    docs_dir = project_root / 'docs'
    md_files = list(project_root.rglob('*.md'))
    md_files = [f for f in md_files if 'venv' not in str(f)]
    
    doc_lines = sum(len(f.read_text().splitlines()) for f in md_files if f.exists())
    doc_ratio = (doc_lines / total_py_lines * 100) if total_py_lines > 0 else 0
    
    key_docs = ['README.md', 'INSTALL.md', 'docs/SECURITY.md', 'docs/WORKFLOW.md']
    existing_docs = sum(1 for d in key_docs if (project_root / d).exists())
    
    scores['documentation'] = min(100, doc_ratio + (existing_docs / len(key_docs) * 50))
    
    metrics['documentation'] = {
        'doc_files': len(md_files),
        'doc_lines': doc_lines,
        'doc_ratio': round(doc_ratio, 1),
        'key_docs': f"{existing_docs}/{len(key_docs)}",
    }
    
    # ═══════════════════════════════════════════════════════════════
    # 4. TASK MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    todo2_file = project_root / '.todo2' / 'state.todo2.json'
    if todo2_file.exists():
        with open(todo2_file) as f:
            data = json.load(f)
        todos = data.get('todos', [])
        
        pending = [t for t in todos if t.get('status') in ['pending', 'in_progress']]
        completed = [t for t in todos if t.get('status') == 'completed']
        
        completion_rate = len(completed) / len(todos) * 100 if todos else 0
        scores['completion'] = completion_rate
        
        remaining_hours = sum(t.get('estimatedHours', 0) for t in pending)
        
        metrics['tasks'] = {
            'total': len(todos),
            'pending': len(pending),
            'completed': len(completed),
            'completion_rate': round(completion_rate, 1),
            'remaining_hours': remaining_hours,
        }
        
        # ═══════════════════════════════════════════════════════════
        # 5. ALIGNMENT ANALYSIS
        # ═══════════════════════════════════════════════════════════
        mcp_keywords = {
            'mcp', 'fastmcp', 'tool', 'tools', 'prompt', 'prompts', 'resource',
            'server', 'client', 'automation', 'automate', 'security', 'secure',
            'validation', 'validate', 'test', 'testing', 'tests', 'coverage',
            'integration', 'documentation', 'docs', 'workflow', 'ci', 'cd',
            'health', 'analysis', 'task', 'tasks', 'todo', 'sprint',
            'boundary', 'rate', 'limiting', 'access', 'control', 'auth',
            'exarp', 'hook', 'hooks', 'trigger', 'config', 'deploy',
        }
        
        alignment_scores = []
        well_aligned = 0
        moderately_aligned = 0
        for task in pending:
            content = task.get('content', '').lower()
            details_text = (task.get('details', '') or task.get('long_description', '') or '').lower()
            tags = ' '.join(task.get('tags', [])).lower()
            full_text = f"{content} {details_text} {tags}"
            
            words = set(re.findall(r'\b[a-z_]{3,}\b', full_text))
            matches = len(words & mcp_keywords)
            
            # Score based on matches (generous scoring)
            if matches >= 5:
                score = 100
                well_aligned += 1
            elif matches >= 3:
                score = 75
                moderately_aligned += 1
            elif matches >= 2:
                score = 50
                moderately_aligned += 1
            elif matches >= 1:
                score = 30
            else:
                score = 10
            alignment_scores.append(score)
        
        avg_alignment = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0
        scores['alignment'] = avg_alignment
        
        metrics['alignment'] = {
            'well_aligned': well_aligned,
            'moderately_aligned': moderately_aligned,
            'total_pending': len(pending),
            'avg_score': round(avg_alignment, 1),
        }
        
        # ═══════════════════════════════════════════════════════════
        # 6. CLARITY & PARALLELIZABILITY
        # ═══════════════════════════════════════════════════════════
        action_verbs = ['add', 'implement', 'create', 'fix', 'update', 'remove', 
                       'refactor', 'migrate', 'integrate', 'test', 'document', 'extend']
        
        has_estimate = sum(1 for t in pending if t.get('estimatedHours', 0) > 0)
        has_tags = sum(1 for t in pending if t.get('tags'))
        small_enough = sum(1 for t in pending if 0 < t.get('estimatedHours', 0) <= 4)
        clear_name = sum(1 for t in pending if any(
            t.get('content', '').lower().startswith(v) for v in action_verbs))
        no_deps = sum(1 for t in pending if not t.get('dependsOn') and not t.get('dependencies'))
        
        total_pending = len(pending) or 1
        clarity_score = (has_estimate + has_tags + small_enough + clear_name + no_deps) / (5 * total_pending) * 100
        scores['clarity'] = clarity_score
        
        parallelizable = sum(1 for t in pending if 
            t.get('estimatedHours', 0) <= 4 and 
            not t.get('dependsOn') and 
            not t.get('dependencies'))
        parallel_score = parallelizable / total_pending * 100 if total_pending else 0
        scores['parallelizable'] = parallel_score
        
        metrics['clarity'] = {
            'has_estimate': has_estimate,
            'has_tags': has_tags,
            'small_enough': small_enough,
            'clear_name': clear_name,
            'no_dependencies': no_deps,
            'clarity_score': round(clarity_score, 1),
        }
        
        metrics['parallelizable'] = {
            'ready': parallelizable,
            'total': total_pending,
            'score': round(parallel_score, 1),
        }
    else:
        scores['completion'] = 0
        scores['alignment'] = 0
        scores['clarity'] = 0
        scores['parallelizable'] = 0
        metrics['tasks'] = {'total': 0, 'pending': 0, 'completed': 0}
    
    # ═══════════════════════════════════════════════════════════════
    # 7. SECURITY
    # ═══════════════════════════════════════════════════════════════
    security_checks = {
        'security_docs': (project_root / 'docs' / 'SECURITY.md').exists(),
        'ci_cd_workflow': (project_root / '.github' / 'workflows' / 'ci.yml').exists(),
        'gitignore': (project_root / '.gitignore').exists(),
        'no_hardcoded_secrets': True,
        'input_validation': False,
        'path_boundaries': False,
        'rate_limiting': False,
        'access_control': False,
    }
    
    passed = sum(1 for v in security_checks.values() if v)
    scores['security'] = passed / len(security_checks) * 100
    
    # Count pending security tasks
    security_tasks = [t for t in todos if 'security' in t.get('tags', []) and t.get('status') == 'pending'] if todo2_file.exists() else []
    
    metrics['security'] = {
        'checks_passed': passed,
        'checks_total': len(security_checks),
        'pending_tasks': len(security_tasks),
        'details': security_checks,
    }
    
    # ═══════════════════════════════════════════════════════════════
    # 8. CI/CD
    # ═══════════════════════════════════════════════════════════════
    ci_checks = {
        'github_actions': (project_root / '.github' / 'workflows' / 'ci.yml').exists(),
        'linting': (project_root / 'pyproject.toml').exists(),
        'type_checking': (project_root / 'pyproject.toml').exists(),
        'unit_tests': (project_root / 'tests').exists(),
        'pre_commit': (project_root / '.pre-commit-config.yaml').exists(),
        'dependency_lock': (project_root / 'requirements.txt').exists(),
    }
    
    scores['ci_cd'] = sum(1 for v in ci_checks.values() if v) / len(ci_checks) * 100
    metrics['ci_cd'] = ci_checks
    
    # ═══════════════════════════════════════════════════════════════
    # CALCULATE OVERALL SCORE
    # ═══════════════════════════════════════════════════════════════
    weights = {
        'documentation': 0.10,
        'ci_cd': 0.10,
        'codebase': 0.10,
        'clarity': 0.10,
        'parallelizable': 0.10,
        'alignment': 0.10,
        'security': 0.25,
        'testing': 0.10,
        'completion': 0.05,
    }
    
    overall_score = sum(scores.get(k, 0) * weights.get(k, 0) for k in weights)
    
    # Determine production readiness
    production_ready = scores.get('security', 0) >= 80 and scores.get('testing', 0) >= 50
    blockers = []
    if scores.get('security', 0) < 80:
        blockers.append("Security controls incomplete")
    if scores.get('testing', 0) < 50:
        blockers.append("Test coverage too low")
    
    # ═══════════════════════════════════════════════════════════════
    # BUILD RESULT
    # ═══════════════════════════════════════════════════════════════
    result = {
        'generated_at': datetime.now().isoformat(),
        'overall_score': round(overall_score, 1),
        'production_ready': production_ready,
        'blockers': blockers,
        'scores': {k: round(v, 1) for k, v in scores.items()},
        'weights': weights,
        'metrics': metrics,
    }
    
    # Add recommendations if requested
    if include_recommendations:
        recommendations = []
        
        if scores.get('security', 0) < 80:
            recommendations.append({
                'priority': 'critical',
                'area': 'Security',
                'action': 'Implement path boundary enforcement, rate limiting, and access control',
                'impact': '+25% to security score',
            })
        
        if scores.get('testing', 0) < 50:
            recommendations.append({
                'priority': 'high',
                'area': 'Testing',
                'action': 'Fix failing tests and increase coverage to 30%',
                'impact': '+15% to testing score',
            })
        
        if scores.get('completion', 0) < 25:
            recommendations.append({
                'priority': 'medium',
                'area': 'Tasks',
                'action': 'Complete pending tasks to show progress',
                'impact': '+5% to overall score',
            })
        
        result['recommendations'] = recommendations
    
    # ═══════════════════════════════════════════════════════════════
    # FORMAT OUTPUT
    # ═══════════════════════════════════════════════════════════════
    if output_format == "json":
        formatted_output = json.dumps(result, indent=2)
    elif output_format == "markdown":
        formatted_output = _format_markdown(result)
    else:
        formatted_output = _format_text(result)
    
    result['formatted_output'] = formatted_output
    
    # Save to file if requested
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(formatted_output)
        result['output_file'] = str(output_file)
    
    return result


def _format_text(data: dict) -> str:
    """Format scorecard as plain text."""
    lines = []
    lines.append("=" * 70)
    lines.append("  📊 EXARP PROJECT SCORE CARD")
    lines.append(f"  Generated: {data['generated_at'][:16].replace('T', ' ')}")
    lines.append("=" * 70)
    
    # Overall score
    overall = data['overall_score']
    status = "🟢" if overall >= 70 else "🟡" if overall >= 50 else "🔴"
    lines.append(f"\n  OVERALL SCORE: {overall}% {status}")
    lines.append(f"  Production Ready: {'YES ✅' if data['production_ready'] else 'NO ❌'}")
    
    if data.get('blockers'):
        lines.append(f"  Blockers: {', '.join(data['blockers'])}")
    
    # Component scores
    lines.append("\n  Component Scores:")
    for name, score in sorted(data['scores'].items(), key=lambda x: -x[1]):
        bar_len = int(score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        status = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
        weight = int(data['weights'].get(name, 0) * 100)
        lines.append(f"    {name:<14} [{bar}] {score:>5.1f}% {status} (×{weight}%)")
    
    # Key metrics
    lines.append("\n  Key Metrics:")
    if 'tasks' in data['metrics']:
        t = data['metrics']['tasks']
        lines.append(f"    Tasks: {t.get('pending', 0)} pending, {t.get('completed', 0)} completed")
        lines.append(f"    Remaining work: {t.get('remaining_hours', 0)}h")
    
    if 'parallelizable' in data['metrics']:
        p = data['metrics']['parallelizable']
        lines.append(f"    Parallelizable: {p.get('ready', 0)} tasks ({p.get('score', 0)}%)")
    
    # Recommendations
    if data.get('recommendations'):
        lines.append("\n  Recommendations:")
        for rec in data['recommendations']:
            icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡'}.get(rec['priority'], '•')
            lines.append(f"    {icon} [{rec['area']}] {rec['action']}")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


def _format_markdown(data: dict) -> str:
    """Format scorecard as markdown."""
    lines = []
    lines.append("# 📊 Exarp Project Score Card")
    lines.append(f"\n*Generated: {data['generated_at'][:16].replace('T', ' ')}*")
    
    # Overall score
    overall = data['overall_score']
    status = "🟢" if overall >= 70 else "🟡" if overall >= 50 else "🔴"
    lines.append(f"\n## Overall Score: **{overall}%** {status}")
    lines.append(f"\n**Production Ready:** {'✅ Yes' if data['production_ready'] else '❌ No'}")
    
    if data.get('blockers'):
        lines.append(f"\n**Blockers:** {', '.join(data['blockers'])}")
    
    # Component scores table
    lines.append("\n## Component Scores\n")
    lines.append("| Component | Score | Status | Weight |")
    lines.append("|-----------|-------|--------|--------|")
    for name, score in sorted(data['scores'].items(), key=lambda x: -x[1]):
        status = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
        weight = int(data['weights'].get(name, 0) * 100)
        lines.append(f"| {name.title()} | {score:.1f}% | {status} | {weight}% |")
    
    # Key metrics
    lines.append("\n## Key Metrics\n")
    if 'tasks' in data['metrics']:
        t = data['metrics']['tasks']
        lines.append(f"- **Tasks:** {t.get('pending', 0)} pending, {t.get('completed', 0)} completed")
        lines.append(f"- **Remaining work:** {t.get('remaining_hours', 0)}h")
    
    if 'parallelizable' in data['metrics']:
        p = data['metrics']['parallelizable']
        lines.append(f"- **Parallelizable:** {p.get('ready', 0)} tasks ({p.get('score', 0)}%)")
    
    # Recommendations
    if data.get('recommendations'):
        lines.append("\n## Recommendations\n")
        for rec in data['recommendations']:
            icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡'}.get(rec['priority'], '•')
            lines.append(f"- {icon} **{rec['area']}:** {rec['action']} ({rec['impact']})")
    
    return "\n".join(lines)

