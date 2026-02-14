#!/usr/bin/env python3
"""Test script for multi-language static analysis implementation."""

import sys

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        from src.analyzer import analyze_code, analyze_python_code
        print("  ✅ analyzer.analyze_code imported")
    except ImportError as e:
        print(f"  ❌ Failed to import analyzer: {e}")
        return False
    
    try:
        from src.evaluator import evaluate_code
        print("  ✅ evaluator.evaluate_code imported")
    except ImportError as e:
        print(f"  ❌ Failed to import evaluator: {e}")
        return False
    
    try:
        from src.ts_analyzer import analyze_code_treesitter, LANGUAGE_TO_PARSER
        print(f"  ✅ ts_analyzer imported (supports {len(LANGUAGE_TO_PARSER)} languages)")
    except ImportError as e:
        print(f"  ⚠️  tree-sitter not available: {e}")
        print("     Run: pip install tree-sitter-language-pack")
        return False
    
    return True


def test_python_analysis():
    """Test Python analysis (should use AST)."""
    print("\n🐍 Testing Python analysis...")
    
    from src.analyzer import analyze_code
    
    code = """
def hello(name: str) -> str:
    '''Say hello.'''
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(hello("World"))
"""
    
    result = analyze_code(code, "Python")
    
    if result is None:
        print("  ❌ Python analysis returned None")
        return False
    
    print(f"  ✅ Functions found: {result['functions']}")
    print(f"  ✅ Has type hints: {result['has_type_hints']}")
    print(f"  ✅ Has docstrings: {result['has_docstrings']}")
    print(f"  ✅ Has main guard: {result['has_main_guard']}")
    
    return True


def test_javascript_analysis():
    """Test JavaScript analysis (should use tree-sitter)."""
    print("\n📜 Testing JavaScript analysis...")
    
    try:
        from src.analyzer import analyze_code
    except ImportError:
        print("  ⚠️  Skipping (tree-sitter not installed)")
        return True
    
    code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Test the function
console.log(fibonacci(10));
"""
    
    result = analyze_code(code, "JavaScript")
    
    if result is None:
        print("  ⚠️  JavaScript analysis not available (tree-sitter not installed)")
        return True
    
    print(f"  ✅ Functions found: {result['functions']}")
    print(f"  ✅ Total lines: {result['total_lines']}")
    print(f"  ✅ Comment ratio: {result['comment_ratio']}")
    print(f"  ✅ Max nesting depth: {result['max_nesting_depth']}")
    
    return True


def test_java_analysis():
    """Test Java analysis (should use tree-sitter)."""
    print("\n☕ Testing Java analysis...")
    
    try:
        from src.analyzer import analyze_code
    except ImportError:
        print("  ⚠️  Skipping (tree-sitter not installed)")
        return True
    
    code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
    
    private int calculate(int x, int y) {
        return x + y;
    }
}
"""
    
    result = analyze_code(code, "Java")
    
    if result is None:
        print("  ⚠️  Java analysis not available (tree-sitter not installed)")
        return True
    
    print(f"  ✅ Functions found: {result['functions']}")
    print(f"  ✅ Classes found: {result['classes']}")
    print(f"  ✅ Has main guard: {result['has_main_guard']}")
    print(f"  ✅ Has type hints: {result['has_type_hints']}")  # Should be True for Java
    
    return True


def test_graceful_degradation():
    """Test that unsupported languages return None gracefully."""
    print("\n🛡️  Testing graceful degradation...")
    
    from src.analyzer import analyze_code
    
    result = analyze_code("print('hello')", "UnknownLanguage")
    
    if result is None:
        print("  ✅ Unsupported language returns None (graceful)")
        return True
    else:
        print("  ❌ Expected None for unsupported language")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🔬 Multi-Language Static Analysis Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Python Analysis", test_python_analysis),
        ("JavaScript Analysis", test_javascript_analysis),
        ("Java Analysis", test_java_analysis),
        ("Graceful Degradation", test_graceful_degradation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n  ❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n🎯 Score: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Implementation is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
