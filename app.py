from flask import Flask, jsonify, request
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

CINETPAY_APIKEY = os.getenv("CINETPAY_APIKEY")
CINETPAY_SITE_ID = os.getenv("CINETPAY_SITE_ID")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/cinetpay/init", methods=["POST"])
def cinetpay_init():
    data = request.json
    amount = int(data.get("amount"))
    phone = data.get("phone")
    owner_phone = data.get("owner_phone")
    owner_percent = float(data.get("owner_percent", 1))
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))

    # Calculate split
    owner_amount = int(amount * (owner_percent / 100))
    merchant_amount = amount - owner_amount

    return jsonify({
        "status": "success",
        "transaction_id": transaction_id,
        "owner_amount": owner_amount,
        "merchant_amount": merchant_amount
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
