from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def get_db():
    db = sqlite3.connect("apex.db")
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def home():
    return jsonify({"status": "Apex API Running", "version": "1.0"})

# AUTH
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
        db = get_db()
    try:
        db.execute("INSERT INTO users (nom, phone, password, role) VALUES (?, ?, ?, ?)",
                   (data['nom'], data['phone'], data['password'], data.get('role','user')))
        db.commit()
        return jsonify({"success": True, "message": "User registered"})
    except:
        return jsonify({"success": False, "message": "Phone already exists"}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE phone=? AND password=?",
                      (data['phone'], data['password'])).fetchone()
    if user:
        return jsonify({"success": True, "user": dict(user)})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# KYC
@app.route('/kyc-check', methods=['POST'])
def kyc_check():
    data = request.json
    print("KYC for:", data.get('name'))
    return jsonify({"status": "ok", "message": "KYC passed"})

# SEND SMS
@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    print("SMS to:", data.get('phone'))
    return jsonify({"status": "sent"})

# SEND WHATSAPP
@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.json
    print("WhatsApp to:", data.get('to'))
    return jsonify({"status": "sent"})

# SEND MONEY
@app.route('/send-money', methods=['POST'])
def send_money():
    data = request.json
    print("Sending", data.get('amount'), "to", data.get('phone'))
    return jsonify({"status": "success", "transactionId": "TX123"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
