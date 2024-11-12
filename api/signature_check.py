import os
import psycopg2
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
    cursor.execute("select signature_data from lbg_epc_complete where z_ref='908112';")

    # Fetch the memoryview object and convert it to bytes
    hex_data = cursor.fetchone()[0]
    if isinstance(hex_data, memoryview):
        hex_data = hex_data.tobytes()

    # Assuming `hex_data` is the raw PNG binary data, save it directly
    with open("output_image.png", "wb") as file:
        file.write(hex_data)

    print("Image saved as output_image.png")

    # Close the cursor and connection
    cursor.close()
    connection.close()

except Exception as e:
    print("Failed to connect to the PostgreSQL database.")
    print("Error:", e)
