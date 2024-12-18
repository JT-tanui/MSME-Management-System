from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from app.inventory import InventoryManager
from app.sales import SalesManager
from app.expenses import ExpenseManager
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
from app.init_db import init_db
from app.db import close_db

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ.get('SECRET_KEY')
app.teardown_appcontext(close_db)

# Initialize database within app context
with app.app_context():
    init_db()

# Initialize managers
inventory_manager = InventoryManager()
sales_manager = SalesManager()
expense_manager = ExpenseManager()

@app.route('/')
def index():
    """Dashboard / Home page"""
    # Get current date for today's calculations
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Gather dashboard data
    products = inventory_manager.get_inventory()
    low_stock = inventory_manager.check_low_stock()
    today_sales = sales_manager.get_daily_sales_total(today)
    total_sales = len(sales_manager.get_sales())
    monthly_expenses = expense_manager.get_monthly_expenses(
        datetime.now().year,
        datetime.now().month
    )
    expense_categories = len(expense_manager.expense_types)
    
    return render_template('index.html',
                         products=products,
                         low_stock=low_stock,
                         today_sales=today_sales,
                         total_sales=total_sales,
                         monthly_expenses=monthly_expenses,
                         expense_categories=expense_categories)

# Inventory routes
@app.route('/inventory')
def inventory():
    """Inventory management page"""
    products = inventory_manager.get_inventory()
    low_stock = inventory_manager.check_low_stock()
    return render_template('inventory.html', products=products, low_stock=low_stock)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_product():
    """Add new product page"""
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            quantity = int(request.form['quantity'])
            unit_price = float(request.form['unit_price'])
            reorder_level = int(request.form['reorder_level'])
            
            if inventory_manager.add_new_product(product_name, quantity, unit_price, reorder_level):
                flash('Product added successfully!', 'success')
            else:
                flash('Failed to add product.', 'error')
        except ValueError:
            flash('Invalid input values.', 'error')
        return redirect(url_for('inventory'))
    return render_template('add_product.html')

@app.route('/inventory/update/<int:product_id>', methods=['POST'])
def update_product(product_id):
    """Update product details"""
    try:
        updates = {
            'product_name': request.form['product_name'],
            'quantity': int(request.form['quantity']),
            'unit_price': float(request.form['unit_price']),
            'reorder_level': int(request.form['reorder_level'])
        }
        
        if inventory_manager.update_product_details(product_id, **updates):
            flash('Product updated successfully!', 'success')
        else:
            flash('Failed to update product.', 'error')
    except ValueError:
        flash('Invalid input values.', 'error')
    return redirect(url_for('inventory'))

