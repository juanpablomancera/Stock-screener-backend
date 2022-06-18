from mysql.connector import Error
from Database.dbconn import create_server_connection
from Database.authentication import check_hash, hash_password

def create_new_user(username, password):
    connection = create_server_connection()
    password_hash = hash_password(password)
    query = f"INSERT INTO Users (username, password) VALUES ('{username}','{password_hash}');"
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print(f"Consulta realizada correctamente: {cursor.rowcount}")
        connection.close()
        print("New user created")
    except Error as err:
        print(f"Error: {err}")


def check_credentials(username,password):
    connection = create_server_connection()
    query = F"SELECT * FROM Users WHERE USERNAME = '{username}'"

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
        if check_hash(password, result[0][1]):
            print("The password matches")
            return True
    else:
        print("The password is wrong")
        return False

def delete_user(username):
    connection = create_server_connection()
    query = f"DELETE FROM Users WHERE USERNAME = '{username}'"
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        print(f"Consultas correctamente realizadas: {cursor.rowcount}")
    except Error as err:
        print(f"Error: {err}")

def check_user_exists(username):
    connection = create_server_connection()
    query = F"SELECT * FROM Users WHERE USERNAME = '{username}'"
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
        print(f"There is already a user with the username of {username}")
        return True
    else:
        print(f"There is no username with the username of {username}")
        return False
