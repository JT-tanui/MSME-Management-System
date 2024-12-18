from app.db import get_db_connection

def init_db():
    """Initialize database tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        reorder_level INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        sale_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (product_id) REFERENCES inventory (id)
    )
    ''')

    # Create expenses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_type TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        expense_date DATE DEFAULT CURRENT_DATE
    )
    ''')

    conn.commit()
    conn.close() 