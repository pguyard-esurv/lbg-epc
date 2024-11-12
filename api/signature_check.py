import os
import sys
import psycopg2
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the `z_ref` from the command-line arguments
if len(sys.argv) < 2:
    print("Usage: python3 signature_check.py <z_ref>")
    sys.exit(1)

z_ref = sys.argv[1]

# Database connection parameters
host = "10.180.10.132"
port = "5432"
user = "psqladmin"
database = "postgres"
password = os.getenv('DB_PASSWORD')

# Set up the connection
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=database
    )
    print("Connected to the PostgreSQL database successfully!")

    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT signature_data FROM lbg_epc_complete WHERE z_ref = %s;", (z_ref,))
    
    # Fetch the data
    hex_data = cursor.fetchone()
    if hex_data is None:
        print(f"No record found for z_ref = {z_ref}")
        sys.exit(1)
    
    hex_data = hex_data[0]
    if isinstance(hex_data, memoryview):
        hex_data = hex_data.tobytes()
    
    # Decode the bytes to a string (if necessary)
    base64_data = hex_data.decode('utf-8')
    
    # Decode the base64 data
    image_data = base64.b64decode(base64_data)
    
    # Save the binary data to a PNG file
    output_file = f"{z_ref}_signature.png"
    with open(output_file, 'wb') as f:
        f.write(image_data)
    
    print(f"Image saved as {output_file}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

except Exception as e:
    print("Failed to connect to the PostgreSQL database or process data.")
    print("Error:", e)
