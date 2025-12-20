#!/bin/bash
# Automated script to pull CodeLlama for Exarp PMA
# Uses uv for package management (project standard)

set -e

echo "🚀 Automated CodeLlama Setup for Exarp PMA (using uv)"
echo "======================================================"
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found, will use system Python"
    PYTHON_CMD="python3"
else
    echo "✅ Using uv for Python execution (project standard)"
    PYTHON_CMD="uv run python"
fi
echo ""

# Check if Ollama CLI is available
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama CLI not found!"
    echo ""
    echo "Please install Ollama first:"
    echo "  macOS: brew install ollama"
    echo "  Or visit: https://ollama.ai/download"
    exit 1
fi

echo "✅ Ollama CLI found: $(which ollama)"
echo ""

# Function to check if Ollama server is running
check_ollama_server() {
    if ollama list &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Check if server is running
if check_ollama_server; then
    echo "✅ Ollama server is already running"
else
    echo "⚠️  Ollama server is not running"
    echo "🔄 Starting Ollama server..."
    
    # Try different methods to start Ollama
    if [ -d "/Applications/Ollama.app" ]; then
        echo "   Opening Ollama app..."
        open -a Ollama
        echo "   ⏳ Waiting for server to start (10 seconds)..."
        sleep 10
    else
        echo "   Starting Ollama server in background..."
        ollama serve > /dev/null 2>&1 &
        OLLAMA_PID=$!
        echo "   ⏳ Waiting for server to start (5 seconds)..."
        sleep 5
    fi
    
    # Check again
    if check_ollama_server; then
        echo "✅ Ollama server started successfully"
    else
        echo "❌ Failed to start Ollama server"
        echo ""
        echo "Please start Ollama manually:"
        echo "  1. Open the Ollama app from Applications"
        echo "  2. Or run: ollama serve"
        exit 1
    fi
fi

echo ""
echo "📦 Checking if CodeLlama is already installed..."

# Check if codellama is already installed
if ollama list | grep -q "codellama"; then
    echo "✅ CodeLlama is already installed!"
    echo ""
    echo "📋 Installed models:"
    ollama list
    echo ""
    echo "🧪 Testing Ollama integration with uv..."
    if $PYTHON_CMD check_ollama.py 2>/dev/null; then
        echo "✅ Ollama integration test passed!"
    else
        echo "⚠️  Integration test skipped (dependencies may need: uv sync)"
    fi
    echo ""
    echo "🎉 Ready to use! You can now use CodeLlama with Exarp PMA."
    exit 0
fi

echo "📥 CodeLlama not found. Pulling CodeLlama..."
echo ""
echo "⏳ This will download ~3.8GB and may take several minutes..."
echo "   (Download speed depends on your internet connection)"
echo ""

# Pull CodeLlama
if ollama pull codellama; then
    echo ""
    echo "✅ CodeLlama pulled successfully!"
    echo ""
    echo "📋 Installed models:"
    ollama list
    echo ""
    echo "🧪 Testing Ollama integration with uv..."
    if $PYTHON_CMD check_ollama.py 2>/dev/null; then
        echo "✅ Ollama integration test passed!"
    else
        echo "⚠️  Integration test skipped (run 'uv sync' if needed)"
    fi
    echo ""
    echo "🎉 Setup complete! CodeLlama is ready to use with Exarp PMA."
    echo ""
    echo "💡 Usage examples:"
    echo "   - Generate code documentation"
    echo "   - Analyze codebases"
    echo "   - Code-related task management"
    echo ""
    echo "   Use via MCP tools: 'Generate text with Ollama using codellama'"
    echo "   Or via uv: $PYTHON_CMD -c \"from project_management_automation.tools.ollama_integration import generate_with_ollama; print(generate_with_ollama('Hello', 'codellama'))\""
else
    echo ""
    echo "❌ Failed to pull CodeLlama"
    echo ""
    echo "Possible issues:"
    echo "  - Network connection problem"
    echo "  - Insufficient disk space"
    echo "  - Ollama server issue"
    echo ""
    echo "Try manually: ollama pull codellama"
    exit 1
fi

