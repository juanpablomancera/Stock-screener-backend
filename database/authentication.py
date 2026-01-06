import bcrypt

def hash_password(password):
    password = password.encode()
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hash.decode()


def check_hash(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash.encode())