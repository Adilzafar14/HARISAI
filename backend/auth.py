import sqlite3

def connect():
    conn = sqlite3.connect('../database/harisai.db')
    return conn

def create_admin(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO admins (username, password)
        VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()
    print(f"Admin '{username}' created!")

def check_admin(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM admins
        WHERE username = ? AND password = ?
    ''', (username, password))
    admin = cursor.fetchone()
    conn.close()
    if admin:
        return True
    return False

if __name__ == '__main__':
    create_admin('admin', 'harisai123')