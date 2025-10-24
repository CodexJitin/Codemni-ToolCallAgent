"""
Gemini LLM Adapter - Implements LLMInterface for Google Gemini.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

from core.llm_interface import LLMInterface


class GeminiLLM(LLMInterface):
    """
    Adapter for Google Gemini LLM.
    Implements the LLMInterface for Gemini models.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", api_key: str = None, **kwargs):
        """
        Initialize Gemini LLM.
        
        Args:
            model_name: Name of the Gemini model
            api_key: Google API key (if None, reads from GOOGLE_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(model_name, **kwargs)
        
        # Get API key
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not provided and not found in environment")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Create model
        self.model = genai.GenerativeModel(model_name)
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate response from Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            The generated response as a string
        """
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating response from Gemini: {str(e)}")
    
    def generate_streaming_response(self, prompt: str, **kwargs):
        """
        Generate streaming response from Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            **kwargs: Additional parameters
            
        Yields:
            Response chunks as they arrive
        """
        try:
            response = self.model.generate_content(prompt, stream=True, **kwargs)
            for chunk in response:
                if hasattr(chunk, 'text'):
                    yield chunk.text
        except Exception as e:
            raise RuntimeError(f"Error in streaming response from Gemini: {str(e)}")
    
    def get_model_info(self) -> dict:
        """Get information about the current Gemini model."""
        info = super().get_model_info()
        info["provider"] = "Google Gemini"
        return info
