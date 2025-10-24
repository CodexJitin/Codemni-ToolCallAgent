# Multi-Agent System - Quick Start Guide

## What Was Created

Your codebase has been refactored into a modular, reusable architecture perfect for building multi-agent systems!

## New Structure

```
x:\
├── agent/
│   ├── core/                    # ⭐ Reusable Components
│   │   ├── base_agent.py        # Base class for all agents
│   │   ├── llm_interface.py     # Abstract LLM interface
│   │   ├── tool_executor.py     # Tool management
│   │   ├── response_parser.py   # Response parsing
│   │   └── colors.py            # Terminal colors
│   │
│   ├── adapters/                # ⭐ LLM Adapters
│   │   ├── gemini_adapter.py    # Gemini implementation
│   │   └── openai_adapter.py    # OpenAI template
│   │
│   └── ToolCall_Agent/
│       ├── agent.py             # Original (still works)
│       ├── refactored_agent.py  # New modular version
│       └── prompt.py
│
├── demo.py                      # Original demo
├── demo_refactored.py           # ⭐ Refactored demo
├── multi_agent_demo.py          # ⭐ Multi-agent example
├── test.py
├── test_report.md
├── README_REFACTORED.md         # ⭐ Full documentation
└── QUICKSTART.md                # This file
```

## Quick Test

### 1. Test the Refactored Agent
```bash
python demo_refactored.py
```

### 2. Test Multi-Agent System
```bash
python multi_agent_demo.py
```

## Core Components

### 1. BaseAgent (Foundation for all agents)
```python
from agent.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, verbose=False):
        super().__init__(name="MyAgent", verbose=verbose)
        # Your initialization
    
    def _compile_prompt(self):
        # Build your prompt
        pass
    
    def invoke(self, query):
        # Your logic
        pass
```

### 2. LLM Adapters (Easy provider switching)
```python
from agent.adapters.gemini_adapter import GeminiLLM

llm = GeminiLLM()  # Auto-reads GOOGLE_API_KEY
agent.set_llm(llm)
```

### 3. Tool Executor (Shared across agents)
```python
agent.add_tool(
    name="calculator",
    description="Calculate math expressions",
    function=calculator_func
)
```

### 4. Response Parser (Reusable parsing)
```python
from agent.core.response_parser import ResponseParser

parser = ResponseParser()
data = parser.parse_json_response(response)
```

## Building Multiple Agents

### Example: Three Specialized Agents

```python
from agent.core.base_agent import BaseAgent
from agent.adapters.gemini_adapter import GeminiLLM

# Shared LLM
llm = GeminiLLM()

# Agent 1: Math specialist
math_agent = MathAgent(verbose=True)
math_agent.set_llm(llm)
math_agent.add_tool("calculator", "Calculate", calc_func)

# Agent 2: Research specialist
research_agent = ResearchAgent(verbose=True)
research_agent.set_llm(llm)
research_agent.add_tool("search", "Search web", search_func)

# Agent 3: Coordinator
coordinator = CoordinatorAgent(
    agents={'math': math_agent, 'research': research_agent},
    verbose=True
)

# Use coordinator to route queries
result = coordinator.invoke("What is 25 * 8?")  # Routes to math_agent
result = coordinator.invoke("Search Python")    # Routes to research_agent
```

## Benefits

✅ **No Code Duplication** - Shared components across all agents  
✅ **Easy to Extend** - Add new agents by inheriting BaseAgent  
✅ **LLM Flexibility** - Swap LLMs without changing agent code  
✅ **Tool Sharing** - Multiple agents can use the same tools  
✅ **Clean Separation** - Each component has a single responsibility  
✅ **Production Ready** - Robust error handling and validation  

## Next Steps

### 1. Create Your Custom Agent
```python
class MySpecializedAgent(BaseAgent):
    def __init__(self, verbose=False):
        super().__init__(name="SpecializedAgent", verbose=verbose)
        self.prompt_template = "Your prompt here with {tool_list} and {user_input}"
    
    def _compile_prompt(self):
        return self.prompt_template.replace("{tool_list}", self.get_tools_description())
    
    def invoke(self, query, **kwargs):
        # Implement your agent logic
        # See refactored_agent.py for example
        pass
```

### 2. Add New LLM Provider
```python
from agent.core.llm_interface import LLMInterface

class AnthropicLLM(LLMInterface):
    def __init__(self, model_name="claude-3", **kwargs):
        super().__init__(model_name, **kwargs)
        # Initialize Anthropic client
    
    def generate_response(self, prompt, **kwargs):
        # Implement Anthropic API call
        pass
```

### 3. Build Agent Pipeline
```python
# Chain multiple agents together
research_result = research_agent.invoke("Research Python async")
code_result = coding_agent.invoke(f"Write code: {research_result}")
review_result = review_agent.invoke(f"Review: {code_result}")
```

### 4. Create Agent Hierarchy
```python
# Parent agent coordinates child agents
supervisor = SupervisorAgent()
supervisor.add_worker(math_agent)
supervisor.add_worker(research_agent)
supervisor.add_worker(coding_agent)

result = supervisor.invoke("Complex multi-step task")
```

## Common Patterns

### Pattern 1: Shared Tools
```python
# Define tools once, share across agents
def search(query):
    return "Results..."

agent1.add_tool("search", "Search web", search)
agent2.add_tool("search", "Search web", search)
agent3.add_tool("search", "Search web", search)
```

### Pattern 2: Agent Communication
```python
class CollaborativeAgent(BaseAgent):
    def __init__(self, partner_agent, verbose=False):
        super().__init__("Collaborative", verbose)
        self.partner = partner_agent
    
    def invoke(self, query):
        # Work with partner agent
        partner_result = self.partner.invoke("Sub-query")
        # Use partner's result
        return self.process(partner_result)
```

### Pattern 3: Specialized Agent Factory
```python
def create_agent(agent_type, llm, tools):
    """Factory for creating specialized agents."""
    agent_classes = {
        'math': MathAgent,
        'research': ResearchAgent,
        'coding': CodingAgent
    }
    
    agent = agent_classes[agent_type](verbose=True)
    agent.set_llm(llm)
    
    for tool in tools:
        agent.add_tool(**tool)
    
    return agent
```

## Troubleshooting

### Import Errors
If you see import errors, make sure you're running from the project root:
```bash
cd x:\
python demo_refactored.py
```

### Missing Dependencies
```bash
pip install google-generativeai
```

### Environment Variables
Make sure GOOGLE_API_KEY is set:
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-key-here"

# Or add to system environment variables
```

## Examples Included

1. **demo_refactored.py** - Refactored version of original demo
2. **multi_agent_demo.py** - Multiple specialized agents working together
3. **README_REFACTORED.md** - Comprehensive documentation

## Support

Created by: **codexJitin**  
Powered by: **Codemni**

For more details, see `README_REFACTORED.md`

---

**You're all set! Start building your multi-agent system! 🚀**
