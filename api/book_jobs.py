import requests

import os
from dotenv import load_dotenv
load_dotenv()

SH_API_KEY = os.getenv('SH_API_KEY')
SH_API_BASE_URL = os.getenv('SH_API_BASE_URL')

def book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number):

    url = f'{SH_API_BASE_URL}api/job'

    try:    
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': SH_API_KEY,
        }
        
        instruction_ref = 'instruction'
        product_name = 'Scottish EPC'
        
        data = f'''{{
            "instructionRef": "{instruction_ref}",
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

        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def book_ehouse_job(house_number, street, postcode, first_name, last_name, email_address, phone_number):
    #write this
    pass
