from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB_PATH = 'harisai.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS zones
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT, count INTEGER,
                      max_capacity INTEGER, status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      type TEXT, message TEXT,
                      zone TEXT, time TEXT)''')
    cursor.execute('SELECT * FROM admins WHERE username="admin"')
    if not cursor.fetchone():
        cursor.execute('INSERT INTO admins (username, password) VALUES (?,?)',
                      ('admin', 'harisai123'))
        print("✅ Admin created!")
    cursor.execute('SELECT * FROM zones')
    if not cursor.fetchone():
        zones = [
            ('Masjid Al-Haram', 0, 1200, 'safe'),
            ('Safa-Marwa Path', 0, 800,  'safe'),
            ('Mina Camp Zone',  0, 1500, 'safe'),
            ('Jamarat Bridge',  0, 600,  'safe'),
            ('Arafat Ground',   0, 2000, 'safe'),
        ]
        cursor.executemany(
            'INSERT INTO zones (name,count,max_capacity,status) VALUES (?,?,?,?)',
            zones)
        print("✅ Zones created!")
    conn.commit()
    conn.close()

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
        'INSERT INTO alerts (type, message, zone, time) VALUES (?,?,?,?)',
        (data['type'], data['message'], data['zone'],
         datetime.datetime.now().strftime('%H:%M:%S'))
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
    init_db()
    app.run(debug=True, port=8000)