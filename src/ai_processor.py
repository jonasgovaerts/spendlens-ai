import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIProcessor:
    def __init__(self):
        self.api_base = os.getenv('LMSTUDIO_API_BASE', 'http://localhost:1234/v1')
        self.model = os.getenv('LMSTUDIO_MODEL', 'default-model')
    
    def get_category_from_ai(self, description, account):
        """Query LM Studio API to categorize the transaction"""
        try:
            # Prepare the prompt for the AI model
            prompt = f"""
            Categorize this transaction based on its description and account:
            
            Description: {description}
            Account: {account}
            
            Please respond with ONLY the category name. 
            Use one of these categories if they match:
            
            - Income
            - Groceries
            - Food & Dining
            - Transport
            - Housing
            - Insurance
            - Healthcare
            - Children & Family
            - Clothing & Shoes
            - Personal Care
            - Leisure & Culture & Events
            - Household
            - Subscriptions
            - Banking
            - Taxes & Government
            - Transfers
            - Gifts & Donations
            - Miscellaneous
            
            If the description doesn't clearly fit any category, respond with "Other".
            Do not create your own categories!
            """
            
            # Prepare API request
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a financial transaction categorization assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
            
            # Send request to LM Studio API
            response = requests.post(
                f"{self.api_base}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                category = result['choices'][0]['message']['content'].strip()
                return category
            else:
                print(f"Error from AI API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error processing with AI: {e}")
            return None