"""
LLM Provider Wrappers for ToolCall Agent

Provides built-in support for popular LLM providers.
Created by: codexJitin
Powered by: Codemni
"""

import os
from typing import Optional


class LLMWrapper:
    """Base wrapper class for LLM integrations."""
    
    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement generate_response")


class OpenAIWrapper(LLMWrapper):
    """Wrapper for OpenAI models."""
    
    def __init__(self, model: str, api_key: str, **kwargs):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **self.kwargs
        )
        return response.choices[0].message.content


class AnthropicWrapper(LLMWrapper):
    """Wrapper for Anthropic Claude models."""
    
    def __init__(self, model: str, api_key: str, **kwargs):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.kwargs.pop('max_tokens', 4096),
            messages=[{"role": "user", "content": prompt}],
            **self.kwargs
        )
        return response.content[0].text


class GroqWrapper(LLMWrapper):
    """Wrapper for Groq models."""
    
    def __init__(self, model: str, api_key: str, **kwargs):
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("Please install groq: pip install groq")
        
        self.client = Groq(api_key=api_key)
        self.model = model
        self.kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **self.kwargs
        )
        return response.choices[0].message.content


class GoogleWrapper(LLMWrapper):
    """Wrapper for Google Gemini models."""
    
    def __init__(self, model: str, api_key: str, **kwargs):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Please install google-generativeai: pip install google-generativeai")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt, **self.kwargs)
        return response.text


class OllamaWrapper(LLMWrapper):
    """Wrapper for Ollama local models."""
    
    def __init__(self, model: str, base_url: str = "http://localhost:11434", **kwargs):
        try:
            from ollama import Client
        except ImportError:
            raise ImportError("Please install ollama: pip install ollama")
        
        self.client = Client(host=base_url)
        self.model = model
        self.kwargs = kwargs
    
    def generate_response(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **self.kwargs
        )
        return response['message']['content']


def initialize_llm(
    provider: str, 
    model: str, 
    api_key: Optional[str] = None,
    **kwargs
):
    """
    Initialize LLM with built-in support for popular providers.
    
    Args:
        provider: LLM provider ('openai', 'anthropic', 'groq', 'google', 'ollama')
        model: Model name
        api_key: API key (will try to read from environment if not provided)
        **kwargs: Additional arguments for the LLM client
        
    Returns:
        LLMWrapper instance
        
    Environment Variables:
        - OPENAI_API_KEY for OpenAI
        - ANTHROPIC_API_KEY for Anthropic
        - GROQ_API_KEY for Groq
        - GOOGLE_API_KEY for Google
        - OLLAMA_BASE_URL for Ollama (optional, defaults to http://localhost:11434)
        
    Examples:
        >>> llm = initialize_llm('openai', 'gpt-4', api_key='sk-...')
        >>> llm = initialize_llm('anthropic', 'claude-3-opus-20240229')  # reads from env
        >>> llm = initialize_llm('groq', 'llama3-70b-8192', temperature=0.7)
        >>> llm = initialize_llm('ollama', 'llama2')
    """
    provider = provider.lower()
    
    # Get API key from environment if not provided
    if api_key is None and provider != 'ollama':
        env_key_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'groq': 'GROQ_API_KEY',
            'google': 'GOOGLE_API_KEY'
        }
        env_var = env_key_map.get(provider)
        if env_var:
            api_key = os.environ.get(env_var)
            if not api_key:
                raise ValueError(
                    f"API key not provided and {env_var} environment variable not set. "
                    f"Please provide api_key or set {env_var}."
                )
    
    # Initialize the appropriate wrapper
    if provider == 'openai':
        return OpenAIWrapper(model, api_key, **kwargs)
    
    elif provider == 'anthropic':
        return AnthropicWrapper(model, api_key, **kwargs)
    
    elif provider == 'groq':
        return GroqWrapper(model, api_key, **kwargs)
    
    elif provider == 'google':
        return GoogleWrapper(model, api_key, **kwargs)
    
    elif provider == 'ollama':
        base_url = kwargs.pop('base_url', os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434'))
        return OllamaWrapper(model, base_url, **kwargs)
    
    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported providers: 'openai', 'anthropic', 'groq', 'google', 'ollama'"
        )
