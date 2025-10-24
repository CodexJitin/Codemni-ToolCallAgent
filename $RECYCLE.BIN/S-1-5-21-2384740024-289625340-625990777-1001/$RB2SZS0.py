"""
Simple Demo - ToolCall Agent with Built-in LLM Initialization

This is a minimal working example showing how easy it is to use the agent
with built-in LLM initialization.
"""

from ToolCall_Agent import ToolCallAgent


# Define a simple calculator tool
def calculator(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


# Define a simple weather tool (mock)
def get_weather(city):
    """Get weather information for a city."""
    # This is a mock function - in real use, you'd call a weather API
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Cloudy, 15°C",
        "tokyo": "Rainy, 20°C",
        "paris": "Clear, 18°C"
    }
    city_lower = city.lower()
    weather = weather_data.get(city_lower, "Weather data not available")
    return f"Weather in {city}: {weather}"


def main():
    print("=" * 70)
    print("ToolCall Agent - Simple Demo")
    print("=" * 70)
    print()
    
    # Choose your LLM provider
    print("Available providers:")
    print("1. OpenAI (gpt-4)")
    print("2. Anthropic (claude-3-sonnet)")
    print("3. Groq (llama3-70b)")
    print("4. Google (gemini-pro)")
    print("5. Ollama (llama2) - local")
    print()
    
    choice = input("Enter choice (1-5) or provider name: ").strip()
    
    # Map choices to providers
    provider_map = {
        "1": ("openai", "gpt-4"),
        "2": ("anthropic", "claude-3-sonnet-20240229"),
        "3": ("groq", "llama3-70b-8192"),
        "4": ("google", "gemini-pro"),
        "5": ("ollama", "llama2"),
        "openai": ("openai", "gpt-4"),
        "anthropic": ("anthropic", "claude-3-sonnet-20240229"),
        "groq": ("groq", "llama3-70b-8192"),
        "google": ("google", "gemini-pro"),
        "ollama": ("ollama", "llama2"),
    }
    
    if choice.lower() not in provider_map:
        print("Invalid choice. Using OpenAI by default.")
        choice = "1"
    
    provider, model = provider_map[choice.lower()]
    
    # Get API key if needed (except for Ollama)
    api_key = None
    if provider != "ollama":
        api_key = input(f"Enter your {provider.upper()} API key (or press Enter to use env var): ").strip()
        if not api_key:
            api_key = None  # Will try to read from environment
            print(f"Will try to read from environment variable...")
    
    print()
    print("=" * 70)
    print(f"Initializing agent with {provider.upper()} - {model}")
    print("=" * 70)
    print()
    
    try:
        # Create agent with built-in LLM initialization
        agent = ToolCallAgent(
            llm_provider=provider,
            model=model,
            api_key=api_key,
            temperature=0.7,
            verbose=True  # Enable beautiful colored output
        )
        
        # Add tools
        agent.add_tool(
            name="calculator",
            description="Evaluate mathematical expressions like '2+2' or '125*48'",
            function=calculator
        )
        
        agent.add_tool(
            name="get_weather",
            description="Get weather information for a city",
            function=get_weather
        )
        
        print("\n✓ Agent initialized successfully!")
        print("✓ Tools added: calculator, get_weather")
        print()
        
        # Run example queries
        queries = [
            "What is 125 multiplied by 48?",
            "What's the weather like in New York?",
            "Calculate 999 + 1 and tell me if that's a round number"
        ]
        
        print("=" * 70)
        print("Running Example Queries")
        print("=" * 70)
        print()
        
        for i, query in enumerate(queries, 1):
            print(f"\n{'─' * 70}")
            print(f"Query {i}: {query}")
            print('─' * 70)
            
            response = agent.invoke(query)
            print(f"\n✓ Final Answer: {response}")
            print()
        
        # Interactive mode
        print("\n" + "=" * 70)
        print("Interactive Mode - Enter your own queries!")
        print("=" * 70)
        print("Type 'exit' or 'quit' to end")
        print()
        
        while True:
            user_query = input("\nYour query: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not user_query:
                continue
            
            print()
            response = agent.invoke(user_query)
            print(f"\n✓ Final Answer: {response}")
    
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nTips:")
        print(f"- Make sure you have the {provider} package installed: pip install {provider}")
        print(f"- Set the environment variable or provide the API key")
        print(f"- For {provider.upper()}, set: {provider.upper()}_API_KEY")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nPlease check your setup and try again.")


if __name__ == "__main__":
    main()
