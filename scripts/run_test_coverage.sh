#!/bin/bash
# Run tests with coverage and aggregate results
# Usage: ./scripts/run_test_coverage.sh [test_path] [coverage_suffix]
# Example: ./scripts/run_test_coverage.sh tests/test_ollama_integration.py ollama

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

TEST_PATH="${1:-tests/}"
COVERAGE_SUFFIX="${2:-}"

if [ -n "$COVERAGE_SUFFIX" ]; then
    COVERAGE_DATA=".coverage.${COVERAGE_SUFFIX}"
    echo "Running tests with coverage suffix: ${COVERAGE_SUFFIX}"
    echo "Coverage data will be saved to: ${COVERAGE_DATA}"
else
    COVERAGE_DATA=".coverage"
    echo "Running tests with default coverage file"
fi

# Run tests with coverage, saving to specific data file
export COVERAGE_FILE="${COVERAGE_DATA}"

if command -v uv &> /dev/null; then
    uv run coverage run -m pytest "${TEST_PATH}" -v
else
    coverage run -m pytest "${TEST_PATH}" -v
fi

echo ""
echo "✅ Coverage data saved to: ${COVERAGE_DATA}"
echo ""
echo "To view coverage report:"
if [ -n "$COVERAGE_SUFFIX" ]; then
    echo "  coverage report --data-file=${COVERAGE_DATA} --include='project_management_automation/**/*.py' -m"
else
    echo "  coverage report --include='project_management_automation/**/*.py' -m"
fi
echo ""
echo "To generate HTML report:"
if [ -n "$COVERAGE_SUFFIX" ]; then
    echo "  coverage html --data-file=${COVERAGE_DATA} --include='project_management_automation/**/*.py' -d coverage-report"
else
    echo "  coverage html --include='project_management_automation/**/*.py' -d coverage-report"
fi
echo ""
echo "To combine with other coverage files:"
echo "  ./scripts/combine_coverage.sh"
