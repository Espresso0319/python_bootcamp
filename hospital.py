from dotenv import load_dotenv  
import os  
import psycopg2
import datetime
from dateutil.relativedelta import relativedelta
  
# Load the environment variables from the .env file  
load_dotenv()

# Get the environment variables

DB_user = os.getenv('DB_USER')
DB_password = os.getenv('DB_PASSWORD')
DB_host = os.getenv('DB_HOST')
DB_port = os.getenv('DB_PORT')
DB_database = os.getenv('DB_DATABASE')

def get_connection():
    connection = psycopg2.connect(user=DB_user,
                                  password=DB_password,
                                  host=DB_host,
                                  port=DB_port,
                                  database=DB_database)
    return connection

def close_connection(connection):
    if connection:
        connection.close()

