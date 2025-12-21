# Ollama GPU Acceleration on macOS

## Summary

**GPU acceleration availability on macOS:**
- ✅ **Apple Silicon (M1/M2/M3/M4)**: Metal GPU acceleration - **FULLY SUPPORTED**
- ❌ **Intel Mac with Radeon GPU**: No GPU acceleration - **CPU-only inference**
- ❌ **ROCm (AMD GPU compute)**: **NOT AVAILABLE on macOS**

## Apple Silicon (M1/M2/M3/M4) - Metal GPU ✅

Apple Silicon Macs have full GPU acceleration via Metal:

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Automatically uses Metal GPU acceleration
result = generate_with_ollama(
    prompt="Your prompt",
    model="llama3.2",
    # GPU layers automatically set to 30-40 based on chip model
)
```

**Performance**: 5-20x faster than CPU-only inference

## Intel Mac with Radeon GPU - CPU Only ❌

Unfortunately, Intel-based Macs with AMD Radeon GPUs **cannot use GPU acceleration** with Ollama:

- ❌ ROCm is not available on macOS
- ❌ Metal does not work with discrete Radeon GPUs (only integrated GPUs on Apple Silicon)
- ✅ CPU-only inference is available (optimized automatically)

### Optimizing for CPU-Only (Intel Mac)

Since GPU acceleration isn't available, focus on CPU optimizations:

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# Optimized for CPU-only inference
result = generate_with_ollama(
    prompt="Your prompt",
    model="phi3",              # Use smaller, faster models
    context_size=2048,         # Smaller context = faster
    num_threads=7,             # Leave 1 core free (adjust based on your CPU)
    stream=True,               # Enable streaming for better UX
)
```

### Best Practices for Intel Macs

1. **Use Smaller Models**: 
   ```bash
   ollama pull phi3          # 2.3GB - Very fast
   ollama pull llama3.2:1b   # ~700MB - Fastest
   ```

2. **Reduce Context Size**: Smaller context windows process much faster

3. **Optimize CPU Threads**: Match your CPU core count (auto-detected)

4. **Enable Streaming**: Makes responses feel faster

5. **Consider Quantized Models**: Models with `q4_0`, `q5_0` suffixes are faster

## Why ROCm Isn't Available on macOS

ROCm (Radeon Open Compute) is AMD's GPU compute platform, but:
- AMD has never released ROCm for macOS
- ROCm is designed for Linux and Windows only
- macOS uses Metal for GPU compute, but Metal doesn't support Radeon GPUs in compute contexts

## Alternatives for Intel Mac Users

If you need faster inference, consider:

1. **Use Smaller Models**: `phi3`, `llama3.2:1b` are much faster
2. **Cloud GPU Services**: Use cloud-based LLM APIs for faster inference
3. **Linux/Windows**: Install Linux or Windows (Boot Camp/virtualization) to use ROCm
4. **Apple Silicon Mac**: Upgrade to Apple Silicon for Metal GPU acceleration

## Performance Comparison

| Platform | GPU Type | Speedup vs CPU |
|----------|----------|----------------|
| Apple Silicon (M1/M2/M3/M4) | Metal | 5-20x faster |
| Intel Mac with Radeon | CPU-only | 1x (baseline) |
| Linux with AMD GPU | ROCm | 5-20x faster |
| Windows with AMD GPU | ROCm | 5-20x faster |

## Checking Your Hardware

Check what GPU acceleration is available:

```python
from project_management_automation.tools.ollama_integration import get_hardware_info
print(get_hardware_info())
```

This will show:
- Platform type (Apple Silicon vs Intel)
- GPU availability
- Recommended settings

## Resources

- [Ollama GPU Documentation](https://docs.ollama.com/gpu)
- [ROCm Platform Support](https://rocm.docs.amd.com/) - Linux/Windows only
- [Apple Metal Documentation](https://developer.apple.com/metal/)
