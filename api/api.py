import json
import os
import time
import uuid
from datetime import datetime
from functools import wraps

import psycopg2
import sentry_sdk
from dotenv import load_dotenv
from flask import (
    Flask,
    g,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
)
from flask_cors import CORS

from api.logging_config import get_logger

# Use the LoggerAdapter so request_id is injected automatically into logs
logger = get_logger(__name__)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


load_dotenv()
PROD_STATUS = os.getenv("PROD_STATUS")
SENTRY_DSN = os.getenv("SENTRY_DSN")
BACKEND_URL = os.getenv("BACKEND_URL")
LBG_URL = os.getenv("LBG_URL")

sentry_sdk.init(
    dsn=SENTRY_DSN,
)

if PROD_STATUS == "dev":
    from api.book_ehouse_job import book_ehouse_job
    from api.book_surveyhub_job import book_surveyhub_job
    from api.validate_token import validate_token
else:
    from book_ehouse_job import book_ehouse_job
    from book_surveyhub_job import book_surveyhub_job
    from validate_token import validate_token

static_folder = (
    os.path.join("..", "client", "build") if PROD_STATUS == "dev" else "staticfiles"
)
app = Flask(__name__, static_folder=static_folder, static_url_path="")

allowed_origins = [
    f"{os.getenv('LBG_URL')}",
    f"{os.getenv('BACKEND_URL')}",
    "http://localhost:3000",
    "http://127.0.0.1:5000",
    "wa-lbgepc-prd.azurewebsites.net",
    "https://lbg-epc.esurv.co.uk",
]

CORS(
    app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True
)


# Mock function - replace with DB call
def get_addresses_from_db(postcode):
    mock_addresses = [
        {
            "building_name_number": "123",
            "street": "High Street",
            "town": "Newcastle upon Tyne",
            "postcode": "W8 7QG",
            "region": "England",
        },
        {
            "building_name_number": "Foundry Park",
            "street": "High Street",
            "town": "Newcastle upon Tyne",
            "postcode": "W8 7QG",
            "region": "England",
        },
        {
            "building_name_number": "789",
            "street": "Side Lane",
            "town": "Newcastle upon Tyne",
            "postcode": "W8 7QG",
            "region": "England",
        },
        {
            "building_name_number": "5",
            "street": "Lower Road",
            "town": "Newcastle upon Tyne",
            "postcode": "W8 7QG",
            "region": "Scotland",
        },
    ]
    return mock_addresses


def split_name(full_name: str | None) -> tuple[str, str]:
    """
    Split full name into first_name and last_name.

    Args:
        full_name: The full name to split. Can be None, empty, or contain various formats.

    Returns:
        A tuple of (first_name, last_name). Returns ("Unknown", "Unknown") for
        invalid/empty inputs.

    Examples:
        >>> split_name("John Smith")
        ('John', 'Smith')
        >>> split_name("John Michael Smith")
        ('John', 'Michael Smith')
        >>> split_name("Madonna")
        ('Madonna', 'Unknown')
        >>> split_name("")
        ('Unknown', 'Unknown')
    """
    # Handle None input explicitly
    if full_name is None:
        return "Unknown", "Unknown"

    # Handle empty or whitespace-only strings
    if not full_name or not full_name.strip():
        return "Unknown", "Unknown"

    # Clean and split the name - handles all types of whitespace
    parts = [part for part in full_name.strip().split() if part]

    if len(parts) == 1:
        return parts[0], "Unknown"
    else:
        return parts[0], " ".join(parts[1:])


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get("token")

        # If the token is already validated in cookies, proceed
        if request.cookies.get("token_validated") == "true":
            logger.info("token already validated via cookie")
            return f(*args, **kwargs)

        # If no token is provided, return an error
        if not token:
            logger.warning("no token provided in request")
            return render_template("error.html")

        # Call the validation API only if a token is provided
        validity = validate_token(token)
        logger.info(
            "validation API called",
            extra={"validity": validity},
        )

        # Check the validity of the token
        if validity != "valid":
            logger.warning(
                "token validation failed",
                extra={"validity": validity},
            )
            return render_template("error.html")

        # Set a cookie to indicate the token has been validated
        response = make_response(f(*args, **kwargs))
        response.set_cookie("token_validated", "true", httponly=True, samesite="Strict")

        logger.info("token validated and cookie set")

        return response

    return decorated_function


