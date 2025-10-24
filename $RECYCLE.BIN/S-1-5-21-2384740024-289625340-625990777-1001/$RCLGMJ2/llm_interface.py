"""
LLM Interface - Abstract base class for different LLM providers.
Allows easy swapping between different LLM providers.
"""

from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """
    Abstract base class for LLM providers.
    Implement this to add support for different LLMs (OpenAI, Anthropic, etc.)
    """
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters for the LLM
            
        Returns:
            The generated response as a string
        """
        pass
    
    @abstractmethod
    def generate_streaming_response(self, prompt: str, **kwargs):
        """
        Generate a streaming response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters for the LLM
            
        Yields:
            Response chunks as they arrive
        """
        pass
    
    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return {
            "model_name": self.model_name,
            "config": self.config
        }
