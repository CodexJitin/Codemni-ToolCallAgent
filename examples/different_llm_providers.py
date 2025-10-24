"""
Example showing how to use different LLM providers with Codemni-ToolCallAgent

Make sure to set the appropriate environment variables:
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GROQ_API_KEY
- GOOGLE_API_KEY
"""

from ToolCall_Agent import ToolCallAgent

# Simple calculator tool for testing
def calculator(expression):
    """Evaluate a mathematical expression"""
    return eval(expression)

# Example 1: OpenAI GPT-4
print("\n" + "="*70)
print("EXAMPLE 1: Using OpenAI GPT-4")
print("="*70)
agent_openai = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    temperature=0.7,
    verbose=True
)
agent_openai.add_tool("calculator", "Evaluates math expressions", calculator)
response = agent_openai.invoke("What is 123 * 456?")
print(f"\nResponse: {response}\n")

# Example 2: Anthropic Claude
print("\n" + "="*70)
print("EXAMPLE 2: Using Anthropic Claude")
print("="*70)
agent_anthropic = ToolCallAgent(
    llm_provider='anthropic',
    model='claude-3-opus-20240229',
    temperature=0.7,
    verbose=True
)
agent_anthropic.add_tool("calculator", "Evaluates math expressions", calculator)
response = agent_anthropic.invoke("Calculate 999 + 111")
print(f"\nResponse: {response}\n")

# Example 3: Groq (fast inference)
print("\n" + "="*70)
print("EXAMPLE 3: Using Groq")
print("="*70)
agent_groq = ToolCallAgent(
    llm_provider='groq',
    model='llama3-70b-8192',
    temperature=0.7,
    verbose=True
)
agent_groq.add_tool("calculator", "Evaluates math expressions", calculator)
response = agent_groq.invoke("What is 50 * 50?")
print(f"\nResponse: {response}\n")

# Example 4: Google Gemini
print("\n" + "="*70)
print("EXAMPLE 4: Using Google Gemini")
print("="*70)
agent_google = ToolCallAgent(
    llm_provider='google',
    model='gemini-pro',
    temperature=0.7,
    verbose=True
)
agent_google.add_tool("calculator", "Evaluates math expressions", calculator)
response = agent_google.invoke("Calculate 777 / 7")
print(f"\nResponse: {response}\n")

# Example 5: Ollama (local model)
# Make sure Ollama is running locally: ollama serve
print("\n" + "="*70)
print("EXAMPLE 5: Using Ollama (Local)")
print("="*70)
try:
    agent_ollama = ToolCallAgent(
        llm_provider='ollama',
        model='llama2',
        verbose=True
    )
    agent_ollama.add_tool("calculator", "Evaluates math expressions", calculator)
    response = agent_ollama.invoke("What is 100 - 25?")
    print(f"\nResponse: {response}\n")
except Exception as e:
    print(f"Ollama error (make sure Ollama is running): {e}\n")

# Example 6: Switching LLM providers dynamically
print("\n" + "="*70)
print("EXAMPLE 6: Switching LLM Providers Dynamically")
print("="*70)
agent = ToolCallAgent(verbose=True)
agent.add_tool("calculator", "Evaluates math expressions", calculator)

# Start with OpenAI
agent.set_llm('openai', 'gpt-4')
response1 = agent.invoke("What is 10 + 10?")
print(f"\nOpenAI Response: {response1}\n")

# Switch to Groq
agent.set_llm('groq', 'llama3-70b-8192')
response2 = agent.invoke("What is 20 + 20?")
print(f"\nGroq Response: {response2}\n")
