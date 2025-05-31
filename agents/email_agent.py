import json
import re
from langchain_core.messages import HumanMessage
from config import Config

class EmailAgent:
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
                "sender": "unknown",
                "recipient": "unknown",
                "subject": "Processing failed",
                "intent": "Other",
                "urgency": "Low",
                "key_content": "Could not parse response"
            }
        except json.JSONDecodeError:
            return {
                "sender": "unknown",
                "recipient": "unknown",
                "subject": "JSON error",
                "intent": "Other",
                "urgency": "Low",
                "key_content": "JSON parsing failed"
            }
    
    def process(self, email_content):
        messages = [
            Config.EMAIL_AGENT_PROMPT,
            HumanMessage(content=email_content)
        ]
        try:
            response = self.llm.invoke(messages)
            return self._extract_json(response.content)
        except Exception as e:
            print(f"Email processing error: {e}")
            return {
                "sender": "unknown",
                "recipient": "unknown",
                "subject": "Processing failed",
                "intent": "Other",
                "urgency": "Low",
                "key_content": "Error occurred during processing"
            }