
from decimal import Decimal
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('TOWERBANK_BASE_URL')
API_KEY = os.getenv('TOWERBANK_API_KEY')

class TowerbankAPI():

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRutime/7.31.3',
            'Authorization': f'Bearer {API_KEY}',

        }
    
    def get_client_account(self):
        url = f"{BASE_URL}/account"
        try:
            response = requests.get(url, headers=self.headers, data={})
        except Exception as e:
            raise ValueError(e)
        else:
            if response.status_code in [200, 201]:
                data = response.json()
                return data
            else:
                raise ValueError(response.text)
            
    def account_transaction(self, account_id, amount, transaction_type):
        url = f"{BASE_URL}/transaction"
        payload = {
            "accountId": account_id,
	        "amount": amount,
	        "transactionType": transaction_type
        }
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        except Exception as e:
            raise ValueError(e)
        else:
            if response.status_code in [200, 201]:
                data = response.json()
                return data
            else:
                raise ValueError(response.text)
    
    def get_provider_balance(self):
        url = f"{BASE_URL}/providers"
        try:
            response = requests.get(url, headers=self.headers, data={})
        except Exception as e:
            raise ValueError(e)
        else:
            if response.status_code in [200, 201]:
                data = response.json()
                return data
            else:
                raise ValueError(response.text)
            
    def provider_transaction(self, provider_from, provider_to, amount):
        url = f"{BASE_URL}/providerstransaction"
        payload = {
	        "from": provider_from,
	        "to": provider_to,
	        "amount": amount
        }
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        except Exception as e:
            raise ValueError(e)
        else:
            if response.status_code in [200, 201]:
                data = response.json()
                return data
            else:
                raise ValueError(response.text)

