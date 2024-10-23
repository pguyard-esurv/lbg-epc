import requests
import os
from dotenv import load_dotenv
load_dotenv()

EHOUSE_API_BASE_URL = os.getenv('EHOUSE_API_BASE_URL')
EHOUSE_USERNAME = os.getenv('EHOUSE_USERNAME')
EHOUSE_PASSWORD = os.getenv('EHOUSE_PASSWORD')
EHOUSE_BRANCH_ID = os.getenv('EHOUSE_BRANCH_ID')
EHOUSE_BRANCH_SECRET = os.getenv('EHOUSE_BRANCH_SECRET')
EHOUSE_ACCOUNT_ACTIVATION_TOKEN = os.getenv('EHOUSE_ACCOUNT_ACTIVATION_TOKEN')

EHOUSE_ACCESS_TOKEN = os.getenv('EHOUSE_ACCESS_TOKEN')

def register_ehouse_api_account():
    """
    Here you will supply us with API user account information alongside with the branchId 
    and the branchSecret you recieved from our staff. If succesfull you will recieve an email 
    with a token to activate your account.
    """
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        "title": "string",
        "firstName": "string",
        "lastName": "string",
        "jobTitle": "string",
        "email": "string",
        "userName": EHOUSE_USERNAME,
        "password": EHOUSE_PASSWORD,
        "confirmPassword": EHOUSE_PASSWORD,
        "branchId": EHOUSE_BRANCH_ID,
        "branchSecret": EHOUSE_BRANCH_SECRET
    }

    url = EHOUSE_API_BASE_URL + 'Account/Register'

    response = requests.post(url=url, headers=headers, json=data)
    
    return response

def activate_ehouse_api_account():
    """
    This where you actiavte your APi account with the token you recieved from previous step.
    """

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        "userName": EHOUSE_USERNAME,
        "accountActivationToken": EHOUSE_ACCOUNT_ACTIVATION_TOKEN
    }
    
    url = EHOUSE_API_BASE_URL + 'Account/Activate'

    response = requests.post(url=url, headers=headers, json=data)
    
    return response

def get_ehouse_token():
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    }
    
    data = {
        'grant_type': 'password',
        'username': EHOUSE_USERNAME,
        'password': EHOUSE_PASSWORD,
    }

    response = requests.post('https://api.ehouse.co.uk/token', headers=headers, data=data, verify='d:\python\lib\site-packages\certifi\cacert.pem')
    return response

#token_response = get_ehouse_token()
#print(token_response)

response = requests.get('https://google.com', verify=True)
print(response)


headers = {
    'Accept': 'application/json',
    'Authorization': EHOUSE_ACCESS_TOKEN
}
response = requests.get('https://api.ehouse.co.uk/v2/KeyInvoiceItems', headers=headers, verify=True)
print(response)