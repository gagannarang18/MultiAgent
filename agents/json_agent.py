from langchain_core.messages import HumanMessage
from config import Config

class JSONAgent:
    def __init__(self):
        self.llm = Config.get_groq_chat()
    
    def process(self, json_data, target_schema=None):
        if not target_schema:
            target_schema = {
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "date": {"type": "string"},
                    "items": {"type": "array"},
                    "total": {"type": "number"},
                    "metadata": {"type": "object"}
                }
            }
        
        messages = [
            Config.JSON_AGENT_PROMPT,
            HumanMessage(content=f"""
            Target Schema: {target_schema}
            Input JSON: {json_data}
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content