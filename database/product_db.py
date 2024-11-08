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
        self.connect = sqlite3.connect('product.db')  
        self.cursor = self.connect.cursor()  
        self.shopping_carts = {}  
        self.current_product_id = 0  

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            category TEXT NOT NULL
        )''')
        self.connect.commit()  

    def add_products(self, name, price, description, image, category):
        self.cursor.execute("INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
                            (name, price, description, image, category))
        self.connect.commit() 

    def get_all_products(self):
        self.cursor.execute("SELECT id, name, price FROM products")
        return self.cursor.fetchall()  

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.connect.commit()
        return self.cursor.rowcount > 0 

    def update_product(self, id, product_name, description, price, image, category):
        self.cursor.execute("UPDATE products SET name = ?, description = ?, price = ?, image = ?, category = ? WHERE id = ?",
                            (product_name, description, price, image, category, id))
        self.connect.commit()  

    def get_products_by_category(self, category):
        self.cursor.execute("SELECT * FROM products WHERE category=?", (category,))
        return self.cursor.fetchall()  

    def get_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM products")
        return [row[0] for row in self.cursor.fetchall()]  

    def select_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.cursor.fetchone()
        if product is None:
            print(f"Product with ID {product_id} not found.")
        return product


    @staticmethod
    def add_to_cart(shopping_carts, user_id, product_id, quantity=1):
        if user_id not in shopping_carts:
            shopping_carts[user_id] = {}
        cart = shopping_carts[user_id]
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

    
    @staticmethod
    def remove_from_cart(shopping_carts, user_id, product_id, quantity=1):
        if user_id in shopping_carts and product_id in shopping_carts[user_id]:
            cart = shopping_carts[user_id]
            if cart[product_id] > quantity:
                cart[product_id] -= quantity
            else:
                del cart[product_id]

    
    def show_cart(self, user_id):
        if user_id in self.shopping_carts:
            cart = self.shopping_carts[user_id]
            result = ["<b>Sizning savatingizdagi mahsulotlar:</b>\n"]
            total_sum = 0
            
            for product_id, quantity in cart.items():
                product = self.select_product_by_id(product_id)
                if product:
                    product_name = product[1]
                    price = product[2]
                    total_price = price * quantity
                    total_sum += total_price  
                    result.append(f"{product_name}: {quantity} x {price} = {total_price} so'm")
                else:
                    result.append(f"Mahsulot {product_id} topilmadi")

            result.append(f"\n<b>Jami:</b> {total_sum} so'm")
            return "\n".join(result)
        
        return "Sizning savatingiz bo'sh."


    def update_cart_quantity(self, user_id, product_id, quantity_change):
        """Update the quantity of a product in the user's shopping cart by a change in quantity."""
        if user_id in self.shopping_carts:
            cart = self.shopping_carts[user_id]
            if product_id in cart:
                new_quantity = cart[product_id] + quantity_change
                if new_quantity < 1:
                    new_quantity = 1  
                cart[product_id] = new_quantity
            else:
                cart[product_id] = quantity_change if quantity_change > 0 else 1
        else:
            self.shopping_carts[user_id] = {product_id: quantity_change if quantity_change > 0 else 1}


    def get_cart_product_quantity(self, user_id, product_id):
        """Return the current quantity of a product in the user's cart."""
        if user_id in self.shopping_carts and product_id in self.shopping_carts[user_id]:
            return self.shopping_carts[user_id][product_id]
        return 0  


    def close(self):
        if self.cursor:
            self.cursor.close() 
        if self.connect:
            self.connect.close()  
