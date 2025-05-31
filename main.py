from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.shared_memory import SharedMemory
import os
from dotenv import load_dotenv
import json
import traceback

load_dotenv()

class MultiAgentSystem:
    def __init__(self):
        self.classifier = ClassifierAgent()
        self.json_agent = JSONAgent()
        self.email_agent = EmailAgent()
        self.memory = SharedMemory()
    
    def process_input(self, input_data, conversation_id=None):
        try:
            print(f"\nProcessing input: {str(input_data)[:50]}...")
            format, intent = self.classifier.process(input_data)
            print(f"Classifier result: format={format}, intent={intent}")
            
            if format == "JSON":
                if isinstance(input_data, str):
                    try:
                        input_data = json.loads(input_data)
                    except:
                        pass
                result = self.json_agent.process(input_data)
            elif format == "Email":
                result = self.email_agent.process(input_data)
            else:
                result = {"error": f"Unsupported format: {format}"}
            
            print(f"Agent result: {result}")
            
            self.memory.log_context(
                source=str(input_data)[:100],
                format=format,
                intent=intent,
                extracted_fields=result,
                conversation_id=conversation_id
            )
            
            return {
                "status": "success",
                "format": format,
                "intent": intent,
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }

if __name__ == "__main__":
    system = MultiAgentSystem()
    
    # Test with sample email
    sample_email = """From: john.doe@example.com
To: support@company.com
Subject: Urgent Request for Quote
Body: Need pricing for 100 units of Product X. Delivery needed by next week."""

    print("\n" + "="*50)
    print("Processing Email:")
    result = system.process_input(sample_email)
    print(json.dumps(result, indent=2))
    
    # Test with sample JSON
    sample_json = {
        "invoice_number": "INV-2024-1001",
        "date": "2024-05-30",
        "customer": "Global Corp",
        "items": [
            {"name": "Service Package", "quantity": 1, "price": 999.99}
        ],
        "total": 999.99
    }
    
    print("\n" + "="*50)
    print("Processing JSON:")
    result = system.process_input(sample_json)
    print(json.dumps(result, indent=2))