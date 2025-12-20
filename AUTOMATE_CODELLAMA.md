# Automated CodeLlama Setup

I've created automated scripts to pull CodeLlama for Exarp PMA.

## Quick Start

Run the automated script (uses `uv` - project standard):

```bash
# Recommended: Uses uv (project standard)
./pull_codellama_uv.sh

# Python version (also uses uv if available)
python3 pull_codellama.py

# Original bash version
./pull_codellama.sh
```

## What the Scripts Do

1. ✅ Check if Ollama CLI is installed
2. ✅ Check if Ollama server is running
3. ✅ Start Ollama server if needed
4. ✅ Check if CodeLlama is already installed
5. ✅ Pull CodeLlama if not installed (~3.8GB download)
6. ✅ Verify installation

## Manual Steps (if scripts don't work)

If the automated scripts hit permission issues, you can do it manually:

### 1. Start Ollama Server

```bash
# Option 1: Open the app (macOS)
open -a Ollama

# Option 2: Start via CLI
ollama serve
```

Wait a few seconds for it to start.

### 2. Pull CodeLlama

```bash
ollama pull codellama
```

This will download ~3.8GB and may take several minutes.

### 3. Verify

```bash
ollama list
```

You should see `codellama` in the list.

## Usage

Once CodeLlama is installed, you can use it with Exarp PMA:

- Via MCP tools: "Generate text with Ollama using codellama"
- Via Python: Use the `generate_with_ollama` function
- The model recommender will suggest CodeLlama for code-related tasks

## Troubleshooting

### "Ollama server not responding"

Make sure the server is running:
```bash
ollama list
```

If it fails, start it:
```bash
ollama serve
# Or
open -a Ollama
```

### "Permission denied" errors

The Python script (`pull_codellama.py`) handles permissions better. Try that instead.

### Network issues

Make sure you have internet access. The download is ~3.8GB.

## Next Steps

After CodeLlama is installed:

1. Install dependencies (if not already): `uv sync`
2. Test the integration: `uv run python check_ollama.py`
3. Use via MCP tools in your AI assistant
4. The model recommender will automatically suggest CodeLlama for code tasks

## Using uv (Project Standard)

This project uses `uv` for all Python package management. The scripts automatically detect and use `uv` when available:

- ✅ `pull_codellama_uv.sh` - Uses `uv run python` for Python commands
- ✅ `pull_codellama.py` - Detects and uses `uv` automatically
- ✅ All Python commands use `uv run` when `uv` is available