def get_z_ref():
    cursor = None
    cnx = None
    try:
        cnx = psycopg2.connect(
            user="psqladmin",
            password=os.getenv("DB_PASSWORD"),
            host="10.180.10.132",
            port=5432,
            database="postgres",
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(z_ref) FROM lbg_epc_complete;")
        result = cursor.fetchone()
        latest_z_ref = None
        if result:
            try:
                latest_z_ref = result[0]
            except Exception:
                latest_z_ref = None
        z_ref = 900000 if latest_z_ref is None else latest_z_ref + 1

        cursor.close()
        cnx.close()
        logger.info("generated z_ref", extra={"z_ref": z_ref})
        return z_ref

    except Exception as e:
        logger.exception("error getting z_ref")
        sentry_sdk.capture_exception(e)
        if "cursor" in locals() and cursor:
            cursor.close()
        if "cnx" in locals() and cnx:
            cnx.close()
        return None


def log_epc_submission(
    full_name,
    email_address,
    phone_number,
    address,
    api_call,
    signature,
    date,
    complete,
    z_ref,
):
    cnx = psycopg2.connect(
        user="psqladmin",
        password=os.getenv("DB_PASSWORD"),
        host="10.180.10.132",
        port=5432,
        database="postgres",
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
            f"{signature}".encode("utf-8"),
            date,
            complete,
        )

        cursor.execute(query, data)
        cnx.commit()
        logger.info(
            "logged epc submission to DB",
            extra={"z_ref": z_ref, "email": email_address, "complete": complete},
        )

    except Exception as e:
        logger.exception("error logging epc submission")
        sentry_sdk.capture_exception(e)

    finally:
        cursor.close()
        cnx.close()


# Routes


@app.route("/api/get-addresses", methods=["POST"])
def get_addresses():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting JSON"}), 400

    data = request.data
    data = json.loads(data)

    postcode = data.get("postcode")
    if not postcode:
        return jsonify({"error": "Missing postcode"}), 400
    # Structured log for address lookup requests
    logger.info(
        "get_addresses_called",
        extra={"postcode": postcode},
    )
    addresses = get_addresses_from_db(postcode)
    return jsonify({"addresses": addresses}), 200


@app.before_request
def start_request_logging():
    # assign a request id and start time
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    g.request_id = req_id
    g.start_time = time.time()
    logger.info(
        "request_start",
        extra={
            "method": request.method,
            "path": request.path,
            "remote_addr": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
        },
    )


@app.after_request
def log_request(response):
    duration_ms = int((time.time() - getattr(g, "start_time", time.time())) * 1000)
    status = getattr(response, "status_code", None)
    extra = {
        "method": request.method,
        "path": request.path,
        "status": status,
        "duration_ms": duration_ms,
    }
    logger.info("request_end", extra=extra)
    # Surface the request id to clients for correlation
    try:
        if getattr(g, "request_id", None):
            response.headers["X-Request-ID"] = getattr(g, "request_id")
    except Exception:
        # best-effort; don't fail the response if headers can't be set
        pass
    # ensure CORS headers remain as originally set where applicable
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception with structured data and forward to Sentry
    logger.exception("unhandled_exception")
    sentry_sdk.capture_exception(e)
    return render_template("error.html"), 500


@app.route("/api/submit-form", methods=["OPTIONS", "POST"])
def submit_form():
    # Helper function to get a valid origin from the request
    def get_origin_from_request():
        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            return origin
        return None

    if request.method == "OPTIONS":
        # Handle preflight request
        origin = get_origin_from_request()
        if origin:
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type, Authorization, sentry-trace, baggage"
            )
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response
        return make_response(jsonify({"error": "CORS origin not allowed"}), 403)
    if request.method == "POST":
        origin = get_origin_from_request()
        if not origin:
            return jsonify({"error": "CORS origin not allowed"}), 403

        # Log receipt of the form submission (request_start already logs basic request info)
        logger.info(
            "submit_form_received",
            extra={
                "origin": origin,
                "remote_addr": request.remote_addr,
            },
        )

        # Set the default response values
        full_name, email_address, phone_number, address, api_call, signature = [""] * 6
        date = datetime.now()
        complete = -1
        surveyhub_success = False
        z_ref = None

        try:
            # Parse JSON request data
            data = request.get_json()
            full_name = data.get("fullName", "")
            first_name, last_name = split_name(full_name)
            email_address = data.get("email", "")
            phone_number = data.get("telephone", "")
            address = data.get("selectedAddress", {})
            region = address.get("region", "")
            signature = data.get("signature", "")
            date = data.get("date", datetime.now())

            # Generate z_ref for logging if in production
            if PROD_STATUS == "prod":
                z_ref = get_z_ref()
            else:
                z_ref = None

            # Process based on region
            if region == "Scotland":
                response = book_surveyhub_job(
                    address.get("building_name_number", ""),
                    address.get("street", ""),
                    address.get("postcode", ""),
                    first_name,
                    last_name,
                    email_address,
                    phone_number,
                    z_ref,
                )
                status_code = getattr(response, "status_code", None)
                surveyhub_success = status_code == 200
                logger.info(
                    "surveyhub_api_result",
                    extra={
                        "status_code": status_code,
                        "api": "surveyhub",
                        "z_ref": z_ref,
                    },
                )
                api_call = "surveyhub"
            else:
                street_address = f"{address.get('building_name_number', '')} {address.get('street', '')}"
                book_ehouse_job(
                    street_address,
                    address.get("postcode", ""),
                    address.get("town", ""),
                    full_name,
                    email_address,
                    phone_number,
                )
                response = book_surveyhub_job(
                    address.get("building_name_number", ""),
                    address.get("street", ""),
                    address.get("postcode", ""),
                    first_name,
                    last_name,
                    email_address,
                    phone_number,
                    z_ref,
                )
                status_code = getattr(response, "status_code", None)
                surveyhub_success = status_code == 200
                logger.info(
                    "surveyhub_api_result",
                    extra={
                        "status_code": status_code,
                        "api": "ehouse+surveyhub",
                        "z_ref": z_ref,
                    },
                )
                api_call = "ehouse"

            # Set complete status based on SurveyHub API success
            complete = 1 if surveyhub_success else -1
            if PROD_STATUS == "prod":
                log_epc_submission(
                    full_name,
                    email_address,
                    phone_number,
                    address,
                    api_call,
                    signature,
                    date,
                    complete,
                    z_ref,
                )

            response = jsonify({"message": "Form data received successfully"})
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response, 200

        except Exception as e:
            # Handle exceptions, log errors, and return a response
            sentry_sdk.capture_exception(e)
            logger.exception("An error occurred during submit_form")
            # Even if other things fail, preserve API success status
            complete = 1 if surveyhub_success else -1
            if PROD_STATUS == "prod":
                log_epc_submission(
                    full_name,
                    email_address,
                    phone_number,
                    address,
                    api_call,
                    signature,
                    date,
                    complete,
                    z_ref,
                )
            response = jsonify({"message": "Form data received successfully"})
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response, 200


# Route to serve custom static files from the main API folder
@app.route("/api-static/<path:filename>")
def serve_api_static(filename):
    return send_from_directory(os.path.dirname(__file__), filename)


# Route to serve React app and ensure correct file paths
@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
@token_required
def serve_react(path):
    # Serve React static files or index.html
    if path and (path.startswith("static/") or path.endswith((".js", ".css"))):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            return (
                jsonify({"error": f"The requested file '{path}' was not found."}),
                404,
            )

    # Serve index.html as a fallback
    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.isfile(index_path):
        return send_from_directory(app.static_folder, "index.html")
    else:
        return (
            jsonify({"error": "The main page is unavailable. Please contact support."}),
            404,
        )


@app.after_request
def add_security_headers(response):
    response.headers["Strict-Transport-Security"] = (
        "max-age=16070400; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        f"default-src 'self' {BACKEND_URL}; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        "worker-src 'self' blob:; "
        f"connect-src 'self' {BACKEND_URL} https://o4506784279298048.ingest.us.sentry.io; "
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Cache-Control"] = "no-cache, no-store"
    return response


if __name__ == "__main__":
    app.run()
