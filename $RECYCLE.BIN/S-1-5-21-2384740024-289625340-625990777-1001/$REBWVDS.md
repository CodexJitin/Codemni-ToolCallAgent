# Refactored Multi-Agent System Architecture

## Overview

This refactored architecture separates common logic into reusable components, making it easy to build multiple agents that share functionality.

## Architecture

```
agent/
├── core/                       # Reusable core components
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base class for all agents
│   ├── llm_interface.py       # Abstract LLM interface
│   ├── tool_executor.py       # Tool registration and execution
│   ├── response_parser.py     # Response parsing utilities
│   └── colors.py              # Terminal color utilities
│
├── adapters/                   # LLM provider adapters
│   ├── __init__.py
│   ├── gemini_adapter.py      # Google Gemini implementation
│   └── openai_adapter.py      # OpenAI implementation (template)
│
└── ToolCall_Agent/            # Specific agent implementations
    ├── __init__.py
    ├── agent.py               # Original agent (still works)
    ├── refactored_agent.py    # New modular version
    └── prompt.py              # Agent-specific prompt
```

## Key Components

### 1. **BaseAgent** (`core/base_agent.py`)
Abstract base class providing common functionality:
- Tool management
- LLM interface
- Logging utilities
- Configuration management
- Validation

All agents should inherit from this class.

### 2. **LLMInterface** (`core/llm_interface.py`)
Abstract interface for LLM providers:
- `generate_response()` - Standard generation
- `generate_streaming_response()` - Streaming generation
- `get_model_info()` - Model information

Implement this to add new LLM providers.

### 3. **ToolExecutor** (`core/tool_executor.py`)
Manages tool registration and execution:
- `register_tool()` - Add new tools
- `execute()` - Run tools with parameters
- `list_tools()` - Get available tools
- `validate_parameters()` - Validate tool inputs

### 4. **ResponseParser** (`core/response_parser.py`)
Handles parsing of LLM responses:
- `parse_json_response()` - Extract and parse JSON
- `parse_tool_call_response()` - Parse tool call format
- `extract_code_blocks()` - Extract code from markdown
- `parse_key_value_pairs()` - Parse structured data

### 5. **Colors** (`core/colors.py`)
Terminal output utilities:
- Color codes for different message types
- Helper methods for formatted output
- Cross-platform color support

## Usage

### Creating a New Agent

```python
from agent.core.base_agent import BaseAgent
from agent.adapters.gemini_adapter import GeminiLLM

class MyCustomAgent(BaseAgent):
    def __init__(self, verbose=False):
        super().__init__(name="MyAgent", verbose=verbose)
        self.prompt_template = "Your custom prompt here"
    
    def _compile_prompt(self) -> str:
        # Compile your prompt with tools
        tool_list = self.get_tools_description()
        return self.prompt_template.replace("{tools}", tool_list)
    
    def invoke(self, query: str, **kwargs) -> str:
        # Implement your agent logic
        is_valid, error = self.validate_setup()
        if not is_valid:
            raise ValueError(error)
        
        # Your implementation here
        pass

# Use the agent
llm = GeminiLLM()
agent = MyCustomAgent(verbose=True)
agent.set_llm(llm)
agent.add_tool("calculator", "Calculate math", calculator_func)
result = agent.invoke("What is 2 + 2?")
```

### Using the Refactored ToolCall Agent

```python
from agent.ToolCall_Agent.refactored_agent import ToolCallAgent
from agent.adapters.gemini_adapter import GeminiLLM

# Initialize
llm = GeminiLLM()
agent = ToolCallAgent(verbose=True)
agent.set_llm(llm)

# Add tools
agent.add_tool("calculator", "Calculate expressions", calculator)
agent.add_tool("weather", "Get weather data", get_weather)

# Execute
result = agent.invoke("What is 25 * 8 and what's the weather in Paris?")
```

### Adding a New LLM Provider

```python
from agent.core.llm_interface import LLMInterface

class CustomLLM(LLMInterface):
    def __init__(self, model_name="custom-model", **kwargs):
        super().__init__(model_name, **kwargs)
        # Initialize your LLM client
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        # Implement response generation
        pass
    
    def generate_streaming_response(self, prompt: str, **kwargs):
        # Implement streaming generation
        pass
```

## Benefits of Refactored Architecture

### 1. **Reusability**
- Core components can be shared across multiple agents
- No code duplication
- Easier maintenance

### 2. **Extensibility**
- Easy to add new agents by inheriting from `BaseAgent`
- Easy to add new LLM providers by implementing `LLMInterface`
- Easy to add new parsers or executors

### 3. **Testability**
- Each component can be tested independently
- Mock objects for testing
- Clear interfaces

### 4. **Separation of Concerns**
- LLM logic separated from agent logic
- Tool execution separated from agent logic
- Response parsing separated from execution

### 5. **Multi-Agent Ready**
- Multiple agents can share the same tools
- Agents can communicate through shared interfaces
- Easy to orchestrate multiple agents

## Running the Demo

### Original Agent
```bash
python demo.py
```

### Refactored Agent
```bash
python demo_refactored.py
```

Both should produce the same results, but the refactored version uses modular components.

## Migration Guide

To migrate existing code:

1. Replace direct imports:
   ```python
   # Old
   from agent.ToolCall_Agent.agent import ToolCallAgent
   
   # New
   from agent.ToolCall_Agent.refactored_agent import ToolCallAgent
   ```

2. Update LLM initialization:
   ```python
   # Old
   llm = GeminiLLM()
   agent.add_llm(llm)
   
   # New
   from agent.adapters.gemini_adapter import GeminiLLM
   llm = GeminiLLM()
   agent.set_llm(llm)
   ```

3. Everything else remains the same!

## Building Multi-Agent Systems

With this architecture, you can easily build:

1. **Specialized Agents**: Create agents for specific domains
2. **Agent Pipelines**: Chain multiple agents together
3. **Collaborative Agents**: Agents that share tools and communicate
4. **Hierarchical Agents**: Parent agents that coordinate child agents

Example multi-agent system:
```python
# Specialized agents
research_agent = ResearchAgent(verbose=True)
coding_agent = CodingAgent(verbose=True)
review_agent = ReviewAgent(verbose=True)

# Shared LLM
llm = GeminiLLM()
for agent in [research_agent, coding_agent, review_agent]:
    agent.set_llm(llm)

# Shared tools
for agent in [research_agent, coding_agent]:
    agent.add_tool("search", "Search web", search_func)

# Execute pipeline
research = research_agent.invoke("Research Python async programming")
code = coding_agent.invoke(f"Write code based on: {research}")
review = review_agent.invoke(f"Review this code: {code}")
```

## Next Steps

1. Create specialized agents for your use case
2. Implement additional LLM adapters (OpenAI, Anthropic, etc.)
3. Add more response parsers for different formats
4. Build agent orchestration layer
5. Add agent-to-agent communication

---

**Created by:** codexJitin  
**Powered by:** Codemni  
**License:** MIT
