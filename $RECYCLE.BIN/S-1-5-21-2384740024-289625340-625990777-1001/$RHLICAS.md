# 🎭 Flexible Agents Guide

## What This Solves

You want to create **multiple different agent types** with:
- ✅ Different prompts
- ✅ Different JSON response structures
- ✅ Different reasoning styles
- ✅ But **without rewriting the same code** over and over

## The Solution: Configuration-Driven Agents

Instead of creating a new class for each agent type, just **change the configuration**!

---

## Quick Example

### Old Way (Lots of Code Duplication) ❌
```python
class ToolCallAgent(BaseAgent):
    # 200 lines of code
    pass

class ActionAgent(BaseAgent):
    # 200 lines of nearly identical code
    pass

class ReActAgent(BaseAgent):
    # 200 lines of nearly identical code
    pass
```

### New Way (Configuration Only) ✅
```python
# Define configs (just data, no code)
toolcall_config = AgentConfig(...)
action_config = AgentConfig(...)
react_config = AgentConfig(...)

# Use same agent class
agent1 = FlexibleAgent(toolcall_config)
agent2 = FlexibleAgent(action_config)
agent3 = FlexibleAgent(react_config)
```

---

## How It Works

### 1. Define Your Response Format

```python
from agent.core.agent_config import create_custom_config

# What JSON keys do you want?
config = create_custom_config(
    name="MyAgent",
    prompt_template="""
Your custom prompt here.
JSON format:
    "my_key1" — description
    "my_key2" — description
    "my_key3" — description
    
Tools: {tool_list}
Query: {user_input}
""",
    required_keys=["my_key1", "my_key2", "my_key3"],
    key_mapping={
        "tool": "my_key1",      # Which key contains tool name?
        "params": "my_key2",    # Which key contains parameters?
        "response": "my_key3"   # Which key contains final answer?
    }
)
```

### 2. Create Agent from Config

```python
from agent.core.flexible_agent import FlexibleAgent
from agent.adapters.gemini_adapter import GeminiLLM

llm = GeminiLLM()
agent = FlexibleAgent(config, verbose=True)
agent.set_llm(llm)
agent.add_tool("calculator", "Calculate", calculator_func)

result = agent.invoke("What is 2 + 2?")
```

That's it! 🎉

---

## Predefined Agent Types

We've included 5 ready-to-use agent configurations:

### 1. ToolCall Agent (Your Original)
```python
agent = FlexibleAgent.from_config_name("toolcall", verbose=True)
```
**JSON Format:**
```json
{
    "Tool call": "calculator",
    "Tool Parameters": {"25 * 8"},
    "Final Response": "None"
}
```

### 2. Action Agent (Simpler)
```python
agent = FlexibleAgent.from_config_name("action", verbose=True)
```
**JSON Format:**
```json
{
    "action": "calculator",
    "input": "25 * 8",
    "output": "pending"
}
```

### 3. ReACT Agent (With Reasoning)
```python
agent = FlexibleAgent.from_config_name("react", verbose=True)
```
**JSON Format:**
```json
{
    "thought": "I need to calculate 25 * 8",
    "action": "calculator",
    "action_input": "25 * 8",
    "answer": "None"
}
```

### 4. Function Agent (Minimalist)
```python
agent = FlexibleAgent.from_config_name("function", verbose=True)
```
**JSON Format:**
```json
{
    "function": "calculator",
    "args": "25 * 8",
    "result": null
}
```

### 5. Chain of Thought Agent
```python
agent = FlexibleAgent.from_config_name("cot", verbose=True)
```
**JSON Format:**
```json
{
    "reasoning_steps": ["Step 1...", "Step 2..."],
    "tool_needed": "calculator",
    "tool_args": "25 * 8",
    "final_answer": "None"
}
```

---

## Creating Your Own Agent Type

### Step-by-Step

#### 1. Design Your JSON Structure
```python
# What keys do you want in the response?
my_keys = ["thinking", "execute", "inputs", "result"]
```

#### 2. Write Your Prompt
```python
my_prompt = """
You are my custom agent.
Respond in JSON with these keys:
    "thinking" — your reasoning
    "execute" — tool to use or "None"
    "inputs" — tool parameters
    "result" — final answer or "None"

Tools available:
{tool_list}

User query: {user_input}
"""
```

#### 3. Map Keys to Internal Names
```python
# Tell the system which key does what
key_mapping = {
    "tool": "execute",      # "execute" is your tool name key
    "params": "inputs",     # "inputs" is your parameters key
    "response": "result",   # "result" is your final answer key
    "reasoning": "thinking" # "thinking" is your reasoning key (optional)
}
```

#### 4. Create Config
```python
from agent.core.agent_config import create_custom_config

config = create_custom_config(
    name="MyCustomAgent",
    prompt_template=my_prompt,
    required_keys=my_keys,
    key_mapping=key_mapping,
    description="My custom agent type",
    max_iterations=10
)
```

#### 5. Use It!
```python
from agent.core.flexible_agent import FlexibleAgent
from agent.adapters.gemini_adapter import GeminiLLM

llm = GeminiLLM()
agent = FlexibleAgent(config, verbose=True)
agent.set_llm(llm)

# Add your tools
agent.add_tool("calculator", "Calculate math", calculator)
agent.add_tool("search", "Search web", web_search)

# Run it
result = agent.invoke("What is 25 * 8?")
```

