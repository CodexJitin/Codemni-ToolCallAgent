# Loop Functionality in ToolCall_Agent

## Overview

The ToolCall_Agent now runs in a **loop** until a final response is found, enabling multi-step reasoning where the agent can:
1. Call a tool
2. Receive the tool's result
3. Use that result to generate a final response to the user

## How It Works

### The Loop Process

```
User Query
    ↓
[Iteration 1] → LLM decides which tool to call
    ↓
Tool executes and returns result
    ↓
[Iteration 2] → LLM uses tool result to generate final response
    ↓
Final response found → Loop exits
```

### Key Changes

#### 1. **invoke() Method**
```python
def invoke(self, user_input: str, max_iterations: int = 5) -> Dict[str, Any]
```

**New Behavior:**
- Loops until `Final Response != "None"` or max_iterations reached
- Tracks all tool calls and results across iterations
- Updates context after each tool execution
- Returns comprehensive result with all tool calls

**Returns:**
```python
{
    "tool_calls": ["calculator"],           # List of all tools called
    "tool_results": ["62.0"],               # List of all tool results
    "final_response": "The result is 62.0", # Final user-facing response
    "iterations": 2                         # Number of loop iterations
}
```

#### 2. **Context Management**

After each tool execution, the context is updated:
```python
context = f"Original query: {user_input}\n\nTool '{tool_call}' returned: {tool_result}\n\nProvide a final response to the user based on this information."
```

This allows the LLM to:
- Remember the original query
- See the tool's result
- Generate an informed final response

#### 3. **Updated Prompt Template**

The prompt now clearly instructs the LLM:
```
- If you call a tool, set "Final Response" to "None" so the tool can execute.
- After receiving tool results, provide a "Final Response" with "Tool call" set to "None".
```

## Example Flow

### Query: "What is 25 + 37?"

**Iteration 1:**
```json
{
    "Tool call": "calculator",
    "Final Response": "None"
}
```
→ Final Response is "None", so loop continues
→ Calculator tool executes: returns "62.0"

**Iteration 2:**
Context becomes:
```
Original query: What is 25 + 37?

Tool 'calculator' returned: 62.0

Provide a final response to the user based on this information.
```

LLM responds:
```json
{
    "Tool call": "None",
    "Final Response": "The calculation result is 62.0."
}
```
→ Final Response is found, loop exits

## Safety Features

### Max Iterations
Default: 5 iterations
- Prevents infinite loops
- Configurable per request
- Returns accumulated results if limit reached

```python
agent.run("query", max_iterations=10)  # Allow up to 10 iterations
```

### Error Handling
- Tool execution errors stop the loop immediately
- Returns error message as final response
- Preserves partial results (tool calls/results so far)

## Benefits

1. **Multi-Step Reasoning**: Agent can execute tool → analyze result → respond
2. **Better Responses**: Uses actual tool results instead of generic messages
3. **Transparent**: All tool calls and results are tracked
4. **Flexible**: Supports complex workflows with multiple tool calls
5. **Safe**: Max iterations prevent runaway loops

## Usage Examples

### Basic Usage
```python
agent = ToolCall_Agent()
agent.add_llm(your_llm)
agent.add_PromptTemplate(prompt)
agent.add_tools({"calculator": calculator_func})

# Simple call - loops automatically
response = agent.run("What is 5 + 5?")
# Output: "The calculation result is 10.0"
```

### Advanced Usage
```python
# Get full details
result = agent.invoke("What is 5 + 5?", max_iterations=3)

print(f"Iterations: {result['iterations']}")
print(f"Tools: {result['tool_calls']}")
print(f"Results: {result['tool_results']}")
print(f"Response: {result['final_response']}")
```

### Verbose Output
```python
agent.run("What is 5 + 5?", verbose=True)
```

Output:
```
==================================================
User Query: What is 5 + 5?
==================================================
Iterations: 2
Tools Called: calculator
  Step 1 - calculator: 10.0
Final Response: The calculation result is 10.0.
==================================================
```

## Migration from Old Version

### Old API (Single Step)
```python
result = agent.invoke("query")
# Returns: {"tool_call": "calculator", "tool_result": "10", "final_response": "Tool executed successfully. Result: 10"}
```

### New API (Loop)
```python
result = agent.invoke("query")
# Returns: {"tool_calls": ["calculator"], "tool_results": ["10"], "final_response": "The result is 10", "iterations": 2}
```

**Key Differences:**
- `tool_call` (string) → `tool_calls` (list)
- `tool_result` (single) → `tool_results` (list)
- Added `iterations` field
- Final response is now LLM-generated, not generic

## Testing

Run the test file to see the loop in action:
```bash
python x:\agent\test_agent.py
```

This will demonstrate:
- Calculator query (2 iterations)
- Time query (2 iterations)  
- Simple greeting (1 iteration - no tool needed)

## Configuration

The loop behavior can be tuned:

```python
# Allow more iterations for complex tasks
agent.run(query, max_iterations=10)

# Disable verbose output
agent.run(query, verbose=False)

# Get raw result dictionary
result = agent.invoke(query, max_iterations=5)
```

## Future Enhancements

Possible improvements:
- Support for multiple tools in sequence
- Conversation history/memory
- Conditional tool chaining
- Parallel tool execution
- Tool validation before execution
