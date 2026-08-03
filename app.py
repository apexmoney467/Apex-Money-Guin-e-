@app.route("/")
def home():
    return "APEX Money API is Running ✅"
from flask import Flask, jsonify, request
import os
import requests
import uuid 
import base64
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
    from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Apex Money Guinée API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)




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
    return jsonify({"status": "received"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})
### *STEP 3: ADD THIS AT THE VERY BOTTOM OF THE FILE*
Scroll all the way down and paste:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
Then `Commit changes` → `Add CinetPay endpoints`

Reply `DONE STEP 2` when you finish 👇  
Next I’ll give you STEP 3: Orange Money + MTN
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

import uuid

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
    return jsonify({"status": "received"})


# ========== 2. ORANGE MONEY ==========
def get_orange_token():
    auth = base64.b64encode(f"{ORANGE_CLIENT_ID}:{ORANGE_CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    res = requests.post(
        "https://api.orange.com/oauth/v3/token",
        headers=headers,
        data={"grant_type": "client_credentials"}
    )
    return res.json().get("access_token")

@app.route("/orange/pay", methods=["POST"])
def orange_pay():
    data = request.json
    amount = data.get("amount")
    phone = data.get("phone") # format: 224622924439,224666363078
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))
    
    token = get_orange_token()
    
    payload = {
        "amount": amount,
        "currency": "GNF",
        "orderId": transaction_id,
        "payer": {"partyIdType": "MSISDN", "partyId": phone},
        "payee": {"partyIdType": "MSISDN", "partyId": "2246YOUR_MERCHANT_NUMBER"},
        "callbackUrl": "https://apex-money-guin-e.onrender.com/orange/notify"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post("https://api.orange.com/orange-money-webpay/v1/payments", json=payload, headers=headers)
    return jsonify(res.json())

@app.route("/orange/notify", methods=["POST"])
def orange_notify():
    data = request.json
    print("Orange Notification:", data)
    return jsonify({"status": "received"})


# ========== 3. MTN MOBILE MONEY ==========
@app.route("/mtn/pay", methods=["POST"])
def mtn_pay():
    data = request.json
    amount = data.get("amount")
    phone = data.get("phone") # format: 224622924439,224666363078
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))
    
    headers = {
        "Ocp-Apim-Subscription-Key": MTN_SUBSCRIPTION_KEY,
        "X-Reference-Id": transaction_id,
        "X-Target-Environment": "sandbox"
    }
    
    payload = {"amount": amount, "currency": "GNF", "payer": {"partyIdType": "MSISDN", "partyId": phone}}
    res = requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay", json=payload, headers=headers)
    
    return jsonify({"status": "pending", "reference": transaction_id})

@app.route("/mtn/notify", methods=["POST"])
def mtn_notify():
    data = request.json
    print("MTN Notification:", data)
    return jsonify({"status": "received"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
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
    data = request.json
    amount = data.get("amount")
    phone = data.get("phone")
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))

    # 1. Get Orange token
    auth_string = f"{ORANGE_CLIENT_ID}:{ORANGE_CLIENT_SECRET}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    
    token_res = requests.post(
        "https://api.orange.com/oauth/v3/token",
        headers={"Authorization": f"Basic {auth_bytes}"},
        data={"grant_type": "client_credentials"}
    )
    token = token_res.json().get("access_token")

    # 2. Make payment
    payload = {
        "amount": amount,
        "currency": "GNF",
        "externalId": transaction_id,
        "payee": {"partyIdType": "MSISDN", "partyId": phone}
    }
    
    pay_res = requests.post(
        "https://api.orange.com/orange-money-webpay/dev/v1/transactions",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )
    return jsonify(pay_res.json())


# ========== 3. MTN MOBILE MONEY ==========
@app.route("/mtn/pay", methods=["POST"])
def mtn_pay():
    data = request.json
    amount = data.get("amount")
    phone = data.get("phone")
    transaction_id = data.get("transaction_id", str(uuid.uuid4()))

    headers = {
        "X-Reference-Id": transaction_id,
        "Ocp-Apim-Subscription-Key": MTN_SUBSCRIPTION_KEY,
        "X-Target-Environment": "sandbox",
        "Content-Type": "application/json"
    }
    
    payload = {
        "amount": str(amount),
        "currency": "GNF",
        "externalId": transaction_id,
        "payer": {"partyIdType": "MSISDN", "partyId": phone},
        "payerMessage": "Apex Money Payment",
        "payeeNote": "Apex Money Payment"
    }
    
    res = requests.post(
        "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",
        headers=headers,
        json=payload
    )
    return jsonify({"status": "sent", "reference": transaction_id})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
# ADD THIS WHOLE BLOCK HERE - BEFORE LINE 274

import os
import sqlite3
from datetime import datetime

