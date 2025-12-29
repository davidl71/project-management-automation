#!/usr/bin/env python3
"""
Convert CodeLlama to Core ML Format - Based on Apple's Llama 3.1 Research

This script follows Apple's research on deploying Llama 3.1 with Core ML:
https://machinelearning.apple.com/research/core-ml-on-device-llama

Adapted for CodeLlama to enable Neural Engine (NPU) acceleration for test generation.

Key techniques from Apple's research:
- Quantization for smaller model size
- Neural Engine optimization
- Efficient token generation
- Real-time performance (33 tokens/sec on M1 Max)
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_dependencies() -> dict[str, Any]:
    """Check if required packages are installed."""
    missing = []
    installed = []
    
    try:
        import coremltools as ct
        installed.append(f"coremltools {ct.__version__}")
    except ImportError:
        missing.append("coremltools")
    
    try:
        import torch
        installed.append(f"torch {torch.__version__}")
    except ImportError:
        missing.append("torch")
    
    try:
        import transformers
        installed.append(f"transformers {transformers.__version__}")
    except ImportError:
        missing.append("transformers")
    
    return {
        "all_installed": len(missing) == 0,
        "installed": installed,
        "missing": missing,
        "install_command": f"uv pip install {' '.join(missing)}" if missing else None,
    }


def convert_codellama_to_coreml(
    model_name: str = "codellama/CodeLlama-7b-Instruct-hf",
    output_path: Optional[str] = None,
    quantization: str = "q4_bitwise",  # Apple's recommended quantization
    compute_units: str = "all",  # Use Neural Engine when available
    max_context_length: int = 2048,  # Adjust based on memory
) -> dict[str, Any]:
    """
    Convert CodeLlama PyTorch model to Core ML format.
    
    Based on Apple's Llama 3.1 conversion techniques:
    - Quantization for size reduction
    - Neural Engine optimization
    - Efficient token generation
    
    Args:
        model_name: Hugging Face model name
        output_path: Output path for Core ML model
        quantization: Quantization method (q4_bitwise, q8, fp16)
        compute_units: Core ML compute units (all, cpu_and_ane, cpu_and_gpu)
        max_context_length: Maximum context length
    
    Returns:
        Dict with conversion status
    """
    # Check dependencies
    deps = check_dependencies()
    if not deps["all_installed"]:
        return {
            "success": False,
            "error": f"Missing dependencies: {', '.join(deps['missing'])}",
            "install_command": deps["install_command"],
        }
    
    try:
        import coremltools as ct
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        logger.info("=" * 70)
        logger.info("  CodeLlama to Core ML Conversion")
        logger.info("  Based on Apple's Llama 3.1 Research")
        logger.info("=" * 70)
        logger.info("")
        
        # Set output path
        if not output_path:
            model_safe_name = model_name.replace("/", "_").replace("-", "_")
            output_path = f"models/coreml/{model_safe_name}.mlpackage"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Model: {model_name}")
        logger.info(f"Output: {output_path}")
        logger.info(f"Quantization: {quantization}")
        logger.info(f"Compute Units: {compute_units}")
        logger.info("")
        
        # Step 1: Load PyTorch model
        logger.info("Step 1: Loading PyTorch model from Hugging Face...")
        logger.info("  This may take several minutes and requires significant disk space...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use float16 for efficiency
            device_map="auto",  # Auto device placement
        )
        
        logger.info("  ✅ Model loaded successfully")
        logger.info(f"  Model size: {sum(p.numel() * p.element_size() for p in model.parameters()) / 1024**3:.2f} GB")
        logger.info("")
        
        # Step 2: Prepare for Core ML conversion
        logger.info("Step 2: Preparing model for Core ML conversion...")
        logger.info("  Note: Full conversion of large language models is complex.")
        logger.info("  Apple's research uses specialized conversion techniques.")
        logger.info("")
        
        # Step 3: Convert to Core ML
        logger.info("Step 3: Converting to Core ML format...")
        logger.warning(
            "⚠️  Direct conversion of large language models (7B+ parameters) "
            "to Core ML requires specialized tools and can be memory-intensive."
        )
        logger.warning(
            "⚠️  Apple's research uses optimized conversion pipelines that may "
            "not be directly available in coremltools."
        )
        logger.info("")
        
        # Note: Actual conversion requires:
        # 1. Model-specific conversion scripts
        # 2. Quantization handling
        # 3. Neural Engine optimization
        # 4. Token generation loop implementation
        
        logger.info("📚 Recommended Approach:")
        logger.info("  1. Follow Apple's Llama 3.1 conversion guide:")
        logger.info("     https://machinelearning.apple.com/research/core-ml-on-device-llama")
        logger.info("  2. Use Apple's conversion utilities if available")
        logger.info("  3. Consider using smaller models (1B-3B) for easier conversion")
        logger.info("  4. Use MLX as an alternative (currently working well)")
        logger.info("")
        
        return {
            "success": False,
            "error": "Full conversion requires specialized tools. See recommendations above.",
            "model_name": model_name,
            "output_path": str(output_path),
            "recommendations": [
                "Follow Apple's Llama 3.1 conversion research",
                "Use Apple's conversion utilities if available",
                "Consider smaller models (1B-3B) for easier conversion",
                "Use MLX as alternative (GPU acceleration, currently working)",
                "Check for pre-converted Core ML models on Hugging Face",
            ],
            "apple_research_url": "https://machinelearning.apple.com/research/core-ml-on-device-llama",
            "next_steps": [
                "Review Apple's research paper for detailed conversion steps",
                "Check if Apple provides conversion scripts",
                "Consider using MLX for immediate GPU acceleration",
                "Wait for community-converted Core ML CodeLlama models",
            ],
        }
        
    except ImportError as e:
        return {
            "success": False,
            "error": f"Missing dependency: {e}",
            "install_command": "uv pip install coremltools transformers torch",
        }
    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "recommendations": [
                "Check model name is correct",
                "Ensure sufficient disk space (7B model ~14GB)",
                "Check internet connection for model download",
                "Review Apple's conversion guide for best practices",
            ],
        }


def get_apple_research_summary() -> dict[str, Any]:
    """Get summary of Apple's Llama 3.1 Core ML research."""
    return {
        "title": "On-Device Llama 3.1 with Core ML",
        "url": "https://machinelearning.apple.com/research/core-ml-on-device-llama",
        "key_findings": [
            "Achieved 33 tokens/second on M1 Max",
            "Real-time performance for language models",
            "Neural Engine acceleration enabled",
            "Quantization techniques for size reduction",
            "Efficient token generation pipeline",
        ],
        "techniques": [
            "Model quantization (q4_bitwise recommended)",
            "Neural Engine optimization",
            "Efficient attention mechanisms",
            "Optimized token generation loop",
            "Memory-efficient inference",
        ],
        "applicable_to": [
            "CodeLlama (similar architecture to Llama)",
            "Text generation tasks",
            "Code generation tasks",
            "Test generation (our use case)",
        ],
        "conversion_complexity": "High - requires specialized tools",
        "recommendation": "Follow Apple's research guide or use MLX as alternative",
    }


