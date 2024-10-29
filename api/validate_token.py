import requests
import uuid
import os

from dotenv import load_dotenv
load_dotenv()
LBG_SUBSCRIPTION_KEY = os.getenv('LBG_SUBSCRIPTION_KEY')
LBG_API_BASE_URL = os.getenv('LBG_API_BASE_URL')
LBG_API_ENV = os.getenv('LBG_API_ENV')
PROD_STATUS = os.getenv('PROD_STATUS')

def validate_token(token):
    
    halifax_url = 'https://mortgages.secure.halifax-online.co.uk/home/external-apis/sustainability/epc/token'

    lloyds_url = 'https://mortgages.secure.lloydsbank.co.uk/home/external-apis/sustainability/epc/token'
    
    url = halifax_url

    
    correlation_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    headers = {
        'x-correlation-id': correlation_id,
        'x-session-id': session_id,
        'Ocp-Apim-Subscription-Key': LBG_SUBSCRIPTION_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }

    data = {
        'token': token
    }
    
    if PROD_STATUS == 'dev':
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