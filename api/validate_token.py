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
    
    halifax_url = 'https://mortgages.secure.halifax-online.co.uk/homes/external-apis/sustainability/v1/epc/token'

    lloyds_url = 'https://mortgages.secure.lloydsbank.co.uk/home/external-apis/sustainability/epc/token'
    
    url = halifax_url
    
    correlation_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    headers = {
        'x-correlation-id': correlation_id,
        'x-session-id': session_id,
        'Ocp-Apim-Subscription-Key': LBG_SUBSCRIPTION_KEY,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent':'e.surv-user',
        'origin': 'https://lbg-epc.esurv.co.uk/',
        'Referer': 'https://lbg-epc.esurv.co.uk/'
    }

    data = {
        'token': token
    }

    try:
        response = requests.put(url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            json_response = response.json()
            status = json_response.get('status')
            return status  # Expected values: 'valid', 'invalid', 'expired', 'used'
        else:
            json_response = response.json()
            errors = json_response.get('errors', [])
            error_messages = '; '.join([f"{error.get('code')}: {error.get('message')}" for error in errors])
            return f"Error {response.status_code}: {error_messages}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

"""

PROD_STATUS = 'prod'

token = '43edc231106d834b894f364087232c5a:7e2d040228b35f18b7c043786ac73b9c344a92d0c92bd9a5d5457cf694ff6bb4069e9cc540424cf9e42ed52a628f69cb6d40e52b5f237871c73dec4a3c13f924073c275d218ff3a9af67805310f25376c2c29db8e9f6f901d535f6158b59c06ac05d322bd7b14bd04a44c99c522433fe'

token = 'xx1234567ax123bx456cx789dx00123456789e'

token = 'valid'

token = '7c2f4e002d10b82d583ddc82:9350aefef679d5b2e7fde4d75c7abfc7798e4282c10d479445042b1cbc00e4dac7733510953b1e40b0259de10a8d8e3be94163a059abb36d564bb9007ce1e3d174b99e41a23525dc8795052bd2834160c99331248405bf7769a6d28df886e75061c3:a57532340bc1ce453d1b81bbd30e4686'

token = 'valid'                                          

validity = validate_token(token)

print(validity)

"""