from app.inventory import InventoryManager

def test_inventory():
    inventory = InventoryManager()
    
    print("Testing Inventory Management System")
    print("\n1. Adding new products...")
    
    # Add test products
    inventory.add_new_product("Test Laptop", 5, 1299.99, 3)
    inventory.add_new_product("Test Mouse", 15, 24.99, 5)
    
    print("\n2. Checking current inventory...")
    products = inventory.get_inventory()
    for product in products:
        print(f"Product: {product['product_name']}, "
              f"Quantity: {product['quantity']}, "
              f"Price: ${product['unit_price']:.2f}")
    
    print("\n3. Testing stock adjustment...")
    # Reduce laptop stock by 2
    inventory.adjust_stock(1, -2)
    
    print("\n4. Checking low stock products...")
    low_stock = inventory.check_low_stock(5)
    for product in low_stock:
        print(f"Low stock warning: {product['product_name']} "
              f"(Quantity: {product['quantity']})")
    
    print("\n5. Testing product search...")
    results = inventory.search_inventory("laptop")
    for product in results:
        print(f"Found: {product['product_name']}")

if __name__ == "__main__":
    test_inventory() 