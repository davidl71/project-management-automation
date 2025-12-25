# MLX Model Names Research

**Date:** 2025-01-25  
**Status:** ✅ Complete

## Summary

Researched and corrected MLX model identifiers for Hugging Face mlx-community organization. Updated all model names in `project_management_automation/tools/mlx_integration.py` to use verified, working model identifiers.

## Research Method

1. **Direct Hugging Face API Query**: Used `huggingface_hub.list_models()` to query actual available models
2. **Verified Model Names**: Tested actual model loading and generation
3. **API Compatibility Check**: Verified `mlx_lm.generate()` parameter compatibility

## Findings

### ✅ Corrected Model Names

#### Code Generation Models
- **OLD**: `mlx-community/CodeLlama-7b-Instruct-mlx` ❌
- **NEW**: `mlx-community/CodeLlama-7b-mlx` ✅
- **NEW**: `mlx-community/CodeLlama-7b-Python-mlx` ✅ (Python-focused variant)

#### General Purpose Models
- **OLD**: `mlx-community/Llama-3.1-8B-Instruct-mlx` ❌
- **NEW**: `mlx-community/Meta-Llama-3.1-8B-Instruct-bf16` ✅ (full precision, ~16GB)
- **NEW**: `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit` ✅ (quantized, ~4.5GB)

- **OLD**: `mlx-community/Phi-3.5-mini-4k-instruct-mlx` ❌
- **NEW**: `mlx-community/Phi-3.5-mini-instruct-4bit` ✅
- **Also available**: `-8bit`, `-bf16` variants

- **OLD**: `mlx-community/Mistral-7B-Instruct-v0.2-mlx` ❌
- **NEW**: `mlx-community/Mistral-7B-Instruct-v0.2` ✅ (no `-mlx` suffix)

#### Small/Fast Models
- **OLD**: `mlx-community/TinyLlama-1.1B-Chat-v1.0-mlx` ✅ (already correct)
- **OLD**: `mlx-community/Phi-3-mini-128k-instruct-mlx` ❌
- **NEW**: `mlx-community/Phi-3-mini-128k-instruct-4bit` ✅

### 🔑 Key Patterns Discovered

1. **Suffix Variability**: 
   - Some models have `-mlx` suffix, some don't
   - No consistent pattern

2. **Quantization Variants**:
   - Models often available in multiple quantization formats: `-4bit`, `-8bit`, `-bf16`
   - Quantized models are smaller and recommended for most use cases

3. **Model Naming Conventions**:
   - Llama 3.1 models use `Meta-` prefix: `Meta-Llama-3.1-8B-Instruct-4bit`
   - Phi-3.5 models don't include version numbers in base name
   - Mistral models use original organization names

### API Compatibility Issues Fixed

1. **Temperature Parameter**: 
   - ❌ `temp=temperature` - Not supported
   - ❌ `temperature=temperature` - Not supported
   - ✅ Removed temperature parameter (not available in current mlx_lm API)
   - Note: Temperature parameter accepted in function signature for API compatibility, but ignored during generation

2. **max_tokens Parameter**:
   - ✅ Works correctly: `max_tokens=max_tokens`

## Updated Files

### `project_management_automation/tools/mlx_integration.py`

**Changes:**
1. Updated `list_mlx_models()` recommended model list with verified names
2. Updated default model in `generate_with_mlx()`: `mlx-community/Phi-3.5-mini-instruct-4bit`
3. Removed temperature parameter from `generate()` call (not supported by API)
4. Added quantization variants to model recommendations

**Model List Updates:**
- Code models: Added Python variant, corrected names
- General models: Added Llama 3.1 with quantization variants, corrected Phi-3.5 and Mistral
- Small models: Corrected Phi-3 mini model name

## Verification

✅ **Tested and Working:**
- Model loading: `mlx-community/Phi-3.5-mini-instruct-4bit` ✅
- Text generation: Successfully generates text ✅
- Model listing: Returns corrected model names ✅

**Test Results:**
```bash
✅ Model downloaded successfully
✅ Text generation working
✅ Generated: "Machine learning is a subset of artificial intelligence..."
```

## Available Model Categories

From Hugging Face mlx-community organization:

1. **Llama Models**: 
   - Llama 2 (7B, 13B variants)
   - Llama 3.1 (8B, 70B variants with quantization)

2. **Phi Models**:
   - Phi-2 (base, 4bit variants)
   - Phi-3 (mini, medium, small with 4k/128k context)
   - Phi-3.5 (mini, vision, MoE variants)

3. **Mistral Models**:
   - Mistral-7B-Instruct (v0.1, v0.2, v0.3 variants)

4. **Code Models**:
   - CodeLlama (7B, 13B, Python variants)

5. **Small Models**:
   - TinyLlama (1.1B chat variants)

## Recommendations

1. **Default Model**: `mlx-community/Phi-3.5-mini-instruct-4bit`
   - Good balance of speed, quality, and size
   - Recommended for most use cases

2. **For Code**: `mlx-community/CodeLlama-7b-Python-mlx`
   - Best for Python-specific tasks

3. **For Quality**: `mlx-community/Meta-Llama-3.1-8B-Instruct-4bit`
   - Higher quality but larger model

4. **For Speed**: `mlx-community/TinyLlama-1.1B-Chat-v1.0-mlx`
   - Fastest but lower quality

## Future Considerations

1. **Temperature Support**: Monitor mlx_lm updates for temperature control
2. **Model Discovery**: Consider implementing dynamic model discovery from Hugging Face
3. **Model Recommendations**: Add model recommendation based on hardware (already partially implemented)
4. **Quantization Selection**: Automatically recommend appropriate quantization based on available RAM

## References

- [Hugging Face MLX Documentation](https://huggingface.co/docs/hub/mlx)
- [MLX-LM GitHub](https://github.com/ml-explore/mlx-examples)
- Verified via `huggingface_hub.list_models(author='mlx-community')`

