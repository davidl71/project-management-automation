# AMD GPU Support with Ollama (ROCm)

Ollama supports AMD GPUs through the ROCm (Radeon Open Compute) library, enabling hardware acceleration on **Linux and Windows platforms only**.

**⚠️ Important: ROCm does NOT support macOS**, including Intel-based Macs with Radeon GPUs. On macOS, GPU acceleration is only available via Metal on Apple Silicon (M1/M2/M3/M4) chips.

## Supported AMD GPUs

Ollama supports a wide range of AMD GPUs via ROCm. See the [official Ollama GPU documentation](https://docs.ollama.com/gpu) for the complete list, including:

- **AMD Radeon RX**: 7900 XTX, 7900 XT, 7800 XT, 7700 XT, 7600, 6950 XT, 6900 XTX, 6800 XT, Vega 64, Vega 56
- **AMD Radeon PRO**: W7900, W7800, W7700, W7600, W6900X, W6800X, Vega II Duo
- **AMD Instinct**: MI300X, MI300A, MI300, MI250X, MI250, MI210, MI200, MI100

**Note**: Windows support requires ROCm v6.1 or later.

## Automatic Detection

The Ollama integration automatically detects AMD GPUs using `rocminfo`:

```python
from project_management_automation.tools.ollama_integration import get_hardware_info
print(get_hardware_info())
```

This will show:
- GPU type: "rocm"
- Recommended GPU layers: 40
- Context size: 8192

## Installation

### ⚠️ macOS Limitation

**ROCm is NOT available on macOS**, including Intel-based Macs with Radeon GPUs. On macOS:
- **Apple Silicon (M1/M2/M3/M4)**: Use Metal GPU acceleration (automatic)
- **Intel Mac with Radeon GPU**: CPU-only inference (no GPU acceleration available)

If you need GPU acceleration on a Mac with Radeon GPU, you would need to:
1. Use Linux (via Boot Camp, virtualization, or dual boot)
2. Use Windows (via Boot Camp or virtualization)
3. Consider using smaller models optimized for CPU inference

### Linux

1. Install ROCm following the [official ROCm installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/)

2. Verify installation:
   ```bash
   rocminfo
   ```

3. Ollama will automatically detect and use the AMD GPU

### Windows

1. Install ROCm v6.1 or later from the [ROCm releases](https://github.com/ROCm/ROCm/releases)

2. Verify installation:
   ```powershell
   rocminfo
   ```

3. Ollama will automatically detect and use the AMD GPU

## Using AMD GPU with Ollama

Once ROCm is installed and detected, Ollama will automatically use the AMD GPU:

```python
from project_management_automation.tools.ollama_integration import generate_with_ollama

# AMD GPU is automatically detected and used
result = generate_with_ollama(
    prompt="Your prompt here",
    model="llama3.2",
    # num_gpu is auto-set to 40 for AMD GPUs
)
```

## GPU Selection

If you have multiple AMD GPUs, you can specify which ones to use:

```bash
# List available GPUs
rocminfo

# Limit Ollama to specific GPU(s)
export ROCR_VISIBLE_DEVICES=0,1  # Use GPU 0 and 1
ollama serve

# Force CPU usage (if needed)
export ROCR_VISIBLE_DEVICES=-1
ollama serve
```

## Troubleshooting

### GPU Not Detected

1. **Check ROCm installation**:
   ```bash
   rocminfo
   ```

2. **Check Ollama logs**:
   ```bash
   tail -f ~/.ollama/logs/server.log
   ```
   Look for entries indicating ROCm/Metal device usage.

3. **Verify GPU is supported**: Check the [Ollama GPU documentation](https://docs.ollama.com/gpu) for supported AMD GPU models.

### Unsupported GPU

For AMD GPUs not officially supported by ROCm, you can attempt to force compatibility:

```bash
# Set HSA_OVERRIDE_GFX_VERSION to a similar supported LLVM target
# Example: Using RX 5400 (gfx1034) as gfx1030
export HSA_OVERRIDE_GFX_VERSION=10.3.0
ollama serve
```

**Warning**: This may enable functionality on unsupported GPUs, but success can vary.

### SELinux Issues (Linux)

On certain Linux distributions, SELinux may prevent containers from accessing AMD GPU devices:

```bash
sudo setsebool container_use_devices=1
```

## Performance

AMD GPUs with ROCm provide significant performance improvements over CPU-only inference:

- **Speed**: 5-20x faster than CPU-only
- **Recommended GPU layers**: 40 (auto-detected)
- **Context size**: 8192 (auto-optimized)

## Resources

- [ROCm Documentation](https://rocm.docs.amd.com/)
- [Ollama GPU Documentation](https://docs.ollama.com/gpu)
- [ROCm GitHub Repository](https://github.com/ROCm/ROCm)
- [ROCm Installation Guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/)
