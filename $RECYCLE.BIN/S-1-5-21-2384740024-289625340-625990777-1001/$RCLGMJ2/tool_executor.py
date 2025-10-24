"""
Tool Executor - Handles tool registration and execution.
Reusable across different agent types.
"""

import json
from typing import Dict, Callable, Any, Optional


class ToolExecutor:
    """
    Manages tool registration and execution.
    Provides a unified interface for tool management.
    """
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(self, name: str, description: str, function: Callable, 
                     parameter_schema: Optional[Dict] = None):
        """
        Register a tool for the agent to use.
        
        Args:
            name: Tool name (unique identifier)
            description: Description of what the tool does
            function: Callable function to execute
            parameter_schema: Optional JSON schema for parameters
        """
        self.tools[name] = {
            "description": description,
            "function": function,
            "parameter_schema": parameter_schema
        }
    
    def unregister_tool(self, name: str) -> bool:
        """
        Remove a tool from the registry.
        
        Args:
            name: Tool name to remove
            
        Returns:
            True if tool was removed, False if tool didn't exist
        """
        if name in self.tools:
            del self.tools[name]
            return True
        return False
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get tool information by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        """Get list of all registered tool names."""
        return list(self.tools.keys())
    
    def get_tools_description(self) -> str:
        """
        Get formatted description of all tools.
        Useful for building prompts.
        """
        descriptions = []
        for name, info in self.tools.items():
            descriptions.append(f"- {name}: {info['description']}")
        return "\n".join(descriptions)
    
    def execute(self, tool_name: str, tool_parameters: Any) -> str:
        """
        Execute a tool with the provided parameters.
        
        Args:
            tool_name: Name of the tool to execute
            tool_parameters: Parameters in various formats
            
        Returns:
            Result from tool execution or error message
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        tool_function = self.tools[tool_name]["function"]
        
        # Handle no parameters case
        if not tool_parameters or tool_parameters == "None":
            try:
                return str(tool_function())
            except Exception as e:
                return f"Error executing tool '{tool_name}': {str(e)}"
        
        # Parse parameters if string
        if isinstance(tool_parameters, str):
            try:
                tool_parameters = json.loads(tool_parameters)
            except json.JSONDecodeError:
                return f"Error: Invalid parameter format"
        
        # Execute with parameters
        try:
            return self._execute_with_params(tool_function, tool_parameters, tool_name)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def _execute_with_params(self, tool_function: Callable, 
                            tool_parameters: Any, tool_name: str) -> str:
        """
        Internal method to handle parameter parsing and execution.
        
        Args:
            tool_function: The function to execute
            tool_parameters: Parameters to pass
            tool_name: Name of the tool (for error messages)
            
        Returns:
            Result as string
        """
        if isinstance(tool_parameters, dict):
            # Check if it's a key-value dict or a set-like dict
            if len(tool_parameters) > 0:
                first_key = list(tool_parameters.keys())[0]
                first_value = tool_parameters[first_key]
                
                # If the key looks like a parameter name, treat as kwargs
                if first_key and any(c.isalpha() for c in first_key):
                    # Key-value parameters like {"expression": "125 * 48"}
                    return str(tool_function(**tool_parameters))
                else:
                    # Comma-separated parameters like {"125 * 48"}
                    param_string = first_value if first_value else first_key
                    params = [p.strip() for p in str(param_string).split(',')]
                    return str(tool_function(*params))
            else:
                return str(tool_function())
        elif isinstance(tool_parameters, set):
            param_string = list(tool_parameters)[0]
            params = [p.strip() for p in str(param_string).split(',')]
            return str(tool_function(*params))
        elif isinstance(tool_parameters, list):
            return str(tool_function(*tool_parameters))
        else:
            return str(tool_function(tool_parameters))
    
    def validate_parameters(self, tool_name: str, parameters: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate parameters against tool schema if available.
        
        Args:
            tool_name: Name of the tool
            parameters: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if tool_name not in self.tools:
            return False, f"Tool '{tool_name}' not found"
        
        schema = self.tools[tool_name].get("parameter_schema")
        if not schema:
            return True, None  # No schema to validate against
        
        # Basic schema validation (can be extended)
        required = schema.get("required", [])
        for req in required:
            if req not in parameters:
                return False, f"Missing required parameter: {req}"
        
        return True, None