# 1. DATABASE SETUP
def init_db():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT PRIMARY KEY, phone TEXT, amount REAL, type TEXT, status TEXT, date TEXT)''')
    conn.commit()
    conn.close()
init_db()

# 2. CHECK BALANCE ENDPOINT
@app.route('/balance/<phone>', methods=['GET'])
def balance(phone):
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (phone,))
    row = c.fetchone()
    conn.close()
    return jsonify({"phone": phone, "balance": row[0] if row else 0})

# 3. NEW WEBHOOK FOR CINETPAY + WALLET
@app.route('/webhook/cinetpay', methods=['POST'])
def webhook():
    data = request.json
    if data['cpm_result'] == '00': # 00 = Payment Success
        trans_id = data['cpm_trans_id']
        amount = float(data['cpm_amount'])
        phone = data['cpm_phone']
        
        conn = sqlite3.connect('apex.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))

import os
import sqlite3
from datetime import datetime

ADMIN_PHONE = "224622924439" # <-- CHANGE THIS TO YOUR 1 REAL NUMBER ONLY
FEE_PERCENT = 1.5 # 1.5% fee

# CREATE ADMIN + TABLES
def init_db():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT PRIMARY KEY, phone TEXT, amount REAL, type TEXT, status TEXT, date TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (phone, balance) VALUES (?, 0)", (ADMIN_PHONE,))
    conn.commit()
    conn.close()
init_db()

@app.route('/admin/balance', methods=['GET'])
def admin_balance():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (ADMIN_PHONE,))
    row = c.fetchone()
    conn.close()
    return jsonify({"admin_phone": ADMIN_PHONE, "balance": row[0] if row else 0})

@app.route('/balance/<phone>', methods=['GET'])
def balance(phone):
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (phone,))
    row = c.fetchone()
    conn.close()
    return jsonify({"phone": phone, "balance": row[0] if row else 0})

@app.route('/webhook/cinetpay', methods=['POST'])
def webhook():
    data = request.json
    if data['cpm_result'] == '00':
        trans_id = data['cpm_trans_id']
        amount = float(data['cpm_amount'])
        phone = data['cpm_phone']
        fee = round(amount * FEE_PERCENT / 100, 2)
        user_amount = amount - fee
        conn = sqlite3.connect('apex.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (user_amount, phone))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (fee, ADMIN_PHONE))
        conn.commit()
        conn.close()
        print(f"PAID: {user_amount} GNF to {phone} | FEE: {fee} GNF to ADMIN")
    return jsonify({"status": "ok"})        


    

# CHECK YOUR BALANCE
@app.route('/admin/balance', methods=['GET'])
def admin_balance():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (ADMIN_PHONE,))
    row = c.fetchone()
    conn.close()
    return jsonify({"admin_phone": ADMIN_PHONE, "balance": row[0] if row else 0})

# CHECK USER BALANCE
@app.route('/balance/<phone>', methods=['GET'])
def balance(phone):
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (phone,))
    row = c.fetchone()
    conn.close()
    return jsonify({"phone": phone, "balance": row[0] if row else 0})

# WEBHOOK - ADDS MONEY TO USER + FEE TO YOU
@app.route('/webhook/cinetpay', methods=['POST'])
def webhook():
    data = request.json
    if data['cpm_result'] == '00':
        trans_id = data['cpm_trans_id']
        amount = float(data['cpm_amount'])
        phone = data['cpm_phone']

        fee = round(amount * FEE_PERCENT / 100, 2)
        user_amount = amount - fee

        conn = sqlite3.connect('apex.db')
        c = conn.cursor()
        # 1. Give money to user
        c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (user_amount, phone))
        # 2. Give FEE to YOU
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (fee, ADMIN_PHONE))

        conn.commit()
        conn.close()
        print(f"PAID: {user_amount} GNF to {phone} | FEE: {fee} GNF to ADMIN")
    return jsonify({"status": "ok"})execute("UPDATE users SET balance = balance +? WHERE phone =?", (amount, phone))
        c.execute("INSERT INTO transactions VALUES (?,?,?, 'TOPUP', 'SUCCESS',?)", 
                  (trans_id, phone, amount, datetime.now()))
        conn.commit()
        conn.close()
        print(f"PAID: {trans_id} - {amount} GNF to {phone}")
    return jsonify({"status": "ok"})

@app.route('/webhook/cinetpay', methods=['POST'])
def webhook():
    data = request.json
    if data['cpm_result'] == '00': # 00 = success
        trans_id = data['cpm_trans_id']
        amount = float(data['cpm_amount'])
        phone = data['cpm_phone']
        
        # Add money to user wallet + fee to you
        conn = sqlite3.connect('apex.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (amount, phone))
        conn.commit()
        conn.close()
    return jsonify({"status": "ok"})
if __name__ == "__main__": # THIS WAS ALREADY THERE
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, request, jsonify
import sqlite3
import requests
import os
from datetime import datetime

app = Flask(__name__)

# 1. YOUR EXISTING ROUTES GO HERE
# like /create-payment, /balance etc

# 2. PASTE THE ADMIN + WEBHOOK CODE HERE AT THE BOTTOM
import sqlite3
from datetime import datetime

ADMIN_PHONE = "224622924439,224666363078" # <-- CHANGE THIS
FEE_PERCENT = 1.5

def init_db():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, balance REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT PRIMARY KEY, phone TEXT, amount REAL, type TEXT, status TEXT, date TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (phone, balance) VALUES (?, 0)", (ADMIN_PHONE,))
    conn.commit()
    conn.close()
init_db()

@app.route('/admin/balance', methods=['GET'])
def admin_balance():
    conn = sqlite3.connect('apex.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone =?", (ADMIN_PHONE,))
    row = c.fetchone()
    conn.close()
    return jsonify({"admin_phone": ADMIN_PHONE, "balance": row[0] if row else 0})

@app.route('/webhook/cinetpay', methods=['POST'])
def webhook():
    data = request.json
    if data['cpm_result'] == '00':
        trans_id = data['cpm_trans_id']
        amount = float(data['cpm_amount'])
        phone = data['cpm_phone']

        fee = round(amount * FEE_PERCENT / 100, 2)
        user_amount = amount - fee

        conn = sqlite3.connect('apex.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (user_amount, phone))
        c.execute("UPDATE users SET balance = balance +? WHERE phone =?", (fee, ADMIN_PHONE))
        conn.commit()
        conn.close()
        print(f"PAID: {user_amount} GNF to {phone} | FEE: {fee} GNF to ADMIN")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
