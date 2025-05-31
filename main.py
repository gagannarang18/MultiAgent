from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.shared_memory import SharedMemory
import os
from dotenv import load_dotenv
import json
import traceback  # Add this import

load_dotenv()

class MultiAgentSystem:
    def __init__(self):
        self.classifier = ClassifierAgent()
        self.json_agent = JSONAgent()
        self.email_agent = EmailAgent()
        self.memory = SharedMemory()
    
    def process_input(self, input_data):
        try:
            format, intent = self.classifier.process(input_data)
            
            if format == "JSON":
                result = self.json_agent.process(input_data)
            elif format == "Email":
                result = self.email_agent.process(input_data)
            else:
                result = {"error": f"Unsupported format: {format}"}

            self.memory.log_context(
                source=str(input_data)[:100],
                format=format,
                intent=intent,
                extracted_fields=result
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
Subject: Urgent Request
Body: Need immediate assistance with product defect"""
    
    print("Processing Email:")
    print(json.dumps(system.process_input(sample_email), indent=2))
    
    # Test with sample JSON
    sample_json = {
        "order_id": "12345",
        "customer": "Acme Corp",
        "total": 299.99
    }
    
    print("\nProcessing JSON:")
    print(json.dumps(system.process_input(sample_json), indent=2))