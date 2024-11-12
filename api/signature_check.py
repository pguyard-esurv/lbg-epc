import os
import psycopg2
import base64
from dotenv import load_dotenv
load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')

# Database connection parameters
host = "10.180.10.132"
port = "5432"
user = "psqladmin"
database = "postgres"
password = DB_PASSWORD

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
    cursor.execute("SELECT signature_data FROM lbg_epc_complete WHERE z_ref='908112';")
    
    # Fetch the data
    hex_data = cursor.fetchone()[0]
    if isinstance(hex_data, memoryview):
        hex_data = hex_data.tobytes()
    
    # Decode the bytes to a string (if necessary)
    base64_data = hex_data.decode('utf-8')
    
    # Decode the base64 data
    image_data = base64.b64decode(base64_data)
    
    # Save the binary data to a PNG file
    with open('output_image.png', 'wb') as f:
        f.write(image_data)
    
    print("Image saved as output_image.png")

    # Close the cursor and connection
    cursor.close()
    connection.close()

except Exception as e:
    print("Failed to connect to the PostgreSQL database or process data.")
    print("Error:", e)
