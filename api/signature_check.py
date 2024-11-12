import psycopg2

# Database connection parameters
host = "10.180.10.132"
port = "5432"
user = "psqladmin"
database = "postgres"

# Prompt for the password securely (optional)
password = 's6^3tarXiwmD'

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
    
    # Remember to close the connection when done
    connection.close()
except Exception as e:
    print("Failed to connect to the PostgreSQL database.")
    print("Error:", e)