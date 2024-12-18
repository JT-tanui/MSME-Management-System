from app.expenses import ExpenseManager
from datetime import datetime, timedelta

def test_expenses():
    expense_manager = ExpenseManager()
    
    print("Testing Expense Management System")
    
    # Test adding expenses
    print("\n1. Adding test expenses...")
    expenses = [
        ("Rent", 1500.00, "Monthly office rent"),
        ("Utilities", 250.00, "Electricity and water"),
        ("Salaries", 3000.00, "Staff salaries"),
        ("Office Supplies", 150.00, "Paper, ink, etc.")
    ]
    
    for expense_type, amount, description in expenses:
        if expense_manager.add_expense(expense_type, amount, description):
            print(f"Added {expense_type} expense: ${amount:.2f}")
    
    # Test invalid expense type
    print("\n2. Testing invalid expense type...")
    if not expense_manager.add_expense("Invalid", 100.00):
        print("Successfully prevented invalid expense type")
    
    # Get all expenses
    print("\n3. Retrieving all expenses...")
    all_expenses = expense_manager.get_expenses()
    for expense in all_expenses:
        print(f"Type: {expense['expense_type']}, "
              f"Amount: ${expense['amount']:.2f}, "
              f"Date: {expense['expense_date']}")
    
    # Get expense summary
    print("\n4. Getting expense summary...")
    summary = expense_manager.get_expense_summary()
    for expense_type, total in summary.items():
        print(f"{expense_type}: ${total:.2f}")
    
    # Get monthly expenses
    current_date = datetime.now()
    print(f"\n5. Getting expenses for {current_date.strftime('%B %Y')}...")
    monthly_total = expense_manager.get_monthly_expenses(
        current_date.year,
        current_date.month
    )
    print(f"Total expenses this month: ${monthly_total:.2f}")

if __name__ == "__main__":
    test_expenses() 