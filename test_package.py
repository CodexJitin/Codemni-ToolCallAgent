"""
Quick test script to verify the package installation and basic functionality.
Run this after installing the package to make sure everything works.
"""

import sys

def test_import():
    """Test if the package can be imported"""
    print("Testing import...")
    try:
        from ToolCall_Agent import ToolCallAgent
        print("✓ Package imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import package: {e}")
        return False

def test_version():
    """Test if version is accessible"""
    print("\nTesting version...")
    try:
        from ToolCall_Agent import __version__
        print(f"✓ Package version: {__version__}")
        return True
    except ImportError as e:
        print(f"✗ Failed to get version: {e}")
        return False

def test_basic_functionality():
    """Test basic agent functionality with a mock LLM"""
    print("\nTesting basic functionality...")
    try:
        from ToolCall_Agent import ToolCallAgent
        
        # Create a simple mock LLM for testing
        class MockLLM:
            def generate_response(self, prompt):
                return '''json
{
    "Tool call": "test_tool",
    "Tool Parameters": {"Hello World"},
    "Final Response": "None"
}
'''
        
        # Create agent
        agent = ToolCallAgent()
        
        # Add mock LLM
        agent.add_llm(MockLLM())
        
        # Add test tool
        def test_tool(text):
            return f"Received: {text}"
        
        agent.add_tool("test_tool", "A test tool", test_tool)
        
        print("✓ Agent initialized and configured successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed basic functionality test: {e}")
        return False

def test_llm_providers():
    """Test which LLM providers are available"""
    print("\nChecking available LLM providers...")
    
    providers = {
        'openai': 'openai',
        'anthropic': 'anthropic',
        'groq': 'groq',
        'google': 'google.generativeai',
        'ollama': 'ollama'
    }
    
    available = []
    unavailable = []
    
    for name, module in providers.items():
        try:
            __import__(module)
            available.append(name)
            print(f"  ✓ {name} is available")
        except ImportError:
            unavailable.append(name)
            print(f"  ✗ {name} is not available (install with: pip install Codemni-ToolCallAgent[{name}])")
    
    return len(available) > 0

def main():
    """Run all tests"""
    print("="*70)
    print("Codemni-ToolCallAgent Package Verification")
    print("="*70)
    
    results = []
    results.append(("Import Test", test_import()))
    results.append(("Version Test", test_version()))
    results.append(("Functionality Test", test_basic_functionality()))
    results.append(("LLM Providers Test", test_llm_providers()))
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests passed")
    print("-"*70)
    
    if passed == total:
        print("\n✓ All tests passed! Package is ready to use.")
        return 0
    else:
        print("\n⚠ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
