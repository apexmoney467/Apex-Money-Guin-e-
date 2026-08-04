
from flask import Flask, jsonify, request, render_template
import os
import uuid
import requests
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
    try:
        data = request.json
        amount = int(data.get("amount"))
        phone = data.get("phone")
        owner_percent = float(data.get("owner_percent", 1))
        transaction_id = data.get("transaction_id", str(uuid.uuid4()))

        # Calculate split: 1% for you
        owner_amount = int(amount * (owner_percent / 100))
        merchant_amount = amount - owner_amount

        # REAL CINETPAY API CALL
        payload = {
            "apikey": CINETPAY_APIKEY,
            "site_id": CINETPAY_SITE_ID,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "XOF",
            "description": "Apex Money Guinee Payment",
            "customer_name": "Customer",
            "customer_surname": "Apex",
            "customer_email": "customer@apex.com",
            "customer_phone_number": phone,
            "notify_url": "https://apex-money-guin-e-1.onrender.com/cinetpay/notify",
            "return_url": "https://apex-money-guin-e-1.onrender.com/success",
            "channels": "ALL"  # Orange Money + MTN MoMo + Card
        }

        r = requests.post("https://api.cinetpay.com/v1/?method=payment&version=1.0", json=payload)
        res = r.json()

        if res.get("code") == "201":
            return jsonify({
                "status": "success",
                "payment_url": res["data"]["payment_url"],
                "transaction_id": transaction_id,
                "owner_1%": owner_amount,
                "merchant_99%": merchant_amount
            })
        else:
            return jsonify({"status": "error", "cinetpay_response": res}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/cinetpay/notify", methods=["POST"])
def cinetpay_notify():
    data = request.json
    print("Payment Notification:", data)
    return jsonify({"status": "ok"})

@app.route("/success")
def success():
    return "<h1>Payment Successful!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
