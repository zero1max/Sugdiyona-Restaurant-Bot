import aiosqlite

DATABASE = 'news.db'

async def setup_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS news(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        await db.commit()

async def add_newss(title, description, image):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO news (title, description, image) VALUES (?, ?, ?)",
            (title, description, image)
        )
        await db.commit()

async def get_all_news():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT * FROM news') as cursor:
            return await cursor.fetchall()
