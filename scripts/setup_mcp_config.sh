#!/bin/bash
# Setup MCP configuration from template
# Generates .cursor/mcp.json with correct absolute paths for this machine

set -e

# Detect project root dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

TEMPLATE_FILE="$PROJECT_ROOT/.cursor/mcp.json.template"
OUTPUT_FILE="$PROJECT_ROOT/.cursor/mcp.json"

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ Error: Template file not found: $TEMPLATE_FILE"
    exit 1
fi

# Convert PROJECT_ROOT to absolute path (normalize)
PROJECT_ROOT_ABS="$(cd "$PROJECT_ROOT" && pwd)"

echo "🔧 Setting up MCP configuration..."
echo "   Project root: $PROJECT_ROOT_ABS"
echo "   Output file: $OUTPUT_FILE"
echo ""

# Replace {{PROJECT_ROOT}} placeholder with actual absolute path
sed "s|{{PROJECT_ROOT}}|$PROJECT_ROOT_ABS|g" "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "✅ MCP configuration generated successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Review the generated file: $OUTPUT_FILE"
echo "   2. Restart Cursor completely for changes to take effect"
echo "   3. Verify MCP servers are working in Cursor"
echo ""
