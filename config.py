from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

class Config:
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE = 0.1
    
    @staticmethod
    def get_groq_chat():
        return ChatGroq(
            temperature=Config.GROQ_TEMPERATURE,
            model_name=Config.GROQ_MODEL,
        )
    
    CLASSIFIER_PROMPT = SystemMessage(content="""
    ### INSTRUCTIONS ###
    1. Analyze the input data
    2. Determine the FORMAT (JSON, Email, or PDF)
    3. Determine the INTENT (Invoice, RFQ, Complaint, Regulation, Other)
    
    ### RESPONSE FORMAT ###
    Return ONLY JSON with these exact keys:
    {
        "format": "detected_format",
        "intent": "detected_intent"
    }
    
    ### EXAMPLE ###
    Input: "From: user@example.com\nSubject: Invoice #123"
    Response: {"format": "Email", "intent": "Invoice"}
    """)
    
    JSON_AGENT_PROMPT = SystemMessage(content="""
    ### INSTRUCTIONS ###
    1. Reformat the input JSON to match this schema:
    {
        "sender": string,
        "date": string,
        "items": array,
        "total": number,
        "metadata": object
    }
    2. Identify any anomalies
    3. List missing required fields
    
    ### RESPONSE FORMAT ###
    Return ONLY JSON with these exact keys:
    {
        "formatted_data": {...},
        "anomalies": ["...", "..."],
        "missing_fields": ["...", "..."]
    }
    """)
    
    EMAIL_AGENT_PROMPT = SystemMessage(content="""
    ### INSTRUCTIONS ###
    Extract these fields from the email:
    - sender (email address)
    - recipient (email address)
    - subject
    - intent (Invoice, RFQ, Complaint, Regulation, Other)
    - urgency (Low, Medium, High)
    - key_content (summary of main points)
    
    ### RESPONSE FORMAT ###
    Return ONLY JSON with these exact keys:
    {
        "sender": "...",
        "recipient": "...",
        "subject": "...",
        "intent": "...",
        "urgency": "...",
        "key_content": "..."
    }
    """)