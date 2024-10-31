from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from book_ehouse_job import book_ehouse_job
from book_surveyhub_job import book_surveyhub_job
from validate_token import validate_token
import os
from functools import wraps
import esurv_db_manager as es

load_dotenv()
PROD_STATUS = os.getenv('PROD_STATUS')

static_folder = os.path.join('..', 'client', 'build') if PROD_STATUS == 'dev' else 'staticfiles'

app = Flask(__name__, static_folder=static_folder, static_url_path='')

CORS(app)

# Helper functions

# Mock function - replace with DB call
def get_addresses_from_db(postcode):
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
            'region': 'Scotland',
        },
    ]
    return mock_addresses

def split_name(full_name):
    parts = full_name.split(" ")
    if len(parts) == 1:
        return "", parts[0]
    return " ".join(parts[:-1]), parts[-1]

#def validate_token(token):
#    return 'valid' if token == "xyz" else 'invalid'

# Decorator for token validation
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        validity = validate_token(token)
        print(validity)
        print(PROD_STATUS)
        if not token or validate_token(token) not in ('valid', 'used'):
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function

def log_epc_submission(full_name, email_address, phone_number, address, api_call, complete):
    print(full_name, email_address, phone_number, address, api_call, complete)

# Routes

@app.route('/', methods=['GET'])
def index():
    token = request.args.get('token')
    if token:
        validity = validate_token(token)
        return f"{validity}"
    else:
        return "no token"

@app.route('/external-page')
def simulate_external():
    return """
    <a href="/?token=valid">Simulate External Request</a>
    """
"""
# Initial token validation and serving React app with GET request
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@token_required
def serve_react(path):
    if path and (path.startswith("static/") or path.endswith((".js", ".css"))):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')
"""

@app.route('/api/get-addresses', methods=['POST'])
def get_addresses():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting JSON"}), 400
    
    data = request.get_json()
    postcode = data.get('postcode')
    if not postcode:
        return jsonify({"error": "Missing postcode"}), 400
    
    addresses = get_addresses_from_db(postcode)
    return jsonify({"addresses": addresses}), 200

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    full_name, email_address, phone_number, address, api_call = [''] * 5
    complete = -1
    try:
        data = request.get_json()
        full_name = data['fullName']
        first_name, last_name = split_name(full_name)
        email_address = data['email']
        phone_number = data['telephone']
        address = data['selectedAddress']
        region = address['region']
        
        

        if region == 'Scotland':
            book_surveyhub_job(address['building_name_number'], address['street'], address['postcode'], first_name, last_name, email_address, phone_number)
            api_call = 'surveyhub'
        else:
            street_address = f"{address['building_name_number']} {address['street']}"
            book_ehouse_job(street_address, address['postcode'], address['town'], full_name, email_address, phone_number)
            api_call = 'ehouse'
            
        complete = 1
        log_epc_submission(full_name, email_address, phone_number, address, api_call, complete)

        return jsonify({"message": "Form data received successfully"}), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        complete = -1
        log_epc_submission(full_name, email_address, phone_number, address, api_call, complete)
        return jsonify({"error": "Failed to process form data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
