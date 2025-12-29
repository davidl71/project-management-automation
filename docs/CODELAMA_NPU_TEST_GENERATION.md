# CodeLlama NPU-Accelerated Test Generation

**Date:** 2025-12-28  
**Status:** 📋 Proposal  
**Priority:** High

---

## Overview

Enhance test generation with CodeLlama using Neural Engine (NPU) acceleration via Core ML. This will generate actual test code (not just suggestions) with 2-3x faster inference than CPU.

---

## Current State

### ✅ What We Have

1. **Test Generation Tool** (`test_suggestions.py`)
   - AST-based analysis
   - Generates test templates/suggestions
   - No AI/ML models used

2. **Neural Engine Support**
   - ✅ M4 chip has Neural Engine
   - ✅ Core ML can use Neural Engine
   - ✅ Hardware ready for NPU acceleration

3. **CodeLlama Availability**
   - ✅ MLX: `mlx-community/CodeLlama-7b-instruct-4bit`
   - ✅ Can be converted to Core ML format
   - ✅ Optimized for code generation tasks

### ❌ What's Missing

1. **AI-Powered Test Generation**
   - Current: Template-based suggestions
   - Needed: Actual test code generation

2. **NPU Integration**
   - CodeLlama not yet integrated
   - No Core ML model for test generation

---

## Proposed Solution

### Option 1: Core ML + CodeLlama (NPU-Accelerated) ⭐ RECOMMENDED

**Approach:**
1. Convert CodeLlama to Core ML format
2. Use Neural Engine for inference
3. Generate actual test code from function signatures

**Benefits:**
- ✅ **2-3x faster** than CPU inference
- ✅ **Lower power consumption**
- ✅ **On-device processing** (privacy)
- ✅ **Neural Engine optimized**

**Implementation:**
```python
def generate_tests_with_coreml(
    target_file: str,
    test_framework: str = "pytest",
    use_npu: bool = True,
) -> str:
    """
    Generate test code using CodeLlama via Core ML (NPU-accelerated).
    
    Args:
        target_file: Python file to generate tests for
        test_framework: pytest, unittest, etc.
        use_npu: Use Neural Engine (default: True)
    
    Returns:
        Generated test code as string
    """
    # Load Core ML CodeLlama model
    model = ct.models.MLModel(
        "models/coreml/codellama-7b-instruct.mlpackage",
        compute_units=ct.ComputeUnit.CPU_AND_NE if use_npu else ct.ComputeUnit.CPU_ONLY
    )
    
    # Analyze target file
    code = read_file(target_file)
    functions = extract_functions(code)
    
    # Generate tests for each function
    tests = []
    for func in functions:
        prompt = f"Generate a pytest test for this function:\n\n{func.code}"
        result = model.predict({"prompt": prompt})
        tests.append(result["test_code"])
    
    return "\n\n".join(tests)
```

---

### Option 2: MLX CodeLlama (Metal GPU)

**Approach:**
1. Use MLX CodeLlama models directly
2. Metal GPU acceleration (not NPU)
3. Still faster than CPU

**Benefits:**
- ✅ **Easier setup** (no conversion needed)
- ✅ **Metal GPU acceleration**
- ✅ **Good performance**

**Limitations:**
- ⚠️ Uses GPU, not NPU
- ⚠️ Slightly slower than NPU

**Implementation:**
```python
from project_management_automation.tools.mlx_integration import generate_with_mlx

def generate_tests_with_mlx(
    target_file: str,
    test_framework: str = "pytest",
) -> str:
    """Generate test code using MLX CodeLlama (Metal GPU)."""
    code = read_file(target_file)
    functions = extract_functions(code)
    
    tests = []
    for func in functions:
        prompt = f"Generate a pytest test for this Python function:\n\n{func.code}\n\nTest code:"
        test_code = generate_with_mlx(
            prompt=prompt,
            model="mlx-community/CodeLlama-7b-instruct-4bit",
            max_tokens=512,
            temperature=0.3,  # Lower for more deterministic code
        )
        tests.append(test_code)
    
    return "\n\n".join(tests)
```

---

## Comparison

| Approach | Hardware | Speed | Setup Complexity | NPU Usage |
|----------|-----------|-------|------------------|-----------|
| **Core ML + CodeLlama** | Neural Engine | ⭐⭐⭐ Fastest | Medium | ✅ Yes |
| **MLX CodeLlama** | Metal GPU | ⭐⭐ Fast | Easy | ❌ No |
| **Current (AST)** | CPU | ⭐ Slow | Easy | ❌ No |

---

## Implementation Plan

### Phase 1: MLX CodeLlama Integration (Quick Win)

1. **Enhance `test_suggestions.py`**
   - Add `generate_test_code()` function
   - Use MLX CodeLlama for code generation
   - Keep AST analysis for suggestions

2. **Add to `testing` tool**
   - New action: `action="generate"` (actual code)
   - Existing: `action="suggest"` (templates)

**Timeline:** 1-2 hours

---

### Phase 2: Core ML Conversion (NPU Acceleration)

1. **Convert CodeLlama to Core ML**
   - Use `coremltools` to convert MLX model
   - Optimize for Neural Engine operations
   - Test inference speed

2. **Integrate Core ML model**
   - Add Core ML backend to test generation
   - Fallback to MLX if Core ML unavailable
   - Benchmark performance

**Timeline:** 2-4 hours

---

## Usage Examples

### Current (AST-based suggestions)
```python
testing(
    action="suggest",
    target_file="project_management_automation/tools/estimation.py",
    test_framework="pytest",
)
# Returns: Test templates/suggestions
```

### Enhanced (AI-generated code)
```python
testing(
    action="generate",  # New action
    target_file="project_management_automation/tools/estimation.py",
    test_framework="pytest",
    use_coreml=True,  # Use NPU-accelerated Core ML
    use_mlx=False,    # Or use MLX if Core ML unavailable
)
# Returns: Actual test code ready to use
```

---

## Benefits

1. **Faster Test Generation**
   - NPU: 2-3x faster than CPU
   - Generate actual code, not just templates

2. **Better Quality**
   - AI understands code context
   - Generates realistic test cases
   - Handles edge cases better

3. **Developer Productivity**
   - Less manual test writing
   - Faster test coverage improvement
   - Focus on complex test scenarios

---

## Next Steps

1. ✅ **Research:** CodeLlama Core ML conversion feasibility
2. 📋 **Implement:** MLX CodeLlama integration (Phase 1)
3. 📋 **Convert:** CodeLlama to Core ML format (Phase 2)
4. 📋 **Benchmark:** Compare NPU vs GPU vs CPU performance
5. 📋 **Document:** Usage examples and best practices

---

## References

- [Core ML Documentation](https://developer.apple.com/documentation/coreml)
- [MLX CodeLlama Models](https://github.com/ml-explore/mlx-examples/tree/main/codellama)
- [CodeLlama Paper](https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/)

