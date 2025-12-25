#!/bin/bash
# Combine multiple coverage data files into a single report
# Usage: ./scripts/combine_coverage.sh [output_dir]
# Example: ./scripts/combine_coverage.sh coverage-report/combined

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

OUTPUT_DIR="${1:-coverage-report}"
mkdir -p "${OUTPUT_DIR}"

echo "🔍 Looking for coverage data files..."

# Find all coverage data files with suffixes (exclude main .coverage if it exists)
COVERAGE_FILES=$(find . -maxdepth 1 -name ".coverage.*" -type f 2>/dev/null | sort)

if [ -z "$COVERAGE_FILES" ]; then
    echo "❌ No coverage data files found (.coverage.*)"
    echo ""
    echo "Generate coverage first:"
    echo "  ./scripts/run_test_coverage.sh tests/test_ollama_integration.py ollama_integration"
    exit 1
fi

echo "Found coverage files:"
for file in $COVERAGE_FILES; do
    echo "  - $file"
done

echo ""
echo "📊 Combining coverage data..."

# Use a temporary combined file to avoid overwriting existing .coverage
TEMP_COMBINED=".coverage.combined.tmp"

# Combine all coverage files
if command -v uv &> /dev/null; then
    uv run coverage combine --data-file="${TEMP_COMBINED}" $COVERAGE_FILES
else
    coverage combine --data-file="${TEMP_COMBINED}" $COVERAGE_FILES
fi

echo ""
echo "📈 Generating coverage report..."

# Generate reports using the combined file
if command -v uv &> /dev/null; then
    uv run coverage report --data-file="${TEMP_COMBINED}" --include='project_management_automation/**/*.py' -m || true
    uv run coverage html --data-file="${TEMP_COMBINED}" --include='project_management_automation/**/*.py' -d "${OUTPUT_DIR}" || true
else
    coverage report --data-file="${TEMP_COMBINED}" --include='project_management_automation/**/*.py' -m || true
    coverage html --data-file="${TEMP_COMBINED}" --include='project_management_automation/**/*.py' -d "${OUTPUT_DIR}" || true
fi

# Move combined file to .coverage
mv "${TEMP_COMBINED}" .coverage

echo ""
echo "✅ Coverage report generated:"
echo "  - HTML: ${OUTPUT_DIR}/index.html"
echo "  - Combined data: .coverage"
