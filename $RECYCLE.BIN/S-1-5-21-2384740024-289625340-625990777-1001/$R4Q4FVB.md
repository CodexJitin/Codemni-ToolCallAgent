# Architecture Overview

## Visual Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐              ┌──────▼───────┐
        │  CoordinatorAgent│              │ Other Agents │
        │  (Orchestrator)  │              │              │
        └───────┬────────┘              └──────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼────┐  ┌──▼─────┐  ┌─▼────────┐
│  Math  │  │Research│  │  Coding  │
│ Agent  │  │ Agent  │  │  Agent   │
└───┬────┘  └──┬─────┘  └─┬────────┘
    │          │           │
    └──────────┼───────────┘
               │
        ┌──────▼─────────┐
        │   BASE AGENT   │  ← All agents inherit from this
        │  (Abstract)    │
        └──────┬─────────┘
               │
    ┌──────────┼──────────────┬──────────────┐
    │          │              │              │
┌───▼────┐ ┌──▼──────┐ ┌────▼────┐ ┌───────▼────────┐
│  Tool  │ │Response │ │   LLM   │ │     Colors     │
│Executor│ │ Parser  │ │Interface│ │   Utilities    │
└────────┘ └─────────┘ └────┬────┘ └────────────────┘
                             │
                  ┌──────────┼──────────┐
                  │          │          │
              ┌───▼───┐  ┌───▼────┐ ┌──▼────────┐
              │Gemini │  │OpenAI  │ │ Anthropic │
              │Adapter│  │Adapter │ │  Adapter  │
              └───────┘  └────────┘ └───────────┘
```

## Component Interaction Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│      Coordinator Agent              │
│  (Routes to specialized agents)     │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│  Math Agent  │    │Research Agent│
│              │    │              │
│ Uses:        │    │ Uses:        │
│ - BaseAgent  │    │ - BaseAgent  │
│ - Tools      │    │ - Tools      │
│ - LLM        │    │ - LLM        │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 │
        ┌────────▼────────┐
        │   Tool Executor │
        │   Execute Tool  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  LLM Interface  │
        │  Generate Text  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │Response Parser  │
        │  Parse Output   │
        └────────┬────────┘
                 │
                 ▼
            Final Result
```

## Data Flow Example

```
Query: "Calculate 25 * 8 and search for Python tutorials"
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ Step 1: Coordinator analyzes query                  │
│ - Detects: math + research needed                   │
│ - Decision: Route to MathAgent first                │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 2: MathAgent processes "25 * 8"                │
│ - Compiles prompt with tools                        │
│ - Sends to LLM                                      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 3: LLM responds with tool call                 │
│ {                                                   │
│   "Tool call": "calculator",                        │
│   "Tool Parameters": {"25 * 8"},                    │
│   "Final Response": "None"                          │
│ }                                                   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 4: ToolExecutor runs calculator("25 * 8")      │
│ Result: "200"                                       │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 5: Result fed back to LLM                      │
│ Scratchpad: "Tool: calculator, Result: 200"         │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 6: LLM provides final response                 │
│ {                                                   │
│   "Tool call": "None",                              │
│   "Tool Parameters": "None",                        │
│   "Final Response": "25 * 8 = 200"                  │
│ }                                                   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 7: Coordinator routes to ResearchAgent         │
│ Query: "Search for Python tutorials"                │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 8: ResearchAgent uses search tool              │
│ Returns: Search results                             │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Step 9: Final combined response                     │
│ "25 * 8 = 200. Here are Python tutorials..."       │
└─────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
LLMInterface (Abstract)
    ├── GeminiLLM (Concrete)
    ├── OpenAILLM (Concrete)
    └── AnthropicLLM (Future)

BaseAgent (Abstract)
    ├── ToolCallAgent (Concrete)
    ├── MathAgent (Concrete)
    ├── ResearchAgent (Concrete)
    ├── CoordinatorAgent (Concrete)
    └── YourCustomAgent (Your implementation)

ToolExecutor (Concrete - Reusable)
    └── Used by all agents

ResponseParser (Concrete - Reusable)
    └── Used by all agents

Colors (Utility - Reusable)
    └── Used by all agents
```

## File Dependencies

```
demo_refactored.py
    ├── agent.ToolCall_Agent.refactored_agent
    │   ├── agent.core.base_agent
    │   │   ├── agent.core.tool_executor
    │   │   ├── agent.core.response_parser
    │   │   └── agent.core.llm_interface
    │   └── agent.core.colors
    └── agent.adapters.gemini_adapter
        └── agent.core.llm_interface

multi_agent_demo.py
    ├── agent.core.base_agent
    │   ├── agent.core.tool_executor
    │   ├── agent.core.response_parser
    │   └── agent.core.llm_interface
    ├── agent.adapters.gemini_adapter
    └── agent.core.colors
```

## Key Design Patterns Used

### 1. **Abstract Factory Pattern**
```
LLMInterface → Defines interface
GeminiLLM, OpenAILLM → Concrete implementations
```

### 2. **Template Method Pattern**
```
BaseAgent defines structure
Subclasses implement specific methods:
  - _compile_prompt()
  - invoke()
```

### 3. **Strategy Pattern**
```
Different agents = Different strategies
Coordinator selects strategy based on query
```

### 4. **Composition Pattern**
```
BaseAgent contains:
  - ToolExecutor (has-a)
  - ResponseParser (has-a)
  - LLMInterface (has-a)
```

### 5. **Dependency Injection**
```
agent.set_llm(llm)  ← LLM injected into agent
coordinator = CoordinatorAgent(agents={...})  ← Agents injected
```

## Extension Points

### Add New Agent Type
```python
class MyAgent(BaseAgent):
    def _compile_prompt(self):
        # Your prompt logic
        
    def invoke(self, query):
        # Your execution logic
```

### Add New LLM Provider
```python
class MyLLM(LLMInterface):
    def generate_response(self, prompt):
        # Your API call
```

### Add New Tool
```python
def my_tool(param1, param2):
    # Your tool logic
    return result

agent.add_tool("my_tool", "Description", my_tool)
```

### Add Agent Communication
```python
class TeamAgent(BaseAgent):
    def __init__(self, team_members):
        super().__init__("Team")
        self.members = team_members
    
    def invoke(self, query):
        results = []
        for member in self.members:
            results.append(member.invoke(query))
        return self.synthesize(results)
```

---

**Created by:** codexJitin  
**Powered by:** Codemni
