#!/usr/bin/env python3
"""Quick test with smaller model to compare performance."""

import json
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from project_management_automation.tools.ollama_integration import generate_with_ollama, get_hardware_info

def test_small_model():
    """Test with smaller model optimized for CPU."""
    print("="*60)
    print("TESTING WITH SMALLER MODEL (llama3.2)")
    print("="*60)
    
    # Show hardware info
    print("\n🔍 Hardware Configuration:")
    hw_info = json.loads(get_hardware_info())
    if hw_info.get("success"):
        data = hw_info["data"]
        print(f"   Platform: {data.get('platform')}")
        print(f"   GPU: {data.get('gpu_type', 'None')}")
        print(f"   CPU Cores: {data.get('cpu_cores')}")
        print(f"   Recommended threads: {data.get('recommended_settings', {}).get('num_threads')}")
    
    # Test prompt
    prompt = """Write a brief 2-sentence explanation of why smaller models are faster for CPU inference."""
    
    print(f"\n📝 Prompt length: {len(prompt)} characters")
    
    # Test with the smaller 1B model
    model = "llama3.2:1b"
    print(f"🤖 Model: {model} (1.3 GB - smaller and faster!)")
    print("\n⏳ Generating with RAM-optimized settings (auto-detected)...")
    
    start = time.time()
    result = generate_with_ollama(
        prompt=prompt,
        model=model,
        stream=False,  # Disable streaming for accurate timing
    )
    duration = time.time() - start
    
    result_data = json.loads(result)
    
    if result_data.get("success"):
        data = result_data["data"]
        response = data.get("response", "")
        perf = data.get("performance_options", {})
        
        print(f"\n✅ Generation successful!")
        print(f"   ⏱️  Duration: {duration:.2f} seconds")
        print(f"   📊 Response length: {len(response)} characters")
        print(f"   📈 Throughput: {len(response) / duration:.1f} chars/sec")
        print(f"\n   Performance settings:")
        print(f"   - GPU layers: {perf.get('num_gpu', 'None')}")
        print(f"   - CPU threads: {perf.get('num_threads', 'None')}")
        print(f"   - Context size: {perf.get('context_size', 'None')}")
        
        print(f"\n📝 Response preview:")
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"   {preview}")
        
        print(f"\n💡 Tip: Try an even smaller model for faster inference:")
        print(f"   ollama pull phi3          # ~2.3GB - Very fast")
        print(f"   ollama pull llama3.2:1b   # ~700MB - Fastest")
        
    else:
        error = result_data.get("error", {})
        print(f"\n❌ Generation failed: {error.get('message', 'Unknown error')}")

if __name__ == "__main__":
    try:
        test_small_model()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
