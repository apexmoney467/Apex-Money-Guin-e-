
from flask import Flask, jsonify, request
import os
import requests
import uuid

app = Flask(__name__)

# KEYS - we'll add these in Render Environment
CINETPAY_APIKEY = os.environ.get("CINETPAY_APIKEY")
CINETPAY_SITE_ID = os.environ.get("CINETPAY_SITE_ID")

ORANGE_CLIENT_ID = os.environ.get("ORANGE_CLIENT_ID")
ORANGE_CLIENT_SECRET = os.environ.get("ORANGE_CLIENT_SECRET")

MTN_API_KEY = os.environ.get("MTN_API_KEY")
MTN_SUBSCRIPTION_KEY = os.environ.get("MTN_SUBSCRIPTION_KEY")

@app.route("/")
def home():
    return jsonify({"message": "Apex Money Guinée API is running", "status": "success"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ========== 1. CINETPAY ==========
@app.route("/cinetpay/init", methods=["POST"])
def cinetpay_init():
    data = request.json
    amount = data.get("amount")
    phone = data.get("phone")
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))

    payload = {
        "apikey": CINETPAY_APIKEY,
        "site_id": CINETPAY_SITE_ID,
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": "GNF",
        "description": "Apex Money Payment",
        "return_url": "https://apex-money-guin-e.onrender.com/success",
        "notify_url": "https://apex-money-guin-e.onrender.com/cinetpay/notify",
        "customer_phone_number": phone,
        "channels": "ALL"
    }
    
    res = requests.post("https://api-checkout.cinetpay.com/v2/payment", json=payload)
    return jsonify(res.json())

@app.route("/cinetpay/notify", methods=["POST"])
def cinetpay_notify():
    data = request.json
    print("CinetPay Notification:", data)
    # TODO: Update your database here when payment = ACCEPTED
    return jsonify({"status": "received"})


# ========== 2. ORANGE MONEY ==========
@app.route("/orange/pay", methods=["POST"])
def orange_pay():
    # We will fill this after CinetPay works
    return jsonify({"status": "coming_soon", "provider": "Orange Money"})


# ========== 3. MTN MOBILE MONEY ==========
@app.route("/mtn/pay", methods=["POST"])
def mtn_pay():
    # We will fill this after CinetPay works
    return jsonify({"status": "coming_soon", "provider": "MTN MoMo"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
