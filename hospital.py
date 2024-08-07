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
        except psycopg2.OperationalError as error:
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
            except psycopg2.OperationalError as error:
                print(f"Error fetching database version: {error}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed")

    def get_doctor_details(self, doctor_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM doctor WHERE doctor_id = %s;", (doctor_id,))
                doctor_details = cursor.fetchone()
                cursor.close()
                if doctor_details:
                    print(f"Doctor Details: {doctor_details}")
                else:
                    print(f"No doctor found with ID: {doctor_id}")
                return doctor_details
            except psycopg2.OperationalError as error:
                print(f"Error fetching doctor details: {error}")
                return None

    def get_hospital_details(self, hospital_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM hospital WHERE hospital_id = %s;", (hospital_id,))
                hospital_details = cursor.fetchone()
                cursor.close()
                if hospital_details:
                    print(f"Hospital Details: {hospital_details}")
                else:
                    print(f"No hospital found with ID: {hospital_id}")
                return hospital_details
            except psycopg2.OperationalError as error:
                print(f"Error fetching hospital details: {error}")
                return None

    def get_doctors_by_salary_and_specialty(self, salary, specialty):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "SELECT * FROM doctor WHERE salary > %s AND speciality = %s;", 
                    (salary, specialty)
                )
                doctors = cursor.fetchall()
                cursor.close()
                if doctors:
                    for doctor in doctors:
                        print(f"Q3 Doctor: {doctor}")
                else:
                    print(f"No doctors found with salary higher than {salary} and specialty {specialty}")
                return doctors
            except psycopg2.OperationalError as error:
                print(f"Error fetching doctors: {error}")
                return None

    def get_doctors_by_hospital_id(self, hospital_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    """
                    SELECT d.*, h.hospital_name 
                    FROM doctor d
                    JOIN hospital h ON d.hospital_id = h.hospital_id
                    WHERE d.hospital_id = %s;
                    """, 
                    (hospital_id,)
                )
                doctors = cursor.fetchall()
                cursor.close()
                if doctors:
                    for doctor in doctors:
                        print(f"Q4 Doctor: {doctor}")
                else:
                    print(f"No doctors found for hospital ID: {hospital_id}")
                return doctors
            except psycopg2.OperationalError as error:
                print(f"Error fetching doctors: {error}")
                return None

# Usage example
if __name__ == "__main__":
    db_connector = DatabaseConnector()
    # Q1
    db_connector.get_version()
    # Q2
    doctor_id = '101'
    hospital_id = '1'
    db_connector.get_doctor_details(doctor_id)
    db_connector.get_hospital_details(hospital_id)
    # Q3
    min_salary = 30000  
    specialty = 'Garnacologist' 
    db_connector.get_doctors_by_salary_and_specialty(min_salary, specialty)
    # Q4
    db_connector.get_doctors_by_hospital_id(hospital_id)

    db_connector.close_connection()
