"""
Project 1: Data Structure Design and Implementation
Dynamic Inventory Management System - Copied and Optimized.

Implementing an inventory management system that can handle dynamic changes in product quantities, prices, and categories. Adding optimizations to account for large data sets.
Changes include using more efficient data structures and adding a performance analysis framework.
"""
## Adding additional packages for performance testing.
import time
import random
import sys
from collections import defaultdict

# Increase  recursion limit for deep recursion.
sys.setrecursionlimit(20000)

# Define a class for products in the inventory
class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.data = {
            'product_id' : product_id,
            'name' : name,
            'price' : price,
            'quantity' : quantity,
            'category' : category
        }

        self.product_id =  product_id

# Tie-breaker for sorting products by product_id
    def __lt__(self, other):
        return self.product_id < other.product_id
    
 # Printing of product objects
    def __repr__(self):
        return (f"Product ID: {self.product_id}, Name: {self.data['name']}, "
                f"Price: {self.data['price']}, Quantity: {self.data['quantity']}, "
                f"Category: {self.data['category']})")

# Enabling Product objects to be used as dictionary keys and in sets.
    def __hash__(self):
        return hash(self.product_id)
    
# Equality comparsion for Product objects based on product id.
    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.product_id == other.product_id
    
# Define a class for the inventory which manages products for rapid lookup.
class Inventory:
    # Initialize the inventory with a dictionary to hold products
    def __init__(self):
        self.products = {}
        # Secondary index to hold products grouped by categories.
        self.products_by_category =defaultdict(set) #Changing from list to set for more efficient searching.

    # Helper to update category index when product category changes.
    def _update_product_category(self, product_id, old_category, new_category):
       # New optimized helper for updating category index when product category changes.
       if old_category:
           # Remove from old category set.
           self.products_by_category[old_category].discard(product_id)
           # Removal of category key is set is empty.
           if not self.products_by_category[old_category]:
               del self.products_by_category[old_category]

       # Add new category set.
       if new_category:
           self.products_by_category[new_category].add(product_id) 

    # Add a new product or update an existing product
    def add_product(self, product_id, name, price, quantity, category):
       # New optimized add product function.
       # Check if new product exists.
       if product_id in self.products:
           old_category = self.products[product_id].data['category']
           new_product = self.products[product_id]
           new_product.data.update({'name': name, 'price': price, 'quantity': quantity, 'category': category})
           self._update_product_category(product_id, old_category, category)
       else:
           # Adding new product.
           new_product = Product(product_id, name, price, quantity, category)
           self.products[product_id] = new_product
           # Add new product id to category set
           self.products_by_category[category].add(product_id)

    # Get a product by its ID
    def get_product(self, product_id):
        return self.products.get(product_id, None)

    # Remove a product from the inventory
    def remove_product(self, product_id):
       # New optimized removal of products.
        if product_id in self.products:
           product = self.products[product_id]
           category = product.data['category']
           # Removal of product from dictionary.
           del self.products[product_id]
           # Removal of product from secondary category index.
           self.products_by_category[category].discard(product_id)
           if not self.products_by_category[category]:
               del self.products_by_category[category]
           return True
        return False
    
    # List all products in the inventory
    def list_products(self):
        return sorted(self.products.values())
    
    #Filter products based on multiple criteria.
    def filter_products(self, category=None, min_price=None, max_price =None,
                        min_quantity=None, max_quantity=None, name_keyword=None):
        # Subset of products if category selected, otherwise all products.
       filtered_results = []
       if category and category in self.products_by_category:
            candidate_ids = self.products_by_category[category]
            candidate = [self.products[candid] for candid in candidate_ids]
       else:
            candidate = self.products.values()

       for product in candidate:
            is_match = True

            # Price filter
            if min_price is not None and product.data['price'] < min_price:
                is_match = False
            if max_price is not None and product.data['price'] > max_price:
                is_match = False

            # Quantity filter
            if min_quantity is not None and product.data['quantity'] < min_quantity:
                is_match = False
            if max_quantity is not None and product.data['quantity'] > max_quantity:
                is_match = False

            # Name keyword filter (not case sensitive)
            if name_keyword is not None and name_keyword.lower() not in product.data['name'].lower():
                is_match = False

            if is_match:
                filtered_results.append(product)

        # Results sorted by product id.
       return filtered_results

# Generate a large dataset for testing.    
def generate_large_ds(size):
    inventory = Inventory()
    categories = ["Lounge", "Chairs", "Tables", "Case Goods"]
    for i in range(size):
        product_id = i + 1
        name = f"Product : {product_id}"
        price = round(random.uniform(10, 1000), 2)
        quantity = random.randint(0, 100)
        category = random.choice(categories)
        inventory.add_product(product_id, name, price, quantity, category)
    return inventory

