"""
ToolCall Agent - Refactored to use core components.
Now inherits from BaseAgent for better reusability.

Created by: codexJitin
Powered by: Codemni
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.colors import Colors
from .prompt import prompt


class ToolCallAgent(BaseAgent):
    """
    Agent that can call tools based on LLM decisions.
    Refactored to use core components for reusability.
    """
    
    def __init__(self, name: str = "ToolCallAgent", verbose: bool = False):
        """
        Initialize the ToolCall Agent.
        
        Args:
            name: Name of the agent
            verbose: Whether to enable verbose logging
        """
        super().__init__(name=name, verbose=verbose)
        self.prompt_template = prompt
    
    def _compile_prompt(self) -> str:
        """Compile the prompt template with available tools."""
        if not self.prompt_template:
            raise ValueError("Prompt template not set")
        
        # Get tool descriptions
        tool_list = self.get_tools_description()
        
        # Replace {tool_list} placeholder
        compiled = self.prompt_template.replace("{tool_list}", tool_list)
        return compiled
    
    def invoke(self, query: str, **kwargs) -> str:
        """
        Execute the agent with a user query.
        
        Args:
            query: User's question or request
            **kwargs: Additional parameters
                - max_iterations: Override default max iterations
            
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
        
        # Get max iterations from kwargs or use default
        max_iterations = kwargs.get('max_iterations', self.max_iterations)
        
        # Print header if verbose
        if self.verbose:
            Colors.print_header(f"Starting {self.name}", color='cyan')
        
        # Format initial prompt with query
        prompt_text = self._compiled_prompt.format(user_input=query)
        scratchpad = ""
        iteration = 0
        
        # Main agent loop
        while iteration < max_iterations:
            iteration += 1
            
            # Generate LLM response
            full_prompt = f"{prompt_text}\n{scratchpad}" if scratchpad else prompt_text
            response = self.llm.generate_response(full_prompt)
            
            # Parse response
            try:
                tool_call, tool_params, final_response = self.response_parser.parse_tool_call_response(response)
            except Exception as e:
                error_msg = f"Error parsing response: {str(e)}"
                self.log(error_msg, "error")
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
            
            tool_result = self.tool_executor.execute(tool_name, params)
            
            if self.verbose:
                print(f"{Colors.GREEN}📤 Result:{Colors.ENDC} {tool_result}\n")
            
            # Update scratchpad with tool result for next iteration
            scratchpad += f"\n\n--- Previous Tool Call ---\nTool Used: {tool_name}\nResult: {tool_result}\n\nNow provide the final response to the user based on this result."
        
        # Max iterations reached
        error_msg = "Error: Maximum iterations reached"
        self.log(error_msg, "error")
        return error_msg
