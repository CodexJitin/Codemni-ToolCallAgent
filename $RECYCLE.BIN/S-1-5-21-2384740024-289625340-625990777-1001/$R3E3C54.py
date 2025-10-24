"""
Real LLM Integration Examples for ToolCall_Agent

This file shows how to integrate the ToolCall_Agent with various real LLM providers.
"""

from ToolCall_Agent.agent import ToolCall_Agent
from ToolCall_Agent.prompt import prompt


# ============================================================================
# Example 1: OpenAI Integration
# ============================================================================

def example_openai():
    """Example using OpenAI's GPT models"""
    try:
        from langchain_openai import ChatOpenAI
        
        # Initialize OpenAI LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,  # Use 0 for more consistent tool calling
            api_key="your-openai-api-key-here"  # Or use environment variable
        )
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Use the agent
        response = agent.run("What is 25 + 37?")
        print(response)
        
    except ImportError:
        print("Install: pip install langchain-openai")


# ============================================================================
# Example 2: Anthropic Claude Integration
# ============================================================================

def example_anthropic():
    """Example using Anthropic's Claude models"""
    try:
        from langchain_anthropic import ChatAnthropic
        
        # Initialize Claude
        llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0,
            api_key="your-anthropic-api-key-here"
        )
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Use the agent
        response = agent.run("What is 25 + 37?")
        print(response)
        
    except ImportError:
        print("Install: pip install langchain-anthropic")


# ============================================================================
# Example 3: Ollama (Local) Integration
# ============================================================================

def example_ollama():
    """Example using Ollama for local models"""
    try:
        from langchain_ollama import ChatOllama
        
        # Initialize Ollama (runs locally)
        llm = ChatOllama(
            model="llama2",  # or "mistral", "codellama", etc.
            temperature=0
        )
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Use the agent
        response = agent.run("What is 25 + 37?")
        print(response)
        
    except ImportError:
        print("Install: pip install langchain-ollama")
        print("Also install Ollama: https://ollama.ai/")


# ============================================================================
# Example 4: Using OpenAI directly (without LangChain)
# ============================================================================

def example_openai_direct():
    """Example using OpenAI's official Python client directly"""
    try:
        from openai import OpenAI
        
        # Create a wrapper class for direct OpenAI usage
        class OpenAIWrapper:
            def __init__(self, api_key, model="gpt-4"):
                self.client = OpenAI(api_key=api_key)
                self.model = model
            
            def invoke(self, prompt: str) -> str:
                """Invoke the OpenAI API and return the response"""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                return response.choices[0].message.content
        
        # Initialize wrapper
        llm = OpenAIWrapper(api_key="your-openai-api-key-here")
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Use the agent
        response = agent.run("What is 25 + 37?")
        print(response)
        
    except ImportError:
        print("Install: pip install openai")


# ============================================================================
# Example 5: Using Anthropic directly (without LangChain)
# ============================================================================

def example_anthropic_direct():
    """Example using Anthropic's official Python client directly"""
    try:
        import anthropic
        
        # Create a wrapper class for direct Anthropic usage
        class AnthropicWrapper:
            def __init__(self, api_key, model="claude-3-sonnet-20240229"):
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = model
            
            def invoke(self, prompt: str) -> str:
                """Invoke the Anthropic API and return the response"""
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
        
        # Initialize wrapper
        llm = AnthropicWrapper(api_key="your-anthropic-api-key-here")
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Use the agent
        response = agent.run("What is 25 + 37?")
        print(response)
        
    except ImportError:
        print("Install: pip install anthropic")


# ============================================================================
# Example Tool Implementations
# ============================================================================

def calculator_tool(query: str) -> str:
    """Performs basic arithmetic calculations. Use for math operations."""
    import re
    match = re.search(r'(\d+\.?\d*)\s*([\+\-\*/])\s*(\d+\.?\d*)', query)
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = float(num1), float(num2)
        
        if operator == '+':
            return str(num1 + num2)
        elif operator == '-':
            return str(num1 - num2)
        elif operator == '*':
            return str(num1 * num2)
        elif operator == '/':
            return str(num1 / num2) if num2 != 0 else "Error: Division by zero"
    return "Could not parse calculation"


def search_tool(query: str) -> str:
    """Searches for information. Replace with real search API."""
    # This is a placeholder - integrate with real search API
    # Options: Google Custom Search, Bing API, DuckDuckGo, etc.
    return f"Search results for: {query}"


# ============================================================================
# Complete Working Example with Environment Variables
# ============================================================================

def example_with_env_vars():
    """
    Example using environment variables for API keys (recommended approach)
    
    Set up your environment:
    Windows: setx OPENAI_API_KEY "your-key-here"
    Linux/Mac: export OPENAI_API_KEY="your-key-here"
    """
    import os
    
    try:
        from langchain_openai import ChatOpenAI
        
        # API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Please set OPENAI_API_KEY environment variable")
            return
        
        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # or "gpt-4"
            temperature=0,
            api_key=api_key
        )
        
        # Set up agent
        agent = ToolCall_Agent()
        agent.add_llm(llm)
        agent.add_PromptTemplate(prompt)
        agent.add_tools({
            "calculator": calculator_tool,
            "search": search_tool
        })
        
        # Test queries
        queries = [
            "What is 42 * 17?",
            "Search for information about Python programming",
            "Calculate 100 / 4"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            response = agent.run(query, verbose=True)
            
    except ImportError:
        print("Install: pip install langchain-openai")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("ToolCall_Agent - Real LLM Integration Examples")
    print("=" * 70)
    print("\nChoose an example to run:")
    print("1. OpenAI (via LangChain)")
    print("2. Anthropic Claude (via LangChain)")
    print("3. Ollama - Local models (via LangChain)")
    print("4. OpenAI (direct SDK)")
    print("5. Anthropic (direct SDK)")
    print("6. OpenAI with environment variables (recommended)")
    print("\nNote: Uncomment the example you want to try and add your API key")
    
    # Uncomment the example you want to try:
    # example_openai()
    # example_anthropic()
    # example_ollama()
    # example_openai_direct()
    # example_anthropic_direct()
    # example_with_env_vars()
