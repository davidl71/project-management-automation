# Ollama Performance Optimization Guide

This guide covers various strategies to speed up Ollama inference and improve response times.

## 🚀 Automatic Hardware Detection (New!)

**The Ollama integration now automatically detects your hardware and optimizes settings!**

- **Apple Silicon (M1/M2/M3/M4)**: Automatically uses Metal GPU acceleration
- **Intel Mac**: Optimized for CPU-only inference
- **Linux with NVIDIA GPU**: Detects and uses CUDA acceleration
- **Linux/Windows with AMD GPU**: Detects and uses ROCm acceleration (ROCm v6.1+ for Windows)

You can check your hardware configuration:
```python
from project_management_automation.tools.ollama_integration import get_hardware_info
print(get_hardware_info())
```

Or use the MCP tool: "Check my hardware configuration for Ollama"

Settings are automatically applied unless you explicitly override them. You can still manually set parameters if needed.

## Quick Wins (Start Here)

### 1. Use Smaller/Quantized Models

Smaller models are significantly faster. If quality allows, switch to smaller variants:

```bash
# Fast, lightweight models
ollama pull phi3              # 2.3GB - Very fast, good for simple tasks
ollama pull llama3.2:1b       # ~700MB - Fastest, basic tasks
ollama pull mistral:7b-instruct-q4_0  # Quantized, faster than full 7B

# Medium models (balanced speed/quality)
ollama pull llama3.2          # 2.7GB - Good balance
ollama pull codellama:7b      # ~3.8GB - Code-focused, reasonably fast
```

**Speed Impact**: 2-5x faster than larger models

### 2. Enable Streaming

Streaming makes responses appear faster to users:

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Streaming enables faster perceived response time
result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    stream=True  # Enable streaming
)
```

**Speed Impact**: Immediate first token, better user experience

### 3. Reduce Context Window Size

Smaller context windows process faster:

```python
# Use smaller context for faster inference
result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    context_size=2048  # Smaller = faster (default is usually 4096+)
)
```

**Speed Impact**: 20-40% faster with smaller context

---

## GPU Optimization

### Set GPU Layer Offloading

Offload model layers to GPU for significant speedup (if you have a GPU):

#### Via Environment Variable (Recommended)
```bash
# Set number of layers to run on GPU (experiment with values)
export OLLAMA_NUM_GPU=40

# Start Ollama with GPU support
ollama serve
```

#### Via Code
```python
result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    num_gpu=40  # Offload 40 layers to GPU
)
```

**Finding the Right Number:**
- Start with 35-40 for 7B models
- Use 20-25 for 3B models
- Check GPU memory: `nvidia-smi` (NVIDIA), `rocminfo` (AMD), or Activity Monitor (macOS)
- Too many layers = out of memory error
- Too few = not using GPU fully

**GPU Types Supported:**
- **NVIDIA (CUDA)**: Automatic detection via `nvidia-smi`
- **AMD (ROCm)**: Automatic detection via `rocminfo` (Linux and Windows ROCm v6.1+)
- **Apple Silicon (Metal)**: Automatic detection on macOS

**Speed Impact**: 5-20x faster with GPU (vs CPU-only)

---

## CPU Optimization

### Set CPU Thread Count

Optimize CPU parallelism:

#### Via Environment Variable
```bash
# Match your CPU core count (or slightly less)
export OLLAMA_NUM_THREADS=8  # For 8-core CPU

ollama serve
```

#### Via Code
```python
result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    num_threads=8  # Match your CPU cores
)
```

**How to Find Core Count:**
```bash
# macOS/Linux
sysctl -n hw.ncpu  # macOS
nproc  # Linux

# Or check Activity Monitor / System Monitor
```

**Speed Impact**: 20-50% faster with optimized threading

---

## Advanced Optimizations

### 1. Enable Flash Attention (if supported)

Flash Attention reduces memory usage and speeds up attention computation:

```bash
export OLLAMA_FLASH_ATTENTION=true
ollama serve
```

**Speed Impact**: 10-30% faster for long contexts

### 2. Optimize Model Parameters

Tune generation parameters for speed vs quality:

```python
import json

# Faster generation options
fast_options = {
    "temperature": 0.7,      # Lower = faster, more deterministic
    "top_p": 0.9,           # Lower = faster sampling
    "top_k": 40,            # Lower = faster sampling
    "repeat_penalty": 1.1,  # Prevent repetition
    "num_predict": 512,     # Limit output length
}

