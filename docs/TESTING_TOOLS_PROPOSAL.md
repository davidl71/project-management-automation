# Testing Tools Proposal for Exarp


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me Python examples examples use context7"
> - "Python best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-25  
**Status**: 📋 Proposal  
**Priority**: High

---

## Overview

Exarp currently has **indirect** testing support but lacks dedicated tools for:
- Running tests
- Analyzing coverage
- Suggesting test cases
- Validating test structure

This proposal outlines 4 new testing tools to add to Exarp.

---

## Current State

### ✅ What Exarp Can Do (Indirectly)

1. **`find_automation_opportunities`** - Can discover testing gaps
   - Finds untested code patterns
   - Identifies repetitive testing tasks
   - Suggests automation for test execution

2. **`validate_ci_cd_workflow`** - Validates CI/CD (which includes tests)
   - Checks if tests run in CI/CD
   - Validates test job configurations

3. **Documentation Tracking** - Tracks test status
   - `docs/UNIT_TEST_STATUS.md` documents coverage
   - Test files are tracked

### ❌ What Exarp Cannot Do (Currently)

1. **Run Tests** - No tool to execute pytest/unittest/ctest
2. **Coverage Analysis** - No tool to generate coverage reports
3. **Test Suggestions** - No tool to suggest test cases
4. **Test Validation** - No tool to validate test structure

---

## Proposed Tools

### 1. `run_tests` Tool

**Purpose**: Execute test suites with flexible options

**Parameters**:
- `test_path`: Path to test file/directory (default: `tests/`)
- `test_framework`: `pytest`, `unittest`, `ctest`, `auto` (default: `auto`)
- `verbose`: Show detailed output (default: `true`)
- `coverage`: Generate coverage report (default: `false`)
- `output_path`: Path for test results (default: `test-results/`)

**Features**:
- Auto-detect test framework (pytest, unittest, ctest)
- Run specific tests or entire suite
- Generate JUnit XML reports
- Return pass/fail counts

**Example Usage**:
```python
# Run all tests
run_tests()

# Run specific test file with coverage
run_tests(test_path="tests/test_tools.py", coverage=True)

# Run C++ tests (ctest)
run_tests(test_path="build/", test_framework="ctest")
```

---

### 2. `analyze_test_coverage` Tool

**Purpose**: Generate coverage reports and identify gaps

**Parameters**:
- `coverage_file`: Path to coverage file (default: auto-detect)
- `min_coverage`: Minimum coverage threshold (default: `80`)
- `output_path`: Path for coverage report (default: `coverage-report/`)
- `format`: Report format: `html`, `json`, `terminal` (default: `html`)

**Features**:
- Parse coverage data (coverage.py, gcov, lcov)
- Identify untested files/functions
- Generate HTML reports
- Compare against thresholds
- Suggest files needing tests

**Example Usage**:
```python
# Analyze coverage
analyze_test_coverage(min_coverage=80)

# Generate HTML report
analyze_test_coverage(format="html", output_path="docs/coverage/")
```

---

### 3. `suggest_test_cases` Tool

**Purpose**: Suggest test cases based on code analysis

**Parameters**:
- `target_file`: File to analyze (optional)
- `test_framework`: Framework for suggestions (default: `pytest`)
- `output_path`: Path for suggestions (default: `test-suggestions/`)
- `min_confidence`: Minimum confidence threshold (default: `0.7`)

**Features**:
- Analyze function signatures
- Identify edge cases
- Suggest parameter combinations
- Generate test templates
- Use AI/LLM for intelligent suggestions

**Example Usage**:
```python
# Suggest tests for a file
suggest_test_cases(target_file="tools/docs_health.py")

# Generate high-confidence suggestions
suggest_test_cases(min_confidence=0.8)
```

---

### 4. `validate_test_structure` Tool

**Purpose**: Validate test organization and patterns

**Parameters**:
- `test_path`: Path to test directory (default: `tests/`)
- `framework`: Expected framework (default: `auto`)
- `output_path`: Path for validation report (default: `test-validation-report.md`)

**Features**:
- Check test naming conventions
- Validate test organization
- Check for missing test files
- Validate test patterns
- Check test coverage of critical paths

**Example Usage**:
```python
# Validate test structure
validate_test_structure()

# Validate specific framework
validate_test_structure(framework="pytest")
```

---

## Implementation Plan

### Phase 1: Core Test Runner (Week 1)
- ✅ Create `run_tests` tool
- ✅ Support pytest and unittest
- ✅ Basic test execution
- ✅ Pass/fail reporting

### Phase 2: Coverage Analysis (Week 2)
- ✅ Create `analyze_test_coverage` tool
- ✅ Parse coverage.py output
- ✅ Generate HTML reports
- ✅ Identify gaps

### Phase 3: Test Suggestions (Week 3)
- ✅ Create `suggest_test_cases` tool
- ✅ Code analysis for test cases
- ✅ Template generation
- ✅ Integration with Context7 for patterns

### Phase 4: Test Validation (Week 4)
- ✅ Create `validate_test_structure` tool
- ✅ Pattern validation
- ✅ Organization checks
- ✅ Coverage validation

---

## Integration with Existing Tools

### With `find_automation_opportunities`
- Can discover testing automation needs
- Identifies repetitive testing tasks
- Suggests test automation opportunities

### With `validate_ci_cd_workflow`
- Validates test execution in CI/CD
- Checks test job configurations
- Ensures tests run in pipelines

### With `check_documentation_health`
- Validates test documentation
- Checks test README files
- Ensures test coverage docs are up-to-date

---

## Benefits

1. **Automated Test Execution** - Run tests without manual commands
2. **Coverage Tracking** - Monitor and improve test coverage
3. **Test Generation** - AI-assisted test case suggestions
4. **Quality Assurance** - Validate test structure and patterns
5. **CI/CD Integration** - Automated testing in workflows

---

## Example Workflow

```python
# 1. Run tests
run_tests(coverage=True)

# 2. Analyze coverage
analyze_test_coverage(min_coverage=80)

# 3. Get suggestions for low-coverage files
suggest_test_cases(target_file="tools/docs_health.py")

# 4. Validate test structure
validate_test_structure()
```

---

## Next Steps

1. **Create Todo2 tasks** for each tool
2. **Implement Phase 1** (test runner)
3. **Test with existing test suite**
4. **Iterate based on feedback**

---

**Status**: Ready for implementation  
**Priority**: High (complements existing automation tools)

