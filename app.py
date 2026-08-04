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
    owner_phone = data.get("owner_phone")  # NEW: Owner number to receive %
    owner_percent = float(data.get("owner_percent", 10))  # NEW: Default 10%
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))

    # Calculate split
    owner_amount = int(amount * (owner_percent / 100))
    merchant_amount = amount - owner_amount

    payload = {
        "apikey": CINETPAY_APIKEY,
        "site_id": CINETPAY_SITE_ID,
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": "GNF",
        "description": "Apex Money Payment",
        "return_url": "https://apex-money-guin-e-1.onrender.com/success",
        "notify_url": "https://apex-money-guin-e-1.onrender.com/webhook",
        "metadata": {
            "owner_phone": owner_phone,
            "owner_amount": owner_amount,
            "merchant_amount": merchant_amount
        }
    }
    return jsonify({
        "status": "ok", 
        "payload": payload, 
        "transaction_id": transaction_id,
        "split": {"total": amount, "owner": owner_amount, "merchant": merchant_amount}
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
