import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

def create_server_connection():
    connection = None
    try:
        print("dbconn::connection::try")
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password= os.getenv("PASSWORD"),
            database="prueba"
        )
        print("MySQL Dtabase connection succesful")

    except Error as err:
        print("dbconn::create_server_connection::excepcion")
        print(f"Error: {err}")
    return connection