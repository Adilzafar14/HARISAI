import sqlite3

def connect():
    conn = sqlite3.connect('harisai.db')
    return conn

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            message TEXT,
            zone TEXT,
            time TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            count INTEGER,
            max_capacity INTEGER,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables created!")

def insert_default_zones():
    conn = connect()
    cursor = conn.cursor()

    zones = [
        ('Masjid Al-Haram', 0, 1200, 'safe'),
        ('Safa-Marwa Path', 0, 800, 'safe'),
        ('Mina Camp Zone', 0, 1500, 'safe'),
        ('Jamarat Bridge', 0, 600, 'safe'),
        ('Arafat Ground', 0, 2000, 'safe'),
    ]

    cursor.executemany('''
        INSERT INTO zones (name, count, max_capacity, status)
        VALUES (?, ?, ?, ?)
    ''', zones)

    conn.commit()
    conn.close()
    print("Default zones added!")

if __name__ == '__main__':
    create_tables()
    insert_default_zones()