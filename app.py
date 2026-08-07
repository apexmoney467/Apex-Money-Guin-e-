
from flask import Flask, request, jsonify, render_template
import requests
import os
import time

app = Flask(__name__, template_folder='.')

# YOUR CINETPAY KEYS - we will add them in Render
SITE_ID = os.getenv("CINETPAY_SITE_ID")
API_KEY = os.getenv("CINETPAY_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/payment', methods=['POST'])
def payment():
    data = request.json
    total_amount = data['amount']
    
    payload = {
        "cpm_site_id": SITE_ID,
        "cpm_amount": total_amount,
        "cpm_currency": "GNF",
        "cpm_trans_id": str(int(time.time())),
        "cpm_description": data['description'],
        "notify_url": "https://apex-money-guin-e-1.onrender.com/api/notify",
        "return_url": "https://apex-money-guin-e-1.onrender.com/success",
        "cpm_version": "V2"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    res = requests.post("https://api-checkout.cinetpay.com/v2/payment", json=payload, headers=headers)
    return jsonify(res.json())

@app.route('/api/notify', methods=['POST'])
def notify():
    # CinetPay will send payment status here
    return jsonify({"status": "ok"})

@app.route('/success')
def success():
    return "Paiement reussi! Merci"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
API_SECRET = os.getenv("API_SECRET", "ApexSecret2026")

def check_auth():
    return request.headers.get("Authorization") == f"Bearer {API_SECRET}"

@app.route("/")
def home():
    return jsonify({"status": "Apex Money API Running ✅"})

# 1. KYC
@app.route("/kyc-check", methods=["POST"])
def kyc():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    print("KYC:", request.json)
    return jsonify({"status": "success", "verified": True})

# 2. SMS
@app.route("/send-sms", methods=["POST"])
def sms():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    print("SMS:", request.json)
    return jsonify({"status": "sent"})

# 3. WHATSAPP
@app.route("/send-whatsapp", methods=["POST"])
def whatsapp():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    print("WhatsApp:", request.json)
    return jsonify({"status": "sent"})

# 4. SEND MONEY
@app.route("/send-money", methods=["POST"])
def send_money():
    if not check_auth(): return jsonify({"error": "Unauthorized"}), 401
    print("Send Money:", request.json)
    return jsonify({"status": "success", "transactionId": f"TXN{int(time.time())}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