result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    options=fast_options
)
```

### 3. Context Caching

For repeated or similar prompts, use context caching (available in Ollama API):

```python
# Reuse context from previous generation
# (Implement caching strategy in your application)
```

---

## Environment Variable Setup

Create a startup script for optimal settings:

### macOS/Linux (`~/.zshrc` or `~/.bashrc`)

```bash
# Ollama Performance Settings
export OLLAMA_NUM_GPU=40           # Adjust based on GPU memory
export OLLAMA_NUM_THREADS=8        # Match your CPU cores
export OLLAMA_NUM_CTX=2048         # Smaller context for speed
export OLLAMA_FLASH_ATTENTION=true # Enable if supported
```

Then restart Ollama:
```bash
# Kill existing Ollama
killall ollama

# Start with optimized settings
ollama serve
```

---

## Model Selection Guide

| Model | Size | Speed | Best For | Recommendation |
|-------|------|-------|----------|----------------|
| `phi3` | 2.3GB | ⚡⚡⚡⚡⚡ | Simple tasks, quick responses | **Best for speed** |
| `llama3.2:1b` | ~700MB | ⚡⚡⚡⚡⚡ | Basic tasks, prototyping | **Fastest** |
| `llama3.2` | 2.7GB | ⚡⚡⚡⚡ | General purpose, balanced | **Good balance** |
| `mistral:7b-instruct-q4_0` | ~4GB | ⚡⚡⚡ | Quantized, efficient | Fast 7B option |
| `codellama:7b` | ~3.8GB | ⚡⚡⚡ | Code tasks | Code-focused |
| `llama3.1:8b` | ~4.7GB | ⚡⚡ | Better quality | Quality over speed |

---

## Performance Testing

Test different configurations to find what works best for your system:

```python
import time
from project_management_automation.tools.ollama_integration import generate_with_ollama

def benchmark_config(prompt, **kwargs):
    """Benchmark different Ollama configurations."""
    start = time.time()
    result = generate_with_ollama(prompt, **kwargs)
    duration = time.time() - start
    return duration, result

# Test different configs
configs = [
    {"model": "phi3", "context_size": 2048},
    {"model": "llama3.2", "context_size": 2048, "num_threads": 8},
    {"model": "llama3.2", "context_size": 4096},
    {"model": "llama3.2", "num_gpu": 40},  # If you have GPU
]

prompt = "Summarize the key points of this code..."

for i, config in enumerate(configs):
    duration, _ = benchmark_config(prompt, **config)
    print(f"Config {i+1}: {duration:.2f}s - {config}")
```

---

## Recommended Settings by Use Case

### Fast Response Times (Speed Priority)
```python
generate_with_ollama(
    prompt=prompt,
    model="phi3",              # Small, fast model
    context_size=1024,         # Small context
    num_threads=8,             # Optimize CPU
    stream=True,               # Enable streaming
    options={
        "num_predict": 256,    # Limit output length
        "temperature": 0.7,
    }
)
```

### Balanced Speed/Quality
```python
generate_with_ollama(
    prompt=prompt,
    model="llama3.2",          # Balanced model
    context_size=2048,         # Medium context
    num_threads=8,             # Optimize CPU
    num_gpu=35,                # If GPU available
    stream=True,
)
```

### Maximum Quality (Quality Priority)
```python
generate_with_ollama(
    prompt=prompt,
    model="llama3.1:8b",       # Higher quality model
    context_size=8192,         # Large context
    num_gpu=40,                # Full GPU offload
    options={
        "temperature": 0.8,    # More creative
        "top_p": 0.95,
    }
)
```

---

## Troubleshooting

### "Out of memory" errors
- Reduce `num_gpu` layers
- Use smaller model
- Reduce `context_size`

### Still slow after optimizations
- Check if GPU is being used: `nvidia-smi` (NVIDIA) or Activity Monitor
- Verify environment variables are set: `echo $OLLAMA_NUM_GPU`
- Try a smaller model
- Reduce context size further

### GPU not being used
- Verify GPU drivers are installed
- Check Ollama version (update if needed): `ollama --version`
- macOS: Ensure Metal is available (most Macs with Apple Silicon)

---

## Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [Model Performance Comparison](https://ollama.com/library)
- [GPU Requirements](https://ollama.com/library)

---

## Quick Reference

```bash
# Fast setup (copy-paste)
export OLLAMA_NUM_GPU=40
export OLLAMA_NUM_THREADS=$(sysctl -n hw.ncpu)  # macOS
export OLLAMA_NUM_THREADS=$(nproc)              # Linux
export OLLAMA_NUM_CTX=2048
ollama serve

# Use fast model
ollama pull phi3
ollama pull llama3.2:1b
```

```python
# Fast Python code
from project_management_automation.tools.ollama_integration import generate_with_ollama

result = generate_with_ollama(
    prompt="Your prompt",
    model="phi3",              # Fast model
    context_size=2048,         # Smaller context
    num_threads=8,             # Your CPU cores
    stream=True,               # Streaming
)
```
