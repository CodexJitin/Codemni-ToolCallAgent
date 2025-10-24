"""
Response Parser - Handles parsing of LLM responses.
Reusable across different agent types.
"""

import re
import json
from typing import Dict, Any, Tuple, Optional


class ResponseParser:
    """
    Parses LLM responses into structured formats.
    Supports multiple response formats.
    """
    
    @staticmethod
    def parse_json_response(response: str, required_keys: list = None) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        
        Args:
            response: Raw response string from LLM
            required_keys: List of required keys in the JSON
            
        Returns:
            Parsed JSON as dictionary
            
        Raises:
            ValueError: If JSON parsing fails or required keys are missing
        """
        # Extract JSON block with ```json or '''json markers
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
        if not json_match:
            json_match = re.search(r"'''json\s*(\{.*?\})\s*'''", response, re.DOTALL)
        
        if not json_match:
            raise ValueError(f"No JSON block found in response: {response[:200]}")
        
        try:
            parsed_json = json.loads(json_match.group(1))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        
        # Validate required keys if provided
        if required_keys:
            missing_keys = [key for key in required_keys if key not in parsed_json]
            if missing_keys:
                raise ValueError(f"Missing required keys: {missing_keys}")
        
        return parsed_json
    
    @staticmethod
    def parse_tool_call_response(response: str) -> Tuple[Dict, Dict, Dict]:
        """
        Parse tool call response with three components.
        
        Args:
            response: Raw response string from LLM
            
        Returns:
            Tuple of (tool_call_dict, tool_parameters_dict, final_response_dict)
        """
        required_keys = ["Tool call", "Tool Parameters", "Final Response"]
        parsed_json = ResponseParser.parse_json_response(response, required_keys)
        
        # Create separate dicts for each component
        tool_call = {"Tool call": parsed_json.get("Tool call", "None")}
        tool_parameters = {"Tool Parameters": parsed_json.get("Tool Parameters", "None")}
        final_response = {"Final Response": parsed_json.get("Final Response", "None")}
        
        return tool_call, tool_parameters, final_response
    
    @staticmethod
    def extract_code_blocks(response: str, language: Optional[str] = None) -> list:
        """
        Extract code blocks from markdown response.
        
        Args:
            response: Response string containing code blocks
            language: Optional language filter (e.g., 'python', 'javascript')
            
        Returns:
            List of code block strings
        """
        if language:
            pattern = rf"```{language}\s*(.*?)\s*```"
        else:
            pattern = r"```(?:\w+)?\s*(.*?)\s*```"
        
        code_blocks = re.findall(pattern, response, re.DOTALL)
        return code_blocks
    
    @staticmethod
    def parse_key_value_pairs(response: str) -> Dict[str, str]:
        """
        Parse key-value pairs from response.
        Format: "key: value" or "key = value"
        
        Args:
            response: Response string
            
        Returns:
            Dictionary of key-value pairs
        """
        pairs = {}
        lines = response.split('\n')
        
        for line in lines:
            # Match "key: value" or "key = value"
            match = re.match(r'\s*([^:=]+)\s*[:=]\s*(.+)', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                pairs[key] = value
        
        return pairs
