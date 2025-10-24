"""
Multiple tools example for Codemni-ToolCallAgent

This example demonstrates using multiple tools together.
"""

from ToolCall_Agent import ToolCallAgent
import random

# Initialize agent
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    verbose=True
)

# Tool 1: Calculator
def calculator(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 2: Random number generator
def random_number(min_val, max_val):
    """Generate a random number between min and max"""
    try:
        min_val = int(min_val)
        max_val = int(max_val)
        return random.randint(min_val, max_val)
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 3: Text length counter
def count_words(text):
    """Count the number of words in a text"""
    return len(text.split())

# Tool 4: Temperature converter
def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between Celsius and Fahrenheit"""
    try:
        value = float(value)
        from_unit = from_unit.strip().lower()
        to_unit = to_unit.strip().lower()
        
        if from_unit == 'c' and to_unit == 'f':
            result = (value * 9/5) + 32
            return f"{value}°C = {result}°F"
        elif from_unit == 'f' and to_unit == 'c':
            result = (value - 32) * 5/9
            return f"{value}°F = {result}°C"
        else:
            return "Invalid units. Use 'c' or 'f'."
    except Exception as e:
        return f"Error: {str(e)}"

# Add all tools
agent.add_tool(
    "calculator",
    "Evaluates mathematical expressions. Input: expression as string.",
    calculator
)

agent.add_tool(
    "random_number",
    "Generates a random number between min and max. Input: min,max",
    random_number
)

agent.add_tool(
    "count_words",
    "Counts the number of words in a text. Input: text string",
    count_words
)

agent.add_tool(
    "convert_temperature",
    "Converts temperature between Celsius and Fahrenheit. Input: value,from_unit,to_unit (use 'c' or 'f')",
    convert_temperature
)

# Test queries
queries = [
    "Calculate 25 * 4 + 10",
    "Generate a random number between 1 and 100",
    "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'",
    "Convert 25 degrees Celsius to Fahrenheit",
]

for i, query in enumerate(queries, 1):
    print(f"\n{'='*70}")
    print(f"QUERY {i}: {query}")
    print('='*70)
    response = agent.invoke(query)
    print(f"\nFinal Answer: {response}\n")
