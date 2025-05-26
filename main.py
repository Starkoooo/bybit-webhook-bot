from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
import time

app = Flask(__name__)

API_KEY = "hGe9T7daJFW9aO2Gmp"
API_SECRET = "36CI82HaiVOR2Y1MmdrMXrRS7OB5oVzspimr"
BASE_URL = "https://api-testnet.bybit.com"

def create_signature(params, api_secret):
    param_str = '&'.join([f"{k}={params[k]}" for k in sorted(params)])
    return hmac.new(bytes(api_secret, "utf-8"), bytes(param_str, "utf-8"), hashlib.sha256).hexdigest()

@app.route('/', methods=['GET'])
def home():
    return "Bot je ONLINE!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Prijaté dáta:", data)

    action = data.get('action')
    if action not in ['buy', 'sell']:
        return jsonify({'error': 'Neznáma akcia'}), 400

    side = "Buy" if action == "buy" else "Sell"

    params = {
        'api_key': API_KEY,
        'symbol': 'BTCUSDT',
        'side': side,
        'order_type': 'Market',
        'qty': '0.01',
        'time_in_force': 'GoodTillCancel',
        'timestamp': int(time.time() * 1000)
    }
    params['sign'] = create_signature(params, API_SECRET)

    response = requests.post(f"{BASE_URL}/v2/private/order/create", data=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
