from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Sale, Product, Customer, Expense
from datetime import datetime, timedelta
import pandas as pd
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    # Get recent sales
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()
    
    # Get low stock products
    low_stock = Product.query.filter(Product.stock_quantity < Product.min_stock).all()
    
    # Calculate today's sales
    today = datetime.now().date()
    today_sales = Sale.query.filter(db.func.date(Sale.sale_date) == today).all()
    today_total = sum(sale.total_amount for sale in today_sales)
    
    # Get monthly sales for chart
    monthly_data = get_monthly_sales_data()
    
    return render_template('dashboard.html',
                         recent_sales=recent_sales,
                         low_stock=low_stock,
                         today_total=today_total,
                         monthly_data=monthly_data)

@main_bp.route('/sales')
@login_required
def sales():
    """Sales page"""
    sales_list = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('sales.html', sales=sales_list)

@main_bp.route('/inventory')
@login_required
def inventory():
    """Inventory management page"""
    products = Product.query.order_by(Product.name).all()

    # Summary values for the inventory dashboard
    total_stock_value = sum((p.stock_quantity or 0) * (p.cost or 0) for p in products)
    low_stock_count = sum(1 for p in products if (p.stock_quantity or 0) < (p.min_stock or 0))
    out_of_stock_count = sum(1 for p in products if (p.stock_quantity or 0) == 0)

    return render_template('inventory.html',
                           products=products,
                           total_stock_value=total_stock_value,
                           low_stock_count=low_stock_count,
                           out_of_stock_count=out_of_stock_count)

@main_bp.route('/customers')
@login_required
def customers():
    """Customers page"""
    customers_list = Customer.query.order_by(Customer.name).all()
    return render_template('customers.html', customers=customers_list)

@main_bp.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')

@main_bp.route('/api/sales-data')
@login_required
def sales_data():
    """API endpoint for sales chart data"""
    data = get_monthly_sales_data()
    return jsonify(data)

@main_bp.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """API endpoint for dashboard statistics"""
    # Today's date
    today = datetime.now().date()
    
    # Calculate statistics
    today_sales = Sale.query.filter(db.func.date(Sale.sale_date) == today).all()
    today_total = sum(sale.total_amount for sale in today_sales)
    
    # Yesterday
    yesterday = today - timedelta(days=1)
    yesterday_sales = Sale.query.filter(db.func.date(Sale.sale_date) == yesterday).all()
    yesterday_total = sum(sale.total_amount for sale in yesterday_sales)
    
    # This month
    month_start = today.replace(day=1)
    month_sales = Sale.query.filter(Sale.sale_date >= month_start).all()
    month_total = sum(sale.total_amount for sale in month_sales)
    
    # Low stock count
    low_stock_count = Product.query.filter(Product.stock_quantity < Product.min_stock).count()
    
    # Total customers
    total_customers = Customer.query.count()
    
    stats = {
        'today_sales': today_total,
        'yesterday_sales': yesterday_total,
        'month_sales': month_total,
        'low_stock_count': low_stock_count,
        'total_customers': total_customers,
        'sales_change': calculate_percentage_change(today_total, yesterday_total)
    }
    
    return jsonify(stats)

def get_monthly_sales_data():
    """Get sales data for the last 6 months"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months
    
    # Query sales grouped by month
    sales_by_month = db.session.query(
        db.func.date_format(Sale.sale_date, '%Y-%m').label('month'),
        db.func.sum(Sale.total_amount).label('total')
    ).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).group_by('month').order_by('month').all()
    
    # Format data for chart
    months = []
    totals = []
    
    for row in sales_by_month:
        months.append(row.month)
        totals.append(float(row.total) if row.total else 0)
    
    return {
        'months': months,
        'totals': totals
    }

def calculate_percentage_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 2)