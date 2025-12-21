# Using RAM for LLM Acceleration & Optimization

While RAM doesn't directly accelerate computation like a GPU, it enables several optimizations that can improve LLM performance and allow for better quality models.

## How RAM Helps LLM Performance

### 1. **Larger Context Windows** 🎯

With more RAM, you can use larger context windows, which:
- **Improves quality** by giving the model more context
- Enables processing longer documents
- Better for multi-turn conversations
- **Trade-off**: Slightly slower inference, but much better results

### 2. **Higher Quality Models** 📈

More RAM allows you to use:
- Less quantized models (better quality)
- Larger model sizes (e.g., 13B, 70B models)
- Full precision models instead of quantized

### 3. **Memory Optimizations** ⚡

- **Flash Attention**: Reduces memory usage for large contexts
- **KV Cache**: Can use full precision instead of quantized
- **Batch Processing**: Process multiple requests if RAM allows

## RAM-Based Automatic Optimizations

The Ollama integration automatically detects your RAM and optimizes settings:

### RAM Detection

```python
from project_management_automation.tools.ollama_integration import get_hardware_info
print(get_hardware_info())
```

This will show:
- Total RAM detected
- Recommended context size based on RAM
- RAM optimization recommendations

### Automatic Context Size Recommendations

| RAM | Recommended Context | Max Context | Notes |
|-----|---------------------|-------------|-------|
| **32GB+** | 8192 | 16384 | Can use very large contexts, larger models |
| **16-32GB** | 6144 | 8192 | Large contexts, good model selection |
| **8-16GB** | 4096 | 4096 | Medium contexts, standard models |
| **<8GB** | 2048 | 2048 | Smaller contexts, use quantized models |

## Using RAM Optimizations

### Automatic (Recommended)

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Automatically uses RAM-optimized settings
result = generate_with_ollama(
    prompt="Your prompt",
    model="llama3.2",
    use_ram_optimizations=True,  # Default: True
    # Context size automatically set based on RAM
    # Flash Attention enabled if RAM >= 8GB
)
```

### Manual Override

If you have a lot of RAM and want larger contexts:

```python
result = generate_with_ollama(
    prompt="Your prompt",
    model="llama3.2",
    context_size=8192,  # Override to use larger context
    use_flash_attention=True,  # Enable Flash Attention for memory efficiency
)
```

## Flash Attention

Flash Attention reduces memory usage and can speed up inference for large contexts:

```python
# Automatically enabled if RAM >= 8GB
# Or enable manually:
result = generate_with_ollama(
    prompt="Your prompt",
    model="llama3.2",
    use_flash_attention=True,
)
```

Or via environment variable:
```bash
export OLLAMA_FLASH_ATTENTION=1
ollama serve
```

**Benefits**:
- 10-30% faster for large contexts
- Lower memory usage
- Enables larger context windows

## KV Cache Optimization

For systems with limited RAM (<16GB), quantized KV cache can help:

```python
# Automatically enabled for systems with <16GB RAM
# Uses q8_0 quantization to reduce memory usage
```

Or manually:
```bash
export OLLAMA_KV_CACHE_TYPE=q8_0  # 8-bit quantization
ollama serve
```

## Model Selection Based on RAM

### Recommended Models by RAM

#### 32GB+ RAM
- **Full precision models**: `llama3.1:8b`, `mistral:7b`
- **Large contexts**: Up to 16K tokens
- **Multiple models**: Can keep multiple models loaded

#### 16-32GB RAM
- **Standard models**: `llama3.2`, `codellama:7b`
- **Large contexts**: Up to 8K tokens
- **Good balance**: Quality and performance

#### 8-16GB RAM
- **Quantized models**: `llama3.2:1b`, `phi3`
- **Medium contexts**: Up to 4K tokens
- **Efficient**: Optimized for memory usage

#### <8GB RAM
- **Small models**: `llama3.2:1b`, quantized variants
- **Small contexts**: Up to 2K tokens
- **Lightweight**: Minimal memory footprint

## Example: Using Large RAM for Better Quality

If you have 32GB+ RAM, you can use larger contexts for better quality:

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# With 32GB+ RAM, automatically uses 8K context
result = generate_with_ollama(
    prompt="Analyze this long document...",  # Can be much longer
    model="llama3.1:8b",  # Higher quality model
    # Automatically optimized for your RAM
)
```

## Performance Impact

### Context Size vs Speed

- **2K context**: Fastest, but limited context
- **4K context**: Good balance
- **8K context**: Slower, but much better quality (if RAM allows)
- **16K context**: Best quality, requires 32GB+ RAM

### RAM Requirements by Context Size

| Context Size | Minimum RAM | Recommended RAM |
|--------------|-------------|-----------------|
| 2K | 4GB | 8GB |
| 4K | 8GB | 16GB |
| 8K | 16GB | 32GB |
| 16K | 32GB | 64GB+ |

## Checking Your RAM

Check detected RAM:

```python
from project_management_automation.tools.ollama_integration import get_hardware_info
import json

info = json.loads(get_hardware_info())
if info.get("success"):
    data = info["data"]
    print(f"Total RAM: {data.get('ram_gb')} GB")
    print(f"Recommended context: {data.get('recommended_settings', {}).get('context_size')}")
    print(f"RAM optimizations: {data.get('ram_optimizations', {})}")
```

## Best Practices

1. **Let the system auto-detect** - RAM optimizations are automatic
2. **Use appropriate models** - Match model size to available RAM
3. **Enable Flash Attention** - Reduces memory usage (auto-enabled if RAM >= 8GB)
4. **Monitor memory usage** - Use Activity Monitor (macOS) or htop (Linux)
5. **Adjust context size** - Increase if you have more RAM, decrease if running low

## Summary

✅ **RAM enables**:
- Larger context windows (better quality)
- Higher quality models
- Flash Attention (memory efficiency)
- Better multitasking

⚠️ **RAM doesn't directly accelerate**:
- Computation speed (CPU/GPU still do the work)
- But it enables optimizations that improve quality

💡 **Best approach**: Let the system auto-detect and optimize based on your RAM!
