#!/usr/bin/env python3
"""
Main application runner for Business Intelligence Dashboard
"""

import os
import sys
from app import create_app
from app.models import db
from flask_migrate import Migrate
import click

# Create application instance
app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Add objects to Flask shell context"""
    from app.models import User, Customer, Product, Sale, Expense
    return {
        'db': db,
        'User': User,
        'Customer': Customer,
        'Product': Product,
        'Sale': Sale,
        'Expense': Expense
    }

@app.cli.command("init-db")
def init_db():
    """Initialize the database with sample data"""
    from app.models import User
    from werkzeug.security import generate_password_hash
    
    # Create tables
    db.create_all()
    
    # Create default admin user if not exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(
            username='admin',
            email='admin@business.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: username='admin', password='admin123'")
    
    print("Database initialized successfully!")

@app.cli.command("create-user")
@click.argument('username')
@click.argument('email')
@click.argument('password')
@click.option('--role', default='staff', help='User role (admin, manager, staff)')
def create_user(username, email, password, role):
    """Create a new user"""
    from app.models import User
    
    if User.query.filter_by(username=username).first():
        print(f"User '{username}' already exists!")
        return
    
    if User.query.filter_by(email=email).first():
        print(f"Email '{email}' already registered!")
        return
    
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    print(f"User '{username}' created successfully with role '{role}'")

@app.cli.command("generate-sample-data")
def generate_sample_data():
    """Generate sample data for testing"""
    import random
    from datetime import datetime, timedelta
    from app.models import Customer, Product, Sale, SaleItem, Expense
    
    print("Generating sample data...")
    
    # Create sample customers
    customer_names = [
        "John Smith", "Mary Johnson", "Robert Brown", "Linda Davis",
        "Michael Wilson", "Sarah Miller", "David Moore", "Karen Taylor",
        "James Anderson", "Jennifer Thomas"
    ]
    
    customers = []
    for name in customer_names:
        customer = Customer(
            name=name,
            email=f"{name.lower().replace(' ', '.')}@example.com",
            phone=f"+265 {random.randint(880, 999)} {random.randint(100000, 999999)}",
            address=f"Address {random.randint(1, 100)}, City",
            customer_type=random.choice(['retail', 'wholesale', 'business'])
        )
        customers.append(customer)
        db.session.add(customer)
    
    db.session.commit()
    print(f"Created {len(customers)} customers")
    
    # Create sample products
    products_data = [
        ("Laptop Dell", "15-inch laptop", "Electronics", 850000, 650000, 20),
        ("Wireless Mouse", "Bluetooth mouse", "Electronics", 15000, 8000, 50),
        ("Keyboard", "Mechanical keyboard", "Electronics", 45000, 25000, 30),
        ("Monitor 24-inch", "Full HD monitor", "Electronics", 180000, 120000, 15),
        ("Office Chair", "Ergonomic chair", "Furniture", 85000, 50000, 25),
        ("Desk Lamp", "LED lamp", "Home", 12000, 6000, 40),
        ("Notebook", "Premium notebook", "Stationery", 8000, 3500, 100),
        ("Pen Set", "Executive pen set", "Stationery", 15000, 7000, 60)
    ]
    
    products = []
    for name, desc, category, price, cost, stock in products_data:
        product = Product(
            name=name,
            description=desc,
            category=category,
            price=price,
            cost=cost,
            stock_quantity=stock,
            min_stock=stock // 3
        )
        products.append(product)
        db.session.add(product)
    
    db.session.commit()
    print(f"Created {len(products)} products")
    
    # Create sample sales (last 30 days)
    sales = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(50):  # 50 sample sales
        sale_date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(9, 17))
        customer = random.choice(customers)
        
        sale = Sale(
            invoice_number=f"INV-{sale_date.strftime('%Y%m%d')}-{i+1:03d}",
            customer_id=customer.id,
            sale_date=sale_date,
            total_amount=0,  # Will be calculated
            discount=random.choice([0, 5000, 10000]),
            tax=random.choice([0, 5000, 10000, 15000]),
            payment_method=random.choice(['cash', 'card', 'mobile_money', 'bank_transfer'])
        )
        
        # Add 1-5 items to each sale
        total_amount = 0
        items_count = random.randint(1, 5)
        
        for j in range(items_count):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            unit_price = product.price
            subtotal = quantity * unit_price
            
            item = SaleItem(
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            sale.items.append(item)
            total_amount += subtotal
        
        sale.total_amount = total_amount - sale.discount + sale.tax
        sales.append(sale)
        db.session.add(sale)
    
    db.session.commit()
    print(f"Created {len(sales)} sales")
    
    # Create sample expenses
    expense_categories = ['Rent', 'Salaries', 'Utilities', 'Marketing', 'Supplies', 'Internet', 'Transport']
    
    for i in range(20):
        expense = Expense(
            category=random.choice(expense_categories),
            description=f"{random.choice(expense_categories)} expense {i+1}",
            amount=random.randint(10000, 300000),
            expense_date=start_date + timedelta(days=random.randint(0, 30)),
            payment_method=random.choice(['cash', 'bank_transfer', 'card'])
        )
        db.session.add(expense)
    
    db.session.commit()
    print("Created sample expenses")
    
    print("Sample data generation complete!")

@app.cli.command("backup-db")
def backup_db():
    """Backup database using the backup script"""
    import subprocess
    result = subprocess.run([sys.executable, "database/backup_script.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

@app.cli.command("stats")
def show_stats():
    """Show database statistics"""
    from app.models import User, Customer, Product, Sale, Expense
    from sqlalchemy import func
    
    stats = {
        "Users": User.query.count(),
        "Customers": Customer.query.count(),
        "Products": Product.query.count(),
        "Sales": Sale.query.count(),
        "Expenses": Expense.query.count(),
        "Total Revenue": db.session.query(func.sum(Sale.total_amount)).scalar() or 0,
        "Total Expenses": db.session.query(func.sum(Expense.amount)).scalar() or 0,
        "Inventory Value": db.session.query(func.sum(Product.stock_quantity * Product.cost)).scalar() or 0
    }
    
    print("=" * 40)
    print("DATABASE STATISTICS")
    print("=" * 40)
    for key, value in stats.items():
        if "Revenue" in key or "Expenses" in key or "Value" in key:
            print(f"{key}: MWK {value:,.2f}")
        else:
            print(f"{key}: {value}")
    print("=" * 40)

if __name__ == "__main__":
    # Run the application
    print("Starting Business Intelligence Dashboard...")
    print(f"Debug mode: {app.debug}")
    print(f"Environment: {app.config.get('ENV', 'production')}")
    
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )