# CodeLlama Test Generation Usage Guide

**Date:** 2025-12-28  
**Status:** ✅ Implemented  
**Feature:** AI-powered test code generation using MLX CodeLlama

---

## Overview

The test generation tool now supports AI-powered test code generation using MLX CodeLlama models. This generates actual, runnable test code (not just templates) with Metal GPU acceleration.

---

## Usage

### Basic Usage

```python
from project_management_automation.tools.consolidated import testing
import json

# Generate test code for a file
result = testing(
    action='generate',
    target_file='project_management_automation/tools/estimation.py',
    test_framework='pytest',
    output_path='tests/test_estimation_generated.py'
)

parsed = json.loads(result)
if parsed.get('success'):
    data = parsed.get('data', {})
    print(f"Generated {data['functions_tested']} tests")
    print(f"Method: {data['method']}")  # mlx_codellama or template
```

### Via MCP Tool

```json
{
  "name": "testing",
  "arguments": {
    "action": "generate",
    "target_file": "project_management_automation/tools/estimation.py",
    "test_framework": "pytest",
    "output_path": "tests/test_estimation_generated.py"
  }
}
```

---

## Actions Comparison

| Action | Output | Method | Use Case |
|--------|--------|--------|----------|
| `suggest` | Test templates/suggestions | AST analysis | Quick overview of what to test |
| `generate` | Actual test code | MLX CodeLlama (AI) | Generate runnable tests |

---

## Features

### ✅ AI-Powered Generation
- Uses MLX CodeLlama for intelligent test generation
- Understands function context and purpose
- Generates comprehensive test cases

### ✅ Metal GPU Acceleration
- Uses Metal GPU (not NPU, but still fast)
- Faster than CPU-based generation
- Efficient for batch processing

### ✅ Fallback Support
- Falls back to template-based generation if MLX unavailable
- Graceful degradation ensures tool always works

### ✅ Multiple Frameworks
- Supports `pytest` (default)
- Supports `unittest`
- Easy to extend to other frameworks

---

## Parameters

### `generate_test_code()` Function

- `target_file` (required): Python file to generate tests for
- `test_framework` (default: "pytest"): Framework to use
- `use_mlx` (default: True): Use MLX CodeLlama (False = template only)
- `model` (default: "mlx-community/Phi-3.5-mini-instruct-4bit"): MLX model to use
- `max_tokens` (default: 512): Maximum tokens to generate
- `temperature` (default: 0.3): Generation temperature (lower = more deterministic)
- `output_path` (optional): Save generated code to file

---

## Example Output

```python
{
  "success": true,
  "data": {
    "target_file": "tools/estimation.py",
    "functions_tested": 3,
    "test_framework": "pytest",
    "method": "mlx_codellama",
    "generated_tests": [
      {
        "function": "estimate_task_duration",
        "test_code": "def test_estimate_task_duration():\n    ...",
        "framework": "pytest",
        "method": "mlx_codellama"
      }
    ],
    "combined_test_code": "# Test for estimate_task_duration\n...",
    "output_file": "tests/test_estimation_generated.py"
  }
}
```

---

## Next Steps: Core ML Integration (NPU)

Phase 2 will add Core ML conversion for Neural Engine (NPU) acceleration:

1. Convert CodeLlama to Core ML format
2. Use Neural Engine for 2-3x faster inference
3. Lower power consumption
4. Better batch processing performance

---

## Troubleshooting

### MLX Not Available
- Tool falls back to template-based generation
- Check MLX installation: `uv pip install mlx mlx-lm`

### Model Not Found
- Default model: `mlx-community/Phi-3.5-mini-instruct-4bit`
- Model will be downloaded automatically on first use
- Ensure internet connection for model download

### Generation Quality
- Adjust `temperature` (lower = more deterministic)
- Increase `max_tokens` for longer/complex tests
- Review and edit generated code as needed

---

## Benefits

1. **Faster Test Writing**: Generate tests in seconds vs minutes
2. **Better Coverage**: AI understands code context
3. **Consistent Style**: Generated tests follow framework conventions
4. **GPU Acceleration**: Metal GPU speeds up generation

---

## Future Enhancements

- [ ] Core ML conversion for NPU acceleration
- [ ] Batch generation for multiple files
- [ ] Custom prompt templates
- [ ] Integration with test runners
- [ ] Test code quality scoring

