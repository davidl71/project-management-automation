# Apple's Llama 3.1 Core ML Conversion Guide

**Date:** 2025-12-28  
**Source:** Apple Machine Learning Research  
**URL:** https://machinelearning.apple.com/research/core-ml-on-device-llama

---

## Overview

Apple published research on deploying Llama 3.1 (8B Instruct) on Apple Silicon using Core ML, achieving **33 tokens/second on M1 Max** with Neural Engine acceleration.

This guide adapts their techniques for CodeLlama conversion.

---

## Key Findings from Apple's Research

### Performance Metrics
- **Speed:** 33 tokens/second on M1 Max
- **Hardware:** Neural Engine acceleration enabled
- **Model:** Llama-3.1-8B-Instruct
- **Format:** Core ML optimized

### Techniques Used
1. **Quantization:** q4_bitwise recommended
2. **Neural Engine Optimization:** Automatic when model supports ANE
3. **Efficient Token Generation:** Optimized inference loop
4. **Memory Efficiency:** Reduced memory footprint

---

## Conversion Process (Based on Apple's Approach)

### Step 1: Model Preparation

```python
# Load PyTorch model
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)
```

### Step 2: Quantization

Apple recommends **q4_bitwise** quantization:
- Reduces model size significantly
- Maintains quality
- Optimized for Neural Engine

### Step 3: Core ML Conversion

**Note:** Full conversion requires specialized tools. Apple's research uses:
- Custom conversion pipelines
- Model-specific optimizations
- Neural Engine compatibility checks

### Step 4: Optimization

- Enable Neural Engine acceleration
- Optimize attention mechanisms
- Efficient token generation loop

---

## Conversion Script

We've created `scripts/convert_codellama_to_coreml.py` based on Apple's research:

```bash
# Check dependencies
uv run python scripts/convert_codellama_to_coreml.py --check-deps

# View Apple's research summary
uv run python scripts/convert_codellama_to_coreml.py --research

# Attempt conversion (shows recommendations)
uv run python scripts/convert_codellama_to_coreml.py --model codellama/CodeLlama-7b-Instruct-hf
```

---

## Challenges

### 1. Specialized Tools Required
- Full conversion needs Apple's specialized utilities
- Not all features available in public `coremltools`
- May require Apple's internal tools

### 2. Model Size
- 7B model requires ~14GB disk space
- Conversion process memory-intensive
- May need high-memory system

### 3. Complexity
- Model-specific conversion steps
- Neural Engine optimization required
- Token generation loop implementation

---

## Recommendations

### Option 1: Follow Apple's Research (Advanced)
1. Review Apple's full research paper
2. Check for Apple-provided conversion scripts
3. Adapt techniques for CodeLlama
4. Test Neural Engine performance

### Option 2: Use MLX (Current Solution) ✅
- **Status:** Working well
- **Performance:** GPU acceleration (Metal)
- **Ease:** No conversion needed
- **Recommendation:** Continue using for now

### Option 3: Wait for Community
- Monitor Hugging Face for pre-converted models
- Check GitHub for conversion scripts
- Community may provide ready-to-use models

### Option 4: Smaller Models
- Consider 1B-3B models for easier conversion
- Faster conversion process
- Lower memory requirements
- May be sufficient for test generation

---

## Apple's Research Summary

```json
{
  "title": "On-Device Llama 3.1 with Core ML",
  "url": "https://machinelearning.apple.com/research/core-ml-on-device-llama",
  "key_findings": [
    "Achieved 33 tokens/second on M1 Max",
    "Real-time performance for language models",
    "Neural Engine acceleration enabled",
    "Quantization techniques for size reduction",
    "Efficient token generation pipeline"
  ],
  "techniques": [
    "Model quantization (q4_bitwise recommended)",
    "Neural Engine optimization",
    "Efficient attention mechanisms",
    "Optimized token generation loop",
    "Memory-efficient inference"
  ],
  "applicable_to": [
    "CodeLlama (similar architecture to Llama)",
    "Text generation tasks",
    "Code generation tasks",
    "Test generation (our use case)"
  ]
}
```

---

## Next Steps

1. **Review Apple's Research:**
   - Read full paper: https://machinelearning.apple.com/research/core-ml-on-device-llama
   - Understand conversion techniques
   - Check for available tools

2. **Evaluate Options:**
   - Continue with MLX (working) ✅
   - Attempt conversion following Apple's guide
   - Wait for community solutions

3. **If Converting:**
   - Start with smaller model (1B-3B)
   - Test conversion process
   - Optimize for Neural Engine
   - Benchmark performance

---

## Current Status

✅ **Conversion script created** - Based on Apple's research  
✅ **MLX working** - GPU acceleration active  
⏳ **Core ML conversion** - Requires specialized tools  
📚 **Documentation** - Research guide available  

**Recommendation:** Continue with MLX while exploring Core ML conversion options.