@app.route('/inventory/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product"""
    if inventory_manager.remove_product(product_id):
        flash('Product deleted successfully!', 'success')
    else:
        flash('Failed to delete product.', 'error')
    return redirect(url_for('inventory'))

# Sales routes
@app.route('/sales')
def sales():
    """Sales management page"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get sales data
    all_sales = sales_manager.get_sales()
    products = inventory_manager.get_inventory()
    
    # Calculate summaries
    today_sales = sales_manager.get_daily_sales_total(today)
    today_transactions = len([s for s in all_sales if s['sale_date'].startswith(today)])
    
    # Get weekly data
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    weekly_sales = sum(s['total_amount'] for s in all_sales if s['sale_date'] >= week_start)
    weekly_transactions = len([s for s in all_sales if s['sale_date'] >= week_start])
    
    # Get monthly data
    month_start = datetime.now().strftime('%Y-%m-01')
    monthly_sales = sum(s['total_amount'] for s in all_sales if s['sale_date'] >= month_start)
    monthly_transactions = len([s for s in all_sales if s['sale_date'] >= month_start])
    
    return render_template('sales.html',
                         sales=all_sales,
                         products=products,
                         today_sales=today_sales,
                         today_transactions=today_transactions,
                         weekly_sales=weekly_sales,
                         weekly_transactions=weekly_transactions,
                         monthly_sales=monthly_sales,
                         monthly_transactions=monthly_transactions)

@app.route('/sales/add', methods=['POST'])
def add_sale():
    """Record new sale"""
    try:
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        unit_price = float(request.form['unit_price'])
        
        if sales_manager.record_sale(product_id, quantity, unit_price):
            flash('Sale recorded successfully!', 'success')
        else:
            flash('Failed to record sale.', 'error')
    except ValueError:
        flash('Invalid input values.', 'error')
    return redirect(url_for('sales'))

# Expenses routes
@app.route('/expenses')
def expenses():
    """Expenses management page"""
    # Get current month data
    current_date = datetime.now()
    month_start = current_date.strftime('%Y-%m-01')
    
    # Get all expenses and calculate summaries
    all_expenses = expense_manager.get_expenses()
    monthly_expenses = [e for e in all_expenses if e['expense_date'] >= month_start]
    
    monthly_total = sum(e['amount'] for e in monthly_expenses)
    monthly_count = len(monthly_expenses)
    
    return render_template('expenses.html',
                         expenses=all_expenses,
                         summary=expense_manager.get_expense_summary(),
                         expense_types=expense_manager.expense_types,
                         monthly_total=monthly_total,
                         monthly_count=monthly_count)

@app.route('/expenses/add', methods=['POST'])
def add_expense():
    """Record new expense"""
    try:
        expense_type = request.form['expense_type']
        amount = float(request.form['amount'])
        description = request.form['description']
        
        if expense_manager.add_expense(expense_type, amount, description):
            flash('Expense recorded successfully!', 'success')
        else:
            flash('Failed to record expense.', 'error')
    except ValueError:
        flash('Invalid input values.', 'error')
    return redirect(url_for('expenses'))

@app.route('/expenses/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense record"""
    if expense_manager.delete_expense(expense_id):
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Failed to delete expense.', 'error')
    return redirect(url_for('expenses'))

@app.route('/reports')
def reports():
    """Generate reports and analytics"""
    # Get date range from request args or default to current month
    today = datetime.now()
    start_date = request.args.get('start_date', today.replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', today.strftime('%Y-%m-%d'))

    # Get sales data
    sales_data = sales_manager.get_sales_in_range(start_date, end_date)
    total_sales = sum(sale['total_amount'] for sale in sales_data)
    transaction_count = len(sales_data)

    # Get expenses data
    expenses_data = expense_manager.get_expenses_in_range(start_date, end_date)
    total_expenses = sum(expense['amount'] for expense in expenses_data)
    expense_count = len(expenses_data)

    # Calculate net profit and margin
    net_profit = total_sales - total_expenses
    net_profit_percentage = (net_profit / total_sales * 100) if total_sales > 0 else 0

    # Prepare chart data
    sales_by_date = {}
    for sale in sales_data:
        date = sale['sale_date']
        sales_by_date[date] = sales_by_date.get(date, 0) + sale['total_amount']
    
    sales_dates = list(sales_by_date.keys())
    sales_amounts = list(sales_by_date.values())

    # Get expense categories and amounts
    expense_summary = expense_manager.get_expense_summary(start_date, end_date)
    expense_categories = list(expense_summary.keys())
    expense_amounts = list(expense_summary.values())

    # Get top selling products
    top_products = sales_manager.get_top_products(start_date, end_date, limit=5)
    
    # Add current stock levels to top products
    for product in top_products:
        current_stock = inventory_manager.get_product(product['product_id'])
        product['current_stock'] = current_stock['quantity']
        product['reorder_level'] = current_stock['reorder_level']

    return render_template('reports.html',
                         total_sales=total_sales,
                         transaction_count=transaction_count,
                         total_expenses=total_expenses,
                         expense_count=expense_count,
                         net_profit=net_profit,
                         net_profit_percentage=net_profit_percentage,
                         sales_dates=sales_dates,
                         sales_amounts=sales_amounts,
                         expense_categories=expense_categories,
                         expense_amounts=expense_amounts,
                         top_products=top_products)

@app.route('/export/<report_type>')
def export_report(report_type):
    """Export data to Excel"""
    today = datetime.now()
    start_date = request.args.get('start_date', today.replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', today.strftime('%Y-%m-%d'))
    
    if report_type == 'inventory':
        # Export inventory data
        products = inventory_manager.get_inventory()
        df = pd.DataFrame(products)
        filename = f"inventory_report_{today.strftime('%Y%m%d')}.xlsx"
        
    elif report_type == 'sales':
        # Export sales data
        sales = sales_manager.get_sales_in_range(start_date, end_date)
        df = pd.DataFrame(sales)
        filename = f"sales_report_{start_date}_to_{end_date}.xlsx"
        
    elif report_type == 'expenses':
        # Export expenses data
        expenses = expense_manager.get_expenses_in_range(start_date, end_date)
        df = pd.DataFrame(expenses)
        filename = f"expenses_report_{start_date}_to_{end_date}.xlsx"
        
    else:
        flash('Invalid report type', 'error')
        return redirect(url_for('reports'))
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/test-config')
def test_config():
    """Test configuration and database connection"""
    try:
        # Test environment variables
        config_status = {
            'FLASK_APP': os.environ.get('FLASK_APP', 'Not Set'),
            'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not Set'),
            'SECRET_KEY': 'Set' if os.environ.get('SECRET_KEY') else 'Not Set',
            'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not Set')
        }
        
        # Test database connection
        inventory = inventory_manager.get_inventory()
        db_status = "Connected" if inventory is not None else "Failed"
        
        return render_template('test_config.html', 
                             config=config_status,
                             db_status=db_status)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
