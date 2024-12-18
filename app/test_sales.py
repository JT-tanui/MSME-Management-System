from app.sales import SalesManager
from app.inventory import InventoryManager
from datetime import datetime, timedelta

def test_sales():
    # Initialize managers
    inventory = InventoryManager()
    sales = SalesManager()
    
    print("Testing Sales Management System")
    
    # Add test product if not exists
    print("\n1. Setting up test product...")
    inventory.add_new_product("Test Product", 50, 99.99, 10)
    
    # Get the product ID (assuming it's 1 for this test)
    product_id = 1
    
    print("\n2. Recording test sales...")
    # Record multiple sales
    sales.record_sale(product_id, 5, 99.99)  # Regular price sale
    sales.record_sale(product_id, 3, 89.99)  # Discounted sale
    
    print("\n3. Checking sales records...")
    all_sales = sales.get_sales()
    for sale in all_sales:
        print(f"Sale ID: {sale['id']}, "
              f"Product: {sale['product_name']}, "
              f"Quantity: {sale['quantity_sold']}, "
              f"Total: ${sale['total_amount']:.2f}")
    
    print("\n4. Checking daily sales total...")
    today = datetime.now().strftime('%Y-%m-%d')
    daily_total = sales.get_daily_sales_total(today)
    print(f"Total sales for today: ${daily_total:.2f}")
    
    print("\n5. Checking product sales history...")
    history = sales.get_product_sales_history(product_id)
    for sale in history:
        print(f"Date: {sale['sale_date']}, "
              f"Quantity: {sale['quantity_sold']}, "
              f"Amount: ${sale['total_amount']:.2f}")
    
    # Verify inventory was updated
    print("\n6. Verifying inventory update...")
    products = inventory.get_inventory()
    for product in products:
        if product['id'] == product_id:
            print(f"Current stock for {product['product_name']}: {product['quantity']}")

if __name__ == "__main__":
    test_sales() 