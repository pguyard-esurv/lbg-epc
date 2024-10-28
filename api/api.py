from flask import Flask, request, redirect, jsonify, make_response
from flask_cors import CORS
from api.book_ehouse_job import book_ehouse_job
from api.book_surveyhub_job import book_surveyhub_job
from api.validate_token import validate_token
import os

from dotenv import load_dotenv
load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL')

import esurv_db_manager as es
app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

    #Mock - replace with DB call
def get_addresses_from_db(postcode):
    
    'building_name_number' #concatenate from buildingname and buildingnumber from the address db
    'street' #addr1 in the address db
    'town' #posttown in the address db
    'postcode'
    'region' #country in the address db
    
    mock_addresses = [
        
        {
            'building_name_number': '123',
            'street': 'High Street',
            'town': 'Newcastle upon Tyne',
            'postcode': 'W8 7QG',
            'region': 'England',
            },
        {
            'building_name_number': 'Foundry Park',
            'street': 'High Street',
            'town': 'Newcastle upon Tyne',
            'postcode': 'W8 7QG',
            'region': 'England',
            },
        {
            'building_name_number': '789',
            'street': 'Side Lane',
            'town': 'Newcastle upon Tyne',
            'postcode': 'W8 7QG',
            'region': 'England',
            },
        {
            'building_name_number': '5',
            'street': 'Lower Road',
            'town': 'Newcastle upon Tyne',
            'postcode': 'W8 7QG',
            'region': 'England',
            },
    ]

    return mock_addresses

def split_name(full_name):
    parts = full_name.split(" ")
    
    if len(parts) == 1:
        # If there's only one name, treat it as the last name with an empty first name
        first_name = ""
        last_name = parts[0]
    else:
        # Otherwise, join all parts except the last one for the first name
        first_name = " ".join(parts[:-1])
        last_name = parts[-1]
    
    return first_name, last_name

@app.route('/', methods=['GET'])
def index():
    #token = request.headers.get('token')
    token = '12345'
    
    validity = validate_token(token)
    if validity == 'valid':
        response = make_response(redirect(FRONTEND_URL))
        return response
    else:
        return 'Invalid Token'
    
@app.route('/api/get-addresses', methods=['POST'])
def get_addresses():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting JSON"}), 400
    
    data = request.get_json()
    
    print(data)
    
    postcode = data.get('postcode')

    if not postcode:
        return jsonify({"error": "Missing postcode"}), 400
    
    addresses = get_addresses_from_db(postcode)

    if addresses is None:
        return jsonify({"error": "Invalid token or postcode"}), 400
    
    response = {
        "addresses": addresses,
    }
    
    return jsonify(response), 200

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        full_name = data['fullName']
        first_name, last_name = split_name(full_name)
        
        email_address = data['email']
        phone_number = data['telephone']
        
        house_number = data['selectedAddress']['building_name_number']
        street = data['selectedAddress']['street']
        town = data['selectedAddress']['town']
        postcode = data['selectedAddress']['postcode']
        region = data['selectedAddress']['region']
        
        if region == 'Scotland':
            book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number)
        else:
            street_address = house_number + ' ' + street
            
            print(street_address, postcode, town, full_name, email_address, phone_number)

            book_ehouse_job(street_address, postcode, town, full_name, email_address, phone_number)
            

        return jsonify({"message": "Form data received successfully"}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to process form data"}), 400

if __name__ == "__main__":
    app.run(debug=True)


