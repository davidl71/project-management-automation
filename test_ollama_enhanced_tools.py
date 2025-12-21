#!/usr/bin/env python3
"""
Test script for Ollama Enhanced Tools

Tests the three enhanced Ollama tools:
1. generate_code_documentation
2. analyze_code_quality
3. enhance_context_summary

Run with: uv run python test_ollama_enhanced_tools.py
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_generate_code_documentation():
    """Test generate_code_documentation tool."""
    print("\n" + "="*80)
    print("TEST 1: generate_code_documentation")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        
        # Test with a simple Python file
        test_file = project_root / "check_ollama.py"
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        print(f"📄 Testing with file: {test_file}")
        print("⏳ Generating documentation (this may take 10-30 seconds)...")
        
        result = generate_code_documentation(
            file_path=str(test_file),
            style="google",
            model="codellama"
        )
        
        result_data = json.loads(result)
        
        if result_data.get("success"):
            print("✅ generate_code_documentation: SUCCESS")
            data = result_data.get("data", {})
            print(f"   - Original length: {data.get('original_length', 0)} chars")
            print(f"   - Documented length: {data.get('documented_length', 0)} chars")
            print(f"   - Style: {data.get('style', 'unknown')}")
            return True
        else:
            print("❌ generate_code_documentation: FAILED")
            print(f"   Error: {result_data.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ generate_code_documentation: EXCEPTION - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analyze_code_quality():
    """Test analyze_code_quality tool."""
    print("\n" + "="*80)
    print("TEST 2: analyze_code_quality")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import analyze_code_quality
        
        # Test with a simple Python file
        test_file = project_root / "check_ollama.py"
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        print(f"📄 Testing with file: {test_file}")
        print("⏳ Analyzing code quality (this may take 10-30 seconds)...")
        
        result = analyze_code_quality(
            file_path=str(test_file),
            include_suggestions=True,
            model="codellama"
        )
        
        result_data = json.loads(result)
        
        if result_data.get("success"):
            print("✅ analyze_code_quality: SUCCESS")
            data = result_data.get("data", {})
            analysis = data.get("analysis", {})
            
            if "quality_score" in analysis:
                print(f"   - Quality score: {analysis.get('quality_score', 'N/A')}/100")
            if "maintainability" in analysis:
                print(f"   - Maintainability: {analysis.get('maintainability', 'N/A')}")
            if "code_smells" in analysis:
                print(f"   - Code smells: {len(analysis.get('code_smells', []))}")
            if "suggestions" in analysis:
                print(f"   - Suggestions: {len(analysis.get('suggestions', []))}")
            
            return True
        else:
            print("❌ analyze_code_quality: FAILED")
            print(f"   Error: {result_data.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ analyze_code_quality: EXCEPTION - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enhance_context_summary():
    """Test enhance_context_summary tool."""
    print("\n" + "="*80)
    print("TEST 3: enhance_context_summary")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary
        
        # Test with sample project data
        test_data = {
            "project_name": "Exarp PMA",
            "tasks": {
                "pending": 12,
                "in_progress": 3,
                "completed": 45
            },
            "health_score": 85,
            "issues": [
                "Documentation needs updating",
                "Test coverage at 72%"
            ],
            "recommendations": [
                "Add more unit tests",
                "Update README.md"
            ]
        }
        
        print("📊 Testing with sample project data")
        print("⏳ Generating summary (this may take 5-15 seconds)...")
        
        result = enhance_context_summary(
            data=test_data,
            level="brief",
            model="codellama"
        )
        
        result_data = json.loads(result)
        
        if result_data.get("success"):
            print("✅ enhance_context_summary: SUCCESS")
            data = result_data.get("data", {})
            print(f"   - Level: {data.get('level', 'unknown')}")
            print(f"   - Original length: {data.get('original_length', 0)} chars")
            print(f"   - Summary length: {data.get('summary_length', 0)} chars")
            summary = data.get("summary", "")
            if summary:
                # Print first 200 chars of summary
                preview = summary[:200] + "..." if len(summary) > 200 else summary
                print(f"   - Summary preview: {preview}")
            return True
        else:
            print("❌ enhance_context_summary: FAILED")
            print(f"   Error: {result_data.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ enhance_context_summary: EXCEPTION - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling for enhanced tools."""
    print("\n" + "="*80)
    print("TEST 4: Error Handling")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import (
            generate_code_documentation,
            analyze_code_quality,
            enhance_context_summary
        )
        
        # Test with non-existent file
        print("📄 Testing with non-existent file...")
        result = generate_code_documentation(
            file_path="/nonexistent/file.py",
            model="codellama"
        )
        result_data = json.loads(result)
        
        if not result_data.get("success"):
            print("✅ Error handling: SUCCESS (correctly handled missing file)")
            return True
        else:
            print("❌ Error handling: FAILED (should have returned error)")
            return False
            
    except Exception as e:
        print(f"❌ Error handling: EXCEPTION - {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("OLLAMA ENHANCED TOOLS TEST SUITE")
    print("="*80)
    print("\n⚠️  Note: Ollama server must be running for these tests to work.")
    print("   Start it with: ollama serve")
    print("   Or: open -a Ollama (macOS)")
    
    results = []
    
    # Test 1: generate_code_documentation
    results.append(("generate_code_documentation", test_generate_code_documentation()))
    
    # Test 2: analyze_code_quality
    results.append(("analyze_code_quality", test_analyze_code_quality()))
    
    # Test 3: enhance_context_summary
    results.append(("enhance_context_summary", test_enhance_context_summary()))
    
    # Test 4: Error handling
    results.append(("error_handling", test_error_handling()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
