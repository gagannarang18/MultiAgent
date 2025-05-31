import json
import re
from langchain_core.messages import HumanMessage
from config import Config
from pypdf import PdfReader

class ClassifierAgent:
    def __init__(self):
        self.llm = Config.get_groq_chat()
    
    def detect_format(self, input_data):
        if isinstance(input_data, dict):
            return "JSON"
        elif isinstance(input_data, str) and input_data.lower().startswith("from:"):
            return "Email"
        try:
            if isinstance(input_data, str):
                with open(input_data, 'rb') as f:
                    PdfReader(f)
            else:
                PdfReader(input_data)
            return "PDF"
        except:
            return self._llm_detect_format(input_data)
    
    def _extract_json(self, text):
        """Extract JSON from LLM response text"""
        try:
            # Look for JSON-like patterns
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {"format": "Unknown", "intent": "Other"}
        except json.JSONDecodeError:
            return {"format": "Unknown", "intent": "Other"}
    
    def _llm_detect_format(self, input_data):
        messages = [
            Config.CLASSIFIER_PROMPT,
            HumanMessage(content=f"Input data: {str(input_data)[:1000]}")
        ]
        try:
            response = self.llm.invoke(messages)
            response_dict = self._extract_json(response.content)
            return response_dict.get("format", "Unknown")
        except Exception as e:
            print(f"Format detection error: {e}")
            return "Unknown"
    
    def detect_intent(self, content):
        messages = [
            Config.CLASSIFIER_PROMPT,
            HumanMessage(content=f"Input data: {str(content)[:1000]}")
        ]
        try:
            response = self.llm.invoke(messages)
            response_dict = self._extract_json(response.content)
            return response_dict.get("intent", "Other")
        except Exception as e:
            print(f"Intent detection error: {e}")
            return "Other"
    
    def process(self, input_data):
        format = self.detect_format(input_data)
        intent = self.detect_intent(input_data)
        return format, intent