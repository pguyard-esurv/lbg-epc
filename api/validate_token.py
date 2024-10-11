import requests
import uuid
import os

from dotenv import load_dotenv
load_dotenv()
LBG_SUBSCRIPTION_KEY = os.getenv('LBG_SUBSCRIPTION_KEY')
LBG_API_BASE_URL = os.getenv('LBG_API_BASE_URL')
LBG_API_ENV = os.getenv('LBG_API_ENV')

def validate_token(token):
    url = f'{LBG_API_BASE_URL}/homes/external-apis/{LBG_API_ENV}sustainability/v1/epc/token/'
    
    correlation_id = str(uuid.uuid4())

    headers = {
        'x-correlation-id': correlation_id,
        'Ocp-Apim-Subscription-Key': LBG_SUBSCRIPTION_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }

    data = {
        'token': token
    }
    
    return 'valid'

    try:
        response = requests.put(url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            json_response = response.json()
            status = json_response.get('payload', {}).get('status')
            return status  # Expected values: 'valid', 'invalid', 'expired', 'used'
        else:
            json_response = response.json()
            errors = json_response.get('errors', [])
            error_messages = '; '.join([f"{error.get('code')}: {error.get('message')}" for error in errors])
            return f"Error {response.status_code}: {error_messages}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"