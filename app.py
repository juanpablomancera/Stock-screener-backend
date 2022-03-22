from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, JWTManager
from screener.screener import results

app = Flask(__name__)
jwt = JWTManager(app)
cors = CORS(app)

app.config["JWT_SECRET_KEY"] = "kdasfwrtka"


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


@app.route("/login", methods=["POST", "GET"])
def login():
    req_data = request.get_json()
    valor1 = req_data["username"]
    valor2 = req_data["password"]
    suma = valor1 + valor2
    response = jsonify({"a": valor1, "b": valor2, "_c": suma})
    return response

if __name__ == "__main__":
    app.run(debug=True)