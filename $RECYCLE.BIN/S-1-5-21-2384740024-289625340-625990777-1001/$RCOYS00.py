import json
import re
import time
import logging
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from datetime import datetime
from functools import wraps


# Custom Exceptions for better error handling
class AgentConfigurationError(Exception):
    """Raised when agent is not properly configured"""
    pass


class ToolExecutionError(Exception):
    """Raised when tool execution fails"""
    pass


class LLMResponseError(Exception):
    """Raised when LLM response is invalid"""
    pass


class MaxIterationsError(Exception):
    """Raised when max iterations is exceeded"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


# Decorator for method validation
def requires_configuration(method):
    """Decorator to ensure agent is properly configured before execution"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._is_configured():
            missing = self._get_missing_components()
            raise AgentConfigurationError(
                f"Agent not fully configured. Missing: {', '.join(missing)}"
            )
        return method(self, *args, **kwargs)
    return wrapper


class ToolCall_Agent:
    """
    An intelligent agent that can invoke tools based on user queries.
    Uses an LLM to determine which tool to call and generates responses.
    """
    
    def __init__(self, 
                 enable_logging: bool = False,
                 log_level: str = "INFO",
                 max_tool_execution_time: int = 30,
                 validate_tools: bool = True) -> None:
        """
        Initialize the ToolCall_Agent with empty configurations.
        
        Args:
            enable_logging: Enable detailed logging
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            max_tool_execution_time: Maximum time in seconds for tool execution
            validate_tools: Whether to validate tools on addition
        """
        # Core components
        self.llm = None
        self.prompt_template = None
        self.tools: Dict[str, Callable] = {}
        self.tool_descriptions: List[str] = []
        
        # Configuration
        self.max_tool_execution_time = max_tool_execution_time
        self.validate_tools_on_add = validate_tools
        
        # Execution tracking
        self.execution_history: List[Dict[str, Any]] = []
        self.total_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        
        # Validation rules
        self._required_json_keys = ["Tool call", "Final Response"]
        self._reserved_tool_names = ["None", "none", "null", ""]
        
        # Logging setup
        self.enable_logging = enable_logging
        if enable_logging:
            self.logger = self._setup_logger(log_level)
        else:
            self.logger = None
    
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """Setup logger for the agent"""
        logger = logging.getLogger("ToolCall_Agent")
        logger.setLevel(getattr(logging, log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _log(self, level: str, message: str) -> None:
        """Log a message if logging is enabled"""
        if self.logger:
            getattr(self.logger, level.lower())(message)
    
    def _is_configured(self) -> bool:
        """Check if agent is fully configured"""
        return all([
            self.llm is not None,
            self.prompt_template is not None,
            len(self.tools) > 0
        ])
    
    def _get_missing_components(self) -> List[str]:
        """Get list of missing configuration components"""
        missing = []
        if self.llm is None:
            missing.append("LLM")
        if self.prompt_template is None:
            missing.append("Prompt Template")
        if len(self.tools) == 0:
            missing.append("Tools")
        return missing
    
    def add_llm(self, llm: Any) -> 'ToolCall_Agent':
        """
        Add a language model to the agent with validation.
        
        Args:
            llm: A language model instance (e.g., OpenAI, Anthropic, etc.)
                 Must have a method to generate text (e.g., chat, generate, invoke)
        
        Returns:
            Self for method chaining
        
        Raises:
            ValidationError: If LLM doesn't have required interface
        """
        if llm is None:
            raise ValidationError("LLM cannot be None")
        
        # Validate LLM has at least one callable interface
        valid_methods = ['invoke', 'generate', 'chat', '__call__']
        has_valid_method = any(
            hasattr(llm, method) and callable(getattr(llm, method, None))
            for method in valid_methods
        )
        
        if not has_valid_method:
            raise ValidationError(
                f"LLM must have at least one of these callable methods: {valid_methods}"
            )
        
        self.llm = llm
        self._log("info", f"LLM added successfully: {type(llm).__name__}")
        return self
    
    def add_PromptTemplate(self, prompt_template: str) -> 'ToolCall_Agent':
        """
        Add a prompt template to the agent with validation.
        
        Args:
            prompt_template: A string template with placeholders like {tool_list} and {user_input}
        
        Returns:
            Self for method chaining
        
        Raises:
            ValidationError: If template is invalid
        """
    def add_tools(self, tools: Dict[str, Callable]) -> 'ToolCall_Agent':
        """
        Add tools that the agent can invoke with comprehensive validation.
        
        Args:
            tools: A dictionary mapping tool names to callable functions.
                   Each function should have a docstring describing its purpose.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValidationError: If tools are invalid
        """
        if not tools or not isinstance(tools, dict):
            raise ValidationError("Tools must be a non-empty dictionary")
        
        # Validate each tool
        validated_tools = {}
        for tool_name, tool_func in tools.items():
            # Validate tool name
            if not tool_name or not isinstance(tool_name, str):
                raise ValidationError(f"Tool name must be a non-empty string, got: {tool_name}")
            
            if tool_name in self._reserved_tool_names:
                raise ValidationError(f"Tool name '{tool_name}' is reserved and cannot be used")
            
            if not tool_name.replace('_', '').isalnum():
                raise ValidationError(
                    f"Tool name '{tool_name}' must be alphanumeric (underscores allowed)"
                )
            
            # Validate tool function
            if not callable(tool_func):
                raise ValidationError(f"Tool '{tool_name}' must be callable")
            
            if self.validate_tools_on_add:
                # Validate function signature
                import inspect
                sig = inspect.signature(tool_func)
                if len(sig.parameters) == 0:
                    raise ValidationError(
                        f"Tool '{tool_name}' must accept at least one parameter (query)"
                    )
                
                # Check for docstring
                if not tool_func.__doc__ or not tool_func.__doc__.strip():
                    self._log("warning", f"Tool '{tool_name}' has no docstring")
            
            validated_tools[tool_name] = tool_func
        
    def _validate_json_response(self, parsed: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate the parsed JSON response structure.
        
        Args:
            parsed: Parsed JSON dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if all required keys are present
        missing_keys = [key for key in self._required_json_keys if key not in parsed]
        if missing_keys:
            return False, f"Missing required keys: {missing_keys}"
        
        # Validate Tool call value
        tool_call = parsed.get("Tool call")
        if not isinstance(tool_call, str):
            return False, f"'Tool call' must be a string, got {type(tool_call).__name__}"
        
        # Validate Final Response value
        final_response = parsed.get("Final Response")
        if not isinstance(final_response, str):
            return False, f"'Final Response' must be a string, got {type(final_response).__name__}"
        
        # Check if tool exists (if not "None")
        if tool_call != "None" and tool_call not in self.tools:
            return False, f"Unknown tool: '{tool_call}'. Available tools: {list(self.tools.keys())}"
        
        return True, ""
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse and validate the LLM response to extract JSON.
        
        Args:
            response: Raw response from the LLM
        
        Returns:
            Parsed and validated JSON dictionary
        
        Raises:
            LLMResponseError: If response is invalid
        """
        if not response or not isinstance(response, str):
            raise LLMResponseError("LLM response must be a non-empty string")
        
        # Try to extract JSON from response
        try:
            # Method 1: Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
            else:
                # Method 2: Try parsing the whole response
                parsed = json.loads(response)
            
            # Validate the parsed JSON
            is_valid, error_msg = self._validate_json_response(parsed)
            if not is_valid:
                self._log("error", f"Invalid JSON structure: {error_msg}")
                raise LLMResponseError(f"Invalid response structure: {error_msg}")
            
            self._log("debug", f"Successfully parsed LLM response: {parsed}")
            return parsed
            
        except json.JSONDecodeError as e:
            self._log("error", f"JSON decode error: {e}")
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the given prompt with error handling.
        
        Args:
            prompt: The formatted prompt to send to the LLM
        
        Returns:
            The LLM's response as a string
        
        Raises:
            AgentConfigurationError: If LLM not configured
            LLMResponseError: If LLM call fails
        """
        if self.llm is None:
            raise AgentConfigurationError("LLM not configured. Call add_llm() first.")
        
        if not prompt or not isinstance(prompt, str):
            raise ValidationError("Prompt must be a non-empty string")
        
        self._log("debug", f"Calling LLM with prompt length: {len(prompt)}")
        
        try:
            # Try different common LLM interfaces
            if hasattr(self.llm, 'invoke'):
                # LangChain-style interface
                response = self.llm.invoke(prompt)
                if hasattr(response, 'content'):
                    result = response.content
                else:
                    result = str(response)
            elif hasattr(self.llm, 'generate'):
                # Some LLMs use generate
                response = self.llm.generate(prompt)
                result = str(response)
    def _execute_tool_safely(self, tool_name: str, context: str) -> Tuple[bool, str]:
        """
        Execute a tool with timeout and error handling.
        
        Args:
            tool_name: Name of the tool to execute
            context: Context/query to pass to the tool
        
        Returns:
            Tuple of (success, result_or_error_message)
        """
        if tool_name not in self.tools:
            return False, f"Tool '{tool_name}' not found"
        
        tool_func = self.tools[tool_name]
        start_time = time.time()
        
        try:
            self._log("info", f"Executing tool: {tool_name}")
            
            # Execute with timeout simulation (simplified)
            result = tool_func(context)
            
            execution_time = time.time() - start_time
            
            # Validate result
            if result is None:
                self._log("warning", f"Tool '{tool_name}' returned None")
                return False, "Tool returned no result"
            
            # Convert to string
            result_str = str(result)
            
            # Check execution time
            if execution_time > self.max_tool_execution_time:
                self._log("warning", 
                    f"Tool '{tool_name}' took {execution_time:.2f}s (limit: {self.max_tool_execution_time}s)"
                )
            
            self._log("info", f"Tool '{tool_name}' executed successfully in {execution_time:.2f}s")
            return True, result_str
            
        except Exception as e:
            self._log("error", f"Tool '{tool_name}' execution failed: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def _validate_user_input(self, user_input: str) -> None:
        """
        Validate user input.
        
        Args:
            user_input: The user's query
        
        Raises:
            ValidationError: If input is invalid
        """
        if not user_input or not isinstance(user_input, str):
            raise ValidationError("User input must be a non-empty string")
        
        if len(user_input.strip()) == 0:
            raise ValidationError("User input cannot be empty or whitespace only")
        
        if len(user_input) > 10000:
            raise ValidationError("User input too long (max 10000 characters)")
    
    def _validate_max_iterations(self, max_iterations: int) -> None:
        """
        Validate max iterations parameter.
        
        Args:
            max_iterations: Maximum iterations value
        
        Raises:
            ValidationError: If value is invalid
        """
        if not isinstance(max_iterations, int):
            raise ValidationError("max_iterations must be an integer")
        
        if max_iterations < 1:
            raise ValidationError("max_iterations must be at least 1")
        
        if max_iterations > 20:
            raise ValidationError("max_iterations cannot exceed 20")
    
    @requires_configuration
    def invoke(self, user_input: str, max_iterations: int = 5) -> Dict[str, Any]:
                # Chat-style interface
                response = self.llm.chat(prompt)
                result = str(response)
            elif callable(self.llm):
                # If the LLM itself is callable
                response = self.llm(prompt)
                result = str(response)
            else:
                raise LLMResponseError(
                    "LLM does not have a recognized interface (invoke, generate, chat, or __call__)"
                )
            
            if not result or not isinstance(result, str):
                raise LLMResponseError("LLM returned empty or invalid response")
            
            self._log("debug", f"LLM response received: {len(result)} characters")
            return result
            
        except Exception as e:
            self._log("error", f"LLM call failed: {str(e)}")
            raise LLMResponseError(f"LLM call failed: {str(e)}")
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # If no JSON found, try parsing the whole response
                return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Response was: {response}")
            return {
                "Tool call": "None",
                "Final Response": "I encountered an error processing your request. Please try again."
            }
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the given prompt.
        
        Args:
            prompt: The formatted prompt to send to the LLM
        
        Returns:
            The LLM's response as a string
        """
        if self.llm is None:
            raise ValueError("LLM not configured. Call add_llm() first.")
        
        # Try different common LLM interfaces
        if hasattr(self.llm, 'invoke'):
            # LangChain-style interface
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        elif hasattr(self.llm, 'generate'):
            # Some LLMs use generate
            response = self.llm.generate(prompt)
            return str(response)
        elif hasattr(self.llm, 'chat'):
            # Chat-style interface
            response = self.llm.chat(prompt)
            return str(response)
        elif callable(self.llm):
            # If the LLM itself is callable
            response = self.llm(prompt)
            return str(response)
        else:
            raise ValueError("LLM does not have a recognized interface (invoke, generate, chat, or __call__)")
    
    def invoke(self, user_input: str, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Process a user query and invoke appropriate tools if needed.
        Runs in a loop until a final response is found or max iterations reached.
        
        Args:
            user_input: The user's query or request
            max_iterations: Maximum number of iterations to prevent infinite loops
        
        Returns:
            A dictionary containing:
                - tool_calls: List of all tools that were called
                - tool_results: List of all tool results
                - final_response: The final response to the user
                - iterations: Number of iterations performed
        """
        if self.llm is None:
            raise ValueError("LLM not configured. Call add_llm() first.")
        
        if self.prompt_template is None:
            raise ValueError("Prompt template not configured. Call add_PromptTemplate() first.")
        
        # Initialize tracking variables
        tool_calls = []
        tool_results = []
        iteration = 0
        context = user_input
        
        # Loop until we get a final response or hit max iterations
        while iteration < max_iterations:
            iteration += 1
            
            # Format the prompt with tool list and current context
            tool_list_str = "\n        ".join(self.tool_descriptions) if self.tool_descriptions else "No tools available"
            formatted_prompt = self.prompt_template.format(
                tool_list=tool_list_str,
                user_input=context
            )
            
            # Get response from LLM
            llm_response = self._call_llm(formatted_prompt)
            
            # Parse the response
            parsed_response = self._parse_llm_response(llm_response)
            
            # Extract tool call and final response
            tool_call = parsed_response.get("Tool call", "None")
            final_response = parsed_response.get("Final Response", "None")
            
            # If we have a final response (not "None"), we're done
            if final_response != "None":
                return {
                    "tool_calls": tool_calls,
                    "tool_results": tool_results,
                    "final_response": final_response,
                    "iterations": iteration
                }
            
            # If tool call is needed, execute it
            if tool_call != "None" and tool_call in self.tools:
                try:
                    tool_func = self.tools[tool_call]
                    tool_result = tool_func(context)
                    
                    # Track the tool call and result
                    tool_calls.append(tool_call)
                    tool_results.append(tool_result)
                    
                    # Update context with tool result for next iteration
                    context = f"Original query: {user_input}\n\nTool '{tool_call}' returned: {tool_result}\n\nProvide a final response to the user based on this information."
                    
                except Exception as e:
                    error_msg = f"Error executing tool {tool_call}: {str(e)}"
                    tool_calls.append(tool_call)
                    tool_results.append(error_msg)
                    
                    return {
                        "tool_calls": tool_calls,
                        "tool_results": tool_results,
                        "final_response": f"I encountered an error while using the {tool_call} tool: {str(e)}",
                        "iterations": iteration
                    }
            else:
                # No tool call and no final response - something went wrong
                return {
                    "tool_calls": tool_calls,
                    "tool_results": tool_results,
                    "final_response": "I'm not sure how to help with that request.",
                    "iterations": iteration
                }
        
        # Max iterations reached without final response
        return {
            "tool_calls": tool_calls,
            "tool_results": tool_results,
            "final_response": f"I processed your request but reached the maximum number of steps ({max_iterations}). Tool results: {', '.join(tool_results) if tool_results else 'None'}",
            "iterations": iteration
        }
    
    def run(self, user_input: str, verbose: bool = True, max_iterations: int = 5) -> str:
        """
        Convenience method to invoke the agent and return just the final response.
        
        Args:
            user_input: The user's query or request
            verbose: Whether to print detailed information about the execution
            max_iterations: Maximum number of iterations to prevent infinite loops
        
        Returns:
            The final response string
        """
        result = self.invoke(user_input, max_iterations=max_iterations)
        
        if verbose:
            print(f"\n{'='*50}")
            print(f"User Query: {user_input}")
            print(f"{'='*50}")
            print(f"Status: {'✓ Success' if result['success'] else '✗ Failed'}")
            print(f"Iterations: {result['iterations']}")
            print(f"Execution Time: {result['execution_time']:.3f}s")
            
            if result['tool_calls']:
                print(f"Tools Called: {', '.join(result['tool_calls'])}")
                for i, (tool, tool_result) in enumerate(zip(result['tool_calls'], result['tool_results']), 1):
                    print(f"  Step {i} - {tool}: {tool_result}")
            else:
                print("No tools were called")
            
            if result['errors']:
                print(f"Errors: {len(result['errors'])}")
                for i, error in enumerate(result['errors'], 1):
                    print(f"  Error {i}: {error}")
                
            print(f"Final Response: {result['final_response']}")
            print(f"{'='*50}\n")
        
        return result['final_response']
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get execution statistics.
        
        Returns:
            Dictionary with execution statistics
        """
        success_rate = (self.successful_executions / self.total_executions * 100 
                       if self.total_executions > 0 else 0)
        
        return {
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "success_rate": f"{success_rate:.2f}%",
            "tools_available": len(self.tools),
            "tool_names": list(self.tools.keys()),
            "is_configured": self._is_configured(),
            "history_count": len(self.execution_history)
        }
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get execution history.
        
        Args:
            limit: Maximum number of recent executions to return (None for all)
        
        Returns:
            List of execution history dictionaries
        """
        if limit is None:
            return self.execution_history.copy()
        return self.execution_history[-limit:].copy() if self.execution_history else []
    
    def clear_history(self) -> None:
        """Clear execution history"""
        self.execution_history.clear()
        self._log("info", "Execution history cleared")
    
    def reset_stats(self) -> None:
        """Reset execution statistics"""
        self.total_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self._log("info", "Statistics reset")