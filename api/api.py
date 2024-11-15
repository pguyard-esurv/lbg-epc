from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, render_template, make_response
from flask_cors import CORS
import os
from functools import wraps
import sentry_sdk
import psycopg2
from datetime import datetime
import json
import psycopg2
import os
import sentry_sdk

load_dotenv()
PROD_STATUS = os.getenv('PROD_STATUS')
SENTRY_DSN = os.getenv('SENTRY_DSN')
BACKEND_URL = os.getenv('BACKEND_URL')
LBG_URL = os.getenv('LBG_URL')

sentry_sdk.init(
    dsn=SENTRY_DSN,
)

if PROD_STATUS == 'dev':
    from api.book_ehouse_job import book_ehouse_job
    from api.book_surveyhub_job import book_surveyhub_job
    from api.validate_token import validate_token
else:
    from book_ehouse_job import book_ehouse_job
    from book_surveyhub_job import book_surveyhub_job
    from validate_token import validate_token

static_folder = os.path.join('..', 'client', 'build') if PROD_STATUS == 'dev' else 'staticfiles'
app = Flask(__name__, static_folder=static_folder, static_url_path='')

allowed_origins = [
    f"{os.getenv('LBG_URL')}",
    f"{os.getenv('BACKEND_URL')}",
    'http://localhost:3000',
    'http://127.0.0.1:5000',
    'wa-lbgepc-prd.azurewebsites.net'
]



CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

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

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        
        # If the token is already validated in cookies, proceed
        if request.cookies.get('token_validated') == 'true':
            return f(*args, **kwargs)

        # If no token is provided, return an error
        if not token:
            return render_template('error.html')

        # Call the validation API only if a token is provided
        validity = validate_token(token)
        print('*' * 15)
        print('Validation API called - validity is:')
        print(validity)
        print('*' * 15)
        
        # Check the validity of the token
        if validity != 'valid':
            return render_template('error.html')

        # Set a cookie to indicate the token has been validated
        response = make_response(f(*args, **kwargs))
        response.set_cookie('token_validated', 'true', httponly=True, samesite='Strict')
        
        return response
    return decorated_function

def get_z_ref():
    try:
        cnx = psycopg2.connect(
            user="psqladmin",
            password=os.getenv('DB_PASSWORD'),
            host="10.180.10.132",
            port=5432,
            database="postgres"
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(z_ref) FROM lbg_epc_complete;")
        result = cursor.fetchone()
        latest_z_ref = result[0]
        z_ref = 900000 if latest_z_ref is None else latest_z_ref + 1
        cursor.close()
        cnx.close()
        return z_ref

    except Exception as e:
        print("An error occurred:", e)
        sentry_sdk.capture_exception(e)
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def log_epc_submission(full_name, email_address, phone_number, address, api_call, signature, date, complete, z_ref):
    cnx = psycopg2.connect(
        user="psqladmin",
        password=os.getenv('DB_PASSWORD'),
        host="10.180.10.132",
        port=5432,
        database="postgres"
    )

    cursor = cnx.cursor()

    try:

        query = """
            INSERT INTO lbg_epc_complete (
                z_ref, full_name, email_address, phone_number, address, api_call, signature_data, todays_date, complete
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        data = (
            z_ref,
            full_name,
            email_address,
            phone_number,
            str(address),
            api_call,
            f"{signature}".encode('utf-8'),
            date,
            complete
        )
        
        cursor.execute(query, data)
        cnx.commit()

    except Exception as e:
        print("An error occurred:", e)
        sentry_sdk.capture_exception(e)

    finally:
        cursor.close()
        cnx.close()

# Routes

@app.route('/api/get-addresses', methods=['POST'])
def get_addresses():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting JSON"}), 400
    
    data = request.data
    data = json.loads(data)
    
    postcode = data.get('postcode')
    if not postcode:
        return jsonify({"error": "Missing postcode"}), 400
    
    addresses = get_addresses_from_db(postcode)
    return jsonify({"addresses": addresses}), 200

@app.route('/api/submit-form', methods=['OPTIONS', 'POST'])
def submit_form():
    # Helper function to get a valid origin from the request
    def get_origin_from_request():
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            return origin
        return None

    if request.method == 'OPTIONS':
        # Handle preflight request
        origin = get_origin_from_request()
        if origin:
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, sentry-trace, baggage'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        return make_response(jsonify({"error": "CORS origin not allowed"}), 403)

    if request.method == 'POST':
        origin = get_origin_from_request()
        if not origin:
            return jsonify({"error": "CORS origin not allowed"}), 403

        # Set the default response values
        full_name, email_address, phone_number, address, api_call, signature = [''] * 6
        date = datetime.now()
        complete = -1

        try:
            # Parse JSON request data
            data = request.get_json()
            full_name = data.get('fullName', '')
            first_name, last_name = split_name(full_name)
            email_address = data.get('email', '')
            phone_number = data.get('telephone', '')
            address = data.get('selectedAddress', {})
            region = address.get('region', '')
            signature = data.get('signature', '')
            date = data.get('date', datetime.now())

            # Generate z_ref for logging if in production
            z_ref = get_z_ref() if PROD_STATUS == 'prod' else None

            # Process based on region
            if region == 'Scotland':
                book_surveyhub_job(
                    address.get('building_name_number', ''),
                    address.get('street', ''),
                    address.get('postcode', ''),
                    first_name,
                    last_name,
                    email_address,
                    phone_number,
                    z_ref
                )
                api_call = 'surveyhub'
            else:
                street_address = f"{address.get('building_name_number', '')} {address.get('street', '')}"
                book_ehouse_job(
                    street_address,
                    address.get('postcode', ''),
                    address.get('town', ''),
                    full_name,
                    email_address,
                    phone_number
                )
                api_call = 'ehouse'

            # Mark submission as complete and log in production
            complete = 1
            if PROD_STATUS == 'prod':
                log_epc_submission(full_name, email_address, phone_number, address, api_call, signature, date, complete, z_ref)

            response = jsonify({"message": "Form data received successfully"})
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response, 200

        except Exception as e:
            # Handle exceptions, log errors, and return a response
            sentry_sdk.capture_exception(e)
            print(f"An error occurred: {e}")
            complete = -1
            if PROD_STATUS == 'prod':
                log_epc_submission(full_name, email_address, phone_number, address, api_call, signature, date, complete, z_ref)
            return jsonify({"error": str(e)}), 400



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

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=16070400; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
    f"default-src 'self' {BACKEND_URL}; "
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
    "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
    "worker-src 'self' blob:; "
    f"connect-src 'self' {BACKEND_URL} https://o4506784279298048.ingest.us.sentry.io; "
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    return response

if __name__ == "__main__":
    app.run()
