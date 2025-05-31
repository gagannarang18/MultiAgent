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
            PdfReader(input_data)
            return "PDF"
        except:
            return self._llm_detect_format(input_data)
    
    def _llm_detect_format(self, input_data):
        messages = [
            Config.CLASSIFIER_PROMPT,
            HumanMessage(content=f"Input data: {str(input_data)[:1000]}")
        ]
        response = self.llm.invoke(messages)
        return response.content.get("format", "Unknown")
    
    def detect_intent(self, content):
        messages = [
            Config.CLASSIFIER_PROMPT,
            HumanMessage(content=f"Input data: {str(content)[:1000]}")
        ]
        response = self.llm.invoke(messages)
        return response.content.get("intent", "Other")
    
    def process(self, input_data):
        format = self.detect_format(input_data)
        intent = self.detect_intent(input_data)
        return format, intent