from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, jwt_required

from screener.crypto_filters.filters import price_above_sma, volume_spike, volatility_expansion, orderbook_imbalance, \
    tight_spread
from screener.screener import results
import os
from dotenv import load_dotenv
from database.crud import create_new_user, check_credentials, delete_user, check_user_exists

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
cors = CORS(app, supports_credentials=True)

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
        return jsonify({"msg": "User already exists"})
    else:
        create_new_user(email, password)
        access_token = create_access_token(identity=email)
        return jsonify({"msg":access_token})




@app.route("/login",methods=["POST"])
def login():
    req_data = request.get_json()
    email = req_data["email"]
    password = req_data["password"]
    user = check_credentials(email, password)
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(acces_token=access_token)
    else:
        return jsonify({"msg":"User not found"})

CRYPTO_FILTERS = {
        "trend": price_above_sma,
        "volume": volume_spike,
        "volatility": volatility_expansion,
        "orderbook": orderbook_imbalance,
        "spread": tight_spread
    }

@app.route("/crypto/screener", methods=["POST"])
@jwt_required()
def crypto_screener():
    """
    Expected JSON:
    {
        "symbol": "BTC/USD",
        "filters": ["trend", "volume", "spread"]
    }
    """
    req_data = request.get_json()
    symbol = req_data.get("symbol")
    filters = req_data.get("filters", [])

    if not symbol:
        return jsonify({"error": "symbol is required"}), 400

    results = {}

    for f in filters:
        if f not in CRYPTO_FILTERS:
            results[f] = "unknown filter"
            continue

        try:
            results[f] = CRYPTO_FILTERS[f](symbol)
        except Exception as e:
            results[f] = f"Could not fetch the data"

    return jsonify({
        "symbol": symbol,
        "results": results
    })



if __name__ == "__main__":
    app.run(debug=True)