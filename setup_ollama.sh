#!/bin/bash
# Setup script for Ollama integration

set -e

echo "🔍 Checking Ollama installation..."

# Check if Ollama CLI is available
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama CLI not found. Please install Ollama first:"
    echo "   Visit: https://ollama.ai/download"
    echo "   Or install via Homebrew: brew install ollama"
    exit 1
fi

echo "✅ Ollama CLI found: $(which ollama)"

# Check if Ollama server is running
if ollama list &> /dev/null; then
    echo "✅ Ollama server is running"
    echo ""
    echo "📦 Installed models:"
    ollama list
else
    echo "⚠️  Ollama server is not running"
    echo ""
    echo "Starting Ollama server..."
    
    # Try to start Ollama (method depends on installation)
    if [ -d "/Applications/Ollama.app" ]; then
        echo "Opening Ollama app..."
        open -a Ollama
        echo "⏳ Waiting for server to start (10 seconds)..."
        sleep 10
    else
        echo "Starting Ollama server in background..."
        ollama serve &
        echo "⏳ Waiting for server to start (5 seconds)..."
        sleep 5
    fi
    
    # Check again
    if ollama list &> /dev/null; then
        echo "✅ Ollama server started successfully"
        echo ""
        echo "📦 Installed models:"
        ollama list
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
echo "📥 Installing Python dependencies..."
cd "$(dirname "$0")"
uv sync

echo ""
echo "🧪 Testing Ollama integration..."
if uv run python check_ollama.py; then
    echo ""
    echo "✅ Ollama integration is ready!"
    echo ""
    echo "💡 Quick start:"
    echo "   - Check status: uv run python check_ollama.py"
    echo "   - List models: ollama list"
    echo "   - Pull a model: ollama pull llama3.2"
else
    echo ""
    echo "⚠️  Integration test failed, but Ollama server is running"
    echo "   You can still use Ollama via the CLI"
fi

