"""
Tests for database models
"""

import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Customer, Product, Sale, SaleItem, Expense

class ModelsTestCase(unittest.TestCase):
    """Test case for database models"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_creation(self):
        """Test User model creation"""
        user = User(
            username='testuser',
            email='test@example.com',
            role='admin'
        )
        user.set_password('testpass123')
        
        db.session.add(user)
        db.session.commit()
        
        # Retrieve user from database
        retrieved_user = User.query.filter_by(username='testuser').first()
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertEqual(retrieved_user.role, 'admin')
        self.assertTrue(retrieved_user.check_password('testpass123'))
        self.assertFalse(retrieved_user.check_password('wrongpass'))
    
    def test_user_role_methods(self):
        """Test User role methods"""
        admin = User(username='admin', role='admin')
        manager = User(username='manager', role='manager')
        staff = User(username='staff', role='staff')
        
        self.assertTrue(admin.is_admin())
        self.assertTrue(admin.is_manager())
        
        self.assertFalse(manager.is_admin())
        self.assertTrue(manager.is_manager())
        
        self.assertFalse(staff.is_admin())
        self.assertFalse(staff.is_manager())
    
    def test_customer_creation(self):
        """Test Customer model creation"""
        customer = Customer(
            name='John Doe',
            email='john@example.com',
            phone='+265 888 123456',
            address='Lilongwe, Malawi',
            customer_type='retail'
        )
        
        db.session.add(customer)
        db.session.commit()
        
        retrieved_customer = Customer.query.filter_by(name='John Doe').first()
        
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.email, 'john@example.com')
        self.assertEqual(retrieved_customer.customer_type, 'retail')
        self.assertIsInstance(retrieved_customer.created_at, datetime)
    
    def test_product_creation(self):
        """Test Product model creation"""
        product = Product(
            name='Test Product',
            description='A test product',
            category='Electronics',
            price=1000.00,
            cost=600.00,
            stock_quantity=50,
            min_stock=10
        )
        
        db.session.add(product)
        db.session.commit()
        
        retrieved_product = Product.query.filter_by(name='Test Product').first()
        
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.price, 1000.00)
        self.assertEqual(retrieved_product.cost, 600.00)
        self.assertEqual(retrieved_product.stock_quantity, 50)
        self.assertEqual(retrieved_product.min_stock, 10)
    
    def test_product_profit_margin(self):
        """Test Product profit margin calculation"""
        product = Product(price=1000.00, cost=600.00)
        
        margin = product.profit_margin()
        expected_margin = ((1000.00 - 600.00) / 1000.00) * 100
        
        self.assertEqual(margin, expected_margin)
    
    def test_product_needs_restock(self):
        """Test Product needs_restock method"""
        # Product with low stock
        low_stock_product = Product(stock_quantity=5, min_stock=10)
        self.assertTrue(low_stock_product.needs_restock())
        
        # Product with sufficient stock
        sufficient_stock_product = Product(stock_quantity=15, min_stock=10)
        self.assertFalse(sufficient_stock_product.needs_restock())
    
    def test_sale_creation(self):
        """Test Sale model creation"""
        customer = Customer(name='Test Customer')
        db.session.add(customer)
        db.session.commit()
        
        sale = Sale(
            invoice_number='INV-001',
            customer_id=customer.id,
            total_amount=1000.00,
            discount=50.00,
            tax=100.00,
            payment_method='cash'
        )
        
        db.session.add(sale)
        db.session.commit()
        
        retrieved_sale = Sale.query.filter_by(invoice_number='INV-001').first()
        
        self.assertIsNotNone(retrieved_sale)
        self.assertEqual(retrieved_sale.total_amount, 1000.00)
        self.assertEqual(retrieved_sale.discount, 50.00)
        self.assertEqual(retrieved_sale.tax, 100.00)
        self.assertEqual(retrieved_sale.payment_method, 'cash')
        self.assertEqual(retrieved_sale.customer_id, customer.id)
    
    def test_sale_item_creation(self):
        """Test SaleItem model creation"""
        product = Product(name='Test Product', price=100.00, cost=50.00)
        sale = Sale(invoice_number='INV-002', total_amount=0)
        
        db.session.add_all([product, sale])
        db.session.commit()
        
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=2,
            unit_price=100.00,
            subtotal=200.00
        )
        
        db.session.add(sale_item)
        db.session.commit()
        
        retrieved_item = SaleItem.query.filter_by(sale_id=sale.id).first()
        
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.quantity, 2)
        self.assertEqual(retrieved_item.unit_price, 100.00)
        self.assertEqual(retrieved_item.subtotal, 200.00)
    
    def test_sale_calculate_total(self):
        """Test Sale calculate_total method"""
        sale = Sale(invoice_number='INV-003', discount=50.00, tax=100.00)
        
        product1 = Product(name='Product 1', price=100.00)
        product2 = Product(name='Product 2', price=200.00)
        
        db.session.add_all([sale, product1, product2])
        db.session.commit()
        
        # Create sale items
        item1 = SaleItem(
            sale_id=sale.id,
            product_id=product1.id,
            quantity=2,
            unit_price=100.00,
            subtotal=200.00
        )
        
        item2 = SaleItem(
            sale_id=sale.id,
            product_id=product2.id,
            quantity=1,
            unit_price=200.00,
            subtotal=200.00
        )
        
        sale.items.append(item1)
        sale.items.append(item2)
        
        total = sale.calculate_total()
        expected_total = (200.00 + 200.00) - 50.00 + 100.00
        
        self.assertEqual(total, expected_total)
        self.assertEqual(sale.total_amount, 0)  # Not updated automatically
    
    def test_expense_creation(self):
        """Test Expense model creation"""
        expense = Expense(
            category='Rent',
            description='Monthly office rent',
            amount=250000.00,
            expense_date=datetime.now().date(),
            payment_method='bank_transfer',
            receipt_number='REC-001'
        )
        
        db.session.add(expense)
        db.session.commit()
        
        retrieved_expense = Expense.query.filter_by(receipt_number='REC-001').first()
        
        self.assertIsNotNone(retrieved_expense)
        self.assertEqual(retrieved_expense.category, 'Rent')
        self.assertEqual(retrieved_expense.amount, 250000.00)
        self.assertEqual(retrieved_expense.payment_method, 'bank_transfer')
    
    def test_relationships(self):
        """Test model relationships"""
        # Create customer
        customer = Customer(name='Relationship Test Customer')
        
        # Create product
        product = Product(name='Relationship Test Product', price=100.00, cost=50.00)
        
        # Create sale
        sale = Sale(
            invoice_number='INV-REL-001',
            customer=customer,
            total_amount=300.00
        )
        
        # Create sale item
        sale_item = SaleItem(
            sale=sale,
            product=product,
            quantity=3,
            unit_price=100.00,
            subtotal=300.00
        )
        
        db.session.add_all([customer, product, sale, sale_item])
        db.session.commit()
        
        # Test relationships
        self.assertEqual(sale.customer.name, 'Relationship Test Customer')
        self.assertEqual(len(sale.items), 1)
        self.assertEqual(sale.items[0].product.name, 'Relationship Test Product')
        self.assertEqual(product.sale_items[0].sale.invoice_number, 'INV-REL-001')
    
    def test_timestamps(self):
        """Test automatic timestamp fields"""
        customer = Customer(name='Timestamp Test')
        
        db.session.add(customer)
        db.session.commit()
        
        self.assertIsInstance(customer.created_at, datetime)
        
        # Test updated_at for products
        product = Product(name='Test Product', price=100.00, cost=50.00)
        
        db.session.add(product)
        db.session.commit()
        
        initial_updated_at = product.updated_at
        
        # Update product
        product.price = 120.00
        db.session.commit()
        
        self.assertNotEqual(product.updated_at, initial_updated_at)

if __name__ == '__main__':
    unittest.main()