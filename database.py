import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS review(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                complaint TEXT
            )
            """)
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS dishes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        description TEXT,
                        category TEXT,
                        portion_options TEXT
                    )
                ''')
        self.conn.commit()

    def dishes_review(self, data):
        try:
            self.cursor.execute('''
                    INSERT INTO dishes (name, price, description, category, portion_options)
                    VALUES (?, ?, ?, ?, ?)
                ''', (data['name'], data['price'], data['description'], data['category'], data['portion_options']))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка записи в БД: {e}")
            self.conn.rollback()
            return False

    def save_complaint(self, data: dict):
        try:
            self.cursor.execute(
                """
                    INSERT INTO review (name, age, complaint)
                    VALUES (?, ?, ?)
                """,
                (data["name"], data["age"], data["review"])
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка записи жалобы в БД: {e}")
            self.conn.rollback()
            return False

    def get_all_dishes(self):
        self.cursor.execute("SELECT * FROM dishes")
        rows = self.cursor.fetchall()
        dishes = []
        for row in rows:
            dishes.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "description": row[3],
                "category": row[4],
                "portion_options": row[5]
            })
        return dishes

    def close(self):
        self.conn.close()
