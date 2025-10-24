"""
OpenAI LLM Adapter - Implements LLMInterface for OpenAI.
This is a template/placeholder for OpenAI integration.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_interface import LLMInterface


class OpenAILLM(LLMInterface):
    """
    Adapter for OpenAI LLM.
    Implements the LLMInterface for OpenAI models.
    
    Note: This is a placeholder. Install openai package and implement as needed.
    """
    
    def __init__(self, model_name: str = "gpt-4", api_key: str = None, **kwargs):
        """
        Initialize OpenAI LLM.
        
        Args:
            model_name: Name of the OpenAI model
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(model_name, **kwargs)
        
        # Get API key
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided and not found in environment")
        
        # Note: Uncomment and implement when openai package is installed
        # import openai
        # self.client = openai.OpenAI(api_key=self.api_key)
        
        raise NotImplementedError(
            "OpenAI adapter is a placeholder. "
            "Install openai package and implement the methods."
        )
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate response from OpenAI.
        
        Args:
            prompt: The prompt to send to OpenAI
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            The generated response as a string
        """
        # Placeholder implementation
        # response = self.client.chat.completions.create(
        #     model=self.model_name,
        #     messages=[{"role": "user", "content": prompt}],
        #     **kwargs
        # )
        # return response.choices[0].message.content
        raise NotImplementedError("OpenAI adapter not implemented")
    
    def generate_streaming_response(self, prompt: str, **kwargs):
        """
        Generate streaming response from OpenAI.
        
        Args:
            prompt: The prompt to send to OpenAI
            **kwargs: Additional parameters
            
        Yields:
            Response chunks as they arrive
        """
        # Placeholder implementation
        raise NotImplementedError("OpenAI streaming not implemented")
    
    def get_model_info(self) -> dict:
        """Get information about the current OpenAI model."""
        info = super().get_model_info()
        info["provider"] = "OpenAI"
        return info
