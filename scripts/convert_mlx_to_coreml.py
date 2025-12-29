#!/usr/bin/env python3
"""
Convert MLX Models to Core ML Format for Neural Engine Acceleration

This script helps convert MLX models (or PyTorch/Transformers models) to Core ML format
for use with Neural Engine (NPU) acceleration on Apple Silicon.

Note: Direct MLX to Core ML conversion is not straightforward. This script provides
utilities for converting from PyTorch/Transformers models to Core ML, which can then
be used for test generation with NPU acceleration.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def convert_pytorch_to_coreml(
    model_name: str,
    output_path: Optional[str] = None,
    task: str = "text-generation",
) -> dict[str, Any]:
    """
    Convert a PyTorch/Transformers model to Core ML format.
    
    This is a helper for converting models that can be used for test generation.
    Most CodeLlama models are available in PyTorch format on Hugging Face.
    
    Args:
        model_name: Hugging Face model name (e.g., "codellama/CodeLlama-7b-Instruct-hf")
        output_path: Output path for Core ML model (default: models/coreml/{model_name}.mlpackage)
        task: Task type (text-generation, text2text-generation, etc.)
    
    Returns:
        Dict with conversion status
    """
    try:
        import coremltools as ct
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        logger.info(f"Converting {model_name} to Core ML format...")
        
        # Load model and tokenizer
        logger.info("Loading PyTorch model from Hugging Face...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use float16 for smaller size
        )
        
        # Convert to Core ML
        logger.info("Converting to Core ML format...")
        # Note: This is a simplified example. Actual conversion may require
        # more configuration based on the specific model architecture.
        
        # For text generation models, we need to specify input/output types
        # This is a placeholder - actual conversion requires model-specific handling
        logger.warning(
            "Direct PyTorch to Core ML conversion for large language models "
            "is complex and may require model-specific optimizations. "
            "Consider using pre-converted Core ML models or specialized conversion tools."
        )
        
        return {
            "success": False,
            "error": "Direct conversion of large language models to Core ML requires specialized tools. "
                     "Consider using pre-converted models or Apple's conversion utilities.",
            "recommendations": [
                "Use Apple's Core ML Tools for model conversion",
                "Look for pre-converted Core ML models on Hugging Face",
                "Consider using smaller models optimized for Core ML",
            ],
        }
        
    except ImportError as e:
        return {
            "success": False,
            "error": f"Required packages not installed: {e}",
            "install_command": "uv pip install coremltools transformers torch",
        }
    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
        }


def check_coreml_model_availability(model_name: str) -> dict[str, Any]:
    """
    Check if a Core ML model is available (pre-converted or downloadable).
    
    Args:
        model_name: Model identifier to check
    
    Returns:
        Dict with availability status and download info
    """
    # Check local models
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models" / "coreml"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    local_models = list(models_dir.glob("*.mlpackage")) + list(models_dir.glob("*.mlmodel"))
    
    result = {
        "model_name": model_name,
        "local_available": False,
        "local_path": None,
        "recommendations": [],
    }
    
    # Check if model exists locally
    for model_path in local_models:
        if model_name.lower() in model_path.name.lower():
            result["local_available"] = True
            result["local_path"] = str(model_path)
            break
    
    if not result["local_available"]:
        result["recommendations"].append(
            "No local Core ML model found. Options:"
        )
        result["recommendations"].append(
            "1. Search Hugging Face for pre-converted Core ML models"
        )
        result["recommendations"].append(
            "   - Filter by 'coreml' tag"
        )
        result["recommendations"].append(
            "   - Look for community-converted models"
        )
        result["recommendations"].append(
            "2. Use MLX models (Metal GPU) as fallback (currently working)"
        )
        result["recommendations"].append(
            "3. Convert PyTorch model using coremltools"
        )
        result["recommendations"].append(
            "4. Note: Apple's Core ML gallery doesn't include text generation models"
        )
        result["recommendations"].append(
            "   - Apple provides: image classification, depth, segmentation, Q&A"
        )
        result["recommendations"].append(
            "   - For text/code generation, use MLX or convert PyTorch models"
        )
    
    return result


def main():
    """Main conversion utility."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert models to Core ML format")
    parser.add_argument(
        "--check",
        type=str,
        help="Check if Core ML model is available for given model name"
    )
    parser.add_argument(
        "--convert",
        type=str,
        help="Convert PyTorch model to Core ML (model name from Hugging Face)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for Core ML model"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  Core ML Model Conversion Utility")
    print("=" * 70)
    print()
    
    if args.check:
        print(f"Checking Core ML model availability for: {args.check}")
        result = check_coreml_model_availability(args.check)
        print(json.dumps(result, indent=2))
        return 0
    
    if args.convert:
        print(f"Converting model: {args.convert}")
        result = convert_pytorch_to_coreml(
            model_name=args.convert,
            output_path=args.output,
        )
        print(json.dumps(result, indent=2))
        return 0 if result.get("success") else 1
    
    print("Usage:")
    print("  --check MODEL_NAME    Check if Core ML model is available")
    print("  --convert MODEL_NAME Convert PyTorch model to Core ML")
    print()
    print("Note: Direct conversion of large language models is complex.")
    print("Consider using pre-converted Core ML models when available.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

