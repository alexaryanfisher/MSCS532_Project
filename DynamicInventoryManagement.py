"""
Project 1: Data Structure Design and Implementation
Dynamic Inventory Management System

Implementing an inventory management system that can handle dynamic changes in product quantities, prices, and categories.
"""

from collections import defaultdict

# Define a class for products in the inventory
class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

# Tie-breaker for sorting products by product_id
    def __lt__(self, other):
        return self.product_id < other.product_id
    
# Define a class for the inventory which manages products for rapid lookup.
class Inventory:
    # Initialize the inventory with a dictionary to hold products
    def __init__(self):
        self.products = {}

    # Add a new product or update an existing product
    def add_product(self, product_id, name, price, quantity, category):
        if product_id in self.products:
            existing_product = self.products[product_id]
            existing_product.name = name
            existing_product.price = price
            existing_product.quantity += quantity
            existing_product.category = category
        else:
            self.products[product_id] = Product(product_id, name, price, quantity, category)
    
    # Update the quantity of an existing product
    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].quantity += quantity
            if self.products[product_id].quantity < 0:
                self.products[product_id].quantity = 0
        else:
            print(f"Product ID {product_id} not found in inventory.")
    
    # Update the price of an existing product
    def update_price(self, product_id, price):
        if product_id in self.products:
            self.products[product_id].price = price
        else:
            print(f"Product ID {product_id} not found in inventory.")

    # Get a product by its ID
    def get_product(self, product_id):
        return self.products.get(product_id, None)
    
    # Remove a product from the inventory
    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
        else:
            print(f"Product ID {product_id} not found in inventory.")
    
    # List all products in the inventory
    def list_products(self):
        return sorted(self.products.values())
    
# Main function to demonstrate the inventory management system, example use cases.

if __name__ == "__main__":
    inventory = Inventory()
    
    # Adding products
    inventory.add_product(1, "Three-seater Sofa", 1899.99, 10, "Lounge")
    inventory.add_product(2, "Two-seater Sofa", 999.99, 20, "Lounge")
    inventory.add_product(3, "Desk Chair", 389.99, 25, "Chairs")
    inventory.add_product(4, "Desk", 469.99, 20, "Tables")
    inventory.add_product(5, "Bookshelf", 289.99, 15, "Case Goods")
    
    # Listing products
    print("Initial Inventory:")
    for product in inventory.list_products():
        print(f"{product.product_id}: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Category: {product.category}")
    
    # Updating quantity
    #Example: Selling 2 three-seater sofas
    inventory.update_quantity(1, -2) 
    print("\nAfter selling 2 three-seater sofas:")
    for product in inventory.list_products():
        print(f"{product.product_id}: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Category: {product.category}")
    
    # Adding 5 more desk chairs
    inventory.update_quantity(3, 5)   # Add 5 desk chairs
    print("\nAfter adding 5 desk chairs to inventory:")
    for product in inventory.list_products():
        print(f"{product.product_id}: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Category: {product.category}")
    
    # Updating price
    inventory.update_price(4, 429.99)  # Discount on desks.
    print("\nAfter updating desk price:")
    for product in inventory.list_products():
        print(f"{product.product_id}: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Category: {product.category}")
    
    # Removing a product
    inventory.remove_product(5)  # Removing bookshelves.
    print("\nAfter removing bookshelves:")
    for product in inventory.list_products():
        print(f"{product.product_id}: {product.name}, Price: {product.price}, Quantity: {product.quantity}, Category: {product.category}")