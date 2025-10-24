"""
Basic usage example for Codemni-ToolCallAgent

This example shows how to:
1. Initialize the agent with OpenAI
2. Add a simple calculator tool
3. Make a query that requires tool usage
"""

from ToolCall_Agent import ToolCallAgent

# Initialize agent with OpenAI (make sure to set OPENAI_API_KEY environment variable)
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    verbose=True  # Enable colored verbose output
)

# Define a simple calculator tool
def calculator(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Add the tool to the agent
agent.add_tool(
    name="calculator",
    description="Evaluates mathematical expressions. Input should be a valid Python expression like '125 * 48' or '(10 + 5) * 3'.",
    function=calculator
)

# Use the agent
print("\n" + "="*70)
print("EXAMPLE 1: Simple calculation")
print("="*70)
response = agent.invoke("What is 125 multiplied by 48?")
print(f"\nFinal Answer: {response}\n")

print("\n" + "="*70)
print("EXAMPLE 2: Complex calculation")
print("="*70)
response = agent.invoke("Calculate the result of (456 + 789) * 12")
print(f"\nFinal Answer: {response}\n")

print("\n" + "="*70)
print("EXAMPLE 3: No tool needed")
print("="*70)
response = agent.invoke("Hello! Who are you?")
print(f"\nFinal Answer: {response}\n")
