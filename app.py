from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from screener.screener import results
import os
from dotenv import load_dotenv
from Database.crud import create_new_user, check_user, delete_user, check_user_exists
load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
cors = CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


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
    #user_exists = check_user_exists(email)
    #if user_exists:
    #    return jsonify({"msg": "User already exists"})
    #else:
    create_new_user(email, password)
    return jsonify({"msg": "User created"})




@app.route("/login",methods=["POST"])
def login():
    req_data = request.get_json()
    email = req_data["email"]
    password = req_data["password"]
    user = check_user(email, password)
    if user:
        return jsonify({"msg":"Login succesful"})
    else:
        return jsonify({"msg":"User not found"})


if __name__ == "__main__":
    app.run(debug=True)