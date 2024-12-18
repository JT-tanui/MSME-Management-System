import sqlite3
from pathlib import Path
from datetime import datetime

# Create data directory if it doesn't exist
Path("data").mkdir(exist_ok=True)

DATABASE_PATH = "data/database.db"

def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        reorder_level INTEGER DEFAULT 10,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity_sold INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES inventory (id)
    )
    ''')

    # Create Expenses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_type TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        expense_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

def add_product(product_name: str, quantity: int, unit_price: float, reorder_level: int = 10):
    """Add a new product to inventory"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO inventory (product_name, quantity, unit_price, reorder_level)
    VALUES (?, ?, ?, ?)
    ''', (product_name, quantity, unit_price, reorder_level))
    
    conn.commit()
    conn.close()

def get_all_products():
    """Retrieve all products from inventory"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM inventory')
    products = cursor.fetchall()
    
    conn.close()
    return products

def update_product(product_id: int, **kwargs):
    """Update product details in inventory"""
    valid_fields = {'product_name', 'quantity', 'unit_price', 'reorder_level'}
    update_fields = {k: v for k, v in kwargs.items() if k in valid_fields}
    
    if not update_fields:
        return False
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{field} = ?" for field in update_fields.keys()])
    query = f"UPDATE inventory SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    
    values = list(update_fields.values()) + [product_id]
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    return True

def delete_product(product_id: int) -> bool:
    """Delete a product from inventory"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if product exists
        cursor.execute('SELECT id FROM inventory WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            return False
            
        cursor.execute('DELETE FROM inventory WHERE id = ?', (product_id,))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def search_products(search_term: str):
    """Search for products by name"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM inventory 
    WHERE product_name LIKE ?
    ''', (f'%{search_term}%',))
    
    products = cursor.fetchall()
    conn.close()
    return products

def get_low_stock_products(threshold: int = None):
    """Get products with quantity below reorder level or specified threshold"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if threshold is not None:
        cursor.execute('''
        SELECT * FROM inventory 
        WHERE quantity <= ?
        ''', (threshold,))
    else:
        cursor.execute('''
        SELECT * FROM inventory 
        WHERE quantity <= reorder_level
        ''')
    
    products = cursor.fetchall()
    conn.close()
    return products

if __name__ == "__main__":
    # Initialize the database when this file is run directly
    init_db()
    print("Database initialized successfully!")
