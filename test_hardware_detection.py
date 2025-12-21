#!/usr/bin/env python3
"""Quick test script to verify hardware detection for Ollama."""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from project_management_automation.tools.ollama_integration import (
        detect_hardware_config,
        get_hardware_info,
    )
    
    print("🔍 Hardware Detection Test")
    print("=" * 60)
    print()
    
    # Test hardware detection
    print("1. Detecting hardware configuration...")
    hw_config = detect_hardware_config()
    print(f"   Platform: {hw_config['platform']}")
    print(f"   Architecture: {hw_config['architecture']}")
    print(f"   CPU Cores: {hw_config['cpu_cores']}")
    print(f"   GPU Available: {hw_config['gpu_available']}")
    print(f"   GPU Type: {hw_config['gpu_type']}")
    print()
    
    print("2. Recommended Ollama settings:")
    print(f"   CPU Threads: {hw_config['recommended_num_threads']}")
    print(f"   GPU Layers: {hw_config['recommended_num_gpu']}")
    print(f"   Context Size: {hw_config['recommended_context_size']}")
    print()
    
    # Test hardware info tool
    print("3. Hardware info (formatted):")
    hw_info_json = get_hardware_info()
    hw_info = json.loads(hw_info_json)
    
    if hw_info.get("success"):
        data = hw_info.get("data", {})
        print(f"   Platform: {data.get('platform')}")
        print(f"   GPU: {data.get('gpu_type', 'None')}")
        print()
        print("   Notes:")
        for note in data.get("notes", []):
            print(f"   - {note}")
    else:
        print(f"   Error: {hw_info.get('error', {}).get('message', 'Unknown error')}")
    
    print()
    print("✅ Hardware detection test complete!")
    print()
    print("💡 These settings will be automatically used when calling generate_with_ollama()")
    print("   unless you explicitly override them.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root and dependencies are installed.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
