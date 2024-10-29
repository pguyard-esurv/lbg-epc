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
    
    SH_API_KEY = 'c13f7b11-41b5-4a54-8d26-b6f3bd1e7dc1'
        
    headers = {
    'accept': '*/*',
    'X-API-KEY': SH_API_KEY,
    }
    
    SH_API_BASE_URL = 'https://esurv.surveyhublive.net/ExternalApi/'
    
    url = SH_API_BASE_URL + 'api/test/AuthTest'
    
    print(url)

    response = requests.get(url=url, headers=headers)
    
    return response

def get_job_details():
    
    SH_API_KEY = 'c13f7b11-41b5-4a54-8d26-b6f3bd1e7dc1'
    
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': SH_API_KEY,
    }
    
    SH_API_BASE_URL = 'https://esurv.surveyhublive.net/ExternalApi/'
    
    job_id = '018542ef-c479-422f-918d-0c132e2e1604'
    job_id = 'b05ea820-b682-426e-9a40-58824e6bb7bf'
    
    job_id = 'c62372d5-66e1-4373-af02-5b0c862f3fd9'
    
    es_ref = '903641' #UAT
    es_ref = '6209614' #Live
    
    url = SH_API_BASE_URL + 'api/job/' + job_id.upper() + '/jobDetails'
    
    url = SH_API_BASE_URL + 'api/job/' + es_ref

    
    print(url)

    response = requests.get(
        url=url,
        headers=headers,
    )
    
    return response

"""

response = test_sh_auth_api()
#response = get_job_details()

print(response.status_code)
print(response.text)


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

"""