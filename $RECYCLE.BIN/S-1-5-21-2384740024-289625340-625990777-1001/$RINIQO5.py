"""
Example usage of ToolCall Agent with built-in LLM initialization.

This demonstrates how users can simply define which LLM, model, and API key
without writing separate initialization code.
"""

from ToolCall_Agent import ToolCallAgent


# Define some example tools
def calculator(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


def get_weather(city):
    """Get weather information for a city (mock function)."""
    return f"The weather in {city} is sunny with a temperature of 72°F"


def search_web(query):
    """Search the web (mock function)."""
    return f"Here are the search results for '{query}': [Mock results...]"


# ====================================================================
# METHOD 1: Initialize agent with LLM in constructor (Recommended)
# ====================================================================
print("=" * 70)
print("METHOD 1: Initialize with LLM in constructor")
print("=" * 70)

# Example with OpenAI
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-openai-api-key-here',  # Or set OPENAI_API_KEY env var
    temperature=0.7,
    verbose=True
)

# Add tools
agent.add_tool("calculator", "Evaluate mathematical expressions", calculator)
agent.add_tool("get_weather", "Get weather information for a city", get_weather)
agent.add_tool("search_web", "Search the web for information", search_web)

# Run query
response = agent.invoke("What is 125 * 48?")
print(f"\nFinal Answer: {response}\n")


# ====================================================================
# METHOD 2: Initialize agent first, then set LLM
# ====================================================================
print("=" * 70)
print("METHOD 2: Initialize agent first, then set LLM")
print("=" * 70)

# Create agent
agent2 = ToolCallAgent(verbose=True)

# Add tools
agent2.add_tool("calculator", "Evaluate mathematical expressions", calculator)
agent2.add_tool("get_weather", "Get weather information for a city", get_weather)

# Set LLM using the built-in method
agent2.set_llm(
    provider='groq',
    model='llama3-70b-8192',
    api_key='your-groq-api-key-here',  # Or set GROQ_API_KEY env var
    temperature=0.5
)

# Run query
response = agent2.invoke("What's the weather like in New York?")
print(f"\nFinal Answer: {response}\n")


# ====================================================================
# METHOD 3: Using environment variables (Most secure)
# ====================================================================
print("=" * 70)
print("METHOD 3: Using environment variables")
print("=" * 70)

# Set environment variable first:
# export ANTHROPIC_API_KEY="your-key-here"  # Linux/Mac
# $env:ANTHROPIC_API_KEY="your-key-here"    # Windows PowerShell

agent3 = ToolCallAgent(
    llm_provider='anthropic',
    model='claude-3-sonnet-20240229',
    # api_key not provided - will read from ANTHROPIC_API_KEY env var
    verbose=True
)

agent3.add_tool("calculator", "Evaluate mathematical expressions", calculator)
response = agent3.invoke("Calculate 999 + 1")
print(f"\nFinal Answer: {response}\n")


# ====================================================================
# METHOD 4: Using different LLM providers
# ====================================================================
print("=" * 70)
print("METHOD 4: Different LLM providers")
print("=" * 70)

# Google Gemini
agent_google = ToolCallAgent(
    llm_provider='google',
    model='gemini-pro',
    api_key='your-google-api-key'
)

# Ollama (local models - no API key needed)
agent_ollama = ToolCallAgent(
    llm_provider='ollama',
    model='llama2',
    base_url='http://localhost:11434'  # Optional, this is the default
)

print("Google Gemini and Ollama agents initialized!")


# ====================================================================
# METHOD 5: Using custom LLM (Advanced)
# ====================================================================
print("=" * 70)
print("METHOD 5: Using custom LLM")
print("=" * 70)

# If you have a custom LLM class with generate_response method
class CustomLLM:
    def generate_response(self, prompt):
        # Your custom implementation
        return "Custom response"

agent_custom = ToolCallAgent()
agent_custom.add_llm(CustomLLM())
agent_custom.add_tool("calculator", "Evaluate mathematical expressions", calculator)


# ====================================================================
# SUPPORTED LLM PROVIDERS
# ====================================================================
print("\n" + "=" * 70)
print("SUPPORTED LLM PROVIDERS")
print("=" * 70)
print("""
1. OpenAI
   - Provider: 'openai'
   - Models: 'gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo', etc.
   - Env Variable: OPENAI_API_KEY
   - Install: pip install openai

2. Anthropic (Claude)
   - Provider: 'anthropic'
   - Models: 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', etc.
   - Env Variable: ANTHROPIC_API_KEY
   - Install: pip install anthropic

3. Groq
   - Provider: 'groq'
   - Models: 'llama3-70b-8192', 'mixtral-8x7b-32768', etc.
   - Env Variable: GROQ_API_KEY
   - Install: pip install groq

4. Google Gemini
   - Provider: 'google'
   - Models: 'gemini-pro', 'gemini-1.5-pro', etc.
   - Env Variable: GOOGLE_API_KEY
   - Install: pip install google-generativeai

5. Ollama (Local)
   - Provider: 'ollama'
   - Models: 'llama2', 'mistral', 'codellama', etc.
   - Env Variable: OLLAMA_BASE_URL (optional)
   - Install: pip install ollama
   - Note: Requires Ollama running locally
""")


print("\n" + "=" * 70)
print("QUICK START")
print("=" * 70)
print("""
# 1. Install the required LLM library
pip install openai  # or anthropic, groq, google-generativeai, ollama

# 2. Create agent with built-in LLM
from ToolCall_Agent import ToolCallAgent

agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-api-key',
    temperature=0.7
)

# 3. Add your tools
agent.add_tool("tool_name", "tool_description", tool_function)

# 4. Run!
response = agent.invoke("Your query here")
""")
