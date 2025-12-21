#!/usr/bin/env python3
"""
Ollama Performance Comparison Test

Compares performance with and without hardware optimizations.
Tests basic text generation to measure speed differences.

Run with: uv run python test_ollama_performance.py
"""

import json
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_generation(prompt, model="llama3.2", use_optimizations=True, **kwargs):
    """Test Ollama generation with timing."""
    try:
        from project_management_automation.tools.ollama_integration import generate_with_ollama
        
        print(f"\n{'='*60}")
        if use_optimizations:
            print(f"🚀 Testing WITH hardware optimizations (auto-detected)")
        else:
            print(f"🐌 Testing WITHOUT hardware optimizations (manual override)")
        print(f"{'='*60}")
        print(f"Model: {model}")
        print(f"Prompt length: {len(prompt)} characters")
        
        start_time = time.time()
        
        # Test with or without optimizations
        if use_optimizations:
            # Auto-detect hardware optimizations
            result = generate_with_ollama(
                prompt=prompt,
                model=model,
                stream=False,
                **kwargs
            )
        else:
            # Disable optimizations (CPU-only, no GPU, default context)
            result = generate_with_ollama(
                prompt=prompt,
                model=model,
                stream=False,
                num_gpu=None,  # Explicitly disable GPU
                num_threads=None,  # Use default
                context_size=None,  # Use default
                options={},  # No custom options
                **kwargs
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Parse result
        result_data = json.loads(result)
        
        if result_data.get("success"):
            data = result_data.get("data", {})
            response_length = data.get("length", 0)
            perf_options = data.get("performance_options", {})
            
            print(f"\n✅ Generation successful")
            print(f"   Duration: {duration:.2f} seconds")
            print(f"   Response length: {response_length} characters")
            print(f"   Throughput: {response_length / duration:.1f} chars/sec")
            
            if perf_options:
                print(f"\n   Performance settings used:")
                print(f"   - GPU layers: {perf_options.get('num_gpu', 'None')}")
                print(f"   - CPU threads: {perf_options.get('num_threads', 'None')}")
                print(f"   - Context size: {perf_options.get('context_size', 'None')}")
            
            if data.get("hardware_detected"):
                hw = data["hardware_detected"]
                print(f"\n   Hardware detected:")
                print(f"   - Platform: {hw.get('platform', 'Unknown')}")
                print(f"   - GPU type: {hw.get('gpu_type', 'None')}")
                print(f"   - CPU cores: {hw.get('cpu_cores', 'Unknown')}")
            
            return {
                "success": True,
                "duration": duration,
                "response_length": response_length,
                "throughput": response_length / duration,
                "performance_options": perf_options,
            }
        else:
            print(f"\n❌ Generation failed")
            error = result_data.get("error", {})
            print(f"   Error: {error.get('message', 'Unknown error')}")
            return {
                "success": False,
                "error": error.get("message", "Unknown error"),
            }
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
        }


def main():
    """Run performance comparison tests."""
    print("="*60)
    print("OLLAMA PERFORMANCE COMPARISON TEST")
    print("="*60)
    print("\nThis test compares performance with and without hardware optimizations.")
    print("Make sure Ollama is running and you have a model available (e.g., llama3.2)")
    
    # Test prompt (simple but realistic)
    test_prompt = """Write a brief summary (2-3 sentences) about the benefits of 
automated code documentation. Focus on maintainability and developer productivity."""
    
    # Use a smaller/faster model for better CPU performance
    # Try phi3 first (fastest), fall back to llama3.2:1b, then llama3.2
    model = "phi3"  # Small, fast model - ideal for CPU-only inference
    
    print(f"\nUsing model: {model}")
    print("If this model is not available, the test will fail.")
    print("To install: ollama pull phi3")
    print("Or change the model variable in the script to llama3.2:1b or llama3.2")
    
    # Test 1: With hardware optimizations (auto-detected)
    print("\n" + "="*60)
    print("TEST 1: WITH Hardware Optimizations")
    print("="*60)
    result_with_opt = test_generation(test_prompt, model=model, use_optimizations=True)
    
    # Wait a bit between tests
    print("\n⏳ Waiting 2 seconds before next test...")
    time.sleep(2)
    
    # Test 2: Without hardware optimizations (CPU-only, defaults)
    print("\n" + "="*60)
    print("TEST 2: WITHOUT Hardware Optimizations (CPU-only)")
    print("="*60)
    result_without_opt = test_generation(test_prompt, model=model, use_optimizations=False)
    
    # Compare results
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    if result_with_opt.get("success") and result_without_opt.get("success"):
        opt_duration = result_with_opt["duration"]
        no_opt_duration = result_without_opt["duration"]
        opt_throughput = result_with_opt["throughput"]
        no_opt_throughput = result_without_opt["throughput"]
        
        speedup = no_opt_duration / opt_duration if opt_duration > 0 else 0
        throughput_improvement = (opt_throughput / no_opt_throughput - 1) * 100 if no_opt_throughput > 0 else 0
        
        print(f"\n📊 Results:")
        print(f"   WITH optimizations:    {opt_duration:.2f}s ({opt_throughput:.1f} chars/sec)")
        print(f"   WITHOUT optimizations: {no_opt_duration:.2f}s ({no_opt_throughput:.1f} chars/sec)")
        print(f"\n⚡ Speedup: {speedup:.2f}x faster with optimizations")
        print(f"📈 Throughput improvement: {throughput_improvement:+.1f}%")
        
        if speedup > 1.1:
            print(f"\n✅ Hardware optimizations are providing significant speedup!")
        elif speedup > 0.9:
            print(f"\n⚠️  Minimal difference - optimizations may not be effective on this hardware")
        else:
            print(f"\n❌ Unexpected: optimizations made it slower (check configuration)")
            
    elif result_with_opt.get("success"):
        print(f"\n⚠️  Only test with optimizations succeeded")
        print(f"   Duration: {result_with_opt['duration']:.2f}s")
    elif result_without_opt.get("success"):
        print(f"\n⚠️  Only test without optimizations succeeded")
        print(f"   Duration: {result_without_opt['duration']:.2f}s")
    else:
        print(f"\n❌ Both tests failed")
        print(f"   With optimizations: {result_with_opt.get('error', 'Unknown error')}")
        print(f"   Without optimizations: {result_without_opt.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
