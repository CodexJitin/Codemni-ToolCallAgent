"""
Flexible Agents Demo - Creating different agent types with different behaviors.
Shows how to easily create agents with different prompts and JSON structures.

Created by: codexJitin
Powered by: Codemni
"""

import sys
import os
import time

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from agent.core.flexible_agent import FlexibleAgent
from agent.core.agent_config import (
    AGENT_CONFIGS, 
    create_custom_config,
    AgentConfig,
    ResponseFormat
)
from agent.adapters.gemini_adapter import GeminiLLM
from agent.core.colors import Colors


# ==================== TOOLS ====================

def calculator(expression):
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"Error: {str(e)}"


def web_search(query, num_results="5"):
    """Simulate web search."""
    return f"Found {num_results} results for '{query}'"


def get_weather(city):
    """Get weather for a city."""
    weather_data = {
        "Paris": "☀️ Sunny, 25°C",
        "London": "🌧️ Rainy, 18°C",
        "Tokyo": "☁️ Cloudy, 22°C",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


# ==================== DEMO ====================

def demo_agent(agent, query, wait=2):
    """Demo a single agent."""
    print(f"\n{'='*80}")
    print(f"📝 Query: {query}")
    print('='*80 + '\n')
    
    start = time.time()
    result = agent.invoke(query)
    elapsed = time.time() - start
    
    print(f"⏱️  Time: {elapsed:.2f}s")
    time.sleep(wait)


def main():
    Colors.print_box(
        "🎭 FLEXIBLE AGENTS DEMONSTRATION 🎭\n\n"
        "Create different agent types by just changing config!\n"
        "Same logic, different prompts & JSON formats\n\n"
        "Created by: codexJitin\n"
        "Powered by: Codemni",
        width=78
    )
    
    time.sleep(2)
    
    # Initialize shared LLM
    print("\n🔧 Initializing LLM...")
    llm = GeminiLLM()
    print(f"✅ LLM ready: {llm.model_name}\n")
    time.sleep(1)
    
    # Show available agent types
    print("📚 Available Agent Types:")
    for config_name, config in AGENT_CONFIGS.items():
        print(f"  • {config_name}: {config.description}")
    print()
    time.sleep(2)
    
    # Test query
    query = "What is 456 multiplied by 789?"
    
    # ==================== 1. TOOLCALL AGENT ====================
    Colors.print_header("AGENT 1: ToolCall Agent (Original Format)", width=80)
    print("📋 JSON Format: Tool call, Tool Parameters, Final Response\n")
    
    agent1 = FlexibleAgent.from_config_name("toolcall", verbose=True)
    agent1.set_llm(llm)
    agent1.add_tool("calculator", "Calculate math. Param: 'expression' (string)", calculator)
    agent1.add_tool("search", "Search web. Params: 'query', 'num_results'", web_search)
    
    demo_agent(agent1, query)
    
    # ==================== 2. ACTION AGENT ====================
    Colors.print_header("AGENT 2: Action Agent (Simpler Format)", width=80)
    print("📋 JSON Format: action, input, output\n")
    
    agent2 = FlexibleAgent.from_config_name("action", verbose=True)
    agent2.set_llm(llm)
    agent2.add_tool("calculator", "Calculate math. Param: 'expression' (string)", calculator)
    agent2.add_tool("search", "Search web. Params: 'query', 'num_results'", web_search)
    
    demo_agent(agent2, query)
    
    # ==================== 3. REACT AGENT ====================
    Colors.print_header("AGENT 3: ReACT Agent (Reasoning + Acting)", width=80)
    print("📋 JSON Format: thought, action, action_input, answer\n")
    
    agent3 = FlexibleAgent.from_config_name("react", verbose=True)
    agent3.set_llm(llm)
    agent3.add_tool("calculator", "Calculate math. Param: 'expression' (string)", calculator)
    agent3.add_tool("search", "Search web. Params: 'query', 'num_results'", web_search)
    
    demo_agent(agent3, query)
    
    # ==================== 4. FUNCTION AGENT ====================
    Colors.print_header("AGENT 4: Function Agent (Minimalist)", width=80)
    print("📋 JSON Format: function, args, result\n")
    
    agent4 = FlexibleAgent.from_config_name("function", verbose=True)
    agent4.set_llm(llm)
    agent4.add_tool("calculator", "Calculate math. Param: 'expression' (string)", calculator)
    
    demo_agent(agent4, query)
    
    # ==================== 5. CUSTOM AGENT ====================
    Colors.print_header("AGENT 5: Custom Agent (Your Own Format!)", width=80)
    print("📋 JSON Format: step, execute, parameters, outcome\n")
    
    # Create a completely custom configuration
    custom_config = create_custom_config(
        name="CustomAgent",
        description="Agent with custom JSON structure",
        prompt_template="""
You are a custom agent with a unique response format.
Respond in JSON with these keys:
    "step" — what you plan to do
    "execute" — tool to execute or "None"
    "parameters" — tool parameters or "None"
    "outcome" — final result or "None"

Tools:
{tool_list}

query: {user_input}
""",
        required_keys=["step", "execute", "parameters", "outcome"],
        key_mapping={
            "tool": "execute",
            "params": "parameters",
            "response": "outcome",
            "reasoning": "step"
        },
        max_iterations=10
    )
    
    agent5 = FlexibleAgent(custom_config, verbose=True)
    agent5.set_llm(llm)
    agent5.add_tool("calculator", "Calculate math. Param: 'expression' (string)", calculator)
    
    demo_agent(agent5, query)
    
    # ==================== COMPARISON ====================
    Colors.print_header("COMPARISON: Different Prompts, Same Result!", width=80)
    print("""
    All 5 agents solved the same problem, but with different:
    • Prompt structures
    • JSON response formats
    • Reasoning styles
    
    Yet they all use the SAME underlying code! 🎉
    
    This is the power of configuration-driven agents!
    """)
    
    # ==================== SUMMARY ====================
    Colors.print_header("SUMMARY: Creating New Agent Types", width=80)
    print("""
    ✨ To create a new agent type, just:
    
    1️⃣  Define your JSON structure:
        required_keys = ["your_key1", "your_key2", "your_key3"]
    
    2️⃣  Write your prompt template:
        prompt = "Your instructions with {tool_list} and {user_input}"
    
    3️⃣  Create config:
        config = create_custom_config(name, prompt, required_keys, key_mapping)
    
    4️⃣  Create agent:
        agent = FlexibleAgent(config, verbose=True)
    
    5️⃣  Use it:
        agent.set_llm(llm)
        agent.add_tool(...)
        result = agent.invoke(query)
    
    That's it! No need to write a new agent class! 🚀
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💡 Benefits:
    • Create unlimited agent types
    • No code duplication
    • Just configuration changes
    • Easy to experiment
    • Maintain one codebase
    
    🔧 Predefined Configs Available:
    • toolcall  - Original format (Tool call, Tool Parameters, Final Response)
    • action    - Simple format (action, input, output)
    • react     - ReACT pattern (thought, action, action_input, answer)
    • function  - Minimalist (function, args, result)
    • cot       - Chain of Thought (reasoning_steps, tool_needed, tool_args, final_answer)
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💡 Built from SCRATCH by codexJitin
    
    ✨ Configuration-Driven | Flexible | Reusable
    
    🏢 Powered by: Codemni
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    print(f"\n{'=' * 80}\n")
    print("Thank you for watching! 🙏")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
