# Codemni-ToolCallAgent

An intelligent agent that can call tools based on LLM decisions. Built by **codexJitin** and powered by **Codemni**.

## Features

- 🤖 **Multi-LLM Support**: Built-in support for OpenAI, Anthropic, Groq, Google Gemini, and Ollama
- 🔧 **Tool Calling**: Easily add custom tools that the agent can intelligently use
- 🎨 **Verbose Mode**: Beautiful colored output for debugging and monitoring
- 📦 **Zero Dependencies**: Core package has no dependencies; install only the LLM providers you need
- 🚀 **Easy to Use**: Simple API for quick integration

## Installation

### Basic Installation
```bash
pip install Codemni-ToolCallAgent
```

### With Specific LLM Provider
```bash
# For OpenAI
pip install Codemni-ToolCallAgent[openai]

# For Anthropic Claude
pip install Codemni-ToolCallAgent[anthropic]

# For Groq
pip install Codemni-ToolCallAgent[groq]

# For Google Gemini
pip install Codemni-ToolCallAgent[google]

# For Ollama (local models)
pip install Codemni-ToolCallAgent[ollama]

# Install all providers
pip install Codemni-ToolCallAgent[all]
```

## Quick Start

```python
from ToolCall_Agent import ToolCallAgent

# Initialize agent with OpenAI
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-api-key',  # or set OPENAI_API_KEY env variable
    verbose=True
)

# Add a custom tool
def calculator(expression):
    """Evaluate a mathematical expression"""
    return eval(expression)

agent.add_tool(
    name="calculator",
    description="Evaluates mathematical expressions. Input should be a valid Python expression.",
    function=calculator
)

# Use the agent
response = agent.invoke("What is 125 multiplied by 48?")
print(response)
```

## Supported LLM Providers

### OpenAI
```python
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-api-key',
    temperature=0.7
)
```

Environment variable: `OPENAI_API_KEY`

### Anthropic Claude
```python
agent = ToolCallAgent(
    llm_provider='anthropic',
    model='claude-3-opus-20240229',
    api_key='your-api-key',
    temperature=0.7
)
```

Environment variable: `ANTHROPIC_API_KEY`

### Groq
```python
agent = ToolCallAgent(
    llm_provider='groq',
    model='llama3-70b-8192',
    api_key='your-api-key',
    temperature=0.7
)
```

Environment variable: `GROQ_API_KEY`

### Google Gemini
```python
agent = ToolCallAgent(
    llm_provider='google',
    model='gemini-pro',
    api_key='your-api-key',
    temperature=0.7
)
```

Environment variable: `GOOGLE_API_KEY`

### Ollama (Local Models)
```python
agent = ToolCallAgent(
    llm_provider='ollama',
    model='llama2',
    base_url='http://localhost:11434'  # optional
)
```

Environment variable: `OLLAMA_BASE_URL` (optional)

## Advanced Usage

### Adding Multiple Tools

```python
def search_web(query, num_results):
    """Search the web and return results"""
    # Your implementation here
    return f"Found {num_results} results for: {query}"

def get_weather(city):
    """Get weather information for a city"""
    # Your implementation here
    return f"Weather in {city}: Sunny, 25°C"

agent.add_tool("search", "Search the web. Takes query and number of results.", search_web)
agent.add_tool("weather", "Get weather for a city. Takes city name.", get_weather)

response = agent.invoke("What's the weather in New York?")
```

### Using Custom LLM

If you want to use a custom LLM implementation:

```python
class MyCustomLLM:
    def generate_response(self, prompt):
        # Your custom implementation
        return response

agent = ToolCallAgent()
agent.add_llm(MyCustomLLM())
```

## API Reference

### ToolCallAgent

#### `__init__(llm_provider=None, model=None, api_key=None, verbose=False, **llm_kwargs)`

Initialize the ToolCall Agent.

**Parameters:**
- `llm_provider` (str, optional): LLM provider name ('openai', 'anthropic', 'groq', 'google', 'ollama')
- `model` (str, optional): Model name
- `api_key` (str, optional): API key for the provider
- `verbose` (bool): Enable verbose logging with colors
- `**llm_kwargs`: Additional arguments to pass to the LLM client

#### `add_tool(name, description, function)`

Add a tool that the agent can use.

**Parameters:**
- `name` (str): Tool name
- `description` (str): Description of what the tool does
- `function` (callable): Function to execute when tool is called

#### `invoke(query)`

Execute the agent with a user query.

**Parameters:**
- `query` (str): User's question or request

**Returns:**
- `str`: Final response from the agent

#### `set_llm(provider, model, api_key=None, **kwargs)`

Set or change the LLM provider.

**Parameters:**
- `provider` (str): LLM provider name
- `model` (str): Model name
- `api_key` (str, optional): API key
- `**kwargs`: Additional LLM arguments

## Environment Variables

You can set API keys using environment variables:

```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
export OLLAMA_BASE_URL="http://localhost:11434"  # optional
```

## Examples

Check out the `examples/` directory for more usage examples:
- Basic tool usage
- Multiple tools
- Different LLM providers
- Custom tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Credits

Created by **CodexJitin**  
Powered by **Codemni**

## Support

For issues, questions, or contributions, please visit our [GitHub repository](https://github.com/Codexjitin/Codemni-ToolCallAgent).
