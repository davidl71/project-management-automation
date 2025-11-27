# Project Goals - Exarp MCP Server

**Project**: Project Management Automation MCP Server (Exarp)
**Type**: MCP Server / Developer Tools
**Updated**: 2025-11-26

---

## Vision

A comprehensive MCP server providing project management automation tools for AI-assisted development workflows. Enables documentation health checks, task alignment, duplicate detection, security scanning, and intelligent automation orchestration.

---

## Strategic Phases

### Phase 1: Core Infrastructure
**Timeline**: Foundation
**Priority**: Critical

**Goals**:
- MCP server setup and configuration
- Tool registration and discovery
- Error handling and logging
- Basic automation tools

**Keywords**: mcp, server, infrastructure, setup, configuration, tool, registration, error handling, logging, foundation

---

### Phase 2: Integration & Interoperability  
**Timeline**: Integration
**Priority**: High

**Goals**:
- Agentic-tools MCP integration
- Context7 library verification
- Sequential Thinking workflow generation
- Tractatus structured analysis
- Cross-MCP communication

**Keywords**: integration, mcp, agentic-tools, context7, sequential thinking, tractatus, interoperability, client, async

---

### Phase 3: Automation & Intelligence
**Timeline**: Enhancement
**Priority**: High

**Goals**:
- Sprint automation orchestration
- Nightly task processing
- Batch task approval
- AI wishlist generation
- Human contribution identification

**Keywords**: automation, sprint, nightly, batch, orchestration, wishlist, ai, intelligent, background, parallel

---

### Phase 4: Quality & Testing
**Timeline**: Stabilization
**Priority**: Medium

**Goals**:
- Test coverage improvements
- Test runner integration
- Coverage analysis tools
- CI/CD validation
- Security scanning

**Keywords**: testing, test, coverage, ci, cd, validation, security, scan, quality, unittest, pytest

---

### Phase 5: Documentation & Polish
**Timeline**: Documentation
**Priority**: Medium

**Goals**:
- Documentation health tools
- External tool hints
- API documentation
- User guides
- Best practices

**Keywords**: documentation, docs, health, hints, guide, readme, api, polish, cleanup

---

## Design Constraints

### Tool Count Limit: ≤30 Tools

**Rationale**: Context pollution is the silent killer of agentic workflows. Too many tools:
- Increase token usage in tool discovery
- Slow AI decision-making
- Create confusion about which tool to use
- Reduce tool discoverability

**Strategy to stay under 30**:
1. **Consolidate**: Combine related tools with `action=` parameter
2. **Resources over tools**: Use resources for read-only data retrieval
3. **Dynamic loading**: Use focus modes to show only relevant tools
4. **Ruthless pruning**: Remove rarely-used or redundant tools

**Current Count**: ~30 tools (after consolidation of assignee tools: 6→1)

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Tool Count | ≤30 | ~30 ✅ |
| Test Coverage | 80% | TBD |
| Doc Health Score | 90+ | TBD |
| MCP Compliance | Full | Partial |

---

## Infrastructure Keywords

Tasks matching these keywords are considered infrastructure/support work (not misaligned):

- research, analysis, review, investigation
- config, configuration, setup, infrastructure  
- testing, test, unittest, pytest
- documentation, docs, readme
- build, package, release, version
- refactor, cleanup, optimization
- migration, upgrade, deprecation

---

## File Format

This file is parsed by the Todo2 alignment analyzer. Structure:

```markdown
### Phase N: Name
**Keywords**: comma, separated, keywords
```

Keywords are case-insensitive and matched against task content, description, and tags.

