#!/usr/bin/env python3
"""
Quick test runner for Ollama Enhanced Tools
Runs tests one at a time with progress output
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_error_handling():
    """Test error handling."""
    print("\n" + "="*80)
    print("TEST 1: Error Handling")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        
        result = generate_code_documentation('/nonexistent/file.py', model='codellama')
        data = json.loads(result)
        
        if not data.get('success'):
            print("✅ PASS: Error handling works correctly")
            error_msg = data.get('error', {}).get('message', 'N/A')
            print(f"   Error message: {error_msg[:100]}")
            return True
        else:
            print("❌ FAIL: Should have returned error")
            return False
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False


def test_generate_documentation():
    """Test generate_code_documentation with a real file."""
    print("\n" + "="*80)
    print("TEST 2: generate_code_documentation")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import generate_code_documentation
        
        test_file = project_root / "check_ollama.py"
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        print(f"📄 Testing with: {test_file.name}")
        print("⏳ Generating documentation (this may take 10-30 seconds)...")
        
        result = generate_code_documentation(str(test_file), style='google', model='codellama')
        data = json.loads(result)
        
        if data.get('success'):
            print("✅ SUCCESS")
            result_data = data.get('data', {})
            print(f"   - Original length: {result_data.get('original_length', 0)} chars")
            print(f"   - Documented length: {result_data.get('documented_length', 0)} chars")
            print(f"   - Style: {result_data.get('style', 'unknown')}")
            
            # Show preview of documentation
            docs = result_data.get('documentation', '')
            if docs:
                preview = docs[:200] + "..." if len(docs) > 200 else docs
                print(f"   - Preview: {preview[:100]}...")
            
            return True
        else:
            print("❌ FAILED")
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            print(f"   Error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analyze_quality():
    """Test analyze_code_quality."""
    print("\n" + "="*80)
    print("TEST 3: analyze_code_quality")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import analyze_code_quality
        
        test_file = project_root / "check_ollama.py"
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            return False
        
        print(f"📄 Testing with: {test_file.name}")
        print("⏳ Analyzing code quality (this may take 10-30 seconds)...")
        
        result = analyze_code_quality(str(test_file), include_suggestions=True, model='codellama')
        data = json.loads(result)
        
        if data.get('success'):
            print("✅ SUCCESS")
            result_data = data.get('data', {})
            analysis = result_data.get('analysis', {})
            
            if 'quality_score' in analysis:
                print(f"   - Quality score: {analysis.get('quality_score', 'N/A')}/100")
            if 'maintainability' in analysis:
                print(f"   - Maintainability: {analysis.get('maintainability', 'N/A')}")
            if 'code_smells' in analysis:
                smells = analysis.get('code_smells', [])
                print(f"   - Code smells: {len(smells)}")
                if smells:
                    print(f"     Examples: {', '.join(smells[:3])}")
            if 'suggestions' in analysis:
                suggestions = analysis.get('suggestions', [])
                print(f"   - Suggestions: {len(suggestions)}")
            
            return True
        else:
            print("❌ FAILED")
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            print(f"   Error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enhance_summary():
    """Test enhance_context_summary."""
    print("\n" + "="*80)
    print("TEST 4: enhance_context_summary")
    print("="*80)
    
    try:
        from project_management_automation.tools.ollama_enhanced_tools import enhance_context_summary
        
        test_data = {
            "project_name": "Exarp PMA",
            "tasks": {"pending": 12, "in_progress": 3, "completed": 45},
            "health_score": 85,
            "issues": ["Documentation needs updating", "Test coverage at 72%"],
            "recommendations": ["Add more unit tests", "Update README.md"]
        }
        
        print("📊 Testing with sample project data")
        print("⏳ Generating summary (this may take 5-15 seconds)...")
        
        result = enhance_context_summary(test_data, level='brief', model='codellama')
        data = json.loads(result)
        
        if data.get('success'):
            print("✅ SUCCESS")
            result_data = data.get('data', {})
            print(f"   - Level: {result_data.get('level', 'unknown')}")
            print(f"   - Original length: {result_data.get('original_length', 0)} chars")
            print(f"   - Summary length: {result_data.get('summary_length', 0)} chars")
            
            summary = result_data.get('summary', '')
            if summary:
                preview = summary[:200] + "..." if len(summary) > 200 else summary
                print(f"   - Summary preview: {preview[:150]}...")
            
            return True
        else:
            print("❌ FAILED")
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            print(f"   Error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("OLLAMA ENHANCED TOOLS - QUICK TEST SUITE")
    print("="*80)
    print("\n⚠️  Note: Tests may take 30-90 seconds total (LLM generation is slow)")
    print("   Ollama server must be running")
    print()
    
    results = []
    
    # Run tests
    results.append(("Error Handling", test_error_handling()))
    results.append(("generate_code_documentation", test_generate_documentation()))
    results.append(("analyze_code_quality", test_analyze_quality()))
    results.append(("enhance_context_summary", test_enhance_summary()))
    
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
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
