import sqlite3
from dataclasses import dataclass


@dataclass
class Database_Product:
    connect: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None
    current_product_id: str = None
    current_category: str = None
    shopping_carts: dict = None

    def __post_init__(self):
        self.connect = sqlite3.connect('product.db')  # 'product.db' ma'lumotlar bazasi bilan ulanish
        self.cursor = self.connect.cursor()  # Ma'lumotlar bazasi uchun kursorni yaratish
        self.shopping_carts = {}  # Savatchalar lug'ati
        self.current_product_id = 0  # Hozirgi mahsulot ID

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            category TEXT NOT NULL,
            count INTEGER default 0
        )''')
        self.connect.commit()  # O'zgarishlarni saqlash

    def add_products(self, name, price, description, image, category):
        self.cursor.execute("INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
                            (name, price, description, image, category))
        self.connect.commit()  # O'zgarishlarni saqlash

    def get_all_products(self):
        self.cursor.execute("SELECT id, name, price FROM products")
        return self.cursor.fetchall()  # Barcha mahsulotlarni qaytarish

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.connect.commit()  # O'zgarishlarni saqlash
        return self.cursor.rowcount > 0  # O'chirilgan mahsulotlar sonini qaytarish

    def update_product(self, id, product_name, description, price, image, category):
        self.cursor.execute(
            "UPDATE products SET name = ?, description = ?, price = ?, image = ?, category = ? WHERE id = ?",
            (product_name, description, price, image, category, id))
        self.connect.commit()  # O'zgarishlarni saqlash

    def get_products_by_category(self, category):
        self.cursor.execute("SELECT * FROM products WHERE category=?", (category,))
        return self.cursor.fetchall()  # Ma'lum bir kategoriya bo'yicha mahsulotlarni qaytarish

    def get_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM products")
        return [row[0] for row in self.cursor.fetchall()]  # Barcha kategoriyalarni qaytarish

    def select_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.cursor.fetchone()
        if product is None:
            print(f"Product with ID {product_id} not found.")
        return product

    def add_to_cart(self, user_id, product_id):
        """Foydalanuvchi savatiga mahsulot qo'shadi yoki mavjud mahsulot sonini oshiradi."""
        # Agar foydalanuvchining savati bo'lmasa, yangi yaratish
        if user_id not in self.shopping_carts:
            self.shopping_carts[user_id] = {}
            print(self.shopping_carts)

        # Mahsulotni savatga qo'shish yoki mavjud bo'lsa, sonini oshirish
        if product_id not in self.shopping_carts[user_id]:
            self.shopping_carts[user_id][product_id] = 1  # Yangi mahsulotni soni bilan qo'shish
            print(self.shopping_carts)
        else:
            self.update_cart(user_id, product_id, 1)

    def remove_from_cart(self, user_id, product_id, quantity=1):
        self.update_cart(user_id, product_id, -quantity)

    def get_users_count(self, product_id):
        self.cursor.execute("SELECT count FROM products WHERE id=?", (product_id,))
        return self.cursor.fetchone()

    def increment_product_count(self, product_id):
        # Avval hozirgi count qiymatini olish
        self.cursor.execute("SELECT count FROM products WHERE id = ?", (product_id,))
        current_count = self.cursor.fetchone()[0]

        # count qiymatini oshirish va yangilash
        self.cursor.execute("UPDATE products SET count = ? WHERE id = ?", (current_count + 1, product_id))
        self.connect.commit()

    def show_cart(self, user_id):
        """Foydalanuvchining savatidagi barcha mahsulotlarning nomi, narxi va sonini qaytaradi."""
        if user_id not in self.shopping_carts or not self.shopping_carts[user_id]:
            return ""  # Agar savat bo'sh bo'lsa, bo'sh qiymat qaytaramiz

        cart = self.shopping_carts[user_id]
        result = []
        total_price = 0  # Jami narxni hisoblash

        # 0 miqdorli mahsulotlarni olib tashlaymiz
        items_to_remove = [product_id for product_id, quantity in cart.items() if quantity <= 0]
        for product_id in items_to_remove:
            del cart[product_id]

        # Agar savat bo'sh bo'lib qolgan bo'lsa
        if not cart:
            return ""

        # Savatdagi barcha mahsulotlar haqida ma'lumot chiqarish
        for product_id, quantity in cart.items():
            product = self.select_product_by_id(product_id)
            if product:
                product_name = product[1]
                price = product[2]
                count = product[-1]
                product_total = price * quantity  # Mahsulotning jami narxi
                total_price += product_total  # Jami narxni yangilash
                result.append(
                    f"{product_name}: {price} so'm (x{quantity}) - Jami: {product_total} Count {count} ID {product_id}")
            else:
                result.append(f"Mahsulot ID {product_id} topilmadi")

        # Mahsulotlar ro'yxati va umumiy narxni qaytaramiz
        return "\n".join(result), total_price

    def update_cart(self, user_id, product_id, quantity_change):
        """Foydalanuvchining savatidagi mahsulot miqdorini o'zgartirish."""
        if user_id not in self.shopping_carts:
            self.shopping_carts[user_id] = {}

        cart = self.shopping_carts[user_id]
        new_quantity = cart.get(product_id, 0) + quantity_change

        if new_quantity <= 0:
            cart.pop(product_id, None)  # Mahsulotni savatdan o'chirish
        else:
            cart[product_id] = new_quantity  # Mahsulot sonini yangilash

    def get_cart_product_quantity(self, user_id, product_id):
        """Foydalanuvchining savatidagi mahsulot miqdorini qaytaradi."""
        return self.shopping_carts.get(user_id, {}).get(product_id, 0)

    def close(self):
        if self.cursor:
            self.cursor.close()  # Kursorni yopish
        if self.connect:
            self.connect.close()  # Ulanishni yopish

import aiosqlite

DATABASE = 'product.db'

async def setup():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,  -- Narxni REAL yoki FLOAT turida saqlash tavsiya etiladi
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
            user_id INTEGER UNIQUE NOT NULL,  -- Agar user_id noyob bo'lsa, UNIQUE qo'shish mumkin
            phone VARCHAR NOT NULL,
            address TEXT NOT NULL
        )''')
        
        await db.commit()


async def add_product(name, price, description, image, category):
    async with aiosqlite.connect(DATABASE) as db:
        db.execute('''INSERT INTO products(name, price, description, image, category) VALUES(?, ?, ?, ?, ?)''', 
                (name, price, description, image, category))
        await db.commit()


async def add_users(user_id, phone, address):
    async with aiosqlite.connect(DATABASE) as db:
        db.execute('''INSERT INTO users(user_id, phone, address) VALUES(?, ?, ?)''',
                (user_id, phone, address))
        await db.commit()


# async def show_savat(user_id):
#     async with aiosqlite.connect(DATABASE) as db:
        

async def user_exists(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('''SELECT * FROM users WHERE user_id = ?''',(user_id)) as cursor:
            result = await cursor.fetchmany(1)
            return bool(len(result))
