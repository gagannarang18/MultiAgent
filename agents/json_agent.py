import json
import re
from langchain_core.messages import HumanMessage
from config import Config

class JSONAgent:
    def __init__(self):
        self.llm = Config.get_groq_chat()
    
    def _extract_json(self, text):
        """Extract JSON from LLM response text"""
        try:
            # Look for JSON-like patterns
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {
                "formatted_data": {},
                "anomalies": ["Invalid response format"],
                "missing_fields": []
            }
        except json.JSONDecodeError:
            return {
                "formatted_data": {},
                "anomalies": ["JSON parsing error"],
                "missing_fields": []
            }
    
    def process(self, json_data, target_schema=None):
        if not target_schema:
            target_schema = {
                "sender": {"type": "string"},
                "date": {"type": "string"},
                "items": {"type": "array"},
                "total": {"type": "number"},
                "metadata": {"type": "object"}
            }
        
        messages = [
            Config.JSON_AGENT_PROMPT,
            HumanMessage(content=f"""
            ### TARGET SCHEMA ###
            {target_schema}
            
            ### INPUT JSON ###
            {json_data}
            """)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return self._extract_json(response.content)
        except Exception as e:
            print(f"JSON processing error: {e}")
            return {
                "formatted_data": {},
                "anomalies": ["Processing failed"],
                "missing_fields": []
            }