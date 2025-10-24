"""
Simple test of the ToolCall_Agent with loop functionality
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ToolCall_Agent.agent import ToolCall_Agent
from ToolCall_Agent.prompt import prompt


# Define some example tools
def calculator(query: str) -> str:
    """Performs basic arithmetic calculations. Use for math operations like addition, subtraction, multiplication, division."""
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


def get_current_time(query: str) -> str:
    """Returns the current date and time. Use when user asks about the time or date."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Mock LLM that simulates the loop behavior
class MockLLM:
    """Mock LLM that demonstrates tool calling and final response loop"""
    
    def __init__(self):
        self.iteration = 0
    
    def invoke(self, prompt: str) -> str:
        """Simulate LLM response"""
        self.iteration += 1
        user_input = prompt.split("query: ")[-1].strip()
        
        print(f"[LLM Call #{self.iteration}]")
        print(f"Input context: {user_input[:100]}...")
        
        # If this is a follow-up with tool results, provide final response
        if "Tool '" in user_input and "returned:" in user_input:
            print("→ Detected tool result in context, generating final response...")
            import re
            result_match = re.search(r"returned:\s*(.+?)(?:\n|$)", user_input)
            if result_match:
                result = result_match.group(1).strip()
                if "calculator" in user_input:
                    return f'''{{
                        "Tool call": "None",
                        "Final Response": "The calculation result is {result}."
                    }}'''
                elif "get_current_time" in user_input:
                    return f'''{{
                        "Tool call": "None",
                        "Final Response": "The current date and time is {result}."
                    }}'''
        
        # Initial query - decide which tool to use
        print("→ Initial query, determining which tool to call...")
        if any(word in user_input.lower() for word in ['calculate', '+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide']):
            print("→ Calling calculator tool...")
            return '''{
                "Tool call": "calculator",
                "Final Response": "None"
            }'''
        elif any(word in user_input.lower() for word in ['time', 'date', 'what time', 'what day']):
            print("→ Calling get_current_time tool...")
            return '''{
                "Tool call": "get_current_time",
                "Final Response": "None"
            }'''
        else:
            print("→ No tool needed, providing direct response...")
            return '''{
                "Tool call": "None",
                "Final Response": "Hello! I can help with calculations and telling time. What would you like to know?"
            }'''


def main():
    print("\n" + "="*70)
    print("ToolCall_Agent Loop Demo")
    print("="*70)
    print("\nThis demo shows how the agent loops until it finds a final response:")
    print("1. First iteration: Agent decides which tool to call")
    print("2. Tool executes and returns result")
    print("3. Second iteration: Agent uses tool result to generate final response")
    print("="*70)
    
    # Initialize and configure agent
    agent = ToolCall_Agent()
    agent.add_llm(MockLLM())
    agent.add_PromptTemplate(prompt)
    agent.add_tools({
        "calculator": calculator,
        "get_current_time": get_current_time
    })
    
    # Test queries
    test_queries = [
        "What is 25 + 37?",
        "What time is it now?",
        "Hello there!"
    ]
    
    for query in test_queries:
        print("\n" + "="*70)
        response = agent.run(query, verbose=True)
        print()


if __name__ == "__main__":
    main()
