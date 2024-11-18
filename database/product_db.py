# import sqlite3
# from dataclasses import dataclass


# @dataclass
# class Database_Product:
#     connect: sqlite3.Connection = None
#     cursor: sqlite3.Cursor = None
#     current_product_id: str = None
#     current_category: str = None
#     shopping_carts: dict = None

#     def __post_init__(self):
#         self.connect = sqlite3.connect('product.db')  # 'product.db' ma'lumotlar bazasi bilan ulanish
#         self.cursor = self.connect.cursor()  # Ma'lumotlar bazasi uchun kursorni yaratish
#         self.shopping_carts = {}  # Savatchalar lug'ati
#         self.current_product_id = 0  # Hozirgi mahsulot ID

#     def create_table(self):
#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
#             id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             price INTEGER NOT NULL,
#             description TEXT NOT NULL,
#             image TEXT NOT NULL,
#             category TEXT NOT NULL,
#             count INTEGER default 0
#         )''')
#         self.connect.commit()  # O'zgarishlarni saqlash

#     def add_products(self, name, price, description, image, category):
#         self.cursor.execute("INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
#                             (name, price, description, image, category))
#         self.connect.commit()  # O'zgarishlarni saqlash

#     def get_all_products(self):
#         self.cursor.execute("SELECT id, name, price FROM products")
#         return self.cursor.fetchall()  # Barcha mahsulotlarni qaytarish

#     def delete_product(self, product_id):
#         self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
#         self.connect.commit()  # O'zgarishlarni saqlash
#         return self.cursor.rowcount > 0  # O'chirilgan mahsulotlar sonini qaytarish

#     def update_product(self, id, product_name, description, price, image, category):
#         self.cursor.execute(
#             "UPDATE products SET name = ?, description = ?, price = ?, image = ?, category = ? WHERE id = ?",
#             (product_name, description, price, image, category, id))
#         self.connect.commit()  # O'zgarishlarni saqlash

#     def get_products_by_category(self, category):
#         self.cursor.execute("SELECT * FROM products WHERE category=?", (category,))
#         return self.cursor.fetchall()  # Ma'lum bir kategoriya bo'yicha mahsulotlarni qaytarish

#     def get_categories(self):
#         self.cursor.execute("SELECT DISTINCT category FROM products")
#         return [row[0] for row in self.cursor.fetchall()]  # Barcha kategoriyalarni qaytarish

#     def select_product_by_id(self, product_id):
#         self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
#         product = self.cursor.fetchone()
#         if product is None:
#             print(f"Product with ID {product_id} not found.")
#         return product

#     def add_to_cart(self, user_id, product_id):
#         """Foydalanuvchi savatiga mahsulot qo'shadi yoki mavjud mahsulot sonini oshiradi."""
#         # Agar foydalanuvchining savati bo'lmasa, yangi yaratish
#         if user_id not in self.shopping_carts:
#             self.shopping_carts[user_id] = {}
#             print(self.shopping_carts)

#         # Mahsulotni savatga qo'shish yoki mavjud bo'lsa, sonini oshirish
#         if product_id not in self.shopping_carts[user_id]:
#             self.shopping_carts[user_id][product_id] = 1  # Yangi mahsulotni soni bilan qo'shish
#             print(self.shopping_carts)
#         else:
#             self.update_cart(user_id, product_id, 1)


#     def increment_product_count(self, product_id):
#         # Avval hozirgi count qiymatini olish
#         self.cursor.execute("SELECT count FROM products WHERE id = ?", (product_id,))
#         current_count = self.cursor.fetchone()[0]

#         # count qiymatini oshirish va yangilash
#         self.cursor.execute("UPDATE products SET count = ? WHERE id = ?", (current_count + 1, product_id))
#         self.connect.commit()

#     def show_cart(self, user_id):
#         """Foydalanuvchining savatidagi barcha mahsulotlarning nomi, narxi va sonini qaytaradi."""
#         if user_id not in self.shopping_carts or not self.shopping_carts[user_id]:
#             return ""  # Agar savat bo'sh bo'lsa, bo'sh qiymat qaytaramiz

#         cart = self.shopping_carts[user_id]
#         result = []
#         total_price = 0  # Jami narxni hisoblash

#         # 0 miqdorli mahsulotlarni olib tashlaymiz
#         items_to_remove = [product_id for product_id, quantity in cart.items() if quantity <= 0]
#         for product_id in items_to_remove:
#             del cart[product_id]

#         # Agar savat bo'sh bo'lib qolgan bo'lsa
#         if not cart:
#             return ""

#         # Savatdagi barcha mahsulotlar haqida ma'lumot chiqarish
#         for product_id, quantity in cart.items():
#             product = self.select_product_by_id(product_id)
#             if product:
#                 product_name = product[1]
#                 price = product[2]
#                 count = product[-1]
#                 product_total = price * quantity  # Mahsulotning jami narxi
#                 total_price += product_total  # Jami narxni yangilash
#                 result.append(
#                     f"{product_name}: {price} so'm (x{quantity}) - Jami: {product_total} Count {count} ID {product_id}")
#             else:
#                 result.append(f"Mahsulot ID {product_id} topilmadi")

#         # Mahsulotlar ro'yxati va umumiy narxni qaytaramiz
#         return "\n".join(result), total_price


#     def get_cart_product_quantity(self, user_id, product_id):
#         """Foydalanuvchining savatidagi mahsulot miqdorini qaytaradi."""
#         return self.shopping_carts.get(user_id, {}).get(product_id, 0)

#     def close(self):
#         if self.cursor:
#             self.cursor.close()  # Kursorni yopish
#         if self.connect:
#             self.connect.close()  # Ulanishni yopish

# -------------------------------------------------------------------------------------

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