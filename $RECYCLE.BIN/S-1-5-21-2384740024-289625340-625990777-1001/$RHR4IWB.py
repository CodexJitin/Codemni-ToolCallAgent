"""
Example Multi-Agent System
Demonstrates how to build specialized agents using the refactored architecture.

This example creates three specialized agents:
1. MathAgent - Specialized in mathematical operations
2. ResearchAgent - Specialized in information gathering
3. CoordinatorAgent - Orchestrates other agents

Created by: codexJitin
Powered by: Codemni
"""

import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from agent.core.base_agent import BaseAgent
from agent.adapters.gemini_adapter import GeminiLLM
from agent.core.colors import Colors


# ==================== SPECIALIZED AGENTS ====================

class MathAgent(BaseAgent):
    """Agent specialized in mathematical operations."""
    
    def __init__(self, verbose=False):
        super().__init__(name="MathAgent", verbose=verbose)
        self.prompt_template = """
You are a mathematical calculation specialist.
You have access to the following tools:
{tool_list}

Always respond in valid JSON format with these three keys:
    "Tool call" — the tool to invoke (or "None")
    "Tool Parameters" — parameters for the tool (or "None")
    "Final Response" — your answer to the user (or "None")

Rules:
- Use tools when mathematical calculations are needed
- Provide clear explanations with your answers
- Set "Final Response" to "None" when calling a tool
- After tool execution, provide a helpful final response

query: {user_input}
"""
    
    def _compile_prompt(self) -> str:
        tool_list = self.get_tools_description()
        return self.prompt_template.replace("{tool_list}", tool_list)
    
    def invoke(self, query: str, **kwargs) -> str:
        is_valid, error = self.validate_setup()
        if not is_valid:
            raise ValueError(error)
        
        if self._compiled_prompt is None:
            self._compiled_prompt = self._compile_prompt()
        
        prompt = self._compiled_prompt.format(user_input=query)
        scratchpad = ""
        max_iterations = kwargs.get('max_iterations', self.max_iterations)
        
        for iteration in range(max_iterations):
            full_prompt = f"{prompt}\n{scratchpad}" if scratchpad else prompt
            response = self.llm.generate_response(full_prompt)
            
            try:
                tool_call, tool_params, final_response = self.response_parser.parse_tool_call_response(response)
            except Exception as e:
                return f"Error: {str(e)}"
            
            tool_name = tool_call.get("Tool call")
            
            if tool_name == "None" or not tool_name:
                return final_response.get("Final Response", "No response")
            
            params = tool_params.get("Tool Parameters")
            if self.verbose:
                self.log(f"Calling tool: {tool_name} with params: {params}")
            
            result = self.tool_executor.execute(tool_name, params)
            scratchpad += f"\n\nTool: {tool_name}\nResult: {result}\nProvide final response."
        
        return "Error: Max iterations reached"


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def __init__(self, verbose=False):
        super().__init__(name="ResearchAgent", verbose=verbose)
        self.prompt_template = """
You are a research specialist focused on gathering information.
You have access to the following tools:
{tool_list}

Always respond in valid JSON format with these three keys:
    "Tool call" — the tool to invoke (or "None")
    "Tool Parameters" — parameters for the tool (or "None")
    "Final Response" — your answer to the user (or "None")

Rules:
- Use search tools to find information
- Synthesize information from multiple sources
- Provide comprehensive summaries
- Set "Final Response" to "None" when calling a tool

query: {user_input}
"""
    
    def _compile_prompt(self) -> str:
        tool_list = self.get_tools_description()
        return self.prompt_template.replace("{tool_list}", tool_list)
    
    def invoke(self, query: str, **kwargs) -> str:
        is_valid, error = self.validate_setup()
        if not is_valid:
            raise ValueError(error)
        
        if self._compiled_prompt is None:
            self._compiled_prompt = self._compile_prompt()
        
        prompt = self._compiled_prompt.format(user_input=query)
        scratchpad = ""
        max_iterations = kwargs.get('max_iterations', self.max_iterations)
        
        for iteration in range(max_iterations):
            full_prompt = f"{prompt}\n{scratchpad}" if scratchpad else prompt
            response = self.llm.generate_response(full_prompt)
            
            try:
                tool_call, tool_params, final_response = self.response_parser.parse_tool_call_response(response)
            except Exception as e:
                return f"Error: {str(e)}"
            
            tool_name = tool_call.get("Tool call")
            
            if tool_name == "None" or not tool_name:
                return final_response.get("Final Response", "No response")
            
            params = tool_params.get("Tool Parameters")
            if self.verbose:
                self.log(f"Calling tool: {tool_name} with params: {params}")
            
            result = self.tool_executor.execute(tool_name, params)
            scratchpad += f"\n\nTool: {tool_name}\nResult: {result}\nProvide final response."
        
        return "Error: Max iterations reached"


