import sqlite3

def create_reviews_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            feedback TEXT,
            rating INTEGER,
            visit_date TEXT
        )
    ''')
    conn.commit()