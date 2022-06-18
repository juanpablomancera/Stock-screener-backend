from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from screener.screener import results
import os
from dotenv import load_dotenv
from Database.crud import create_new_user, check_credentials, delete_user, check_user_exists
load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
cors = CORS(app)

secret_key = os.getenv("JWT_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = secret_key


@app.route("/token", methods=["POST"])
def create_token():
    req_data = request.get_json()
    email = req_data["email"]
    password = req_data["password"]
    if email != "test" or password != "test":
        return jsonify({"msg":"Bad username or password"}), 401

    acces_token = create_access_token(identity=email)
    return jsonify(acces_token=acces_token)


@app.route("/screener", methods=["POST"])
def filter_stocks():
    req_data = request.get_json()
    stocks = results(req_data)
    return jsonify(stocks)


@app.route("/register", methods=["POST"])
def register_user():
    req_data = request.get_json()
    email = req_data["email"]
    password = req_data["password"]
    user_exists = check_user_exists(email)
    if user_exists:
        print("user exists")
        return jsonify({"msg": "User already exists"})
    else:
        create_new_user(email, password)
        acces_token = create_access_token(identity=email)
        print("we're creating a token for" +email+": "+ acces_token)
        return jsonify({"msg":acces_token})




@app.route("/login",methods=["POST"])
def login():
    req_data = request.get_json()
    email = req_data["email"]
    password = req_data["password"]
    user = check_credentials(email, password)
    if user:
        acces_token = create_access_token(identity=email)
        return jsonify(acces_token=acces_token)
    else:
        return jsonify({"msg":"User not found"})

@app.route("/checkUser", methods=["POST","GET"])
def checkUser(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return jsonify({"msg":"Token valid"})

if __name__ == "__main__":
    app.run(debug=True)