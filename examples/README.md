# Codemni-ToolCallAgent Examples

This directory contains examples demonstrating various features of the Codemni-ToolCallAgent.

## Examples

### 1. basic_usage.py
Basic usage example showing:
- How to initialize the agent
- Adding a simple calculator tool
- Making queries that use the tool

### 2. multiple_tools.py
Demonstrates using multiple tools together:
- Calculator
- Random number generator
- Word counter
- Temperature converter

### 3. different_llm_providers.py
Shows how to use different LLM providers:
- OpenAI GPT-4
- Anthropic Claude
- Groq
- Google Gemini
- Ollama (local)
- Switching between providers dynamically

## Running the Examples

Before running, make sure you have:

1. Installed the package:
```bash
pip install Codemni-ToolCallAgent[all]
```

Or install specific providers:
```bash
pip install Codemni-ToolCallAgent[openai]
```

2. Set your API keys as environment variables:
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

3. Run an example:
```bash
python basic_usage.py
```

## Creating Your Own Tools

Tools are simple Python functions that the agent can call. Here's a template:

```python
def my_tool(param1, param2):
    """Description of what this tool does"""
    # Your implementation
    return result

agent.add_tool(
    name="my_tool",
    description="Clear description for the LLM",
    function=my_tool
)
```

The agent will automatically:
- Decide when to use the tool based on the query
- Extract and pass the correct parameters
- Use the tool's result to formulate a response
