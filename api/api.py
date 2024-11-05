from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from functools import wraps
import esurv_db_manager as es
import sentry_sdk

load_dotenv()
PROD_STATUS = os.getenv('PROD_STATUS')
SENTRY_DSN = os.getenv('SENTRY_DSN')

sentry_sdk.init(
    dsn=SENTRY_DSN,
)

if PROD_STATUS == 'dev':
    from api.book_ehouse_job import book_ehouse_job
    from api.book_surveyhub_job import book_surveyhub_job, sh_api_auth_test, sh_api_test
    from api.validate_token import validate_token
else:
    from book_ehouse_job import book_ehouse_job
    from book_surveyhub_job import book_surveyhub_job, sh_api_auth_test, sh_api_test
    from validate_token import validate_token

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

# Decorator for token validation
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        validity = validate_token(token)
        print(validity)
        if not token or validate_token(token) not in ('valid', 'used'):
            return render_template('error.html', message='Invalid or missing token')
        return f(*args, **kwargs)
    return decorated_function

def log_epc_submission(full_name, email_address, phone_number, address, api_call, complete):
    print(full_name, email_address, phone_number, address, api_call, complete)

# Routes

"""

@app.route('/')
def index():
    response1 = sh_api_test()
    response2 = sh_api_auth_test()
    response = str((response1.status_code, response2.status_code))
    print(response)
    
    full_name = 'john smith'
    email_address = 'name@domain.com'
    phone_number = '07444155435'
    street_address = '1234567 street'
    postcode = 'W8 7QG'
    town = 'townsville'

    book_ehouse_job(street_address, postcode, town, full_name, email_address, phone_number)

    
    return response

"""
@app.route('/')
def index():
    from esurv_db_manager import EPC_DB
    pg_db = EPC_DB()
    pg_conn = pg_db.connect()
    pg_db.disconnect()
    return "success"

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
        sentry_sdk.capture_exception(e)
        print(f"An error occurred: {e}")
        complete = -1
        log_epc_submission(full_name, email_address, phone_number, address, api_call, complete)
        error_message = str(e)
        return jsonify({"error": error_message}), 400


# Route to serve custom static files from the main API folder
@app.route('/api-static/<path:filename>')
def serve_api_static(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

# Route to serve React app and ensure correct file paths
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@token_required
def serve_react(path):
    # Serve React static files or index.html
    if path and (path.startswith("static/") or path.endswith((".js", ".css"))):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            return jsonify({"error": f"The requested file '{path}' was not found."}), 404

    # Serve index.html as a fallback
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.isfile(index_path):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return jsonify({"error": "The main page is unavailable. Please contact support."}), 404

"""

if __name__ == "__main__":
    app.run()
