"""
Refactored Demo - Using the new modular architecture.
Demonstrates how to use the refactored agent with core components.

Created by: codexJitin
Powered by: Codemni
"""

import sys
import os
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from agent.ToolCall_Agent.refactored_agent import ToolCallAgent
from agent.adapters.gemini_adapter import GeminiLLM
from agent.core.colors import Colors


# ==================== TOOL DEFINITIONS ====================

def calculator(expression):
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"Error: {str(e)}"


def get_weather(city):
    """Get weather for a city."""
    weather_data = {
        "Paris": "☀️ Sunny, 25°C",
        "London": "🌧️ Rainy, 18°C",
        "Tokyo": "☁️ Cloudy, 22°C",
        "New York": "⛅ Partly Cloudy, 20°C",
        "Mumbai": "🌤️ Hot and Humid, 32°C",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


def web_search(query, num_results="5"):
    """Simulate web search."""
    return f"Found {num_results} results for '{query}':\n1. Tutorial on {query}\n2. Complete guide to {query}\n3. {query} documentation\n4. Best practices for {query}\n5. Advanced {query} techniques"


def translate_text(text, language):
    """Translate text to target language."""
    translations = {
        "Hello": {"Spanish": "Hola", "French": "Bonjour", "German": "Hallo", "Japanese": "こんにちは"},
        "Thank you": {"Spanish": "Gracias", "French": "Merci", "German": "Danke", "Japanese": "ありがとう"},
        "Good morning": {"Spanish": "Buenos días", "French": "Bonjour", "German": "Guten Morgen", "Japanese": "おはよう"},
    }
    
    for phrase, trans in translations.items():
        if phrase.lower() in text.lower():
            return f"'{text}' in {language}: {trans.get(language, f'[Translation to {language}]')}"
    
    return f"'{text}' translated to {language}: [Translation result]"


# ==================== DEMO ====================

def demo_scenario(agent, title, query, wait=2):
    """Execute a demo scenario."""
    Colors.print_header(title, width=80, color='cyan')
    print(f"📝 Query: {query}\n")
    print("─" * 80)
    
    start_time = time.time()
    result = agent.invoke(query)
    elapsed = time.time() - start_time
    
    print("─" * 80)
    print(f"\n⏱️  Time taken: {elapsed:.2f} seconds")
    time.sleep(wait)


def main():
    Colors.print_box(
        "🤖 REFACTORED TOOLCALL AGENT DEMONSTRATION 🤖\n\n"
        "Built with modular, reusable components\n"
        "Perfect for multi-agent systems\n\n"
        "Created by: codexJitin\n"
        "Powered by: Codemni",
        width=78
    )
    
    time.sleep(2)
    
    # Initialize LLM using adapter
    print("\n🔧 Initializing LLM...")
    llm = GeminiLLM()
    print("✅ LLM initialized successfully!")
    print(f"   Model: {llm.get_model_info()['model_name']}\n")
    time.sleep(1)
    
    # Create agent using refactored class
    print("🤖 Creating Refactored ToolCall Agent...")
    agent = ToolCallAgent(name="RefactoredAgent", verbose=True)
    agent.set_llm(llm)
    print("✅ Agent created successfully!\n")
    time.sleep(1)
    
    # Register tools
    print("🔧 Registering tools...")
    
    agent.add_tool(
        name="calculator",
        description="Performs mathematical calculations. Parameter: 'expression' (string) - math expression.",
        function=calculator
    )
    
    agent.add_tool(
        name="weather",
        description="Gets current weather for a city. Parameter: 'city' (string) - city name.",
        function=get_weather
    )
    
    agent.add_tool(
        name="search",
        description="Searches the web. Parameters: 'query' (string) - search query, 'num_results' (string, optional) - number of results.",
        function=web_search
    )
    
    agent.add_tool(
        name="translator",
        description="Translates text. Parameters: 'text' (string) - text to translate, 'language' (string) - target language.",
        function=translate_text
    )
    
    print(f"✅ {len(agent.list_tools())} tools registered: {', '.join(agent.list_tools())}\n")
    time.sleep(1)
    
    # Display agent configuration
    print("📊 Agent Configuration:")
    config = agent.get_config()
    print(f"   Name: {config['name']}")
    print(f"   Verbose: {config['verbose']}")
    print(f"   Max Iterations: {config['max_iterations']}")
    print(f"   Tools: {len(config['tools'])}")
    print()
    time.sleep(1)
    
    Colors.print_box("DEMONSTRATION SCENARIOS", width=78)
    time.sleep(2)
    
    # Scenario 1: Simple Calculation
    demo_scenario(
        agent,
        "SCENARIO 1: Simple Mathematical Calculation",
        "What is 456 multiplied by 789?"
    )
    
    # Scenario 2: Weather Query
    demo_scenario(
        agent,
        "SCENARIO 2: Weather Information",
        "What's the weather in Tokyo?"
    )
    
    # Scenario 3: Multi-tool Query
    demo_scenario(
        agent,
        "SCENARIO 3: Multi-Tool Chaining",
        "Calculate 25 times 8, then check the weather in Paris"
    )
    
    # Scenario 4: Translation
    demo_scenario(
        agent,
        "SCENARIO 4: Language Translation",
        "Translate 'Good morning' to Japanese"
    )
    
    # Final Summary
    Colors.print_header("DEMONSTRATION COMPLETE!", color='green')
    print("""
    ✅ Refactored agent working perfectly!
    
    🎯 Key Improvements:
    • Modular architecture with reusable components
    • Clean separation of concerns
    • Easy to extend for multi-agent systems
    • LLM adapter pattern for multiple providers
    • Shared tool executor and response parser
    • Base agent class for common functionality
    
    📦 New Structure:
    • agent/core/ - Reusable core components
    • agent/adapters/ - LLM provider adapters
    • agent/ToolCall_Agent/ - Specific agent implementation
    
    🚀 Ready for multi-agent systems!
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💡 Built from SCRATCH by codexJitin
    
    ✨ Modular | Reusable | Extensible | Production-Ready
    
    🏢 Powered by: Codemni
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    print(f"\n{'=' * 80}\n")
    print("Thank you for watching! 🙏")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
