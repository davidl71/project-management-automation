# Core ML Quick Start Guide

**Date:** 2025-12-28  
**Purpose:** Quick guide to using Core ML with Neural Engine on M4

---

## Current Status

✅ **Core ML Installed:** `coremltools==9.0`  
✅ **Neural Engine Detected:** M4 chip supports Neural Engine  
✅ **Integration Ready:** Tools available in `coreml()` function

---

## Quick Test

### 1. Check Neural Engine Support

```python
from project_management_automation.tools.consolidated import coreml
import json

result = coreml(action="info")
data = json.loads(result)['data']

print(f"Neural Engine: {data['neural_engine_support']}")
print(f"Compute Units: {data['compute_units_available']}")
```

### 2. List Available Models

```python
result = coreml(action="list")
# Shows any .mlmodel or .mlpackage files found
```

### 3. Run Inference (when you have a model)

```python
result = coreml(
    action="predict",
    model_path="path/to/model.mlpackage",
    input_data='{"input_name": [1.0, 2.0, 3.0]}',
    compute_units="all"  # Uses Neural Engine when available
)
```

---

## Getting Core ML Models

### Option 1: Apple's Sample Models

Visit: https://developer.apple.com/machine-learning/models/

Download pre-trained models like:
- Image Classification models
- Object Detection models
- Natural Language models

### Option 2: Convert Existing Models

**From PyTorch:**
```python
import coremltools as ct
import torch

# Load PyTorch model
torch_model = torch.load("model.pth")
torch_model.eval()

# Convert
example_input = torch.rand(1, 3, 224, 224)
traced = torch.jit.trace(torch_model, example_input)

coreml_model = ct.convert(
    traced,
    inputs=[ct.TensorType(name="input", shape=example_input.shape)],
    compute_units=ct.ComputeUnit.ALL,  # Enable Neural Engine
)

coreml_model.save("model.mlpackage")
```

**From TensorFlow:**
```python
import coremltools as ct
import tensorflow as tf

# Load TensorFlow model
tf_model = tf.keras.models.load_model("model.h5")

# Convert
coreml_model = ct.convert(
    tf_model,
    compute_units=ct.ComputeUnit.ALL,  # Enable Neural Engine
)

coreml_model.save("model.mlpackage")
```

### Option 3: Create Simple Test Model

A simple test model has been created at `models/coreml/test_model.mlpackage` for testing.

---

## Neural Engine Usage

### Automatic Selection

Core ML automatically uses Neural Engine when:
1. ✅ Model has ANE-compatible operations
2. ✅ Hardware has Neural Engine (M1+)
3. ✅ Compute units set to "all" or "cpu_and_ane"

### Verify Neural Engine Usage

1. **Activity Monitor:** Check "Neural Engine" usage
2. **Performance:** Neural Engine is typically 2-5x faster than CPU
3. **Model Spec:** Check if model supports ANE operations

---

## Next Steps

1. **Download a sample model** from Apple's repository
2. **Test inference** with the downloaded model
3. **Compare performance** (CPU vs GPU vs Neural Engine)
4. **Convert your own models** if needed

---

## Resources

- **Apple Models:** https://developer.apple.com/machine-learning/models/
- **Core ML Docs:** https://developer.apple.com/machine-learning/core-ml/
- **Core ML Tools:** https://github.com/apple/coremltools

