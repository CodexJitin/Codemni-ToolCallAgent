"""
Agent Configuration - Defines different agent behaviors and response formats.
Makes it easy to create agents with different prompts and JSON structures.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ResponseFormat:
    """
    Defines the expected response format from an agent.
    Allows different agents to use different JSON structures.
    """
    # Keys expected in the JSON response
    required_keys: List[str]
    
    # Optional: mapping of internal names to JSON keys
    # Example: {"tool": "Tool call", "params": "Tool Parameters"}
    key_mapping: Dict[str, str] = field(default_factory=dict)
    
    # Optional: default values for keys
    defaults: Dict[str, Any] = field(default_factory=dict)
    
    def get_json_key(self, internal_name: str) -> str:
        """Get the JSON key name for an internal field name."""
        return self.key_mapping.get(internal_name, internal_name)
    
    def get_internal_name(self, json_key: str) -> str:
        """Get the internal name for a JSON key."""
        reverse_map = {v: k for k, v in self.key_mapping.items()}
        return reverse_map.get(json_key, json_key)


@dataclass
class AgentConfig:
    """
    Complete configuration for an agent type.
    Defines prompt template, response format, and behavior.
    """
    # Agent metadata
    name: str
    description: str
    
    # Prompt template with placeholders
    prompt_template: str
    
    # Expected response format
    response_format: ResponseFormat
    
    # Agent behavior settings
    max_iterations: int = 10
    verbose: bool = False
    
    # Optional: specific instructions or rules
    special_instructions: str = ""
    
    # Optional: examples for the prompt
    examples: List[str] = field(default_factory=list)


# ==================== PREDEFINED AGENT CONFIGURATIONS ====================

# Standard ToolCall Agent (your current format)
TOOLCALL_AGENT_CONFIG = AgentConfig(
    name="ToolCallAgent",
    description="Agent that calls tools based on JSON responses with Tool call, Tool Parameters, Final Response",
    prompt_template="""
You are an intelligent agent designed by Codemni Team.
Always respond in valid JSON format with exactly the following three keys in every response:
    "Tool call" — the tool to invoke to complete the user request.
        You have access to the following tools:
        {tool_list}
        Use "None" if no tool is needed.

    "Tool Parameters" — a dictionary of parameters required by the tool.
        Provide the parameters as key-value pairs based on the tool's requirements.
        Use "None" if no tool is being called.

    "Final Response" — the final message delivered to the user in natural language.
        Use "None" if you need to call a tool first and wait for its result.
        Only provide a Final Response when you have enough information to answer the user.
        If a tool was called and you received its result, use that information to provide a helpful Final Response.

query: {user_input}
""",
    response_format=ResponseFormat(
        required_keys=["Tool call", "Tool Parameters", "Final Response"],
        key_mapping={
            "tool": "Tool call",
            "params": "Tool Parameters", 
            "response": "Final Response"
        },
        defaults={
            "Tool call": "None",
            "Tool Parameters": "None",
            "Final Response": "None"
        }
    )
)

# Action Agent (different JSON structure)
ACTION_AGENT_CONFIG = AgentConfig(
    name="ActionAgent",
    description="Agent that performs actions with a simpler response format",
    prompt_template="""
You are an action-oriented assistant.
Respond in JSON format with these keys:
    "action" — the action to perform (tool name or "respond")
    "input" — the input for the action
    "output" — your response to the user (or "pending" if action needed)

Available actions:
{tool_list}

query: {user_input}
""",
    response_format=ResponseFormat(
        required_keys=["action", "input", "output"],
        key_mapping={
            "tool": "action",
            "params": "input",
            "response": "output"
        },
        defaults={
            "action": "respond",
            "input": "None",
            "output": ""
        }
    )
)

# ReACT Agent (Reason + Act pattern)
REACT_AGENT_CONFIG = AgentConfig(
    name="ReActAgent", 
    description="Agent that reasons before acting (ReACT pattern)",
    prompt_template="""
