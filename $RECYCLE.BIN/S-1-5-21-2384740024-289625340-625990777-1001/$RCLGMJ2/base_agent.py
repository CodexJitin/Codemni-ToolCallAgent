"""
Base Agent - Abstract base class for all agent types.
Provides common functionality and interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .llm_interface import LLMInterface
from .tool_executor import ToolExecutor
from .response_parser import ResponseParser


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Provides common functionality like tool management, LLM interface, and logging.
    """
    
    def __init__(self, name: str = "Agent", verbose: bool = False):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            verbose: Whether to enable verbose logging
        """
        self.name = name
        self.verbose = verbose
        self.llm: Optional[LLMInterface] = None
        self.tool_executor = ToolExecutor()
        self.response_parser = ResponseParser()
        self.prompt_template: Optional[str] = None
        self._compiled_prompt: Optional[str] = None
        self.max_iterations = 10
    
    def set_llm(self, llm: LLMInterface):
        """Set the LLM to use for generating responses."""
        self.llm = llm
    
    def add_tool(self, name: str, description: str, function: callable, 
                 parameter_schema: Optional[Dict] = None):
        """
        Add a tool that the agent can use.
        
        Args:
            name: Tool name
            description: Description of what the tool does
            function: Callable function to execute
            parameter_schema: Optional JSON schema for parameters
        """
        self.tool_executor.register_tool(name, description, function, parameter_schema)
        # Reset compiled prompt when tools change
        self._compiled_prompt = None
    
    def remove_tool(self, name: str) -> bool:
        """Remove a tool from the agent."""
        result = self.tool_executor.unregister_tool(name)
        if result:
            self._compiled_prompt = None
        return result
    
    def list_tools(self) -> list:
        """Get list of all registered tools."""
        return self.tool_executor.list_tools()
    
    def get_tools_description(self) -> str:
        """Get formatted description of all tools."""
        return self.tool_executor.get_tools_description()
    
    def log(self, message: str, level: str = "info"):
        """
        Log a message if verbose mode is enabled.
        
        Args:
            message: Message to log
            level: Log level (info, success, error, warning)
        """
        if self.verbose:
            colors = {
                "info": "\033[94m",      # Blue
                "success": "\033[92m",   # Green
                "error": "\033[91m",     # Red
                "warning": "\033[93m",   # Yellow
            }
            icons = {
                "info": "ℹ",
                "success": "✓",
                "error": "✗",
                "warning": "⚠",
            }
            color = colors.get(level, colors["info"])
            icon = icons.get(level, "•")
            print(f"{color}{icon}\033[0m {message}")
    
    @abstractmethod
    def _compile_prompt(self) -> str:
        """
        Compile the prompt template with current configuration.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def invoke(self, query: str, **kwargs) -> str:
        """
        Execute the agent with a user query.
        Must be implemented by subclasses.
        
        Args:
            query: User's question or request
            **kwargs: Additional parameters
            
        Returns:
            Final response from the agent
        """
        pass
    
    def validate_setup(self) -> tuple[bool, Optional[str]]:
        """
        Validate that the agent is properly configured.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.llm is None:
            return False, "LLM not set. Call set_llm() first"
        
        if len(self.tool_executor.list_tools()) == 0:
            return False, "No tools added. Call add_tool() at least once"
        
        if self.prompt_template is None:
            return False, "Prompt template not set"
        
        return True, None
    
    def get_config(self) -> Dict[str, Any]:
        """Get current agent configuration."""
        return {
            "name": self.name,
            "verbose": self.verbose,
            "max_iterations": self.max_iterations,
            "tools": self.list_tools(),
            "llm": self.llm.get_model_info() if self.llm else None
        }
