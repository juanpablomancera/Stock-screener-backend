from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
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


@app.route("/screener", methods=["POST"])
@jwt_required()
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


if __name__ == "__main__":
    app.run(debug=True)