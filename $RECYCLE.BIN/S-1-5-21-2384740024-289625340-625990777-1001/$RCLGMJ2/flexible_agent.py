"""
Flexible Agent - A configurable agent that can adapt to different response formats.
Create different agent types just by changing configuration!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.agent_config import AgentConfig, AGENT_CONFIGS
from core.colors import Colors


class FlexibleAgent(BaseAgent):
    """
    A highly flexible agent that adapts its behavior based on configuration.
    Create different agent types just by providing different configs!
    """
    
    def __init__(self, config: AgentConfig, verbose: bool = None):
        """
        Initialize agent with a configuration.
        
        Args:
            config: AgentConfig defining the agent's behavior
            verbose: Override config verbose setting
        """
        verbose = verbose if verbose is not None else config.verbose
        super().__init__(name=config.name, verbose=verbose)
        
        self.config = config
        self.prompt_template = config.prompt_template
        self.max_iterations = config.max_iterations
        self.response_format = config.response_format
    
    def _compile_prompt(self) -> str:
        """Compile prompt with tools."""
        tool_list = self.get_tools_description()
        
        # Add special instructions if any
        compiled = self.prompt_template.replace("{tool_list}", tool_list)
        
        if self.config.special_instructions:
            compiled = f"{compiled}\n\n{self.config.special_instructions}"
        
        # Add examples if any
        if self.config.examples:
            examples_text = "\n\nExamples:\n" + "\n".join(self.config.examples)
            compiled = f"{compiled}{examples_text}"
        
        return compiled
    
    def _parse_response(self, response: str) -> dict:
        """
        Parse response according to the agent's configured format.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed response with standardized internal keys
        """
        # Parse JSON using response parser
        parsed = self.response_parser.parse_json_response(
            response, 
            self.response_format.required_keys
        )
        
        # Map JSON keys to internal standard format
        # Internal format: {"tool": ..., "params": ..., "response": ...}
        standardized = {}
        
        for internal_key in ["tool", "params", "response", "reasoning"]:
            json_key = self.response_format.get_json_key(internal_key)
            if json_key in parsed:
                standardized[internal_key] = parsed[json_key]
        
        return standardized
    
    def invoke(self, query: str, **kwargs) -> str:
        """
        Execute the agent with a user query.
        
        Args:
            query: User's question or request
            **kwargs: Additional parameters (max_iterations, etc.)
            
        Returns:
            Final response from the agent
        """
        # Validate setup
        is_valid, error_msg = self.validate_setup()
        if not is_valid:
            raise ValueError(error_msg)
        
        # Compile prompt if needed
        if self._compiled_prompt is None:
            self._compiled_prompt = self._compile_prompt()
        
        # Get max iterations
        max_iterations = kwargs.get('max_iterations', self.max_iterations)
        
        # Print header if verbose
        if self.verbose:
            Colors.print_header(f"Starting {self.name}", color='cyan')
            print(f"📋 Config: {self.config.description}")
            print(f"🔧 Response Format: {', '.join(self.response_format.required_keys)}\n")
        
        # Format initial prompt
        prompt_text = self._compiled_prompt.format(user_input=query)
        scratchpad = ""
        iteration = 0
        
        # Main agent loop
        while iteration < max_iterations:
            iteration += 1
            
            if self.verbose:
                print(f"{Colors.YELLOW}🔄 Iteration {iteration}{Colors.ENDC}")
            
            # Generate LLM response
            full_prompt = f"{prompt_text}\n{scratchpad}" if scratchpad else prompt_text
            response = self.llm.generate_response(full_prompt)
            
            # Parse response
            try:
                parsed = self._parse_response(response)
            except Exception as e:
                error_msg = f"Error parsing response: {str(e)}"
                self.log(error_msg, "error")
                return error_msg
            
            # Get standardized values
            tool_name = parsed.get("tool", "None")
            params = parsed.get("params", "None")
            final_answer = parsed.get("response", "None")
            reasoning = parsed.get("reasoning", "")
            
            # Check if agent wants to provide final response
            if tool_name == "None" or tool_name is None or not tool_name:
                if self.verbose:
                    if reasoning:
                        print(f"\n{Colors.CYAN}💭 Reasoning:{Colors.ENDC} {reasoning}")
                    print(f"\n{Colors.GREEN}{Colors.BOLD}Final Response:{Colors.ENDC}")
                    print(f"{Colors.GREEN}▸{Colors.ENDC} {final_answer}\n")
                
                return final_answer if final_answer and final_answer != "None" else "No response provided"
            
            # Execute tool
            if self.verbose:
                if reasoning:
                    print(f"{Colors.CYAN}💭 Reasoning:{Colors.ENDC} {reasoning}")
                print(f"{Colors.YELLOW}🔧 Tool:{Colors.ENDC} {Colors.BOLD}{tool_name}{Colors.ENDC}")
                print(f"{Colors.YELLOW}📝 Params:{Colors.ENDC} {params}")
            
            tool_result = self.tool_executor.execute(tool_name, params)
            
            if self.verbose:
                print(f"{Colors.GREEN}📤 Result:{Colors.ENDC} {tool_result}\n")
            
            # Update scratchpad with tool result
            scratchpad += f"\n\n--- Tool Execution ---\nTool: {tool_name}\nResult: {tool_result}\n\nProvide the final response based on this result."
        
        # Max iterations reached
        error_msg = f"Error: Maximum iterations ({max_iterations}) reached"
        self.log(error_msg, "error")
        return error_msg
    
    @classmethod
    def from_config_name(cls, config_name: str, verbose: bool = False):
        """
        Create an agent from a predefined configuration name.
        
        Args:
            config_name: Name of predefined config ("toolcall", "action", "react", etc.)
            verbose: Whether to enable verbose logging
            
        Returns:
            FlexibleAgent instance
        """
        if config_name not in AGENT_CONFIGS:
            available = ", ".join(AGENT_CONFIGS.keys())
            raise ValueError(f"Unknown config '{config_name}'. Available: {available}")
        
        config = AGENT_CONFIGS[config_name]
        return cls(config, verbose=verbose)
