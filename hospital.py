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

class DatabaseConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnector, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.connection = None
        if self.connection is None:
            self.connection = self._create_connection()

    def _create_connection(self):
        try:
            connection = psycopg2.connect(user=DB_user,
                                          password=DB_password,
                                          host=DB_host,
                                          port=DB_port,
                                          database=DB_database)
            print("Database connection successful")
            return connection
        except OperationalError as error:
            print(f"Error connecting to the database: {error}")
            return None

    def get_version(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT version();")
                db_version = cursor.fetchone()
                print(f"Database version: {db_version[0]}")
                cursor.close()
            except OperationalError as error:
                print(f"Error fetching database version: {error}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed")

# Usage example
if __name__ == "__main__":
    db_connector = DatabaseConnector()
    db_connector.get_version()
    db_connector.close_connection()

