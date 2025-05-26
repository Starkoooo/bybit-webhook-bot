from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP
import os

app = Flask(__name__)

# Zober API kľúče z environment variables (nezabudni ich nastaviť v Render!)
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# Pripoj sa na BYBIT TESTNET!
session = HTTP(
    testnet=True,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    action = data.get("action")

    if action == "buy":
        # Vytvoríme jednoduchú market objednávku na BTCUSDT, 0.001 BTC
        try:
            order = session.place_order(
                category="linear",
                symbol="BTCUSDT",
                side="Buy",
                order_type="Market",
                qty=0.001,
                time_in_force="GoodTillCancel"
            )
            return jsonify({"success": True, "order": order}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    if action == "sell":
        try:
            order = session.place_order(
                category="linear",
                symbol="BTCUSDT",
                side="Sell",
                order_type="Market",
                qty=0.001,
                time_in_force="GoodTillCancel"
            )
            return jsonify({"success": True, "order": order}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    return jsonify({"success": False, "error": "Unknown action"}), 400

@app.route("/", methods=["GET"])
def home():
    return "Bot je online!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
