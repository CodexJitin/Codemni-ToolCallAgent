# ToolCall Agent 🤖

An intelligent agent that can call tools based on LLM decisions with **built-in LLM initialization** for popular providers.

Created by: **codexJitin**  
Powered by: **Codemni**

## ✨ Features

- 🎯 **Built-in LLM Support** - No need to write separate initialization code
- 🔌 **Multi-Provider** - Supports OpenAI, Anthropic, Groq, Google, and Ollama
- 🛠️ **Easy Tool Integration** - Simple API to add custom tools
- 📊 **Verbose Mode** - Beautiful colored output for debugging
- 🔐 **Environment Variables** - Secure API key management
- 🎨 **Clean API** - Simple and intuitive interface

## 🚀 Quick Start

### Installation

```bash
# Install the agent (from your package)
pip install ToolCall-Agent

# Install your preferred LLM provider
pip install openai          # For OpenAI
pip install anthropic       # For Anthropic Claude
pip install groq            # For Groq
pip install google-generativeai  # For Google Gemini
pip install ollama          # For Ollama (local)
```

### Basic Usage

```python
from ToolCall_Agent import ToolCallAgent

# Define a tool
def calculator(expression):
    return f"Result: {eval(expression)}"

# Create agent with built-in LLM initialization
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-api-key-here',
    temperature=0.7,
    verbose=True
)

# Add tool
agent.add_tool("calculator", "Evaluate mathematical expressions", calculator)

# Run query
response = agent.invoke("What is 125 * 48?")
print(response)
```

That's it! No separate LLM initialization code needed! 🎉

## 📖 Supported LLM Providers

### 1. OpenAI

```python
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',  # or 'gpt-3.5-turbo', 'gpt-4-turbo'
    api_key='sk-...',
    temperature=0.7
)
```

**Environment Variable:** `OPENAI_API_KEY`

### 2. Anthropic (Claude)

```python
agent = ToolCallAgent(
    llm_provider='anthropic',
    model='claude-3-opus-20240229',  # or 'claude-3-sonnet-20240229'
    api_key='sk-ant-...',
    max_tokens=4096
)
```

**Environment Variable:** `ANTHROPIC_API_KEY`

### 3. Groq

```python
agent = ToolCallAgent(
    llm_provider='groq',
    model='llama3-70b-8192',  # or 'mixtral-8x7b-32768'
    api_key='gsk_...',
    temperature=0.5
)
```

**Environment Variable:** `GROQ_API_KEY`

### 4. Google Gemini

```python
agent = ToolCallAgent(
    llm_provider='google',
    model='gemini-pro',  # or 'gemini-1.5-pro'
    api_key='AI...'
)
```

**Environment Variable:** `GOOGLE_API_KEY`

### 5. Ollama (Local Models)

```python
agent = ToolCallAgent(
    llm_provider='ollama',
    model='llama2',  # or 'mistral', 'codellama'
    base_url='http://localhost:11434'  # optional
)
```

**Environment Variable:** `OLLAMA_BASE_URL` (optional)

## 🔧 Initialization Methods

### Method 1: Constructor (Recommended)

```python
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-key',
    temperature=0.7
)
```

### Method 2: set_llm() Method

```python
agent = ToolCallAgent()
agent.set_llm('openai', 'gpt-4', api_key='your-key')
```

### Method 3: Environment Variables (Most Secure)

```bash
# Set environment variable
export OPENAI_API_KEY="your-key-here"  # Linux/Mac
# or
$env:OPENAI_API_KEY="your-key-here"    # Windows PowerShell
```

```python
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4'
    # api_key will be read from environment
)
```

### Method 4: Custom LLM (Advanced)

```python
class MyCustomLLM:
    def generate_response(self, prompt):
        # Your implementation
        return "response"

agent = ToolCallAgent()
agent.add_llm(MyCustomLLM())
```

## 🛠️ Adding Tools

Tools are functions that the agent can call to perform tasks:

```python
def calculator(expression):
    """Evaluate a mathematical expression."""
    return f"Result: {eval(expression)}"

def get_weather(city):
    """Get weather for a city."""
    # Your implementation
    return f"Weather in {city}: Sunny, 72°F"

def search_web(query):
    """Search the web."""
    # Your implementation
    return f"Search results for: {query}"

# Add tools to agent
agent.add_tool("calculator", "Evaluate math expressions", calculator)
agent.add_tool("get_weather", "Get weather info", get_weather)
agent.add_tool("search_web", "Search the web", search_web)
```

## 📝 Complete Example

```python
from ToolCall_Agent import ToolCallAgent

# Define tools
def calculator(expression):
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(city):
    return f"Weather in {city}: Sunny, 72°F"

# Initialize agent with built-in LLM
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-api-key',
    temperature=0.7,
    verbose=True  # Enable beautiful colored output
)

# Add tools
agent.add_tool(
    name="calculator",
    description="Evaluate mathematical expressions",
    function=calculator
)

agent.add_tool(
    name="get_weather",
    description="Get weather information for a city",
    function=get_weather
)

# Run queries
print(agent.invoke("What is 125 * 48?"))
print(agent.invoke("What's the weather in New York?"))
print(agent.invoke("Calculate 100 + 200, then tell me the weather in London"))
```

## 🎨 Verbose Mode

Enable verbose mode to see the agent's decision-making process:

```python
agent = ToolCallAgent(verbose=True, ...)
```

Output includes:
- 🔧 Tool calls
- 📝 Parameters
- 📤 Results
- ✓ Final responses

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for production
3. **Use .env files** with python-dotenv:

```python
from dotenv import load_dotenv
load_dotenv()

agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4'
    # api_key read from .env file
)
```

## 📚 API Reference

### ToolCallAgent

#### Constructor

```python
ToolCallAgent(
    llm_provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    verbose: bool = False,
    **llm_kwargs
)
```

#### Methods

- `set_llm(provider, model, api_key=None, **kwargs)` - Initialize LLM
- `add_llm(llm)` - Add custom LLM instance
- `add_tool(name, description, function)` - Add a tool
- `invoke(query)` - Execute agent with query

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Your License Here]

## 👤 Author

**codexJitin**  
Powered by **Codemni**

## 🙏 Acknowledgments

Thanks to all the LLM providers for their amazing APIs!

---

Made with ❤️ by codexJitin | Powered by Codemni
