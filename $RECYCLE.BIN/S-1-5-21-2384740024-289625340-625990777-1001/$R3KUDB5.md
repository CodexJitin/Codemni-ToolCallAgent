# Quick Start Guide - ToolCall Agent with Built-in LLM

## 🎯 What's New?

Users no longer need to write separate LLM initialization code! Simply specify:
1. **LLM Provider** (openai, anthropic, groq, google, ollama)
2. **Model Name**
3. **API Key**

The agent handles everything else automatically! 🎉

## ⚡ 30-Second Setup

### Before (Old Way - Complex ❌)
```python
# Users had to write this themselves:
from openai import OpenAI

class MyLLM:
    def __init__(self):
        self.client = OpenAI(api_key="...")
    
    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

llm = MyLLM()
agent = ToolCallAgent()
agent.add_llm(llm)
```

### After (New Way - Simple ✅)
```python
# Now users just do this:
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='your-key'
)
```

## 🚀 Usage Examples

### Example 1: OpenAI (Simplest)
```python
from ToolCall_Agent import ToolCallAgent

agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='sk-...'
)

agent.add_tool("calculator", "Do math", lambda x: eval(x))
print(agent.invoke("What is 2 + 2?"))
```

### Example 2: Using Environment Variables
```python
# Set environment variable first:
# export OPENAI_API_KEY="sk-..."

agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4'
    # No api_key needed - reads from env!
)
```

### Example 3: Different Providers
```python
# OpenAI
agent1 = ToolCallAgent(llm_provider='openai', model='gpt-4', api_key='...')

# Anthropic Claude
agent2 = ToolCallAgent(llm_provider='anthropic', model='claude-3-opus-20240229', api_key='...')

# Groq
agent3 = ToolCallAgent(llm_provider='groq', model='llama3-70b-8192', api_key='...')

# Google Gemini
agent4 = ToolCallAgent(llm_provider='google', model='gemini-pro', api_key='...')

# Ollama (Local - No API Key!)
agent5 = ToolCallAgent(llm_provider='ollama', model='llama2')
```

### Example 4: With Custom Parameters
```python
agent = ToolCallAgent(
    llm_provider='openai',
    model='gpt-4',
    api_key='sk-...',
    temperature=0.7,      # Custom parameter
    max_tokens=2000,      # Custom parameter
    verbose=True          # Enable colored logging
)
```

### Example 5: Set LLM After Creation
```python
agent = ToolCallAgent()

# Add tools first
agent.add_tool("my_tool", "Description", my_function)

# Set LLM later
agent.set_llm('openai', 'gpt-4', api_key='sk-...')

# Now invoke
agent.invoke("My query")
```

## 📦 What's Included

### New Files:
1. **llm_providers.py** - All LLM provider wrappers
   - OpenAIWrapper
   - AnthropicWrapper
   - GroqWrapper
   - GoogleWrapper
   - OllamaWrapper
   - initialize_llm() function

2. **Updated agent.py** - Enhanced ToolCallAgent
   - Constructor accepts llm_provider, model, api_key
   - set_llm() method for later initialization
   - Backward compatible with add_llm()

3. **__init__.py** - Package initialization

4. **example_usage.py** - Complete examples

5. **demo.py** - Interactive demo script

6. **README.md** - Full documentation

## 🎮 Try the Demo!

```bash
python demo.py
```

The demo will:
1. Let you choose an LLM provider
2. Ask for your API key
3. Initialize the agent
4. Run example queries
5. Enter interactive mode

## 🔧 Installation

```bash
# Install your preferred LLM library
pip install openai          # For OpenAI
pip install anthropic       # For Anthropic
pip install groq            # For Groq
pip install google-generativeai  # For Google
pip install ollama          # For Ollama
```

## 🌟 Key Features

✅ **Zero Boilerplate** - No LLM initialization code needed  
✅ **Multi-Provider** - 5 popular LLM providers built-in  
✅ **Environment Variables** - Secure API key management  
✅ **Custom Parameters** - Pass any LLM-specific parameters  
✅ **Backward Compatible** - Old add_llm() still works  
✅ **Type Hints** - Full typing support  
✅ **Error Handling** - Clear error messages

## 📝 Supported Providers Summary

| Provider | Model Examples | Env Variable | Package |
|----------|---------------|--------------|---------|
| OpenAI | gpt-4, gpt-3.5-turbo | OPENAI_API_KEY | openai |
| Anthropic | claude-3-opus, claude-3-sonnet | ANTHROPIC_API_KEY | anthropic |
| Groq | llama3-70b-8192, mixtral-8x7b | GROQ_API_KEY | groq |
| Google | gemini-pro, gemini-1.5-pro | GOOGLE_API_KEY | google-generativeai |
| Ollama | llama2, mistral, codellama | OLLAMA_BASE_URL | ollama |

## 💡 Tips

1. **Use environment variables** in production for security
2. **Enable verbose=True** during development to see what's happening
3. **Install only what you need** - don't install all LLM packages
4. **Try Ollama** for free local testing without API keys

## 🐛 Troubleshooting

### "Import X could not be resolved"
```bash
# Install the missing package
pip install openai  # or anthropic, groq, etc.
```

### "API key not provided and X_API_KEY not set"
```bash
# Either pass api_key parameter:
agent = ToolCallAgent(llm_provider='openai', model='gpt-4', api_key='sk-...')

# Or set environment variable:
export OPENAI_API_KEY="sk-..."  # Linux/Mac
$env:OPENAI_API_KEY="sk-..."   # Windows PowerShell
```

### "Unsupported provider"
```python
# Make sure provider name is correct (lowercase):
# ✅ 'openai', 'anthropic', 'groq', 'google', 'ollama'
# ❌ 'OpenAI', 'gpt', 'claude'
```

## 🎉 That's It!

You now have a fully functional agent with built-in LLM support. No more writing initialization code - just specify the provider, model, and key!

---

**Created by:** codexJitin  
**Powered by:** Codemni