class CoordinatorAgent(BaseAgent):
    """Agent that coordinates other specialized agents."""
    
    def __init__(self, agents: dict, verbose=False):
        super().__init__(name="CoordinatorAgent", verbose=verbose)
        self.specialized_agents = agents  # Dict of agent_name: agent_instance
        self.prompt_template = """
You are a coordinator that delegates tasks to specialized agents.
You have access to the following specialized agents:
{agent_list}

Available tools for each agent:
{tools_info}

Respond in JSON format with these keys:
    "Agent" — which specialized agent to use (or "None")
    "Query" — the query to send to that agent (or "None")
    "Final Response" — your final answer (or "None")

Rules:
- Analyze the user query to determine which agent is best suited
- Delegate to the appropriate specialized agent
- Synthesize responses from multiple agents if needed
- Provide a final comprehensive response

query: {user_input}
"""
    
    def _compile_prompt(self) -> str:
        agent_list = "\n".join([f"- {name}: {agent.name}" 
                                for name, agent in self.specialized_agents.items()])
        
        tools_info = ""
        for name, agent in self.specialized_agents.items():
            tools = agent.list_tools()
            tools_info += f"\n{name}: {', '.join(tools)}"
        
        return (self.prompt_template
                .replace("{agent_list}", agent_list)
                .replace("{tools_info}", tools_info))
    
    def invoke(self, query: str, **kwargs) -> str:
        """Coordinate between specialized agents."""
        if self.verbose:
            self.log(f"Coordinator received query: {query}")
        
        # Simple routing logic - can be enhanced with LLM
        if any(word in query.lower() for word in ['calculate', 'math', 'multiply', 'divide', 'add', 'subtract']):
            if 'math' in self.specialized_agents:
                if self.verbose:
                    self.log("Routing to MathAgent", "info")
                return self.specialized_agents['math'].invoke(query)
        
        if any(word in query.lower() for word in ['search', 'find', 'research', 'look up', 'information']):
            if 'research' in self.specialized_agents:
                if self.verbose:
                    self.log("Routing to ResearchAgent", "info")
                return self.specialized_agents['research'].invoke(query)
        
        # Default: try research agent
        if 'research' in self.specialized_agents:
            return self.specialized_agents['research'].invoke(query)
        
        return "No suitable agent found for this query"


# ==================== TOOLS ====================

def calculator(expression):
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"Error: {str(e)}"


def advanced_math(operation, *numbers):
    """Perform advanced math operations."""
    numbers = [float(n) for n in numbers]
    
    operations = {
        'sum': lambda nums: sum(nums),
        'average': lambda nums: sum(nums) / len(nums),
        'max': lambda nums: max(nums),
        'min': lambda nums: min(nums),
        'product': lambda nums: eval('*'.join(map(str, nums))),
    }
    
    if operation in operations:
        return f"{operations[operation](numbers)}"
    return f"Unknown operation: {operation}"


def web_search(query, num_results="5"):
    """Simulate web search."""
    return (f"Found {num_results} results for '{query}':\n"
            f"1. Comprehensive guide to {query}\n"
            f"2. {query} tutorial for beginners\n"
            f"3. Advanced {query} techniques\n"
            f"4. {query} best practices\n"
            f"5. Latest updates on {query}")


