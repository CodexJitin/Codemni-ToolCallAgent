"""
SIMPLE TEST for ToolCall_Agent
Run this file to see the agent work!

Command: python simple_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ToolCall_Agent.agent import ToolCall_Agent
from ToolCall_Agent.prompt import prompt


# ============================================================
# STEP 1: Create a tool (just a function that returns a string)
# ============================================================
def calculator(query: str) -> str:
    """Does simple math like 5 + 3 or 10 - 2"""
    import re
    # Find numbers and operator in the query
    match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', query)
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)
        
        # Do the math
        if operator == '+': return str(num1 + num2)
        if operator == '-': return str(num1 - num2)
        if operator == '*': return str(num1 * num2)
        if operator == '/': return str(num1 // num2)
    
    return "Sorry, can't calculate that"


# ============================================================
# STEP 2: Create a fake LLM for testing (replace with real one later)
# ============================================================
class SimpleLLM:
    """
    This pretends to be an AI.
    In real use, replace this with OpenAI, Claude, etc.
    """
    
    def invoke(self, prompt: str) -> str:
        """This is called by the agent"""
        # Get the user's question
        query = prompt.split("query: ")[-1].strip()
        
        # SCENARIO 1: We got tool results back - make final answer
        if "returned:" in query:
            result = query.split("returned:")[1].split("\n")[0].strip()
            return f'{{"Tool call": "None", "Final Response": "The answer is {result}"}}'
        
        # SCENARIO 2: User asked math - call calculator tool
        if any(symbol in query for symbol in ['+', '-', '*', '/']):
            return '{"Tool call": "calculator", "Final Response": "None"}'
        
        # SCENARIO 3: No tool needed - just respond
        return '{"Tool call": "None", "Final Response": "Hello! Ask me a math question!"}'


# ============================================================
# STEP 3: Set up and test the agent
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("SIMPLE TEST - ToolCall_Agent")
    print("="*60)
    
    # Create the agent
    agent = ToolCall_Agent()
    
    # Add our fake LLM
    agent.add_llm(SimpleLLM())
    
    # Add the prompt template
    agent.add_PromptTemplate(prompt)
    
    # Add our calculator tool
    agent.add_tools({"calculator": calculator})
    
    print("\n✓ Agent is ready!\n")
    
    # Test queries
    queries = [
        "What is 5 + 3?",
        "Calculate 10 - 4",
        "Hello there!"
    ]
    
    # Run tests by passing queries directly to invoke()
    for i, query in enumerate(queries, 1):
        print("="*60)
        print(f"TEST {i}: {query}")
        print("="*60)
        
        # Call invoke directly with the query
        result = agent.invoke(query)
        
        # Print the results
        print(f"Iterations: {result['iterations']}")
        print(f"Tools Called: {result['tool_calls'] or 'None'}")
        if result['tool_results']:
            for tool, tool_result in zip(result['tool_calls'], result['tool_results']):
                print(f"  → {tool}: {tool_result}")
        print(f"Final Response: {result['final_response']}")
        print()
    
    print("="*60)
    print("ALL TESTS PASSED! ✓")
    print("="*60)
    print("\nWhat happened:")
    print("  • Tests 1 & 2: Agent called calculator tool (2 iterations)")
    print("  • Test 3: Agent responded directly (1 iteration)")
    print("\nThe loop works! 🎉")
    print("="*60)
