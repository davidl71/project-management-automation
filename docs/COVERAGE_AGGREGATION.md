# Coverage Aggregation System

> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Python, testing, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Python patterns? use context7"
> - "Show me testing examples use context7"
> - "Python testing best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

This project supports aggregating coverage from individual test runs, allowing you to build up comprehensive coverage reports incrementally without running all tests at once.

## Quick Start

### Run Tests with Coverage

Run specific test files and save coverage data with a unique suffix:

```bash
# Run Ollama integration tests
./scripts/run_test_coverage.sh tests/test_ollama_integration.py ollama_integration

# Run Ollama enhanced tools tests
./scripts/run_test_coverage.sh tests/test_ollama_enhanced_tools.py ollama_enhanced

# Run any test file
./scripts/run_test_coverage.sh tests/test_some_feature.py some_feature
```

Each command saves coverage data to `.coverage.<suffix>`.

### Combine Coverage Reports

After running individual test suites, combine all coverage data:

```bash
./scripts/combine_coverage.sh
```

This will:
1. Find all `.coverage.*` files
2. Combine them into a single `.coverage` file
3. Generate HTML and terminal reports
4. Save reports to `coverage-report/combined/`

## Usage Examples

### Example 1: Adding New Tests

When you add new tests for a feature:

```bash
# 1. Run your new tests with a descriptive suffix
./scripts/run_test_coverage.sh tests/test_new_feature.py new_feature

# 2. Combine with existing coverage
./scripts/combine_coverage.sh

# 3. View the combined report
open coverage-report/combined/index.html
```

### Example 2: Incremental Coverage Building

Build coverage incrementally as you add tests:

```bash
# Day 1: Test feature A
./scripts/run_test_coverage.sh tests/test_feature_a.py feature_a

# Day 2: Test feature B
./scripts/run_test_coverage.sh tests/test_feature_b.py feature_b

# Day 3: Combine all coverage
./scripts/combine_coverage.sh
```

### Example 3: View Individual Coverage

View coverage for a specific test suite:

```bash
# Generate coverage for specific tests
./scripts/run_test_coverage.sh tests/test_ollama_integration.py ollama

# View that specific coverage
uv run coverage report --data-file=.coverage.ollama --include='project_management_automation/**/*.py' -m
```

## How It Works

1. **Individual Coverage Files**: Each test run saves to `.coverage.<suffix>`
2. **Combination**: `coverage combine` merges multiple coverage data files
3. **Reporting**: Combined data generates comprehensive reports

## Coverage Configuration

Coverage settings are configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["project_management_automation"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
]
```

## Benefits

✅ **Fast**: Run only the tests you need, when you need them  
✅ **Incremental**: Build coverage gradually as you add tests  
✅ **Isolated**: Each test suite's coverage is preserved  
✅ **Comprehensive**: Combine all coverage for full project view  
✅ **Flexible**: Mix unit tests, integration tests, and specific feature tests  

## Files

- `scripts/run_test_coverage.sh` - Run tests with coverage and save to `.coverage.<suffix>`
- `scripts/combine_coverage.sh` - Combine all `.coverage.*` files into a single report
- `pyproject.toml` - Coverage configuration
- `.coverage.*` - Individual coverage data files (gitignored)
- `.coverage` - Combined coverage data file (gitignored)
- `coverage-report/` - Generated HTML reports (gitignored)

## Tips

1. **Use descriptive suffixes**: `ollama_integration`, `api_tests`, `unit_tests`
2. **Combine regularly**: Run `combine_coverage.sh` after adding significant tests
3. **Check individual reports**: Use `--data-file=.coverage.<suffix>` to view specific coverage
4. **Keep files organized**: Coverage files are gitignored, so they won't clutter commits

## Troubleshooting

### No coverage files found

Make sure you've run tests with coverage first:
```bash
./scripts/run_test_coverage.sh tests/test_your_file.py your_suffix
```

### Coverage reports are outdated

Re-run `combine_coverage.sh` after adding new coverage files:
```bash
./scripts/combine_coverage.sh
```

### Want to start fresh

Delete all coverage files and regenerate:
```bash
rm .coverage*
./scripts/run_test_coverage.sh tests/test_file.py suffix
./scripts/combine_coverage.sh
```