def run_performance_testing():
    # Performs performance testing on inventory operations on different dataset sizes.
    print("---Performance Testing Optimized Version---")
    sizes = [1000, 10000, 50000, 100000]

    for size in sizes:
        print(f"\n Testing for {size} products.")
        inventory = generate_large_ds(size)

        # Testing add/update
        # Getting start time.
        start_time = time.perf_counter()
        inventory.add_product(1, "Three-seater Sofa", 1899.99, 10, "Lounge")
        # Getting end time.
        end_time = time.perf_counter()
        # Getting running time in milliseconds.
        elapsed_time = ((end_time - start_time) * 1000)
        print(f" Add/Update Product Running Time: {elapsed_time} milliseconds.")
    
        # Testing Get Product
        product_search =  random.randint(1, size)
        start_time = time.perf_counter()
        inventory.get_product(product_search)
        end_time = time.perf_counter()
        elapsed_time = ((end_time - start_time) * 1000)
        print(f" Search (Get) Product Running Time: {elapsed_time} milliseconds.")

        # Testing Filter Product with Category
        category_filter =  random.choice(["Lounge", "Chairs", "Tables", "Case Goods"])
        start_time = time.perf_counter()
        inventory.filter_products(category=category_filter)
        end_time = time.perf_counter()
        elapsed_time = ((end_time - start_time) * 1000)
        print(f" Filter by Category '{category_filter}': Running Time: {elapsed_time} milliseconds.")

        # Testing Filter Product with no Category
        start_time = time.perf_counter()
        inventory.filter_products(min_price=300, max_quantity=15)
        end_time = time.perf_counter()
        elapsed_time = ((end_time - start_time) * 1000)
        print(f" Filter Product with no Category Running Time: {elapsed_time} milliseconds.")        

        # Testing Removal
        product_removal = random.randint(1, size)
        start_time = time.perf_counter()
        inventory.remove_product(product_removal)
        end_time = time.perf_counter()
        elapsed_time = ((end_time - start_time) * 1000)
        print(f" Removing Product Running Time: {elapsed_time} milliseconds.")

# Advanced Testing and Validation
def run_advance_testing():
    print("---Advanced Testing and Validation---")
    print("\n---Use Cases---")
    inventory = Inventory()

    # Add new product.
    print("Test Case 1: Adding a new product.")
    inventory.add_product(101, "Planter", 3200.00, 50, "Case Goods")
    product = inventory.get_product(101)
    assert product is not None and product.data['name'] == "Planter", "Test Case 1 Failed: Product not added correctly."
    assert "Case Goods" in inventory.products_by_category and 101 in inventory.products_by_category["Case Goods"], "Test Case 1 Failed: Category index not updated."
    print("Test Case 1 Passed.")

    # Update existing product's attributes
    print("Test Case 2: Updating an existing product.")
    inventory.add_product(101, "Single Planter", 3400.00, 50, "Case Goods")
    product = inventory.get_product(101)
    assert product.data['name'] == "Single Planter" and product.data['price'] == 3400.00, "Test Case 2 Failed: Product not updated correctly."
    print("Test Case 2 Passed.")

    # Update product category
    print("Test Case 3: Updating product category.")
    inventory.add_product(101, "Single Planter", 3400.00, 50, "Decor")
    assert "Case Goods" not in inventory.products_by_category or 101 not in inventory.products_by_category["Case Goods"], "Test Case 3 Failed: Old category not cleared."
    assert "Decor" in inventory.products_by_category and 101 in inventory.products_by_category["Decor"], "Test Case 3 Failed: New category not updated."
    print("Test Case 3 Passed.")

    # Test Case 4: Remove a product
    print("Test Case 4: Removing a product.")
    inventory.remove_product(101)
    assert inventory.get_product(101) is None, "Test Case 4 Failed: Product not removed."
    assert "Decor" not in inventory.products_by_category or 101 not in inventory.products_by_category["Decor"], "Test Case 4 Failed: Product not removed from category index."
    print("Test Case 4 Passed.")

    # Test Case 5: Filter products with multiple criteria
    print("Test Case 5: Filtering products.")
    inventory.add_product(201, "Conference Swivel Chair", 259.99, 100, "Chairs")
    inventory.add_product(202, "Conference Fixed Chair", 279.99, 75, "Chairs")
    inventory.add_product(203, "Accent Chaise", 2469.99, 21, "Lounge")
    
    filtered = inventory.filter_products(category="Chairs", min_price=260)
    assert len(filtered) == 1 and filtered[0].product_id == 202, "Test Case 5 Failed: Filter by category and price."
    
    filtered_keyword = inventory.filter_products(name_keyword="Chaise")
    assert len(filtered_keyword) == 1 and filtered_keyword[0].product_id == 203, "Test Case 5 Failed: Filter by name keyword."
    print("Test Case 5 Passed.")

