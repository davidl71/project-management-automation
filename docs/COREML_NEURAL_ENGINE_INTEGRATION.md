# Core ML Neural Engine Integration

**Date:** 2025-12-28  
**Status:** ✅ Integration Module Created  
**Purpose:** Access Apple Neural Engine (NPU) via Core ML framework

---

## Overview

Core ML is Apple's framework that **automatically uses the Neural Engine** when:
1. The model supports ANE (Apple Neural Engine) operations
2. Hardware has Neural Engine (M1/M2/M3/M4/M5+ chips)
3. Model is optimized for Neural Engine

**Key Advantage:** Unlike MLX (which requires M5+ for NPU), Core ML can use Neural Engine on M1-M4 chips when models support it.

---

## Current Status

### ✅ What's Working

- **Core ML Tools Installed:** `coremltools==9.0`
- **Hardware Detection:** M4 chip detected with Neural Engine support
- **Integration Module:** `project_management_automation/tools/coreml_integration.py` created
- **Functions Available:**
  - `check_coreml_availability()` - Check if Core ML is available
  - `get_coreml_hardware_info()` - Get hardware and Neural Engine info
  - `list_coreml_models()` - List available Core ML models
  - `predict_with_coreml()` - Run inference with Neural Engine support

### ⚠️ Limitations

- **Native Libraries:** Some `libcoremlpython` warnings (expected, doesn't block basic usage)
- **Model Requirements:** Need Core ML format models (`.mlmodel` or `.mlpackage`)
- **Model Conversion:** Existing models need conversion from PyTorch/TensorFlow

---

## How Core ML Uses Neural Engine

### Automatic Hardware Selection

Core ML automatically chooses the best compute unit:

1. **Neural Engine (ANE)** - When model supports ANE operations
2. **GPU (Metal)** - When Neural Engine not available or not optimal
3. **CPU** - Fallback option

### Compute Unit Options

```python
# Available compute unit settings:
- "all" - Use all available (prefers ANE when supported)
- "cpu_and_ane" - Prefer Neural Engine
- "cpu_and_gpu" - Use GPU instead of Neural Engine
- "cpu_only" - CPU only (slowest)
```

---

## Usage Examples

### 1. Check Neural Engine Support

```python
from project_management_automation.tools.coreml_integration import get_coreml_hardware_info
import json

result = get_coreml_hardware_info()
data = json.loads(result)['data']

print(f"Neural Engine Available: {data['neural_engine_support']}")
print(f"Compute Units: {data['compute_units_available']}")
```

### 2. Run Inference with Neural Engine

```python
from project_management_automation.tools.coreml_integration import predict_with_coreml

# Core ML will automatically use Neural Engine if model supports it
result = predict_with_coreml(
    model_path="path/to/model.mlmodel",
    input_data={"input_name": input_value},
    compute_units="all"  # Prefers Neural Engine
)
```

### 3. List Available Models

```python
from project_management_automation.tools.coreml_integration import list_coreml_models

# Search for Core ML models
result = list_coreml_models(model_dir="~/Downloads")
```

---

## Model Conversion

To use Neural Engine, you need Core ML format models:

### Convert PyTorch Model

```python
import coremltools as ct
import torch

# Load PyTorch model
torch_model = torch.load("model.pth")
torch_model.eval()

# Convert to Core ML
example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(torch_model, example_input)

coreml_model = ct.convert(
    traced_model,
    inputs=[ct.TensorType(name="input", shape=example_input.shape)],
    compute_units=ct.ComputeUnit.ALL,  # Enable Neural Engine
)

# Save
coreml_model.save("model.mlpackage")
```

### Convert TensorFlow Model

```python
import coremltools as ct
import tensorflow as tf

# Load TensorFlow model
tf_model = tf.keras.models.load_model("model.h5")

# Convert to Core ML
coreml_model = ct.convert(
    tf_model,
    compute_units=ct.ComputeUnit.ALL,  # Enable Neural Engine
)

# Save
coreml_model.save("model.mlpackage")
```

---

## Neural Engine Optimization

### Model Requirements for ANE

- **Supported Operations:** Core ML automatically identifies ANE-compatible operations
- **Quantization:** Quantized models often work better with Neural Engine
- **Model Size:** Smaller models (< 100MB) typically work better
- **Operation Types:** Convolution, matrix multiplication, activation functions

### Optimization Tips

1. **Use Quantization:**
   ```python
   coreml_model = ct.models.neural_network.quantization_utils.quantize_weights(
       coreml_model, nbits=8
   )
   ```

2. **Optimize for Neural Engine:**
   ```python
   # During conversion, specify Neural Engine preference
   coreml_model = ct.convert(
       model,
       compute_units=ct.ComputeUnit.CPU_AND_NEURAL_ENGINE,
   )
   ```

3. **Use Core ML Tools Optimization:**
   ```python
   # Optimize model for Neural Engine
   optimized_model = ct.optimize.coreml.OptimizeModel(
       coreml_model,
       target="neuralengine"
   )
   ```

---

## Performance Comparison

### Expected Performance (M4 Chip)

| Compute Unit | Use Case | Speed |
|--------------|----------|-------|
| **Neural Engine** | ANE-compatible models | Fastest (2-5x faster than CPU) |
| **GPU (Metal)** | General ML models | Fast (1.5-3x faster than CPU) |
| **CPU** | Fallback | Baseline |

### When Neural Engine is Used

- ✅ Model has ANE-compatible operations
- ✅ Model is optimized for Neural Engine
- ✅ Compute units set to "all" or "cpu_and_ane"
- ✅ Hardware has Neural Engine (M1+)

---

## Integration with Existing Tools

### Adding Core ML to Consolidated Tools

The Core ML integration can be added to `consolidated.py` as a new tool:

```python
def coreml(
    action: str = "info",
    model_path: Optional[str] = None,
    input_data: Optional[str] = None,  # JSON string
    compute_units: str = "all",
    model_dir: Optional[str] = None,
) -> str:
    """Unified Core ML tool with Neural Engine support."""
    # Implementation
```

### Use Cases

1. **Task Estimation:** Use Core ML models for faster inference
2. **Text Classification:** Pre-trained Core ML models for categorization
3. **Image Processing:** Vision models with Neural Engine acceleration
4. **Natural Language:** NLP models optimized for Neural Engine

---

## Next Steps

### To Fully Enable Neural Engine:

1. **Get Core ML Models:**
   - Download pre-trained Core ML models
   - Convert existing models to Core ML format
   - Use Apple's sample models

2. **Test Neural Engine Usage:**
   - Load a Core ML model
   - Run inference and verify Neural Engine is used
   - Compare performance vs GPU/CPU

3. **Integrate with Estimation Tool:**
   - Create Core ML model for task estimation
   - Use Neural Engine for faster inference
   - Compare with MLX performance

---

## Resources

- **Core ML Documentation:** https://developer.apple.com/machine-learning/core-ml/
- **Core ML Tools:** https://github.com/apple/coremltools
- **Sample Models:** https://developer.apple.com/machine-learning/models/
- **Neural Engine Guide:** https://developer.apple.com/documentation/coreml/optimizing-neural-network-models-for-device

---

## Summary

✅ **Core ML Integration Created**  
✅ **Neural Engine Support Detected** (M4 chip)  
✅ **Tools Available** for model loading and inference  
⚠️ **Requires Core ML Format Models** (need conversion or download)  
🎯 **Neural Engine will be used automatically** when models support it

**Current Setup:** Ready to use Neural Engine once Core ML models are available!

