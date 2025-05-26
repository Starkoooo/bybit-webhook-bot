from flask import Flask, request, jsonify
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

# Nacitaj API kľúče z env premennej
BYBIT_API_KEY = os.environ.get("jmlL97WpWUrPn6uC58")
BYBIT_API_SECRET = os.environ.get("s0o8TeD03i6AqlNyx4rAFJuguYMQ6H8ntU3K")

# Pripojenie na Bybit Testnet Unified API
session = HTTP(
    testnet=True,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Prijaté dáta:", data)
    action = data.get("action")
    symbol = data.get("symbol", "BTCUSDT")  # default na BTCUSDT, môžeš meniť
    
    result = {}

    if action == "buy":
        # LONG market order, 0.01 BTC
        result = session.place_order(
            category="linear",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=0.01,
            reduce_only=False
        )
    elif action == "sell":
        # SHORT market order, 0.01 BTC
        result = session.place_order(
            category="linear",
            symbol=symbol,
            side="Sell",
            order_type="Market",
            qty=0.01,
            reduce_only=False
        )
    else:
        return jsonify({"error": "Neznáma akcia", "data": data}), 400
    
    print("Bybit odpoveď:", result)
    return jsonify(result), 200

@app.route('/', methods=['GET'])
def home():
    return "Bot je online!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
