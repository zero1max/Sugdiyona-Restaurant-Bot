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
            category TEXT NOT NULL
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
        self.cursor.execute("UPDATE products SET name = ?, description = ?, price = ?, image = ?, category = ? WHERE id = ?",
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


    def set_current_category(self, category):
        self.current_category = category  # Hozirgi kategoriyani o'rnatish
        self.current_product_id = self.get_min_product_id_for_category(category)  # Minimal mahsulot ID ni olish

    def get_min_product_id_for_category(self, category):
        self.cursor.execute("SELECT MIN(id) FROM products WHERE category=?", (category,))
        min_id = self.cursor.fetchone()[0]
        return min_id if min_id is not None else 0  # Minimal mahsulot ID ni qaytarish

    def get_max_product_id_for_category(self, category):
        self.cursor.execute("SELECT MAX(id) FROM products WHERE category=?", (category,))
        max_id = self.cursor.fetchone()[0]
        return max_id if max_id is not None else 0  # Maksimal mahsulot ID ni qaytarish

    def select_next_product(self):
        self.current_product_id += 1
        
        product = self.select_product_by_id(self.current_product_id)
        
        if not product and self.current_category:
            self.current_product_id = self.get_min_product_id_for_category(self.current_category)
            product = self.select_product_by_id(self.current_product_id)
        
        return product  # Keyingi mahsulotni qaytarish
    
    def select_previous_product(self):
        self.current_product_id -= 1
        
        product = self.select_product_by_id(self.current_product_id)

        if not product and self.current_category:
            self.current_product_id = self.get_max_product_id_for_category(self.current_category)
            product = self.select_product_by_id(self.current_product_id)
        
        return product  # Oldingi mahsulotni qaytarish

    @staticmethod
    def add_to_cart(shopping_carts, user_id, product_id, quantity=1):
        if user_id not in shopping_carts:
            shopping_carts[user_id] = {}
        cart = shopping_carts[user_id]
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity  # Savatchaga mahsulot qo'shish

    
    @staticmethod
    def remove_from_cart(shopping_carts, user_id, product_id, quantity=1):
        # Check if the user exists in the shopping cart
        if user_id in shopping_carts:
            cart = shopping_carts[user_id]

            # Check if the product exists in the user's cart
            if product_id in cart:
                # If the product quantity is greater than the requested quantity, reduce the quantity
                if cart[product_id] > quantity:
                    cart[product_id] -= quantity
                else:
                    # Otherwise, remove the product from the cart
                    del cart[product_id]
                return True  # Indicate the product was successfully removed
        return False  # If the user or product does not exist in the cart

    
    def show_cart(self, user_id):
        """Savatchadagi mahsulotlarni ko'rsatish."""
        if user_id in self.shopping_carts:
            cart = self.shopping_carts[user_id]
            print(cart)
            result = []
            for product_id, quantity in cart.items():
                product = self.select_product_by_id(product_id)
                if product:
                    product_name = product[1]  # Mahsulot nomi
                    price = product[2]  # Mahsulot narxi
                    total_price = price * quantity
                    result.append(f"{product_name}: {quantity} x {price} = {total_price}")
                else:
                    result.append(f"Product {product_id} not found")
            return "\n".join(result) if result else "Sizning savatingiz bo'sh."
        return "Sizning savatingiz bo'sh."  # Savat bo'sh bo'lsa xabar


    def update_cart_quantity(self, user_id, product_id, quantity):
        """Update the quantity of a product in the user's shopping cart."""
        if user_id in self.shopping_carts:
            cart = self.shopping_carts[user_id]
            if product_id in cart:
                cart[product_id] = quantity  # Update the quantity to the new value
            else:
                cart[product_id] = quantity  # If the product is not in the cart, add it with the given quantity
        else:
            self.shopping_carts[user_id] = {product_id: quantity}  # Create a new cart if not existing

    def get_cart_product_quantity(self, user_id, product_id):
        """Return the current quantity of a product in the user's cart."""
        if user_id in self.shopping_carts and product_id in self.shopping_carts[user_id]:
            return self.shopping_carts[user_id][product_id]
        return 0  # If product is not in the cart, return 0


    def close(self):
        if self.cursor:
            self.cursor.close()  # Kursorni yopish
        if self.connect:
            self.connect.close()  # Ulanishni yopish
