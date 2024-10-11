from flask import Flask, request, redirect, jsonify, make_response
from flask_cors import CORS
from api.book_jobs import book_surveyhub_job, book_ehouse_job
from api.validate_token import validate_token
import os

from dotenv import load_dotenv
load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL')

import esurv_db_manager as es
app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

    #Mock - replace with DB call
def get_addresses_and_region(postcode):

    mock_addresses = [
        "123 High Street, W8 7QG",
        "456 Low Road, W8 7QG",
        "789 Side Lane, W8 7QG"
    ]
    
    mock_region = "Scotland"

    return mock_addresses, mock_region

@app.route('/', methods=['GET'])
def index():
    #token = request.headers.get('token')
    token = '12345'
    
    validity = validate_token(token)
    if validity == 'valid':
        response = make_response(redirect(FRONTEND_URL))
        #response.set_cookie('jwt', jwt_token)
        return response
    else:
        return 'Invalid Token'
        
    
@app.route('/api/get-addresses', methods=['POST'])
def get_addresses():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting JSON"}), 400
    
    data = request.get_json()
    
    postcode = data.get('postcode')
    token = data.get('token')

    if not postcode or not token:
        return jsonify({"error": "Missing postcode or token"}), 400
    
    addresses, region = get_addresses_and_region(postcode)

    if addresses is None or region is None:
        return jsonify({"error": "Invalid token or postcode"}), 400
    
    response = {
        "addresses": addresses,
        "region": region
    }
    
    return jsonify(response), 200

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        #need to unpack these from data. Need to separate names and house number/street. Maybe ask for more detailed info from MI for addresses
        
        house_number = '123'
        street = 'Street St'
        postcode = 'W8 7QG'
        
        first_name = 'Firstname'
        last_name = 'Lastname'
        
        email_address = 'name@address.com'
        phone_number = '07123456789'
        
        if data['region'] == 'Scotland':
            book_surveyhub_job(house_number, street, postcode, first_name, last_name, email_address, phone_number)
        else:
            book_ehouse_job(house_number, street, postcode, first_name, last_name, email_address, phone_number)
            

        return jsonify({"message": "Form data received successfully"}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to process form data"}), 400

if __name__ == "__main__":
    app.run(debug=True)


