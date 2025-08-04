"""
Project 1: Data Structure Design and Implementation
Dynamic Inventory Management System - Original (Reverted back previous implementation to run comparsion testing)

Implementing an inventory management system that can handle dynamic changes in product quantities, prices, and categories.
"""
# Importing additional packages for performance testing.
import time
import random
import sys
from collections import defaultdict

# Increasing recursion limit.
sys.setrecursionlimit(20000)

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
    
 # Printing of product objects
    def __repr__(self):
        return (f"Product ID: {self.product_id}, Name: {self.name}, "
                f"Price: {self.price}, Quantity: {self.quantity}, "
                f"Category: {self.category})")   
    
# Define a class for the inventory which manages products for rapid lookup.
class Inventory:
    # Initialize the inventory with a dictionary to hold products
    def __init__(self):
        self.products = {}
        # Secondary index to hold products grouped by categories.
        self.products_by_category =defaultdict(list)

    # Helper to update category index when product category changes.
    def _update_product_category(self, product, old_category, new_category):
        if old_category != new_category:
            # Remove the old category list
            if product in self.products_by_category[old_category]:
                self.products_by_category[old_category].remove(product)
            
            # Add new category list
            self.products_by_category[new_category].append(product)
            # Removing empty category lists.
            if not self.products_by_category[old_category]:
                del self.products_by_category[old_category]

    # Add a new product or update an existing product
    def add_product(self, product_id, name, price, quantity, category):
        if product_id in self.products:
            existing_product = self.products[product_id]
            # Store old category before update.
            old_category = existing_product.category

            existing_product.name = name
            existing_product.price = price
            existing_product.quantity += quantity
            existing_product.category = category
            # Update category if changed.
            self._update_product_category(existing_product, old_category, category)
        else:
            new_product = Product(product_id, name, price, quantity, category)
            self.products[product_id] = new_product
            # Add to category index
            self.products_by_category[category].append(new_product)
        #print(f"Product {product_id} has been added/updated.")
    
    # Update the quantity of an existing product
    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].quantity += quantity
            if self.products[product_id].quantity < 0:
                self.products[product_id].quantity = 0
            print(f"Quantity for Product ID {product_id} has been updated to {self.products[product_id].quantity}.")
        else:
            print(f"Product ID {product_id} not found in inventory.")
    
    # Update the price of an existing product
    def update_price(self, product_id, price):
        if product_id in self.products:
            self.products[product_id].price = price
            print(f"Price for Product ID {product_id} has been updated to {price}.")
        else:
            print(f"Product ID {product_id} not found in inventory.")

    # Get a product by its ID
    def get_product(self, product_id):
        return self.products.get(product_id, None)
    
    # Remove a product from the inventory
    def remove_product(self, product_id):
        if product_id in self.products:
            product_removal = self.products[product_id]
            category =product_removal.category

            # Removal from main products dictionary
            del self.products[product_id]
            # Removal from category index
            if product_removal in self.products_by_category[category]:
                self.products_by_category[category].remove(product_removal)
            # Clean up empty category lists
            if not self.products_by_category[category]:
                del self.products_by_category[category]
            print(f"Product ID {product_id} removed from inventory.")
        else:
            print(f"Product ID {product_id} not found in inventory.")
    
    # List all products in the inventory
    def list_products(self):
        return sorted(self.products.values())
    
    #Filter products based on multiple criteria.
    def filter_products(self, category=None, min_price=None, max_price =None,
                        min_quantity=None, max_quantity=None, name_keyword=None):
        # Subset of products if category selected, otherwise all products.
        if category:
            candidate = self.products_by_category.get(category, [])
        else:
            candidate = list(self.products.values())

        filtered_results = []
        for product in candidate:
            # Price filter
            if min_price is not None and product.price < min_price:
                continue
            if max_price is not None and product.price > max_price:
                continue

            # Quantity filter
            if min_quantity is not None and product.quantity < min_quantity:
                continue
            if max_quantity is not None and product.quantity > max_quantity:
                continue

            # Name keyword filter (not case sensitive)
            if name_keyword is not None and name_keyword.lower() not in product.name.lower():
                continue

            # if all pass, add to results list.
            filtered_results.append(product)
        # Results sorted by product id.
        return sorted(filtered_results)
    
