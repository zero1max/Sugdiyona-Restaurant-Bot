import aiosqlite

DATABASE = 'product.db'

async def setup():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            category TEXT NOT NULL
        )''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS savat(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            phone VARCHAR NOT NULL,
            address TEXT NOT NULL
        )''')
        
        await db.commit()


async def add_product(name, price, description, image, category):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''INSERT INTO products(name, price, description, image, category) 
                             VALUES(?, ?, ?, ?, ?)''', 
                          (name, price, description, image, category))
        await db.commit()


async def add_users(user_id, phone, address):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''INSERT INTO users(user_id, phone, address) 
                             VALUES(?, ?, ?)''',
                          (user_id, phone, address))
        await db.commit()
        

async def add_savat(user_id, product_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''INSERT INTO savat(user_id, product_id) 
                             VALUES(?, ?)''', 
                          (user_id, product_id))
        await db.commit()


async def user_exists(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None

        
async def get_all_products():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT id, name, price, description, image, category FROM products") as pro:
            rows = await pro.fetchall()
            result = [
                {
                    "id": row[0],
                    "name": row[1],
                    "price": row[2],
                    "description": row[3],
                    "image": row[4],
                    "category": row[5],
                }
                for row in rows
            ]
            return result
        

async def delete_product(product_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM products WHERE id=?", (product_id,))
        await db.commit()


async def update_product(id, product_name, description, price, image, category):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "UPDATE products SET name = ?, description = ?, price = ?, image = ?, category = ? WHERE id = ?",
            (product_name, description, price, image, category, id))
        await db.commit()


async def get_products_by_category(category):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM products WHERE category=?", (category,)) as cate:
            result = await cate.fetchall()
            return result
        

async def get_categories():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT DISTINCT category FROM products") as cate:
            rows = await cate.fetchall()
            result = [row[0] for row in rows]
            return result
        

async def select_product_by_id(product_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM products WHERE id = ?", (product_id,)) as pro_id:
            result = await pro_id.fetchone()
            if result is None:
                return f"Product with ID {product_id} not found."
            return result


async def increment_product_count(product_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT count FROM savat WHERE id = ?", (product_id,)) as pro_id:
            row = await pro_id.fetchone()
            if row is None:
                raise ValueError(f"Product with ID {product_id} not found in savat.")
            current_count = row[0]

        await db.execute("UPDATE savat SET count = ? WHERE id = ?", (current_count + 1, product_id))
        await db.commit()


async def decrement_product_count(product_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT count FROM savat WHERE id = ?", (product_id,)) as pro_id:
            row = await pro_id.fetchone()
            if row is None:
                raise ValueError(f"Product with ID {product_id} not found in savat.")
            current_count = row[0]
            if current_count > 0:
                await db.execute("UPDATE savat SET count = ? WHERE id = ?", (current_count - 1, product_id))
                await db.commit()
            else:
                raise ValueError("Product count cannot go below zero.")


async def show_cart(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT id FROM savat WHERE id=?", (user_id)) as product:
            result = await product.fetchone()
            return result