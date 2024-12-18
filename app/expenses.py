from datetime import datetime
from typing import Dict, List, Optional, Union
from app.database import get_db_connection

class ExpenseManager:
    def __init__(self):
        self.expense_types = [
            'Rent', 'Utilities', 'Salaries', 'Inventory', 
            'Marketing', 'Maintenance', 'Office Supplies', 'Other'
        ]

    def add_expense(
        self,
        expense_type: str,
        amount: float,
        description: Optional[str] = None,
        date: Optional[str] = None
    ) -> bool:
        """Record a new expense"""
        try:
            if expense_type not in self.expense_types:
                print(f"Invalid expense type. Must be one of: {', '.join(self.expense_types)}")
                return False
                
            if amount <= 0:
                print("Amount must be greater than 0")
                return False
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO expenses (expense_type, amount, description, expense_date)
            VALUES (?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP))
            ''', (expense_type, amount, description, date))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error recording expense: {e}")
            return False

    def get_expenses(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        expense_type: Optional[str] = None
    ) -> List[Dict]:
        """Get expenses with optional filters"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM expenses WHERE 1=1'
            params = []
            
            if start_date and end_date:
                query += ' AND expense_date BETWEEN ? AND ?'
                params.extend([start_date, end_date])
            
            if expense_type:
                query += ' AND expense_type = ?'
                params.append(expense_type)
                
            query += ' ORDER BY expense_date DESC'
            
            cursor.execute(query, params)
            expenses = cursor.fetchall()
            conn.close()
            return expenses
            
        except Exception as e:
            print(f"Error retrieving expenses: {e}")
            return []

    def get_expense_summary(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, float]:
        """Get summary of expenses by type"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = '''
            SELECT 
                expense_type,
                SUM(amount) as total_amount
            FROM expenses
            '''
            
            params = []
            if start_date and end_date:
                query += ' WHERE expense_date BETWEEN ? AND ?'
                params.extend([start_date, end_date])
                
            query += ' GROUP BY expense_type'
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return {row['expense_type']: float(row['total_amount']) for row in results}
            
        except Exception as e:
            print(f"Error generating expense summary: {e}")
            return {}

    def get_monthly_expenses(self, year: int, month: int) -> float:
        """Calculate total expenses for a specific month"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT SUM(amount) as monthly_total
            FROM expenses
            WHERE strftime('%Y', expense_date) = ?
            AND strftime('%m', expense_date) = ?
            ''', (str(year), str(month).zfill(2)))
            
            result = cursor.fetchone()
            conn.close()
            
            return float(result['monthly_total']) if result['monthly_total'] else 0.0
            
        except Exception as e:
            print(f"Error calculating monthly expenses: {e}")
            return 0.0

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense record"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False

    def get_expenses_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get expenses within a date range"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT * FROM expenses
            WHERE expense_date BETWEEN ? AND ?
            ORDER BY expense_date DESC
            ''', (start_date, end_date))
            
            expenses = cursor.fetchall()
            conn.close()
            return expenses
            
        except Exception as e:
            print(f"Error getting expenses in range: {e}")
            return []
