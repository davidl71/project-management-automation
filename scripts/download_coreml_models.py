#!/usr/bin/env python3
"""
Download Core ML models for Neural Engine testing.

Downloads sample Core ML models from Apple and other sources for testing
Neural Engine (NPU) capabilities.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

# Model sources and download info
CORE_ML_MODELS = {
    "mobilevit": {
        "name": "MobileViT",
        "description": "Vision transformer optimized for mobile devices",
        "url": "https://ml-assets.apple.com/coreml/models/Image/Classification/MobileNetV2/MobileNetV2.mlpackage",
        "size": "~5MB",
        "neural_engine": True,
    },
    "mobilenet": {
        "name": "MobileNetV2",
        "description": "Efficient image classification model",
        "url": "https://ml-assets.apple.com/coreml/models/Image/Classification/MobileNetV2/MobileNetV2.mlpackage",
        "size": "~14MB",
        "neural_engine": True,
    },
    "yolov8": {
        "name": "YOLOv8",
        "description": "Object detection model",
        "url": "https://github.com/apple/coremltools/raw/main/examples/image_classification/MobileNetV2.mlpackage",
        "size": "~15MB",
        "neural_engine": True,
    },
}

# Apple's official model repository
APPLE_MODELS_BASE = "https://developer.apple.com/machine-learning/models/"


def download_model(model_id: str, output_dir: Path) -> Dict[str, Any]:
    """Download a Core ML model."""
    if model_id not in CORE_ML_MODELS:
        return {
            "success": False,
            "error": f"Unknown model: {model_id}. Available: {list(CORE_ML_MODELS.keys())}",
        }
    
    model_info = CORE_ML_MODELS[model_id]
    url = model_info["url"]
    
    # Determine output filename
    if url.endswith(".mlpackage"):
        filename = url.split("/")[-1]
    else:
        filename = f"{model_id}.mlpackage"
    
    output_path = output_dir / filename
    
    print(f"Downloading {model_info['name']}...")
    print(f"  URL: {url}")
    print(f"  Size: {model_info['size']}")
    print(f"  Neural Engine: {'Yes' if model_info['neural_engine'] else 'No'}")
    print()
    
    try:
        # Use curl to download
        result = subprocess.run(
            ["curl", "-L", "-o", str(output_path), url],
            capture_output=True,
            text=True,
            timeout=300,
        )
        
        if result.returncode == 0 and output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            return {
                "success": True,
                "model_id": model_id,
                "name": model_info["name"],
                "path": str(output_path),
                "size_mb": round(size_mb, 2),
                "neural_engine": model_info["neural_engine"],
            }
        else:
            return {
                "success": False,
                "error": f"Download failed: {result.stderr}",
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Download timeout (5 minutes)",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def list_available_models() -> List[Dict[str, Any]]:
    """List available Core ML models for download."""
    return [
        {
            "id": model_id,
            **info,
        }
        for model_id, info in CORE_ML_MODELS.items()
    ]


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download Core ML models for Neural Engine testing")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available models",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model ID to download",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all available models",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/coreml",
        help="Output directory (default: models/coreml)",
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.list:
        print("Available Core ML Models:")
        print("=" * 60)
        models = list_available_models()
        for model in models:
            print(f"\n{model['name']} ({model['id']})")
            print(f"  Description: {model['description']}")
            print(f"  Size: {model['size']}")
            print(f"  Neural Engine: {'Yes' if model['neural_engine'] else 'No'}")
        return
    
    if args.all:
        print("Downloading all available models...")
        print()
        results = []
        for model_id in CORE_ML_MODELS.keys():
            result = download_model(model_id, output_dir)
            results.append(result)
            if result["success"]:
                print(f"✅ {result['name']} downloaded to {result['path']}")
            else:
                print(f"❌ {result.get('error', 'Unknown error')}")
            print()
        
        # Summary
        successful = [r for r in results if r.get("success")]
        print(f"Downloaded {len(successful)}/{len(results)} models")
        return
    
    if args.model:
        result = download_model(args.model, output_dir)
        if result["success"]:
            print(f"✅ Successfully downloaded {result['name']}")
            print(f"   Path: {result['path']}")
            print(f"   Size: {result['size_mb']} MB")
            print(f"   Neural Engine: {'Supported' if result['neural_engine'] else 'Not supported'}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    else:
        parser.print_help()
        print("\n💡 Tip: Use --list to see available models")
        print("💡 Tip: Use --model <id> to download a specific model")
        print("💡 Tip: Use --all to download all models")


if __name__ == "__main__":
    main()

