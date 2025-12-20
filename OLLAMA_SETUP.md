# Ollama Integration Setup Guide

This guide will help you set up and use the Ollama integration in this project.

## Prerequisites

1. **Install Ollama** (if not already installed):
   ```bash
   # macOS (Homebrew)
   brew install ollama
   
   # Or download from: https://ollama.ai/download
   ```

2. **Start Ollama Server**:
   ```bash
   # If installed via Homebrew/CLI
   ollama serve
   
   # If installed as macOS app
   open -a Ollama
   ```

## Quick Setup

Run the automated setup script:

```bash
./setup_ollama.sh
```

This script will:
- ✅ Check if Ollama is installed
- ✅ Start the Ollama server if needed
- ✅ Install Python dependencies (`uv sync`)
- ✅ Test the integration

## Manual Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Verify Ollama Server

```bash
ollama list
```

If you see a list of models (or an empty list), the server is running.

### 3. Pull a Model (Optional)

```bash
# Popular models:
ollama pull llama3.2        # General purpose (2.7B)
ollama pull mistral         # Fast, efficient (7B)
ollama pull codellama       # Code-specific (7B)
ollama pull phi3            # Lightweight (3.8B)
```

## Using the Integration

### Via MCP Server

Once the MCP server is running, you can use these tools:

- **Check Ollama Status**: "Check Ollama status"
- **List Models**: "List my Ollama models"
- **Generate Text**: "Generate text with Ollama using llama3.2"
- **Pull Model**: "Pull the llama3.2 model from Ollama"

### Via Python Script

```bash
# Check status
uv run python check_ollama.py

# Or use the tools directly
uv run python -c "
from project_management_automation.tools.ollama_integration import check_ollama_status
print(check_ollama_status())
"
```

## Available Tools

### `check_ollama_status`
Check if Ollama server is running and accessible.

### `list_ollama_models`
List all available models on your local Ollama server.

### `generate_with_ollama`
Generate text using a local Ollama model.

**Parameters:**
- `prompt`: Text prompt to send to the model
- `model`: Model name (default: "llama3.2")
- `host`: Optional Ollama host URL (default: http://localhost:11434)
- `stream`: Whether to stream the response (default: False)
- `options`: Optional JSON string with model parameters

### `pull_ollama_model`
Download/pull an Ollama model from the registry.

## Troubleshooting

### "Ollama server not responding"

1. Check if Ollama is running:
   ```bash
   ollama list
   ```

2. Start Ollama:
   ```bash
   ollama serve
   # Or
   open -a Ollama
   ```

### "ModuleNotFoundError: No module named 'ollama'"

Run:
```bash
uv sync
```

### "Model not found"

Pull the model first:
```bash
ollama pull <model-name>
```

## Model Recommendations

The model recommender now includes Ollama models:

- **Ollama Llama 3.2**: General local development, privacy-sensitive tasks
- **Ollama Mistral**: Fast local inference, code generation
- **Ollama CodeLlama**: Code-specific tasks, code completion
- **Ollama Phi-3**: Lightweight, resource-efficient

Use the `recommend_model` tool to get suggestions based on your task.

## Next Steps

1. Start Ollama server: `ollama serve` or `open -a Ollama`
2. Pull a model: `ollama pull llama3.2`
3. Test integration: `uv run python check_ollama.py`
4. Use via MCP tools in your AI assistant

