# To run this code you need to install the following dependencies:
# pip install google-genai

import os
import json
from google import genai
from google.genai import types
from agent.ReasonCall_Agent import init_ReasonCall_Agent


class GeminiLLM:
    """Wrapper class for Google Gemini LLM to work with ReasonCall_Agent."""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_instruction = """You are an intelligent virtual assistant.
Always respond in valid JSON format with exactly the following three keys in every response:

"Thinking" — a concise summary of the reasoning or thought process the assistant is following to generate the next step or final response.
    Use "None" if no reasoning needs to be displayed.
    Important: If "Thinking" is not "None", then "Final Response" must be "None".

"Agent call" — the agent to invoke to complete the user request.
    Examples: "Weather_Agent", "PC_Agent", "System_Agent", etc.
    Use "None" if no tool is needed.

"Final Response" — the final message delivered to the user in natural language.
    Use "None" if no final response is needed or if "Thinking" is not "None".
    If no reasoning or agent call is required, provide the response here.

Rules:
    - Only use these three keys in the JSON.
    - "Thinking" and "Final Response" are mutually exclusive: only one can have content at a time.
    - Never add any text outside the JSON.
    - Always capitalize the keys exactly as shown.
    - The JSON must always be valid."""
    
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        
        config = types.GenerateContentConfig(
            system_instruction=[types.Part.from_text(text=self.system_instruction)],
            temperature=0.7,
        )
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )
        
        return response.text if response.text else ""


class DummyAgent:
    """Dummy agent for demonstration purposes."""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, user_input: str) -> str:
        """Execute the agent's task."""
        return f"{self.name} processed: {user_input}"


def test_basic_generation():
    """Test basic Gemini generation."""
    print("=" * 50)
    print("Testing Basic Gemini Generation")
    print("=" * 50)
    
    client = genai.Client(
        api_key=os.environ.get("GOOGLE_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="How are you?"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        system_instruction=[
            types.Part.from_text(text="""You are an intelligent virtual assistant.
Always respond in valid JSON format with exactly the following three keys in every response:

"Thinking" — a concise summary of the reasoning or thought process the assistant is following to generate the next step or final response.

Use "None" if no reasoning needs to be displayed.

Important: If "Thinking" is not "None", then "Final Response" must be "None".

"Agent call" — the agent to invoke to complete the user request.

Examples: "Weather_Agent", "PC_Agent", "System_Agent", etc.

Use "None" if no tool is needed.

"Final Response" — the final message delivered to the user in natural language.

Use "None" if no final response is needed or if "Thinking" is not "None".

If no reasoning or agent call is required, provide the response here.

Rules:

Only use these three keys in the JSON.

"Thinking" and "Final Response" are mutually exclusive: only one can have content at a time.

Never add any text outside the JSON.

Always capitalize the keys exactly as shown.

The JSON must always be valid."""),
        ],
    )

    print("\nResponse (streaming):")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    print("\n")


def test_reason_call_agent():
    """Test the ReasonCall_Agent implementation."""
    print("=" * 50)
    print("Testing ReasonCall_Agent")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("\nError: GOOGLE_API_KEY environment variable not set!")
        print("Please set it using: $env:GOOGLE_API_KEY = 'your-api-key-here'")
        return
    
    # Create LLM instance
    llm = GeminiLLM(api_key=api_key)
    
    # Create dummy agents
    dummy_agents = [
        DummyAgent("Weather_Agent"),
        DummyAgent("PC_Agent"),
        DummyAgent("System_Agent"),
    ]
    
    # Initialize ReasonCall_Agent
    reason_agent = init_ReasonCall_Agent(llm, dummy_agents)
    
    # Test queries
    test_queries = [
        "What's the weather like today?",
        "Hello, how are you?",
        "Can you check my PC status?",
    ]
    
    print(f"\nAvailable agents: {', '.join([a.name for a in dummy_agents])}\n")
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = reason_agent.process(query)
        print(f"Agent Response: {json.dumps(response, indent=2)}")
        print("-" * 50)


if __name__ == "__main__":
    # Test basic generation
    #test_basic_generation()
    
    print("\n" + "=" * 50 + "\n")
    
    # Test ReasonCall_Agent
    test_reason_call_agent()
