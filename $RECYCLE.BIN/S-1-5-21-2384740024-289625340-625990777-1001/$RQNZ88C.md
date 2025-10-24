# ToolCall_Agent

An intelligent agent that can invoke tools based on user queries using a Language Model (LLM).

## Features

- **Flexible Tool Integration**: Add any custom tools as Python functions
- **LLM-Powered Decision Making**: Uses an LLM to determine which tool to invoke
- **Clean JSON Response Format**: Structured responses with tool calls and final answers
- **Method Chaining**: Fluent API for easy configuration
- **Error Handling**: Robust error handling for tool execution and LLM parsing

## Installation

No external dependencies are required for the basic agent. However, you'll need an LLM provider:

```bash
# For OpenAI
pip install openai langchain-openai

# For Anthropic
pip install anthropic langchain-anthropic

# For local models
pip install ollama langchain-ollama
```

## Quick Start

### 1. Define Your Tools

Tools are simple Python functions with docstrings:

```python
def calculator(query: str) -> str:
    """Performs basic arithmetic calculations. Use for math operations."""
    # Your implementation here
    return result

def search_weather(query: str) -> str:
    """Searches for weather information for a given location."""
    # Your implementation here
    return weather_info
```

### 2. Set Up the Agent

```python
from agent import ToolCall_Agent
from prompt import prompt

# Initialize the agent
agent = ToolCall_Agent()

# Configure with LLM, prompt, and tools
agent.add_llm(your_llm_instance)
agent.add_PromptTemplate(prompt)
agent.add_tools({
    "calculator": calculator,
    "search_weather": search_weather
})
```

### 3. Use the Agent

```python
# Simple usage
response = agent.run("What is 25 + 37?", verbose=True)
print(response)

# Advanced usage with full result
result = agent.invoke("What's the weather like?")
print(result['tool_call'])      # The tool that was called
print(result['tool_result'])    # The result from the tool
print(result['final_response']) # The final response to user
```

## Using with Real LLMs

### OpenAI

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key="your-api-key"
)

agent.add_llm(llm)
```

### Anthropic

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    api_key="your-api-key"
)

agent.add_llm(llm)
```

### Ollama (Local)

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama2",
    temperature=0
)

agent.add_llm(llm)
```

## API Reference

### ToolCall_Agent

#### Methods

- **`add_llm(llm)`**: Add a language model to the agent
  - **Args**: `llm` - An LLM instance with `invoke()`, `generate()`, `chat()`, or `__call__()` method
  - **Returns**: Self for method chaining

- **`add_PromptTemplate(prompt_template)`**: Add a prompt template
  - **Args**: `prompt_template` - String with `{tool_list}` and `{user_input}` placeholders
  - **Returns**: Self for method chaining

- **`add_tools(tools)`**: Add tools the agent can use
  - **Args**: `tools` - Dictionary mapping tool names to callable functions
  - **Returns**: Self for method chaining

- **`invoke(user_input)`**: Process a query and invoke tools
  - **Args**: `user_input` - The user's query string
  - **Returns**: Dictionary with `tool_call`, `tool_result`, and `final_response`

- **`run(user_input, verbose=True)`**: Convenience method returning just the final response
  - **Args**: 
    - `user_input` - The user's query string
    - `verbose` - Whether to print detailed execution info
  - **Returns**: The final response string

## Prompt Format

The agent expects a specific JSON response format from the LLM:

```json
{
    "Tool call": "tool_name or None",
    "Final Response": "response text or None"
}
```

The provided prompt template in `prompt.py` is designed to elicit this format.

## Example

See `example.py` for a complete working example with multiple tools.

```bash
python example.py
```

## Error Handling

The agent handles various error scenarios:

- **Invalid JSON from LLM**: Falls back to error response
- **Tool execution errors**: Catches exceptions and returns error message
- **Missing configuration**: Raises ValueError with clear instructions

## Contributing

Feel free to extend the agent with:
- Additional tool types
- Enhanced error handling
- Logging capabilities
- Conversation history/memory
- Multi-turn interactions

## License

MIT License - feel free to use and modify as needed.

## Credits

Developed by the Codemni Team
