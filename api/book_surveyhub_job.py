import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SH_API_KEY = os.getenv('SH_API_KEY')
SH_API_BASE_URL = os.getenv('SH_API_BASE_URL')

def book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number):

    url = SH_API_BASE_URL + 'api/job'

    try:    
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': SH_API_KEY,
        }
        
        instruction_ref = 'instruction'
        product_name = 'Energy Performance'
        product_name = 'Mortgage Valuation'
        
        data = f'''{{
            "instructionRef": '{instruction_ref}',
            "CompanyName": "string",
            "LenderName": "Lloyds",
            "LenderRef": "",
            "InstructedBy": "",
            "products": [
                {{
                    "name": "{product_name}"
                }}
            ],
            "address": {{
                "houseNumber": "{house_number}",
                "street": "{street}",
                "postcode": "{postcode}"
            }},
            "contacts": [
                {{
                    "firstName": "{first_name}",
                    "lastName": "{last_name}",
                    "emailAddress": "{email_address}",
                    "phoneNumbers": [
                        {{
                            "telephoneNumber": "{phone_number}"
                        }}
                    ]
                }}
            ]
        }}'''

        response = requests.post(
            url=url,
            headers=headers,
            data=data,
        )

        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
def test_sh_auth_api():
        
    headers = {
    'accept': '*/*',
    'X-API-KEY': SH_API_KEY,
    }
    
    SH_API_BASE_URL = 'https://esurv.surveyhublive.net/externalapi/'
    
    url = SH_API_BASE_URL + 'api/test/AuthTest'

    response = requests.get(url=url, headers=headers)
    
    return response

response = test_sh_auth_api()
print(response.status_code)


house_number = '123'
street = 'Place St.'
postcode = 'W8 7QG'
first_name = 'First'
last_name = 'Last'
email_address = 'name@domain.com'
phone_number = '07 123 456 789'

#response = book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number)
#print(response.status_code)
#print(response.json())
