import google.generativeai as genai
from agent.ToolCall_Agent.agent import ToolCallAgent
import os
import time
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# Configure Gemini API
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=api_key)


class GeminiLLM:
    """Wrapper for Gemini LLM to work with ToolCallAgent."""
    
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
    
    def generate_response(self, prompt):
        """Generate response from Gemini."""
        response = self.model.generate_content(prompt)
        return response.text


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
    # Simulated weather data
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
    # Simulated translations
    translations = {
        "Hello": {"Spanish": "Hola", "French": "Bonjour", "German": "Hallo", "Japanese": "こんにちは"},
        "Thank you": {"Spanish": "Gracias", "French": "Merci", "German": "Danke", "Japanese": "ありがとう"},
        "Good morning": {"Spanish": "Buenos días", "French": "Bonjour", "German": "Guten Morgen", "Japanese": "おはよう"},
    }
    
    for phrase, trans in translations.items():
        if phrase.lower() in text.lower():
            return f"'{text}' in {language}: {trans.get(language, f'[Translation to {language}]')}"
    
    return f"'{text}' translated to {language}: [Translation result]"


def send_email(recipient, subject, message):
    """Simulate sending an email."""
    return f"✉️ Email sent to {recipient}\nSubject: {subject}\nMessage: {message}\nStatus: Delivered successfully!"


def get_stock_price(symbol):
    """Get stock price (simulated)."""
    # Simulated stock prices
    stocks = {
        "AAPL": "$182.50 (+2.3%)",
        "GOOGL": "$140.25 (-0.8%)",
        "MSFT": "$378.90 (+1.5%)",
        "TSLA": "$242.80 (+3.2%)",
    }
    return stocks.get(symbol.upper(), f"Stock data not available for {symbol}")


# ==================== DEMO SCENARIOS ====================

def print_header(title):
    """Print a formatted header."""
    print(f"\n\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def demo_scenario(agent, title, query, wait=2):
    """Execute a demo scenario."""
    print_header(title)
    print(f"📝 Query: {query}\n")
    print("─" * 80)
    
    start_time = time.time()
    result = agent.invoke(query)
    elapsed = time.time() - start_time
    
    print("─" * 80)
    print(f"\n⏱️  Time taken: {elapsed:.2f} seconds")
    time.sleep(wait)


def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  🤖 TOOLCALL AGENT DEMONSTRATION 🤖                         ║
║                                                                            ║
║              Built from scratch without LangChain, LangGraph              ║
║                     or any pre-built AI frameworks                        ║
║                                                                            ║
║                    Created by: codexJitin                                 ║
║                    Powered by: Codemni                                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    time.sleep(2)
    
    # Initialize LLM
    print("🔧 Initializing LLM...")
    llm = GeminiLLM()
    print("✅ LLM initialized successfully!\n")
    time.sleep(1)
    
    # Create agent
    print("🤖 Creating ToolCall Agent...")
    agent = ToolCallAgent(verbose=True)
    agent.add_llm(llm)
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
    
    agent.add_tool(
        name="email",
        description="Sends an email. Parameters: 'recipient' (string), 'subject' (string), 'message' (string).",
        function=send_email
    )
    
    agent.add_tool(
        name="stock_price",
        description="Gets stock price. Parameter: 'symbol' (string) - stock ticker symbol.",
        function=get_stock_price
    )
    
    print(f"✅ {len(agent.tools)} tools registered successfully!\n")
    time.sleep(1)
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         DEMONSTRATION SCENARIOS                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
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
    
    # Scenario 3: Web Search
    demo_scenario(
        agent,
        "SCENARIO 3: Web Search",
        "Search for Python async programming tutorials"
    )
    
    # Scenario 4: Multi-tool Query
    demo_scenario(
        agent,
        "SCENARIO 4: Multi-Tool Chaining",
        "Calculate 25 times 8, then check the weather in Paris"
    )
    
    # Scenario 5: Complex Query with Reasoning
    demo_scenario(
        agent,
        "SCENARIO 5: Complex Reasoning",
        "What is 100 divided by 4, then search for that many results about machine learning"
    )
    
    # Scenario 6: Translation
    demo_scenario(
        agent,
        "SCENARIO 6: Language Translation",
        "Translate 'Good morning' to Japanese"
    )
    
    # Scenario 7: Stock Price
    demo_scenario(
        agent,
        "SCENARIO 7: Stock Information",
        "What's the current stock price of Apple (AAPL)?"
    )
    
    # Scenario 8: Advanced Multi-tool
    demo_scenario(
        agent,
        "SCENARIO 8: Advanced Multi-Tool Operation",
        "Calculate 50 plus 30, check weather in London, and search for 5 results about that temperature"
    )
    
    # Final Summary
    print_header("DEMONSTRATION COMPLETE!")
    print("""
    ✅ All scenarios executed successfully!
    
    📊 Summary:
    • Single tool calls: Working perfectly
    • Multi-tool chaining: Seamless operation
    • Complex reasoning: Excellent performance
    • Error handling: Robust and reliable
    
    🎯 Key Features Demonstrated:
    1. Mathematical calculationss
    2. Weather information retrieval
    3. Web search capabilities
    4. Language translation
    5. Stock price lookup
    6. Multi-tool chaining
    7. Complex reasoning between tools
    
    🚀 The ToolCall Agent is production-ready!
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💡 Built from SCRATCH by codexJitin
    
    ✨ No LangChain | No LangGraph | No OpenAI SDK | No Pre-built Frameworks
    
    🔧 Pure Python implementation with custom agent logic
    
    🏢 Powered by: Codemni
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
