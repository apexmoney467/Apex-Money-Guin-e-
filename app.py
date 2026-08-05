from flask import Flask, request, jsonify, render_template
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
    return jsonify({"status": "ok"})  # <- only this return               

@app.route("/cinetpay/init", methods=["POST"])
def cinetpay_init():
    try:
        data = request.json
        amount = int(data.get("amount"))
        transaction_id = data.get("transaction_id", str(uuid.uuid4()))
        description = data.get("description", "Apex Money Payment")
        customer_name = data.get("customer_name", "Customer")
        customer_email = data.get("customer_email", "test@apexmoney.gn")
        customer_phone = data.get("customer_phone", "")

        # Build correct CinetPay payload
        payload = {
            "apikey": CINETPAY_APIKEY,
            "site_id": CINETPAY_SITE_ID,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": data.get("currency", "GNF"),
            "description": description,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone,  # <-- FIXED NAME
            "notify_url": "https://apex-money-guin-e-1.onrender.com/cinetpay/notify",
            "return_url": "https://apexmoney.gn/success",
            "channels": "ALL"
        }

        # Call CinetPay API
        response = requests.post("https://api.cinetpay.com/v1/payment", json=payload)
        
        # ADD THIS: Print what CinetPay returns
        print("CinetPay Status:", response.status_code)
        print("CinetPay Response:", response.text)
        
        # Try to parse JSON, but don't crash if it fails
        try:
            result = response.json()
        except:
            result = {"error": "CinetPay did not return JSON", "raw": response.text}
            
        return jsonify(result), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
