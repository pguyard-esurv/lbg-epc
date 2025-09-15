import base64
import os
import sys

import psycopg2
from dotenv import load_dotenv

from api.logging_config import configure_root_logger, get_logger

# Configure logging for this script
configure_root_logger()
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get the `z_ref` from the command-line arguments
if len(sys.argv) < 2:
    logger.error(
        "usage_error", extra={"message": "Usage: python3 signature_check.py <z_ref>"}
    )
    sys.exit(1)

z_ref = sys.argv[1]

# Database connection parameters
host = "10.180.10.132"
port = "5432"
user = "psqladmin"
database = "postgres"
password = os.getenv("DB_PASSWORD")

# Set up the connection
try:
    connection = psycopg2.connect(
        host=host, port=port, user=user, password=password, dbname=database
    )
    logger.info("db_connection_success", extra={"z_ref": z_ref})

    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute(
        "SELECT signature_data FROM lbg_epc_complete WHERE z_ref = %s;", (z_ref,)
    )

    # Fetch the data
    hex_data = cursor.fetchone()
    if hex_data is None:
        logger.warning("no_record_found", extra={"z_ref": z_ref})
        sys.exit(1)

    hex_data = hex_data[0]
    if isinstance(hex_data, memoryview):
        hex_data = hex_data.tobytes()

    # Decode the bytes to a string (if necessary)
    base64_data = hex_data.decode("utf-8")

    # Decode the base64 data
    image_data = base64.b64decode(base64_data)

    # Save the binary data to a PNG file
    output_file = f"{z_ref}_signature.png"
    with open(output_file, "wb") as f:
        f.write(image_data)
    logger.info("image_saved", extra={"output_file": output_file, "z_ref": z_ref})

    # Close the cursor and connection
    cursor.close()
    connection.close()

except Exception as e:
    logger.exception("failed_processing_signature", extra={"z_ref": z_ref})
