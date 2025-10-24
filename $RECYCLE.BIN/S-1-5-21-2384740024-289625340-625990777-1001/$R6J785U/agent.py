import json
from typing import List, Any, Optional


class ReasonCall_Agent:
    """
    Intelligent agent that uses reasoning to determine which agent to call
    or provide a final response to the user.
    """
    
    def __init__(self, llm: Any, prompt_template: str, agents: List[Any]):
        """
        Initialize the ReasonCall_Agent.
        
        Args:
            llm: Language model instance for generating responses
            prompt_template: Template string for the agent's prompts
            agents: List of available agents that can be called
        """
        self.llm = llm
        self.prompt_template = prompt_template
        self.agents = agents
        self.name = "ReasonCall_Agent"
        self.chat_history = []
    
    def _format_chat_history(self) -> str:
        """Format the chat history into a readable string."""
        if not self.chat_history:
            return "No previous messages."
        
        history_str = ""
        for entry in self.chat_history:
            history_str += f"{entry['role']}: {entry['content']}\n"
        return history_str.strip()
    
    def _parse_response(self, response: str) -> dict:
        """
        Parse the JSON response from the LLM.
        
        Args:
            response: Raw response string from LLM
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try to parse the response as JSON
            parsed = json.loads(response.strip())
            return parsed
        except json.JSONDecodeError:
            # If parsing fails, return a default error structure
            return {
                "Thinking": "None",
                "Agent call": "None",
                "Final Response": f"Error parsing response: {response}"
            }
    
    def _find_agent_by_name(self, agent_name: str) -> Optional[Any]:
        """
        Find an agent by its name.
        
        Args:
            agent_name: Name of the agent to find
            
        Returns:
            Agent instance if found, None otherwise
        """
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None
    
    def process(self, user_input: str) -> dict:
        """
        Process user input and determine the appropriate action.
        
        Args:
            user_input: User's message/query
            
        Returns:
            Dictionary containing the agent's response
        """
        # Add user input to chat history
        self.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Format the prompt with chat history
        formatted_prompt = self.prompt_template.format(
            chat_history=self._format_chat_history()
        )
        
        # Get response from LLM
        # Note: This assumes the llm has a generate method
        # You may need to adjust this based on your actual LLM implementation
        llm_response = self.llm.generate(formatted_prompt + f"\nUser: {user_input}")
        
        # Parse the response
        parsed_response = self._parse_response(llm_response)
        
        # Add assistant response to chat history
        self.chat_history.append({
            "role": "assistant",
            "content": json.dumps(parsed_response)
        })
        
        return parsed_response
    
    def execute(self, user_input: str) -> str:
        """
        Execute the full agent workflow including calling other agents if needed.
        
        Args:
            user_input: User's message/query
            
        Returns:
            Final response string to present to the user
        """
        response = self.process(user_input)
        
        # If thinking is active, return the thinking process
        if response.get("Thinking") != "None":
            return f"Thinking: {response['Thinking']}"
        
        # If an agent call is requested
        if response.get("Agent call") != "None":
            agent_name = response["Agent call"]
            target_agent = self._find_agent_by_name(agent_name)
            
            if target_agent:
                # Call the target agent
                # This assumes agents have an execute method
                agent_result = target_agent.execute(user_input)
                return f"Agent {agent_name} response: {agent_result}"
            else:
                return f"Error: Agent '{agent_name}' not found"
        
        # Return the final response
        if response.get("Final Response") != "None":
            return response["Final Response"]
        
        return "No valid response generated"
    
    def reset_history(self):
        """Clear the chat history."""
        self.chat_history = []
