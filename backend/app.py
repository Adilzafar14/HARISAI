from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('../database/harisai.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return jsonify({
        'system': 'HARISAI',
        'status': 'running',
        'message': 'ذكاء لخدمة الحجاج'
    })

@app.route('/api/zones', methods=['GET'])
def get_zones():
    conn = get_db()
    zones = conn.execute('SELECT * FROM zones').fetchall()
    conn.close()
    return jsonify([dict(z) for z in zones])

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    conn = get_db()
    alerts = conn.execute(
        'SELECT * FROM alerts ORDER BY id DESC LIMIT 20'
    ).fetchall()
    conn.close()
    return jsonify([dict(a) for a in alerts])

@app.route('/api/alert/add', methods=['POST'])
def add_alert():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'INSERT INTO alerts (type, message, zone, time) VALUES (?, ?, ?, ?)',
        (
            data['type'],
            data['message'],
            data['zone'],
            datetime.datetime.now().strftime('%H:%M:%S')
        )
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'Alert saved!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db()
    admin = conn.execute(
        'SELECT * FROM admins WHERE username=? AND password=?',
        (data['username'], data['password'])
    ).fetchone()
    conn.close()
    if admin:
        return jsonify({'status': 'success', 'message': 'Welcome Admin!'})
    return jsonify({'status': 'error', 'message': 'Wrong credentials!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)