import sqlite3


class Database:
    def __init__(self, db_path="database.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS review(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                complaint TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                year INTEGER,
                author TEXT,
                price REAL NOT NULL,
                description TEXT,
                category TEXT,
                portion_options TEXT,
                cover TEXT
            )
        ''')
        self.conn.commit()

    def save_dish(self, data):
        try:
            self.cursor.execute('''
                INSERT INTO dishes (name, year, author, price, description, category, portion_options, cover)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (data['name'], data['year'], data['author'], data['price'], data['description'], data['category'],
                  data['portion_options'], data['cover']))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка записи в БД: {e}")
            self.conn.rollback()
            return False

    def save_complaint(self, data: dict):
        try:
            self.cursor.execute('''
                INSERT INTO review (name, age, complaint)
                VALUES (?, ?, ?)
            ''', (data["name"], data["age"], data["review"]))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка записи жалобы в БД: {e}")
            self.conn.rollback()
            return False

    def get_dishes(self, limit=5, offset=0):
        self.cursor.execute('''
            SELECT name, year, author, price, description, category, portion_options, cover FROM dishes
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        return self.cursor.fetchall()

    def get_total_dishes(self):
        self.cursor.execute('SELECT COUNT(*) FROM dishes')
        return self.cursor.fetchone()[0]

    def get_all_dishes(self):
        self.cursor.execute("SELECT * FROM dishes")
        rows = self.cursor.fetchall()
        dishes = []
        for row in rows:
            dishes.append({
                "id": row[0],
                "name": row[1],
                "year": row[2],
                "author": row[3],
                "price": row[4],
                "description": row[5],
                "category": row[6],
                "portion_options": row[7],
                "cover": row[8]
            })
        return dishes

    def close(self):
        self.conn.close()

