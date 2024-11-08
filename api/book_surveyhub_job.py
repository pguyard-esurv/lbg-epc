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
        
        instruction_ref = 900012
        
        data = {
            "instructionRef": instruction_ref,
            "CompanyName": "e.surv Chartered Surveyors",
            "LenderName": "LBG EPC",
            "LenderRef": instruction_ref,
            "InstructedBy": "LBG EPC",
            "products": [
                {
                    "name": "Energy Performance 2",
                    "buyToLet": False,
                    "payableByClient": True,
                    "payableByCustomer": False,
                    "homeSurveySettings": None
                }
            ],
            "address": {
                "subBuildingName": None,
                "houseName": None,
                "houseNumber": house_number,
                "dependentThoroughFareName": None,
                "street": street,
                "doubleDependentLocality": None,
                "dependentLocality": None,
                "town": None,
                "postcode": postcode,
                "propertyType": 'unknown',
                "detachmentType": 'unknown',
                "propertyTenure": 'unknown',
                "numberOfBedrooms": 0
            },
            "contacts": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "salutation": 'unknown',
                    "firstName": first_name,
                    "lastName": last_name,
                    "emailAddress": email_address,
                    "isPrimaryContact": False,
                    "isApplicant": True,
                    "isPropertyOwner": False,
                    "isOccupier": False,
                    "isAgency": False,
                    "companyName": None,
                    "useJobAddress": True,
                    "unknownAddress": True,
                    "availableFrom": "00:00:00",
                    "availableTo": "00:00:00",
                    "isKeyHolder": True,
                    "isUnverified": False,
                    "isAppointmentContact": True,
                    "address": None,
                    "phoneNumbers": [
                        {
                            "telephoneNumber": phone_number,
                            "isPrimary": True,
                            "isMobile": True
                        }
                    ]
                },
            ],
            "appointmentDetails": None,
            "estimatedValue":  0,
            "amountOfAdvance": 0.0,
            "vacantProperty": False,
            "newBuild": False,
            "rightToBuy": False,
            "concessionaryPurchase": False,
            "surveyorNotes": None,
            "overrideCustomerChargeNetFee": None,
            "overrideCustomerChargeVatAmount": None,
            "termsAndConditionsUrl": None
        }

        json_data = json.dumps(data, indent=4)

        response = requests.post(
            url=url,
            headers=headers,
            data=json_data,
        )

        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return e

def sh_api_test():
    headers = {
    'accept': '*/*',
    }
    
    url = SH_API_BASE_URL + 'api/test'

    response = requests.get(url=url, headers=headers)
    return response

def sh_api_auth_test():
    headers = {
    'accept': '*/*',
    'X-API-KEY': SH_API_KEY,
    }

    url = SH_API_BASE_URL + 'api/test/AuthTest'

    response = requests.get(url=url, headers=headers)
    return response


"""

house_number = '123456789012345'
street = 'Street Place.'
postcode = 'W8 7QG'
first_name = 'First'
last_name = 'Last'
email_address = 'name@domain.com'
phone_number = '07 123 456 789'

response = book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number)
print(response.status_code)
print(response.json())

"""