def main():
    """Main conversion script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert CodeLlama to Core ML format (based on Apple's Llama 3.1 research)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="codellama/CodeLlama-7b-Instruct-hf",
        help="Hugging Face model name (default: codellama/CodeLlama-7b-Instruct-hf)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for Core ML model (default: models/coreml/{model_name}.mlpackage)"
    )
    parser.add_argument(
        "--quantization",
        type=str,
        default="q4_bitwise",
        choices=["q4_bitwise", "q8", "fp16"],
        help="Quantization method (default: q4_bitwise)"
    )
    parser.add_argument(
        "--research",
        action="store_true",
        help="Show Apple's Llama 3.1 Core ML research summary"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check if required dependencies are installed"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  CodeLlama to Core ML Converter")
    print("  Based on Apple's Llama 3.1 Research")
    print("=" * 70)
    print()
    
    if args.research:
        summary = get_apple_research_summary()
        print(json.dumps(summary, indent=2))
        print()
        print(f"📚 Full research: {summary['url']}")
        return 0
    
    if args.check_deps:
        deps = check_dependencies()
        print(json.dumps(deps, indent=2))
        if not deps["all_installed"]:
            print()
            print(f"💡 Install missing packages: {deps['install_command']}")
        return 0
    
    # Run conversion
    result = convert_codellama_to_coreml(
        model_name=args.model,
        output_path=args.output,
        quantization=args.quantization,
    )
    
    print()
    print(json.dumps(result, indent=2))
    
    if not result.get("success") and "recommendations" in result:
        print()
        print("💡 Recommendations:")
        for rec in result["recommendations"]:
            print(f"   • {rec}")
    
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())

