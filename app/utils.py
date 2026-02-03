import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import current_app

def generate_invoice_number():
    """Generate unique invoice number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f'INV-{timestamp}'

def calculate_profit(sale):
    """Calculate profit for a sale"""
    total_cost = 0
    for item in sale.items:
        product = item.product
        total_cost += product.cost * item.quantity
    
    return sale.total_amount - total_cost

def get_top_selling_products(days=30):
    """Get top selling products for last N days"""
    from app.models import Sale, SaleItem, Product
    from app import db
    
    start_date = datetime.now() - timedelta(days=days)
    
    top_products = db.session.query(
        Product.name,
        db.func.sum(SaleItem.quantity).label('total_quantity'),
        db.func.sum(SaleItem.subtotal).label('total_sales')
    ).join(SaleItem, Product.id == SaleItem.product_id
    ).join(Sale, SaleItem.sale_id == Sale.id
    ).filter(Sale.sale_date >= start_date
    ).group_by(Product.id
    ).order_by(db.desc('total_sales')
    ).limit(10).all()
    
    return top_products

def get_customer_analytics():
    """Analyze customer purchasing patterns"""
    from app.models import Customer, Sale
    from app import db
    
    analytics = db.session.query(
        Customer.name,
        db.func.count(Sale.id).label('purchase_count'),
        db.func.sum(Sale.total_amount).label('total_spent'),
        db.func.max(Sale.sale_date).label('last_purchase')
    ).join(Sale, Customer.id == Sale.customer_id
    ).group_by(Customer.id
    ).order_by(db.desc('total_spent')).all()
    
    return analytics

def generate_sales_report(start_date, end_date):
    """Generate sales report for given period"""
    from app.models import Sale, SaleItem, Product
    from app import db
    
    sales = Sale.query.filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).all()
    
    report_data = {
        'total_sales': sum(sale.total_amount for sale in sales),
        'total_transactions': len(sales),
        'average_transaction': sum(sale.total_amount for sale in sales) / len(sales) if sales else 0,
        'sales_by_day': get_sales_by_day(start_date, end_date),
        'top_products': get_top_selling_products_in_period(start_date, end_date)
    }
    
    return report_data

def get_sales_by_day(start_date, end_date):
    """Get sales grouped by day"""
    from app.models import Sale
    from app import db
    
    sales_by_day = db.session.query(
        db.func.date(Sale.sale_date).label('date'),
        db.func.sum(Sale.total_amount).label('daily_total')
    ).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).group_by(db.func.date(Sale.sale_date)
    ).order_by('date').all()
    
    return [{'date': str(row.date), 'total': float(row.daily_total)} for row in sales_by_day]

def get_top_selling_products_in_period(start_date, end_date):
    """Get top selling products in specific period"""
    from app.models import Sale, SaleItem, Product
    from app import db
    
    top_products = db.session.query(
        Product.name,
        db.func.sum(SaleItem.quantity).label('quantity_sold'),
        db.func.sum(SaleItem.subtotal).label('revenue')
    ).join(SaleItem, Product.id == SaleItem.product_id
    ).join(Sale, SaleItem.sale_id == Sale.id
    ).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    ).group_by(Product.id
    ).order_by(db.desc('revenue')
    ).limit(5).all()
    
    return [{
        'name': row.name,
        'quantity': int(row.quantity_sold),
        'revenue': float(row.revenue)
    } for row in top_products]