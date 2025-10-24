"""
ToolCall Agent - An intelligent agent that can call tools based on LLM decisions.

Created by: codexJitin
Powered by: Codemni
"""

from .prompt import prompt
from .llm_providers import initialize_llm
import re
import json
from typing import Optional


# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parse_agent_response(response):
    """
    Parse the LLM response to extract tool call, parameters, and final response.
    
    Args:
        response: Raw response string from LLM containing JSON block
        
    Returns:
        tuple: (tool_call_dict, tool_parameters_dict, final_response_dict)
    """
    # Extract JSON block with ```json or '''json markers
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
    if not json_match:
        json_match = re.search(r"'''json\s*(\{.*?\})\s*'''", response, re.DOTALL)
    
    if not json_match:
        raise ValueError(f"Invalid response format: No JSON block found in response: {response[:200]}")
    
    # Parse the single JSON object containing all three keys
    parsed_json = json.loads(json_match.group(1))
    
    # Create separate dicts for each component
    tool_call = {"Tool call": parsed_json.get("Tool call", "None")}
    tool_parameters = {"Tool Parameters": parsed_json.get("Tool Parameters", "None")}
    final_response = {"Final Response": parsed_json.get("Final Response", "None")}
    
    return tool_call, tool_parameters, final_response


def execute_tool(tool_name, tool_parameters, available_tools):
    """
    Execute a tool function with the provided parameters.
    
    Args:
        tool_name: Name of the tool to execute
        tool_parameters: Parameters in format {"value1,value2,..."} or {"key": "value"} or "None"
        available_tools: Dictionary of available tools with their functions
        
    Returns:
        Result from tool execution or error message
    """
    if tool_name not in available_tools:
        return f"Error: Tool '{tool_name}' not found"
    
    tool_function = available_tools[tool_name]["function"]
    
    # Handle no parameters case
    if not tool_parameters or tool_parameters == "None":
        return tool_function()
    
    # Parse parameters if string
    if isinstance(tool_parameters, str):
        try:
            tool_parameters = json.loads(tool_parameters)
        except json.JSONDecodeError:
            return f"Error: Invalid parameter format"
    
    # Extract and handle parameters
    try:
        if isinstance(tool_parameters, dict):
            # Check if it's a key-value dict (like {"expression": "125 * 48"})
            if len(tool_parameters) > 0:
                first_key = list(tool_parameters.keys())[0]
                first_value = tool_parameters[first_key]
                
                # If the key looks like a parameter name (contains letters), treat as kwargs
                if first_key and any(c.isalpha() for c in first_key):
                    # Key-value parameters like {"expression": "125 * 48"}
                    return tool_function(**tool_parameters)
                else:
                    # Comma-separated parameters like {"125 * 48"} or {"value1,value2"}
                    param_string = first_value if first_value else first_key
                    params = [p.strip() for p in str(param_string).split(',')]
                    return tool_function(*params)
            else:
                return tool_function()
        elif isinstance(tool_parameters, set):
            param_string = list(tool_parameters)[0]
            params = [p.strip() for p in str(param_string).split(',')]
            return tool_function(*params)
        else:
            return f"Error: Unexpected parameter type"
            
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"


