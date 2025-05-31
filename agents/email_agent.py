from langchain_core.messages import HumanMessage
from config import Config

class EmailAgent:
    def __init__(self):
        self.llm = Config.get_groq_chat()
    
    def process(self, email_content):
        messages = [
            Config.EMAIL_AGENT_PROMPT,
            HumanMessage(content=email_content)
        ]
        response = self.llm.invoke(messages)
        return response.content