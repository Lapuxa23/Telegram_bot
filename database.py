import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            conn.execute("""
            CREATE TABLE IF NOT EXISTS review(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                complaint TEXT
            )
            """)
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS dishes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL,
                            description TEXT,
                            category TEXT,
                            portion_options TEXT
                        )
                    ''')
            def save_dish(self, data):

                    self.cursor.execute('''
                        INSERT INTO dishes (name, price, description, category, portion_options)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (data['name'], data['price'], data['description'], data['category'], data['portion_options']))

                    self.conn.commit()
            db = Database("restaurant.db")
    def save_complaint(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
            """
                INSERT INTO complaints (name, age, complaint)
                VALUES (?, ?, ?)
            """,
                (data["name"], data["age"], data["complaint"])
            )