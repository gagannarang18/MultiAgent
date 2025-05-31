from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

class Config:
    GROQ_MODEL = "deepseek-r1-distill-llama-70b"
    GROQ_TEMPERATURE = 0.1
    
    @staticmethod
    def get_groq_chat():
        return ChatGroq(
            temperature=Config.GROQ_TEMPERATURE,
            model_name=Config.GROQ_MODEL,
        )
    
    CLASSIFIER_PROMPT = SystemMessage(content="""
    You are a classification agent. Identify:
    1. Input format (JSON, Email, or PDF)
    2. Intent (Invoice, RFQ, Complaint, etc.)
    Respond STRICTLY in JSON format with ONLY these keys:
    {"format": "...", "intent": "..."}
    """)
    
    JSON_AGENT_PROMPT = SystemMessage(content="""
    You are a JSON processing agent. Your tasks:
    1. Reformat input JSON to match target schema
    2. Identify anomalies
    3. Flag missing fields
    Respond STRICTLY in JSON format with ONLY these keys:
    {"formatted_data": {...}, "anomalies": [...], "missing_fields": [...]}
    """)
    
    EMAIL_AGENT_PROMPT = SystemMessage(content="""
    You are an email processing agent. Extract:
    - sender - recipient - subject
    - intent - urgency (Low/Medium/High)
    - key content
   Respond STRICTLY in JSON format with ONLY these keys:
    {"sender": "...", "recipient": "...", "subject": "...", "intent": "...", "urgency": "...", "key_content": "..."}

    """)