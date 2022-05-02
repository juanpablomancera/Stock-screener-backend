import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password= os.getenv("PASSWORD"),
            database="prueba"
        )
        print("MySQL Database connection succesful")

    except Error as err:
        print(f"Error: {err}")
    return connection