# Adding in Performance Testing to get base comparsion for optimized application
def performance_testing(sizes):
    print("\n--Performance Testing Original Version--")
    for size in sizes:
        print(f"\nTesting for {size} products.")
        inventory = Inventory()

        # Adding Products
        # Start timer.
        start_timer_adding = time.perf_counter()
        # Random products.
        categories = ["Lounge", "Chairs", "Tables", "Case Goods"]
        for i in range(size):
            product_id = i + 1
            name = f"Product : {product_id}"
            price = round(random.uniform(10, 1000), 2)
            quantity = random.randint(0, 100)
            category = f"Category : {random.choice(categories)}"
            inventory.add_product(product_id, name, price, quantity, category)
        # End timer.
        end_timer_adding = time.perf_counter()
        # Elapsed time in ms.
        elapsed_add = ((end_timer_adding - start_timer_adding) * 1000)
        print(f"Adding Product Running Time: {elapsed_add} ms.")

        # Testing Get Product
        product_search =  random.randint(1, size)
        start_timer_search = time.perf_counter()
        inventory.get_product(product_search)
        end_timer_search = time.perf_counter()
        elapsed_search = ((end_timer_search - start_timer_search) * 1000)
        print(f"Search (Get) Product Running Time: {elapsed_search} ms.")

        # Filtering by Category
        # Start timer.
        start_timer_filter = time.perf_counter()
        # Random category.
        categories = ["Lounge", "Chairs", "Tables", "Case Goods"]
        test_category = f"Category : {random.choice(categories)}"
        inventory.filter_products(category=test_category)
        # End timer.
        end_timer_filter = time.perf_counter()
        # Elapsed time in ms.
        elapsed_filter = ((end_timer_filter - start_timer_filter) * 1000)
        print(f"Filter by Category '{test_category}': Running Time: {elapsed_filter} ms.")

        # Filtering by Keyword (Without Category)
        # Testing with Product keyword.
        test_keyword = "Product"
        # Start timer.
        start_timer_keyword = time.perf_counter()
        inventory.filter_products(name_keyword=test_keyword)
        # End timer.
        end_timer_keyword = time.perf_counter()
        # Elapsed time in ms.
        elapsed_keyword = ((end_timer_keyword - start_timer_keyword) * 1000)
        print(f"Filter Product by Keyword (Without Category) '{test_keyword}' Running Time: {elapsed_keyword} ms.")



# Main function to demonstrate the inventory management system, example use cases.

if __name__ == "__main__":
    print("Example Use Cases")
    inventory = Inventory()
    
    # Adding products
    inventory.add_product(1, "Three-seater Sofa", 1899.99, 10, "Lounge")
    inventory.add_product(2, "Two-seater Sofa", 999.99, 20, "Lounge")
    inventory.add_product(3, "Desk Chair", 389.99, 25, "Chairs")
    inventory.add_product(4, "Desk", 469.99, 20, "Tables")
    inventory.add_product(5, "Bookshelf", 289.99, 15, "Case Goods")
    inventory.add_product(6, "Adjustable Desk", 559.99, 12, "Tables")
    inventory.add_product(7, "Bar stool", 749.99, 19, "Chairs")
    inventory.add_product(8, "Coffee table", 689.99, 14, "Tables")
    inventory.add_product(9, "One-seater sofa", 899.99, 28, "Lounge")
    
    # Listing products
    print("Initial Inventory:")
    for product in inventory.list_products():
        print(product)
    
    # Updating quantity
    inventory.update_quantity(1, -2) # After selling 2 three-seater sofas
    inventory.update_quantity(3, 5)   # After adding 5 desk chairs
    print("\n--After Quantity Updates--")
    for product in inventory.list_products():
        print(product)
    
    # Updating price
    inventory.update_price(4, 429.99)  # Discount on desks.
    print("\n--After Price Updates--")
    for product in inventory.list_products():
        print(product)
    
    # Removing a product
    inventory.remove_product(5)  # Removing bookshelves.
    print("\n--After Removal of Bookshelves--")
    for product in inventory.list_products():
        print(product)
    
    # Filtering Examples
    print("\n--Filtering Examples--")

    # Filter by Category: Lounge
    print("\nProducts in the 'Lounge' category.")
    lng_products = inventory.filter_products(category="Lounge")
    for product in lng_products:
        print(product)

    # Filter by Price Range
    print("\nProducts with price between $100 and $500:")
    rng_products = inventory.filter_products(min_price=100, max_price=500)
    for product in rng_products:
        print(product)

    #Filter by Quantity Range
    print("\nProducts with quantity between 10 and 20:")
    avail_products = inventory.filter_products(min_quantity=10, max_quantity=20)
    for product in avail_products:
        print(product)

    # Filter by Name Keyword: Chair
    print("\nProducts with name keyword 'Chair'.")
    chr_products = inventory.filter_products(name_keyword="Chair")
    for product in chr_products:
        print(product)   

    # Combined Filters, two criteria.
    print("\n'Chairs' with price between $200 and $400:")
    filter_chairs = inventory.filter_products(category="Chairs", min_price=200, max_price=400)
    for product in filter_chairs:
        print(product)

    # Combined Filters, three criteria.
    print("\n'Lounge' with price > $900 and quantity < 25:")
    filter_lng = inventory.filter_products(category="Lounge", min_price= 900, max_quantity=25)
    for product in filter_lng:
        print(product)

    # Testing Category Changes
    print("\n--Testing Category Change--")
     # Change category of Desk Chair
    inventory.add_product(7,"Bar stool", 749.99, 19, "Kitchen Chairs")
    print("\nProducts in 'Chairs' category after change:")
    for product in inventory.filter_products(category="Chairs"):
        print(product)
    print("\nProducts in 'Kitchen Chairs' category after change:")
    for product in inventory.filter_products(category="Kitchen Chairs"):
        print(product)

    # Run Performance Testuing with different dataset sizes.
    test_sizes = [1000, 10000, 50000, 100000]
    performance_testing(test_sizes)