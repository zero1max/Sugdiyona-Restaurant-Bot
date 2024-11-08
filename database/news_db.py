import sqlite3
from dataclasses import dataclass

@dataclass
class Database_News:
    connect: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __post_init__(self):
        self.connect = sqlite3.connect('news.db')
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS news(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        self.connect.commit()

    def add_news(self, title, description, image):
        self.cursor.execute("INSERT INTO news (title, description, image) VALUES (?, ?, ?)",
                            (title, description, image))
        self.connect.commit()

    def get_all_news(self):
        self.cursor.execute("SELECT * FROM news")
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