---

## Complete Example

```python
from agent.core.flexible_agent import FlexibleAgent
from agent.core.agent_config import create_custom_config
from agent.adapters.gemini_adapter import GeminiLLM

# 1. Define tools
def calculator(expression):
    return str(eval(expression))

# 2. Create custom config
my_config = create_custom_config(
    name="PlanExecuteAgent",
    description="Agent that plans then executes",
    prompt_template="""
You are a planning agent.
JSON format:
    "plan" — your plan
    "tool" — tool to use or null
    "args" — tool arguments
    "answer" — final answer or null

Tools: {tool_list}
Query: {user_input}
""",
    required_keys=["plan", "tool", "args", "answer"],
    key_mapping={
        "tool": "tool",
        "params": "args",
        "response": "answer",
        "reasoning": "plan"
    }
)

# 3. Create agent
llm = GeminiLLM()
agent = FlexibleAgent(my_config, verbose=True)
agent.set_llm(llm)
agent.add_tool("calculator", "Calculate expressions", calculator)

# 4. Use it
result = agent.invoke("What is 456 * 789?")
print(result)
```

---

## Benefits

### ✅ No Code Duplication
- Write agent logic **once**
- Create unlimited agent types
- Just change configuration

### ✅ Easy Experimentation
```python
# Try different prompts instantly
config1 = create_custom_config(name="v1", prompt_template=prompt1, ...)
config2 = create_custom_config(name="v2", prompt_template=prompt2, ...)

agent1 = FlexibleAgent(config1)
agent2 = FlexibleAgent(config2)

# Compare results
result1 = agent1.invoke(query)
result2 = agent2.invoke(query)
```

### ✅ Maintainable
- Bug fix in one place → all agents benefit
- Easy to add new features
- Clear separation of logic and configuration

### ✅ Testable
```python
# Test different configurations easily
def test_agent_config(config, query):
    agent = FlexibleAgent(config)
    agent.set_llm(llm)
    agent.add_tool("calculator", "Calculate", calc)
    return agent.invoke(query)

# Test all configs
for config_name in ["toolcall", "action", "react"]:
    result = test_agent_config(AGENT_CONFIGS[config_name], "2+2")
    assert "4" in result
```

---

## File Structure

```
agent/
├── core/
│   ├── agent_config.py      ⭐ NEW - Agent configurations
│   ├── flexible_agent.py    ⭐ NEW - Configurable agent
│   ├── base_agent.py        ✅ Existing
│   ├── tool_executor.py     ✅ Existing
│   ├── response_parser.py   ✅ Existing
│   └── llm_interface.py     ✅ Existing
│
├── adapters/
│   └── gemini_adapter.py    ✅ Existing
│
└── ToolCall_Agent/
    └── agent.py             ✅ Original (still works)

demo_flexible_agents.py      ⭐ NEW - Demo 5 agent types
```

---

## Running the Demo

```bash
python demo_flexible_agents.py
```

This will show you:
1. ToolCall Agent (original format)
2. Action Agent (simpler format)
3. ReACT Agent (with reasoning)
4. Function Agent (minimalist)
5. Custom Agent (your own format)

All solving the same problem with different styles!

---

## Comparison

| Approach | Code per Agent | Flexibility | Maintainability |
|----------|---------------|-------------|-----------------|
| **Old** (separate classes) | 200+ lines | Low | Hard |
| **New** (configuration) | 0 lines | High | Easy |

---

## When to Use Each Approach

### Use Separate Classes When:
- Agent has **completely different** execution logic
- Need very specialized behavior
- Building framework-level components

### Use Configuration When:
- Different prompts/JSON formats
- Same underlying logic
- Want to experiment quickly
- Need many variations

**For your use case (different prompts/JSON keys): Use Configuration! ✅**

---

## Advanced: Sharing Configs

```python
# Save configs to use across projects
MY_AGENT_CONFIG = create_custom_config(
    name="MyAgent",
    prompt_template="""...""",
    required_keys=["key1", "key2"],
    key_mapping={...}
)

# Use in multiple places
agent1 = FlexibleAgent(MY_AGENT_CONFIG)
agent2 = FlexibleAgent(MY_AGENT_CONFIG)  # Same config, different instance

# Or export to dict/JSON
config_dict = {
    "name": MY_AGENT_CONFIG.name,
    "prompt": MY_AGENT_CONFIG.prompt_template,
    ...
}
```

---

## FAQs

**Q: Can I still use the original ToolCallAgent?**
A: Yes! It still works. This is an additional option.

**Q: What if I need very different logic?**
A: Create a new class inheriting from BaseAgent (like before).

**Q: How do I add more predefined configs?**
A: Add to `agent_config.py` in the `AGENT_CONFIGS` dictionary.

**Q: Can I modify prompts at runtime?**
A: Yes! Just create a new config with the new prompt.

**Q: Does this work with multiple tools?**
A: Absolutely! Add as many tools as you want to any agent.

---

## Next Steps

1. ✅ Run `python demo_flexible_agents.py`
2. ✅ Try creating your own config
3. ✅ Experiment with different prompts
4. ✅ Test different JSON structures
5. ✅ Build your agent zoo! 🦁🐯🐻

---

**Created by:** codexJitin  
**Powered by:** Codemni

**🎭 Create unlimited agent types without writing new code! 🚀**
