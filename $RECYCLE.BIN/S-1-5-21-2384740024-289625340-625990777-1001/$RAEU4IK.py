"""
ToolCall_Agent Package

An intelligent agent that can invoke tools based on user queries using LLMs.
"""

from .agent import ToolCall_Agent
from .prompt import prompt

__all__ = ['ToolCall_Agent', 'prompt']
__version__ = '1.0.0'
