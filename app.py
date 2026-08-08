import sqlite3
from datetime import datetime
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
    d# DATABASE SETUP
def get_db():
    conn = sqlite3.connect('apex.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, nom TEXT, phone TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'user', balance REAL DEFAULT 0)''')
    db.execute('''CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY, type TEXT, amount REAL, platform TEXT, user_phone TEXT, agent_phone TEXT, created_at TEXT)''')
    db.commit()


# AUTH ROUTES
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
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
    except:
        return jsonify({"success": False, "message": "Phone already exists"}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE phone=? AND password=?", 
                      (data['phone'], data['password'])).fetchone()
    if user:
        return jsonify({"success": True, "user": dict(user)})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401


# OWNER ROUTE - SERVES THE HTML PAGE
@app.route('/owner')
def owner():
    return render_template('Owner.html')
@app.route('/success')
def success():
    return "Paiement reussi! Merci"

@app.route('/api/agent/transaction', methods=['POST'])
def agent_transaction():
    data = request.json
    db = get_db()
    
    user = db.execute("SELECT * FROM users WHERE phone=?", (data['userPhone'],)).fetchone()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if data['type'] == 'agent_deposit':
        db.execute("UPDATE users SET balance = balance + ? WHERE phone=?", (data['amount'], data['userPhone']))
    if data['type'] == 'agent_withdraw':
        db.execute("UPDATE users SET balance = balance - ? WHERE phone=?", (data['amount'], data['userPhone']))
    
    db.execute("INSERT INTO transactions (type, amount, platform, user_phone, agent_phone, created_at) VALUES (?, ?, ?)",
               (data['type'], data['amount'], data['platform'], data['userPhone'], data.get('agentPhone','OWNER'), datetime.now()))
    db.commit()
    return jsonify({"success": True, "message": "Transaction completed"})

@app.route('/api/owner/dashboard', methods=['GET'])
def owner_dashboard():
    db = get_db()
    users = db.execute("SELECT COUNT(*) as c FROM users WHERE role='user'").fetchone()['c']
    agents = db.execute("SELECT COUNT(*) as c FROM users WHERE role='agent'").fetchone()['c']
    txs = db.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 50").fetchall()
    return jsonify({
        "totalUsers": users,
        "totalAgents": agents,
        "recentTransactions": [dict(t) for t in txs]
    })

# AGENT TRANSACTION - DEPOSIT / RETRAIT
@app.route('/api/agent/transaction', methods=['POST'])
def agent_transaction():
    data = request.json
    db = get_db()
    
    # Check user exists
    user = db.execute("SELECT * FROM users WHERE phone=?", (data['userPhone'],)).fetchone()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Update balance
    if data['type'] == 'agent_deposit':
        db.execute("UPDATE users SET balance = balance + ? WHERE phone=?", (data['amount'], data['userPhone']))
    if data['type'] == 'agent_withdraw':
        db.execute("UPDATE users SET balance = balance - ? WHERE phone=?", (data['amount'], data['userPhone']))
    
    # Save transaction
    db.execute("INSERT INTO transactions (type, amount, platform, user_phone, agent_phone, created_at) VALUES (?, ?, ?)",
               (data['type'], data['amount'], data['platform'], data['userPhone'], data.get('agentPhone','OWNER'), datetime.now()))
    db.commit()
    return jsonify({"success": True, "message": "Transaction completed"})


# OWNER DASHBOARD DATA
@app.route('/api/owner/dashboard', methods=['GET'])
def owner_dashboard():
    db = get_db()
    users = db.execute("SELECT COUNT(*) as c FROM users WHERE role='user'").fetchone()['c']
    agents = db.execute("SELECT COUNT(*) as c FROM users WHERE role='agent'").fetchone()['c']
    txs = db.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 50").fetchall()
    return jsonify({
        "totalUsers": users,
        "totalAgents": agents,
        "recentTransactions": [dict(t) for t in txs]
    })


# GET ALL USERS FOR OWNER
@app.route('/api/owner/users', methods=['GET'])
def owner_users():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return jsonify([dict(u) for u in users])ata = request.json
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
   

@app.route('/api/notify', methods=['POST'])
def notify():
    # CinetPay will send payment status here
    return jsonify({"status": "ok"})

@app.route('/success')
def success():
    return "Paiement reussi! Merci"

@app.route('/owner')
def owner():
    return render_template('Owner.html')

# AGENT TRANSACTION ENDPOINT
@app.route('/api/agent/transaction', methods=['POST'])
def agent_transaction():
    data = request.json
    db = get_db()
    
    # Update user balance
    if data['type'] == 'agent_deposit':
        db.execute("UPDATE users SET balance = balance + ? WHERE phone=?", (data['amount'], data['userPhone']))
    if data['type'] == 'agent_withdraw':
        db.execute("UPDATE users SET balance = balance - ? WHERE phone=?", (data['amount'], data['userPhone']))
    
    # Log transaction
    db.execute("INSERT INTO transactions (type, amount, platform, user_phone, agent_phone, created_at) VALUES (?, ?, ?)",
               (data['type'], data['amount'], data['platform'], data['userPhone'], data.get('agentPhone','OWNER'), datetime.now()))
    db.commit()
    return jsonify({"success": True, "message": "Transaction completed"})

# OWNER DASHBOARD DATA
@app.route('/api/owner/dashboard', methods=['GET'])
def owner_dashboard():
    db = get_db()
    users = db.execute("SELECT COUNT(*) as c FROM users WHERE role='user'").fetchone()['c']
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/api/owner/dashboard', methods=['GET'])
def owner_dashboard():
    db = get_db()
    users = db.execute("SELECT COUNT(*) as c FROM users WHERE role='user'").fetchone()['c']
    agents = db.execute("SELECT COUNT(*) as c FROM users WHERE role='agent'").fetchone()['c']
    txs = db.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 50").fetchall()
    return jsonify({
        "totalUsers": users,
        "totalAgents": agents,
        "recentTransactions": [dict(t) for t in txs]
    })

def get_db():
    conn = sqlite3.connect('apex.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__, template_folder='.')

def owner_dashboard():
    agents = db.execute("SELECT COUNT(*) as c FROM users WHERE role='agent'").fetchone()['c']
txs = db.execute("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 50").fetchall()
 return jsonify({
     "totalUsers": users,
     "totalAgents": agents,
     "recentTransactions": [dict(t) for t in txs]
    conn = sqlite3.connect('apex.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, nom TEXT, phone TEXT UNIQUE, password TEXT, role TEXT, balance REAL)''')
    db.execute('''CREATE TABLE IF NOT EXISTS transactions
        (id INTEGER PRIMARY KEY, type TEXT, amount REAL, platform TEXT, user_phone TEXT, agent_phone TEXT, created_at TEXT)''')
    db.commit()
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
