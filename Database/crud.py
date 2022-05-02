from mysql.connector import Error
from Database.dbconn import create_server_connection
connection = create_server_connection()


def create_new_user(username, password_hash):
    query = f"INSERT INTO Users (username, password) VALUES ('{username}','{password_hash}');"
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print(f"Consulta realizada correctamente: {cursor.rowcount}")
        connection.close()
    except Error as err:
        print(f"Error: {err}")

def check_user(username,password_hash):
    query = F"SELECT * FROM Users WHERE PASSWORD = '{password_hash}' AND USERNAME = '{username}'"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Consulta realizada: {cursor.rowcount}")
        connection.close()
    except Error as err:
        print(f"Error: {err}")

    if result:
        print(result)
        return True
    else:
        return False

def delete_user(password_hash):
    query = f"DELETE FROM Users WHERE password = '{password_hash}'"
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print(f"Consultas correctamente realizadas: {cursor.rowcount}")
    except Error as err:
        print(f"Error: {err}")

def check_user_exists(email):
    query = F"SELECT * FROM Users WHERE USERNAME = '{email}'"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Consulta realizada: {cursor.rowcount}")
        connection.close()
    except Error as err:
        print(f"Error: {err}")

    if result:
        print(f"There is already a user with the email of {email}")
        return True
    else:
        print(f"There is no username with the email of {email}")
        return False

