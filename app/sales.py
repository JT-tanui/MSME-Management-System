from datetime import datetime
from typing import Dict, List, Optional, Union
from app.database import get_db_connection
from app.inventory import InventoryManager

class SalesManager:
    def __init__(self):
        self.inventory = InventoryManager()

    def record_sale(
        self, 
        product_id: int, 
        quantity_sold: int, 
        unit_price: Optional[float] = None
    ) -> bool:
        """Record a new sale transaction"""
        try:
            # Get product details
            products = self.inventory.get_inventory()
            product = next((p for p in products if p['id'] == product_id), None)
            
            if not product:
                print("Product not found")
                return False
            
            # Check if we have enough stock
            if product['quantity'] < quantity_sold:
                print("Insufficient stock")
                return False
            
            # Use provided unit price or default to product's current price
            selling_price = unit_price if unit_price is not None else product['unit_price']
            total_amount = selling_price * quantity_sold
            
            # Record the sale
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO sales (product_id, quantity_sold, unit_price, total_amount)
            VALUES (?, ?, ?, ?)
            ''', (product_id, quantity_sold, selling_price, total_amount))
            
            # Update inventory
            self.inventory.adjust_stock(product_id, -quantity_sold)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error recording sale: {e}")
            return False

    def get_sales(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Get sales records within date range"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = '''
            SELECT 
                s.id,
                s.product_id,
                i.product_name,
                s.quantity_sold,
                s.unit_price,
                s.total_amount,
                s.sale_date
            FROM sales s
            JOIN inventory i ON s.product_id = i.id
            '''
            
            params = []
            if start_date and end_date:
                query += ' WHERE s.sale_date BETWEEN ? AND ?'
                params = [start_date, end_date]
            
            cursor.execute(query, params)
            sales = cursor.fetchall()
            conn.close()
            return sales
            
        except Exception as e:
            print(f"Error retrieving sales: {e}")
            return []

    def get_daily_sales_total(self, date: Optional[str] = None) -> float:
        """Calculate total sales for a specific date"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = '''
            SELECT SUM(total_amount) as daily_total
            FROM sales
            '''
            
            params = []
            if date:
                query += ' WHERE DATE(sale_date) = DATE(?)'
                params = [date]
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.close()
            
            return float(result['daily_total']) if result['daily_total'] else 0.0
            
        except Exception as e:
            print(f"Error calculating daily sales: {e}")
            return 0.0

    def get_product_sales_history(self, product_id: int) -> List[Dict]:
        """Get sales history for a specific product"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT 
                s.*,
                i.product_name
            FROM sales s
            JOIN inventory i ON s.product_id = i.id
            WHERE s.product_id = ?
            ORDER BY s.sale_date DESC
            ''', (product_id,))
            
            history = cursor.fetchall()
            conn.close()
            return history
            
        except Exception as e:
            print(f"Error retrieving product sales history: {e}")
            return []

    def get_sales_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get sales within a date range"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT s.*, p.product_name 
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.sale_date BETWEEN ? AND ?
            ORDER BY s.sale_date DESC
            ''', (start_date, end_date))
            
            sales = cursor.fetchall()
            conn.close()
            return sales
            
        except Exception as e:
            print(f"Error getting sales in range: {e}")
            return []

    def get_top_products(self, start_date: str, end_date: str, limit: int = 5) -> List[Dict]:
        """Get top selling products within a date range"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT 
                p.id as product_id,
                p.product_name,
                COUNT(*) as units_sold,
                SUM(s.total_amount) as revenue
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY p.id, p.product_name
            ORDER BY revenue DESC
            LIMIT ?
            ''', (start_date, end_date, limit))
            
            products = cursor.fetchall()
            conn.close()
            return products
            
        except Exception as e:
            print(f"Error getting top products: {e}")
            return []