class ToolCallAgent:
    """
    Agent that can call tools based on LLM decisions.
    
    Supported LLM providers:
    - openai: OpenAI models (gpt-4, gpt-3.5-turbo, etc.)
    - anthropic: Claude models (claude-3-opus, claude-3-sonnet, etc.)
    - groq: Groq models (llama3-70b, mixtral-8x7b, etc.)
    - google: Google Gemini models (gemini-pro, gemini-1.5-pro, etc.)
    - ollama: Local Ollama models (llama2, mistral, etc.)
    """
    
    def __init__(
        self, 
        llm_provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        verbose: bool = False,
        **llm_kwargs
    ) -> None:
        """
        Initialize ToolCallAgent with optional built-in LLM configuration.
        
        Args:
            llm_provider: LLM provider name ('openai', 'anthropic', 'groq', 'google', 'ollama')
            model: Model name (e.g., 'gpt-4', 'claude-3-opus-20240229', 'llama3-70b-8192')
            api_key: API key for the provider (can also be set via environment variables)
            verbose: Enable verbose logging
            **llm_kwargs: Additional arguments to pass to the LLM client (e.g., temperature, max_tokens)
        
        Example:
            # Initialize with built-in LLM
            agent = ToolCallAgent(
                llm_provider='openai',
                model='gpt-4',
                api_key='your-api-key',
                temperature=0.7
            )
            
            # Or initialize and set LLM later
            agent = ToolCallAgent()
            agent.initialize_llm('openai', 'gpt-4', 'your-api-key')
        """
        self.prompt_template = prompt
        self.tools = {}
        self.llm = None
        self._compiled_prompt = None
        self.verbose = verbose
        
        # Auto-initialize LLM if provider is specified
        if llm_provider:
            if not model:
                raise ValueError("model parameter is required when llm_provider is specified")
            self.set_llm(llm_provider, model, api_key, **llm_kwargs)
    
    def set_llm(
        self, 
        provider: str, 
        model: str, 
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM with built-in support for popular providers.
        
        Args:
            provider: LLM provider ('openai', 'anthropic', 'groq', 'google', 'ollama')
            model: Model name
            api_key: API key (will try to read from environment if not provided)
            **kwargs: Additional arguments for the LLM client
            
        Environment Variables:
            - OPENAI_API_KEY for OpenAI
            - ANTHROPIC_API_KEY for Anthropic
            - GROQ_API_KEY for Groq
            - GOOGLE_API_KEY for Google
            - OLLAMA_BASE_URL for Ollama (optional, defaults to http://localhost:11434)
            
        Examples:
            >>> agent.set_llm('openai', 'gpt-4', api_key='sk-...')
            >>> agent.set_llm('groq', 'llama3-70b-8192', temperature=0.7)
        """
        self.llm = initialize_llm(provider, model, api_key, **kwargs)
        self._log(f"Initialized {provider.upper()} with model: {model}", "success")
    
    def add_llm(self, llm):
        """
        Set a custom LLM instance (for backwards compatibility).
        
        Args:
            llm: Custom LLM object with a generate_response(prompt) method
        """
        self.llm = llm
    
    def add_tool(self, name, description, function):
        """
        Add a tool that the agent can use.
        
        Args:
            name: Tool name
            description: Description of what the tool does
            function: Callable function to execute
        """
        self.tools[name] = {
            "description": description,
            "function": function
        }
    
    def _compile_prompt(self):
        """Compile the prompt template with available tools."""
        tool_list = "\n".join(
            [f"        - {name}: {info['description']}" 
             for name, info in self.tools.items()]
        )
        # Replace {tool_list} placeholder while preserving {user_input}
        self._compiled_prompt = self.prompt_template.replace("{tool_list}", tool_list)
    
    def _log(self, message, level="info"):
        """Print message if verbose mode is enabled with colors."""
        if self.verbose:
            if level == "info":
                print(f"{Colors.BLUE}ℹ{Colors.ENDC} {message}")
            elif level == "success":
                print(f"{Colors.GREEN}✓{Colors.ENDC} {message}")
            elif level == "error":
                print(f"{Colors.RED}✗{Colors.ENDC} {message}")
            elif level == "warning":
                print(f"{Colors.YELLOW}⚠{Colors.ENDC} {message}")
    
    def invoke(self, query):
        """
        Execute the agent with a user query.
        
        Args:
            query: User's question or request
            
        Returns:
            Final response from the agent
        """
        if self.llm is None:
            raise ValueError("LLM not set. Call add_llm() first")
        
        if not self.tools:
            raise ValueError("No tools added. Call add_tool() at least once")
        
        # Compile prompt if needed
        if self._compiled_prompt is None:
            self._compile_prompt()
        
        if self.verbose:
            print(f"\n{Colors.CYAN}{'─' * 70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.CYAN}Starting ToolCalling Agent{Colors.ENDC}")
            print(f"{Colors.CYAN}{'─' * 70}{Colors.ENDC}\n")
        
        assert self._compiled_prompt is not None
        prompt = self._compiled_prompt.format(user_input=query)
        scratchpad = ""
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Get LLM response
            full_prompt = f"{prompt}\n{scratchpad}" if scratchpad else prompt
            response = self.llm.generate_response(full_prompt)
            
            try:
                tool_call, tool_params, final_response = parse_agent_response(response)
            except Exception as e:
                error_msg = f"Error parsing response: {str(e)}"
                self._log(error_msg, "error")
                return error_msg
            
            # Check if agent wants to provide final response
            tool_name = tool_call.get("Tool call")
            
            if tool_name == "None" or not tool_name:
                final_answer = final_response.get("Final Response", "No response provided")
                
                if self.verbose:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Final Response:{Colors.ENDC}")
                    print(f"{Colors.GREEN}▸{Colors.ENDC} {final_answer}\n")
                
                return final_answer
            
            # Execute tool
            params = tool_params.get("Tool Parameters")
            
            if self.verbose:
                print(f"{Colors.YELLOW}🔧 Tool:{Colors.ENDC} {Colors.BOLD}{tool_name}{Colors.ENDC}")
                print(f"{Colors.YELLOW}📝 Params:{Colors.ENDC} {params}")
            
            tool_result = execute_tool(tool_name, params, self.tools)
            
            if self.verbose:
                print(f"{Colors.GREEN}📤 Result:{Colors.ENDC} {tool_result}\n")
            
            # Update scratchpad with tool result for next iteration
            scratchpad += f"\n\n--- Previous Tool Call ---\nTool Used: {tool_name}\nResult: {tool_result}\n\nNow provide the final response to the user based on this result."
        
        error_msg = "Error: Maximum iterations reached"
        self._log(error_msg, "error")
        return error_msg
    
