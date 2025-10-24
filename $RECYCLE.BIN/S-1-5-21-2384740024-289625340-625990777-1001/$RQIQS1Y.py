"""
Example usage of the ToolCall_Agent

This demonstrates how to set up and use the agent with custom tools.
"""

from ToolCall_Agent.agent import ToolCall_Agent
from ToolCall_Agent.prompt import prompt


# Define some example tools
def calculator(query: str) -> str:
    """Performs basic arithmetic calculations. Use for math operations like addition, subtraction, multiplication, division."""
    # Simple calculator implementation
    import re
    # Extract numbers and operator
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


def search_weather(query: str) -> str:
    """Searches for weather information for a given location. Use when user asks about weather, temperature, or forecast."""
    # Mock weather search
    return "The weather is sunny with a temperature of 72°F (22°C)"


def get_current_time(query: str) -> str:
    """Returns the current date and time. Use when user asks about the time or date."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def search_web(query: str) -> str:
    """Searches the web for information. Use for general knowledge questions or when other tools don't apply."""
    # Mock web search
    return f"Search results for: {query} - [Mock result: Information found on the web]"


# Mock LLM class for demonstration
class MockLLM:
    """A mock LLM for testing purposes. Replace with real LLM (OpenAI, Anthropic, etc.)"""
    
    def __init__(self):
        self.call_count = 0
    
    def invoke(self, prompt: str) -> str:
        """Simulate LLM response based on the query"""
        self.call_count += 1
        
        # Extract the user input from the prompt
        user_input = prompt.split("query: ")[-1].strip()
        
        # Check if this is a follow-up with tool results
        if "Tool '" in user_input and "returned:" in user_input:
            # This is a follow-up after tool execution - provide final response
            if "calculator" in user_input:
                # Extract the result from the context
                import re
                result_match = re.search(r"returned:\s*(.+?)(?:\n|$)", user_input)
                if result_match:
                    result = result_match.group(1).strip()
                    return f'''{{
                        "Tool call": "None",
                        "Final Response": "The calculation result is {result}."
                    }}'''
            elif "search_weather" in user_input:
                return '''{
                    "Tool call": "None",
                    "Final Response": "Based on the weather data, it's sunny with a temperature of 72°F (22°C). Perfect weather for outdoor activities!"
                }'''
            elif "get_current_time" in user_input:
                import re
                result_match = re.search(r"returned:\s*(.+?)(?:\n|$)", user_input)
                if result_match:
                    result = result_match.group(1).strip()
                    return f'''{{
                        "Tool call": "None",
                        "Final Response": "The current date and time is {result}."
                    }}'''
            elif "search_web" in user_input:
                return '''{
                    "Tool call": "None",
                    "Final Response": "Based on my search, I found relevant information about your query. The search returned some interesting results!"
                }'''
            
            # Default follow-up response
            return '''{
                "Tool call": "None",
                "Final Response": "I've processed your request with the available tools."
            }'''
        
        # Initial query - decide which tool to use
        original_query = user_input.split("Original query:")[-1].strip() if "Original query:" in user_input else user_input
        
        if any(word in original_query.lower() for word in ['calculate', 'plus', 'minus', 'times', 'divided', '+', '-', '*', '/', 'add', 'subtract', 'multiply']):
            return '''{
                "Tool call": "calculator",
                "Final Response": "None"
            }'''
        elif any(word in original_query.lower() for word in ['weather', 'temperature', 'forecast']):
            return '''{
                "Tool call": "search_weather",
                "Final Response": "None"
            }'''
        elif any(word in original_query.lower() for word in ['time', 'date', 'what time', 'what day', 'current time', 'today']):
            return '''{
                "Tool call": "get_current_time",
                "Final Response": "None"
            }'''
        elif any(word in original_query.lower() for word in ['search', 'find', 'look up', 'what is', 'who is', 'tell me about']):
            return '''{
                "Tool call": "search_web",
                "Final Response": "None"
            }'''
        else:
            return '''{
                "Tool call": "None",
                "Final Response": "Hello! I'm an AI assistant. I can help you with calculations, weather information, time, and web searches. What would you like to know?"
            }'''


def main():
    """Main function to demonstrate the agent"""
    
    # Initialize the agent
    agent = ToolCall_Agent()
    
    # Configure the agent
    agent.add_llm(MockLLM())
    agent.add_PromptTemplate(prompt)
    agent.add_tools({
        "calculator": calculator,
        "search_weather": search_weather,
        "get_current_time": get_current_time,
        "search_web": search_web
    })
    
    # Example queries
    test_queries = [
        "What is 25 + 37?",
        "What's the weather like today?",
        "What time is it?",
        "Who invented the telephone?",
        "Hello there!"
    ]
    
    print("\n" + "="*70)
    print("ToolCall_Agent Demo - Testing with various queries")
    print("="*70)
    
    for query in test_queries:
        agent.run(query, verbose=True)
        print()


if __name__ == "__main__":
    main()
