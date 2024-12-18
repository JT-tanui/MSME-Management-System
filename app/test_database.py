from app.database import init_db, add_product, get_all_products, update_product, search_products, get_low_stock_products, delete_product

def test_database():
    # Initialize the database
    print("Initializing database...")
    init_db()
    
    # Test adding products
    print("\nAdding sample products...")
    sample_products = [
        ("Laptop", 10, 999.99, 5),
        ("Mouse", 20, 29.99, 8),
        ("Keyboard", 15, 49.99, 7),
        ("Monitor", 8, 299.99, 3)
    ]
    
    for product in sample_products:
        add_product(*product)
        print(f"Added product: {product[0]}")
    
    # Test retrieving products
    print("\nRetrieving all products:")
    products = get_all_products()
    for product in products:
        print(f"ID: {product['id']}, "
              f"Name: {product['product_name']}, "
              f"Quantity: {product['quantity']}, "
              f"Price: ${product['unit_price']:.2f}, "
              f"Reorder Level: {product['reorder_level']}")
    
    # Test updating a product
    print("\nUpdating product (Laptop)...")
    update_product(1, quantity=12, unit_price=899.99)
    
    # Verify the update
    print("\nVerifying update:")
    products = get_all_products()
    for product in products:
        if product['id'] == 1:
            print(f"Updated Laptop - "
                  f"New Quantity: {product['quantity']}, "
                  f"New Price: ${product['unit_price']:.2f}")
    
    # Test searching products
    print("\nSearching for 'top' in products:")
    search_results = search_products('top')
    for product in search_results:
        print(f"Found: {product['product_name']}")
    
    # Test low stock detection
    print("\nChecking low stock products (threshold: 10):")
    low_stock = get_low_stock_products(10)
    for product in low_stock:
        print(f"Low stock alert: {product['product_name']} - Quantity: {product['quantity']}")
    
    # Test deleting a product
    print("\nDeleting Mouse product...")
    if delete_product(2):  # Delete the Mouse (ID: 2)
        print("Mouse product deleted successfully")
    
    # Verify deletion
    print("\nFinal product list:")
    remaining_products = get_all_products()
    for product in remaining_products:
        print(f"ID: {product['id']}, Name: {product['product_name']}")

if __name__ == "__main__":
    test_database() 