You are a reasoning agent that follows the ReACT pattern.
Respond in JSON with these keys:
    "thought" — your reasoning about what to do
    "action" — the tool to use (or "None")
    "action_input" — parameters for the tool
    "answer" — final answer (or "None" if action needed)

Available tools:
{tool_list}

query: {user_input}
""",
    response_format=ResponseFormat(
        required_keys=["thought", "action", "action_input", "answer"],
        key_mapping={
            "tool": "action",
            "params": "action_input",
            "response": "answer",
            "reasoning": "thought"
        },
        defaults={
            "thought": "",
            "action": "None",
            "action_input": "None",
            "answer": "None"
        }
    )
)

# Simple Function Call Agent (minimalist)
FUNCTION_AGENT_CONFIG = AgentConfig(
    name="FunctionAgent",
    description="Minimalist agent with simple function call format",
    prompt_template="""
You are a function-calling assistant.
Respond in JSON:
    "function" — function name or null
    "args" — function arguments or null
    "result" — your response or null

Functions available:
{tool_list}

query: {user_input}
""",
    response_format=ResponseFormat(
        required_keys=["function", "args", "result"],
        key_mapping={
            "tool": "function",
            "params": "args",
            "response": "result"
        },
        defaults={
            "function": None,
            "args": None,
            "result": None
        }
    )
)

# Chain of Thought Agent
COT_AGENT_CONFIG = AgentConfig(
    name="ChainOfThoughtAgent",
    description="Agent that shows step-by-step reasoning",
    prompt_template="""
You are a step-by-step reasoning agent.
Respond in JSON:
    "reasoning_steps" — list of your thinking steps
    "tool_needed" — tool name or "None"
    "tool_args" — tool arguments or "None"
    "final_answer" — your answer or "None"

Tools:
{tool_list}

query: {user_input}
""",
    response_format=ResponseFormat(
        required_keys=["reasoning_steps", "tool_needed", "tool_args", "final_answer"],
        key_mapping={
            "tool": "tool_needed",
            "params": "tool_args",
            "response": "final_answer",
            "reasoning": "reasoning_steps"
        },
        defaults={
            "reasoning_steps": [],
            "tool_needed": "None",
            "tool_args": "None",
            "final_answer": "None"
        }
    )
)


# Registry of all predefined configs
AGENT_CONFIGS = {
    "toolcall": TOOLCALL_AGENT_CONFIG,
    "action": ACTION_AGENT_CONFIG,
    "react": REACT_AGENT_CONFIG,
    "function": FUNCTION_AGENT_CONFIG,
    "cot": COT_AGENT_CONFIG,
}


def get_agent_config(config_name: str) -> AgentConfig:
    """Get a predefined agent configuration by name."""
    if config_name not in AGENT_CONFIGS:
        raise ValueError(f"Unknown agent config: {config_name}. Available: {list(AGENT_CONFIGS.keys())}")
    return AGENT_CONFIGS[config_name]


def create_custom_config(
    name: str,
    prompt_template: str,
    required_keys: List[str],
    key_mapping: Optional[Dict[str, str]] = None,
    **kwargs
) -> AgentConfig:
    """
    Create a custom agent configuration.
    
    Args:
        name: Agent name
        prompt_template: Prompt with {tool_list} and {user_input} placeholders
        required_keys: JSON keys expected in response
        key_mapping: Mapping of internal names to JSON keys
        **kwargs: Additional AgentConfig parameters
    """
    response_format = ResponseFormat(
        required_keys=required_keys,
        key_mapping=key_mapping or {}
    )
    
    return AgentConfig(
        name=name,
        description=kwargs.get("description", f"Custom {name}"),
        prompt_template=prompt_template,
        response_format=response_format,
        max_iterations=kwargs.get("max_iterations", 10),
        verbose=kwargs.get("verbose", False)
    )