def database_query(query_type, table="users"):
    """Simulate database query."""
    return f"Database query results for {query_type} from {table} table: [Mock data results]"


# ==================== DEMO ====================

def main():
    Colors.print_box(
        "🤖 MULTI-AGENT SYSTEM DEMONSTRATION 🤖\n\n"
        "Specialized agents working together\n"
        "Built with modular, reusable components\n\n"
        "Created by: codexJitin\n"
        "Powered by: Codemni",
        width=78
    )
    
    print("\n" + "="*80 + "\n")
    
    # Initialize shared LLM
    print("🔧 Initializing shared LLM...")
    llm = GeminiLLM()
    print(f"✅ LLM initialized: {llm.model_name}\n")
    
    # Create specialized agents
    print("🤖 Creating specialized agents...\n")
    
    # 1. Math Agent
    math_agent = MathAgent(verbose=True)
    math_agent.set_llm(llm)
    math_agent.add_tool(
        "calculator",
        "Performs basic mathematical calculations. Parameter: 'expression' (string)",
        calculator
    )
    math_agent.add_tool(
        "advanced_math",
        "Advanced math operations. Parameters: 'operation' (sum/average/max/min), 'numbers' (comma-separated)",
        advanced_math
    )
    print(f"✅ {math_agent.name} created with tools: {', '.join(math_agent.list_tools())}")
    
    # 2. Research Agent
    research_agent = ResearchAgent(verbose=True)
    research_agent.set_llm(llm)
    research_agent.add_tool(
        "search",
        "Search the web. Parameters: 'query' (string), 'num_results' (string, optional)",
        web_search
    )
    research_agent.add_tool(
        "database_query",
        "Query database. Parameters: 'query_type' (string), 'table' (string, optional)",
        database_query
    )
    print(f"✅ {research_agent.name} created with tools: {', '.join(research_agent.list_tools())}")
    
    # 3. Coordinator Agent
    coordinator = CoordinatorAgent(
        agents={
            'math': math_agent,
            'research': research_agent
        },
        verbose=True
    )
    print(f"✅ {coordinator.name} created to coordinate specialized agents\n")
    
    print("="*80 + "\n")
    
    # Demo scenarios
    scenarios = [
        ("Math Query", "What is 456 multiplied by 789?"),
        ("Research Query", "Search for Python async programming tutorials"),
        ("Coordinated Query", "Calculate the average of 10, 20, 30, 40, 50"),
    ]
    
    for title, query in scenarios:
        Colors.print_header(f"SCENARIO: {title}", width=80, color='cyan')
        print(f"📝 Query: {query}\n")
        print("─" * 80 + "\n")
        
        # Use coordinator for all queries
        result = coordinator.invoke(query)
        
        print("\n" + "─" * 80)
        print(f"\n{Colors.GREEN}{Colors.BOLD}Final Result:{Colors.ENDC}")
        print(f"{Colors.GREEN}▸{Colors.ENDC} {result}\n")
        print("="*80 + "\n")
    
    # Show agent configurations
    Colors.print_header("AGENT CONFIGURATIONS", width=80, color='magenta')
    
    for agent_name, agent in [('Math Agent', math_agent), ('Research Agent', research_agent)]:
        config = agent.get_config()
        print(f"\n{Colors.BOLD}{agent_name}:{Colors.ENDC}")
        print(f"  Name: {config['name']}")
        print(f"  Tools: {len(config['tools'])} ({', '.join(config['tools'])})")
        print(f"  Max Iterations: {config['max_iterations']}")
    
    print("\n" + "="*80 + "\n")
    
    # Summary
    Colors.print_box(
        "✅ Multi-Agent System Demo Complete!\n\n"
        "🎯 Key Features Demonstrated:\n"
        "• Specialized agents for different tasks\n"
        "• Shared LLM across multiple agents\n"
        "• Agent coordination and routing\n"
        "• Modular and reusable components\n"
        "• Easy to extend with new agents\n\n"
        "🚀 Production-ready architecture!",
        width=78
    )
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
