# Ollama Speed Optimization - Quick Start

**TL;DR**: Hardware is auto-detected! Use smaller models. Settings optimized automatically.

## ✨ New: Automatic Hardware Detection

**The Ollama integration now automatically detects your hardware (Intel vs Apple Silicon/M4) and optimizes settings!**

- Apple Silicon: Auto-uses Metal GPU acceleration
- Intel Mac: Optimized for CPU-only
- Linux: Auto-detects NVIDIA GPU (CUDA) or AMD GPU (ROCm) if available
- Windows: Auto-detects AMD GPU (ROCm v6.1+) if available

Just use `generate_with_ollama()` - it's optimized automatically! Check your hardware:
```python
from project_management_automation.tools.ollama_integration import get_hardware_info
print(get_hardware_info())
```

## 🚀 5-Minute Speed Boost

### Step 1: Use a Faster Model
```bash
# Pull a fast, lightweight model
ollama pull phi3          # ~2.3GB, very fast
ollama pull llama3.2:1b   # ~700MB, fastest
```

### Step 2: (Optional) Check Hardware Auto-Detection
```bash
# Test hardware detection
uv run python test_hardware_detection.py

# Or use the MCP tool: "Check my hardware configuration for Ollama"
```

**Note**: Hardware detection is automatic! Environment variables are optional and will override auto-detection if set.

### Step 3: Use Optimized Code (Settings Auto-Applied!)
```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Fast generation - hardware settings are auto-detected!
result = generate_with_ollama(
    prompt="Your prompt here",
    model="phi3",              # Fast model
    stream=True,               # Enable streaming
    # num_gpu, num_threads, context_size are auto-detected!
    # You can override if needed: num_gpu=40, num_threads=8, etc.
)
```

## ⚡ Expected Speed Improvements

- **Smaller model**: 2-5x faster
- **GPU offloading**: 5-20x faster (if GPU available)
- **Optimized threads**: 20-50% faster
- **Smaller context**: 20-40% faster
- **Streaming**: Immediate first token

**Combined**: Up to 10-100x faster depending on hardware!

## 🎯 Quick Model Selection

- **Fastest**: `phi3`, `llama3.2:1b`
- **Balanced**: `llama3.2`, `mistral:7b-instruct-q4_0`
- **Code tasks**: `codellama:7b`

## 📚 Full Guide

See [docs/OLLAMA_PERFORMANCE_OPTIMIZATION.md](docs/OLLAMA_PERFORMANCE_OPTIMIZATION.md) for detailed optimization strategies.
