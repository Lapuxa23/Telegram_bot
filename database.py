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
            conn.execute("""
            CREATE TABLE IF NOT EXISTS food(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                year INTEGER,
                author TEXT,
                price INTEGER
            )
            """)

    def save_complaint(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
            """
                INSERT INTO complaints (name, age, complaint)
                VALUES (?, ?, ?)
            """,
                (data["name"], data["age"], data["complaint"])
            )

    def save_book(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
            """
                INSERT INTO books (name, year, author, price)
                VALUES (?, ?, ?, ?)
            """,
                (data["name"], data["year"], data["author"], data["price"])
            )