# Stress Testing
    print("--Stress Testing--")
    # Larger Size for stress testing.
    stress_size = 200000  
    print(f"Performing stress test with {stress_size} operations.")
    stress_inventory = Inventory()
    start_timer_stress = time.perf_counter()

    # Adding random products in the larger qty.
    for i in range(stress_size):
        product_id = i + 1
        name = f"StressProduct: {product_id}"
        price = random.uniform(1, 1000)
        quantity = random.randint(1, 100)
        category = random.choice(["Lounge", "Chairs", "Tables", "Case Goods"])
        stress_inventory.add_product(product_id, name, price, quantity, category)
    
    # Perform random operations on the large dataset
    for _ in range(stress_size // 2):
        oper_type = random.choice(["add", "get", "remove", "filter"])
        product_id = random.randint(1, stress_size)

        if oper_type == "add":
            stress_inventory.add_product(product_id, f"UpdatedStressProduct_{product_id}", random.uniform(1, 1000), random.randint(1, 100), random.choice(["Lounge", "Chairs", "Tables", "Case Goods"]))
        elif oper_type == "get":
            stress_inventory.get_product(product_id)
        elif oper_type == "remove":
            stress_inventory.remove_product(product_id)
        elif oper_type == "filter":
            stress_inventory.filter_products(category=random.choice(["Lounge", "Chairs", "Tables", "Case Goods"]), min_price=random.uniform(1, 500))

    end_timer_stress = time.perf_counter()
    elapsed_stress = ((end_timer_stress - start_timer_stress) * 1000)
    print(f"Stress test completed in {elapsed_stress} milliseconds.")
    
    # Basic check for consistency after stress test
    print(f"Final number of products after stress test: {len(stress_inventory.products)}")
    assert len(stress_inventory.products) <= stress_size, "Stress Test Failed: Product count inconsistency."

    # Test with unexpected inputs
    print("\n--Unexpected Input--")
    # Getting a non-existent product
    non_existent_product = inventory.get_product(99999)
    assert non_existent_product is None, "Unexpected Input Test Failed: Getting non-existent product should return None."
    print("Non-existent product retrieval handled correctly.")

    # Removing a non-existent product
    remove_result = inventory.remove_product(99999)
    assert remove_result is False, "Unexpected Input Test Failed: Removing non-existent product should return False."
    print("Non-existent product removal handled correctly.")


    # --- Scalability Validation ---
    print("\n--Scalability Validation--")
    # This section analyzes how performance scales with increasing dataset size.
    scalability_sizes = [1000, 10000, 50000, 100000, 200000] 

    for size in scalability_sizes:
        print(f"\nValidating scalability for dataset size: {size} products.")
        
        # Data generation
        start_timer_scale = time.perf_counter()
        scalable_inventory = generate_large_ds(size)
        end_timer_scale = time.perf_counter()
        elapsed_scale = ((end_timer_scale - start_timer_scale) * 1000)
        print(f"Dataset generation ({size} products) Running Time: {elapsed_scale} ms")

        # Test add/update operation
        start_timer_add = time.perf_counter()
        scalable_inventory.add_product(size + 1, "New Scaled Product", 99.99, 10, "Test Category")
        end_timer_add = time.perf_counter()
        elapsed_add = ((end_timer_add - start_timer_add) * 1000)
        print(f"Add/Update Product Running Time: {elapsed_add} ms")

        # Test get operation
        product_search = random.randint(1, size)
        start_timer_get = time.perf_counter()
        scalable_inventory.get_product(product_search)
        end_timer_get = time.perf_counter()
        elapsed_get = ((end_timer_get - start_timer_get) * 1000)
        print(f"Get Product Running Time: {elapsed_get} ms")

        # Test filter operation (by category)
        category_filtered = random.choice(["Lounge", "Chairs", "Tables", "Case Goods"])
        start_timer_filter = time.perf_counter()
        scalable_inventory.filter_products(category=category_filtered)
        end_timer_filter = time.perf_counter()
        elapsed_filter = ((end_timer_filter - start_timer_filter) * 1000)
        print(f"Filter by Category '{category_filtered}' Running Time: {elapsed_filter} ms")

        # Test remove operation
        product_remove = random.randint(1, size)
        start_timer_remove = time.perf_counter()
        scalable_inventory.remove_product(product_remove)
        end_timer_remove = time.perf_counter()
        elapsed_remove = ((end_timer_remove - start_timer_remove) * 1000)
        print(f"Remove Product Running Time: {elapsed_remove} ms")

# Main function to demonstrate the inventory management system, perfermance testing.

if __name__ == "__main__":
     run_performance_testing()
     run_advance_testing()