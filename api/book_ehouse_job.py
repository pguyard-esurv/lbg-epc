import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
EHOUSE_USERNAME = os.getenv('EHOUSE_USERNAME')
EHOUSE_PASSWORD = os.getenv('EHOUSE_PASSWORD')
EHOUSE_API_BASE_URL = os.getenv('EHOUSE_API_BASE_URL')
EHOUSE_ACCESS_TOKEN = os.getenv('EHOUSE_ACCESS_TOKEN')
EHOUSE_KEY_INVOICE_ITEM_ID = os.getenv('EHOUSE_KEY_INVOICE_ITEM_ID')
EHOUSE_CLIENT_INVOICE_ITEM_CODE = os.getenv('EHOUSE_CLIENT_INVOICE_ITEM_CODE')

base_dir = os.path.dirname(os.path.abspath(__file__))
pem_file_path = os.path.join(base_dir, 'custom_ca_bundle.pem')

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
    
    url = EHOUSE_API_BASE_URL + 'token'

    response = requests.post(url=url, headers=headers, data=data, verify=pem_file_path)
    token_response_dict = json.loads(response.text)
    token = f'Bearer {token_response_dict["access_token"]}'
    return token

def get_key_invoice_item_id():

    headers = {
        'Accept': 'application/json',
        'Authorization': EHOUSE_ACCESS_TOKEN
    }

    url = EHOUSE_API_BASE_URL + 'v2/KeyInvoiceItems'

    response = requests.get(url=url, headers=headers, verify=pem_file_path)
    key_invoice_items = json.loads(response.text)
    items = key_invoice_items['keyInvoiceItemsList']
    for item in items:
        if item['clientInvoiceItemCode'] == EHOUSE_CLIENT_INVOICE_ITEM_CODE:
            return item['id']
    raise Exception('keyInvoiceItem id not found')

def send_book_ehouse_job_request(street_address, postcode, town, name, email_address, phone_number, key_invoice_item_id, ehouse_access_token):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': ehouse_access_token,
    }

    data = {
        "keyInvoiceItems": [
            {
                "id": key_invoice_item_id,
                "quantity": 1
            }
        ],
        "buildingNumber": "string",
        "buildingName": "string",
        "subBuilding": "string",
        "streetAddress": street_address, #required
        "town": town, #required
        "postcode": postcode, #required
        "sendVendorBookingSms": True, #required
        "sendVendorBookingEmail": True, #required
        "vendorName": name, #required
        "vendorTelephone": phone_number,
        "vendorEmail": email_address, #required
    }
    
    url = EHOUSE_API_BASE_URL + 'v2/Orders'

    response = requests.post(url=url, headers=headers, data=json.dumps(data), verify=pem_file_path)
    
    return response

def book_ehouse_job(street_address, postcode, town, name, email_address, phone_number):
    
    try:
        key_invoice_item_id = get_key_invoice_item_id()
    except:
        key_invoice_item_id = EHOUSE_KEY_INVOICE_ITEM_ID
    
    ehouse_access_token = EHOUSE_ACCESS_TOKEN
    
    response = send_book_ehouse_job_request(street_address, postcode, town, name, email_address, phone_number, key_invoice_item_id, ehouse_access_token)
    
    if response.status_code == 401:
        ehouse_access_token = get_ehouse_token()
        response = send_book_ehouse_job_request(street_address, postcode, town, name, email_address, phone_number, key_invoice_item_id, ehouse_access_token)
        if response.status_code != 200:
            raise Exception(response.json())
        #poss: send sentry email saying that the token is bad
    
    if response.status_code != 200:
            raise Exception(response.json())


street_address = '12345 Place St'
postcode = 'W8 7QG'
town = 'Gardenfield'
name = 'First Last'
email_address = 'name@domain.com'
phone_number = '07 123 456 789'

book_ehouse_job(street_address, postcode, town, name, email_address, phone_number)