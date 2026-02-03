-- Database setup for Business Intelligence Dashboard
-- Run this script in MySQL to create the database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS business_dashboard;
USE business_dashboard;

-- Users table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('admin', 'manager', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    phone VARCHAR(20),
    address TEXT,
    customer_type ENUM('retail', 'wholesale', 'business') DEFAULT 'retail',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_customer_type (customer_type)
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    min_stock INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_stock (stock_quantity),
    CHECK (price >= 0),
    CHECK (cost >= 0),
    CHECK (stock_quantity >= 0),
    CHECK (min_stock >= 0)
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    tax DECIMAL(10, 2) DEFAULT 0,
    payment_method ENUM('cash', 'card', 'mobile_money', 'bank_transfer') DEFAULT 'cash',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    INDEX idx_invoice (invoice_number),
    INDEX idx_sale_date (sale_date),
    INDEX idx_customer (customer_id),
    CHECK (total_amount >= 0),
    CHECK (discount >= 0),
    CHECK (tax >= 0)
);

-- Sale items table
CREATE TABLE IF NOT EXISTS sale_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_sale (sale_id),
    INDEX idx_product (product_id),
    CHECK (quantity > 0),
    CHECK (unit_price >= 0),
    CHECK (subtotal >= 0)
);

-- Expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(200) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method VARCHAR(20),
    receipt_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_expense_date (expense_date),
    CHECK (amount >= 0)
);

-- Stock adjustments table (for inventory tracking)
CREATE TABLE IF NOT EXISTS stock_adjustments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    adjustment_type ENUM('in', 'out', 'correction') NOT NULL,
    quantity INT NOT NULL,
    reason VARCHAR(200),
    adjusted_by INT,
    adjustment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (adjusted_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_product (product_id),
    INDEX idx_adjustment_date (adjustment_date)
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);

-- Create default admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@business.com', '$2b$12$LQv3c1yqBWVHxkd0q9pzO.FzWtZ7N4RlR1YbHJ7d8kXmKvL9nN0jy', 'admin'),
('manager1', 'manager@business.com', '$2b$12$LQv3c1yqBWVHxkd0q9pzO.FzWtZ7N4RlR1YbHJ7d8kXmKvL9nN0jy', 'manager'),
('staff1', 'staff@business.com', '$2b$12$LQv3c1yqBWVHxkd0q9pzO.FzWtZ7N4RlR1YbHJ7d8kXmKvL9nN0jy', 'staff');

-- Insert sample customers
INSERT INTO customers (name, email, phone, address, customer_type) VALUES
('John Doe', 'john@example.com', '+265 888 123456', 'Lilongwe, Malawi', 'retail'),
('Sarah Smith', 'sarah@example.com', '+265 999 234567', 'Blantyre, Malawi', 'wholesale'),
('Mike Johnson', 'mike@example.com', '+265 777 345678', 'Mzuzu, Malawi', 'business'),
('Alice Williams', 'alice@example.com', '+265 666 456789', 'Zomba, Malawi', 'retail'),
('David Brown', 'david@example.com', '+265 555 567890', 'Salima, Malawi', 'wholesale');

-- Insert sample products
INSERT INTO products (name, description, category, price, cost, stock_quantity, min_stock) VALUES
('Laptop Dell XPS 13', '13-inch laptop with Intel i7 processor', 'Electronics', 1200000.00, 950000.00, 15, 5),
('Wireless Mouse', 'Bluetooth wireless mouse with ergonomic design', 'Electronics', 15000.00, 8000.00, 50, 20),
('Mechanical Keyboard', 'RGB mechanical keyboard with blue switches', 'Electronics', 45000.00, 25000.00, 25, 10),
('24-inch Monitor', 'Full HD monitor with HDMI and VGA ports', 'Electronics', 180000.00, 120000.00, 12, 5),
('Office Chair', 'Ergonomic office chair with lumbar support', 'Furniture', 85000.00, 50000.00, 30, 10),
('Desk Lamp', 'LED desk lamp with adjustable brightness', 'Home', 12000.00, 6000.00, 40, 15),
('Notebook Set', 'Set of 3 premium notebooks', 'Stationery', 8000.00, 3500.00, 100, 30),
('Pen Set', 'Premium pen set with gift box', 'Stationery', 15000.00, 7000.00, 60, 20),
('Coffee Maker', 'Automatic coffee maker with timer', 'Home', 65000.00, 40000.00, 8, 3),
('Water Bottle', 'Insulated stainless steel water bottle', 'Home', 9000.00, 4500.00, 80, 25);

-- Insert sample sales
INSERT INTO sales (invoice_number, customer_id, total_amount, discount, tax, payment_method) VALUES
('INV-20240301-001', 1, 1215000.00, 0, 15000.00, 'cash'),
('INV-20240301-002', 2, 195000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240301-003', 3, 270000.00, 0, 20000.00, 'card'),
('INV-20240302-001', 1, 45000.00, 0, 0, 'mobile_money'),
('INV-20240302-002', 4, 120000.00, 10000.00, 0, 'cash'),
('INV-20240303-001', 5, 33000.00, 0, 3000.00, 'card'),
('INV-20240303-002', 2, 180000.00, 0, 0, 'bank_transfer'),
('INV-20240304-001', 3, 85000.00, 5000.00, 0, 'cash'),
('INV-20240304-002', 1, 24000.00, 0, 0, 'mobile_money'),
('INV-20240305-001', 4, 195000.00, 0, 15000.00, 'card');

-- Insert sample sale items
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 1200000.00, 1200000.00),
(1, 2, 1, 15000.00, 15000.00),
(2, 3, 2, 45000.00, 90000.00),
(2, 4, 1, 180000.00, 180000.00),
(3, 5, 2, 85000.00, 170000.00),
(3, 6, 1, 12000.00, 12000.00),
(4, 7, 5, 8000.00, 40000.00),
(4, 8, 1, 15000.00, 15000.00),
(5, 9, 1, 65000.00, 65000.00),
(5, 10, 2, 9000.00, 18000.00);

-- Insert sample expenses
INSERT INTO expenses (category, description, amount, expense_date, payment_method) VALUES
('Rent', 'Office rent for March 2024', 250000.00, '2024-03-01', 'bank_transfer'),
('Salaries', 'Staff salaries March 2024', 850000.00, '2024-03-05', 'bank_transfer'),
('Utilities', 'Electricity and water bill', 125000.00, '2024-03-10', 'cash'),
('Marketing', 'Facebook ads campaign', 50000.00, '2024-03-15', 'card'),
('Supplies', 'Office supplies purchase', 35000.00, '2024-03-20', 'cash'),
('Internet', 'Monthly internet subscription', 45000.00, '2024-03-25', 'bank_transfer'),
('Transport', 'Delivery and transport costs', 28000.00, '2024-03-28', 'cash');

-- Create views for reporting

-- View for daily sales summary
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    DATE(sale_date) as sale_day,
    COUNT(*) as total_transactions,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction,
    SUM(discount) as total_discount,
    SUM(tax) as total_tax
FROM sales
GROUP BY DATE(sale_date)
ORDER BY sale_day DESC;

-- View for product performance
CREATE OR REPLACE VIEW product_performance AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.price,
    p.cost,
    p.stock_quantity,
    COALESCE(SUM(si.quantity), 0) as total_sold,
    COALESCE(SUM(si.subtotal), 0) as total_revenue,
    (p.price - p.cost) as profit_per_unit,
    COALESCE(SUM(si.quantity * (p.price - p.cost)), 0) as total_profit
FROM products p
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id
GROUP BY p.id, p.name, p.category, p.price, p.cost, p.stock_quantity
ORDER BY total_revenue DESC;

-- View for customer spending
CREATE OR REPLACE VIEW customer_spending AS
SELECT 
    c.id,
    c.name,
    c.customer_type,
    COUNT(s.id) as total_purchases,
    SUM(s.total_amount) as total_spent,
    AVG(s.total_amount) as avg_purchase,
    MAX(s.sale_date) as last_purchase_date
FROM customers c
LEFT JOIN sales s ON c.id = s.customer_id
GROUP BY c.id, c.name, c.customer_type
ORDER BY total_spent DESC;

-- Create stored procedures

-- Procedure to get monthly sales report
DELIMITER //
CREATE PROCEDURE GetMonthlySalesReport(IN year INT, IN month INT)
BEGIN
    SELECT 
        DAY(sale_date) as day_of_month,
        COUNT(*) as transaction_count,
        SUM(total_amount) as daily_revenue,
        SUM(discount) as total_discount,
        SUM(tax) as total_tax
    FROM sales
    WHERE YEAR(sale_date) = year AND MONTH(sale_date) = month
    GROUP BY DAY(sale_date)
    ORDER BY day_of_month;
END //
DELIMITER ;

-- Procedure to update product stock
DELIMITER //
CREATE PROCEDURE UpdateProductStock(
    IN product_id INT,
    IN quantity_change INT,
    IN adjustment_reason VARCHAR(200),
    IN adjusted_by INT
)
BEGIN
    DECLARE current_stock INT;
    
    -- Get current stock
    SELECT stock_quantity INTO current_stock FROM products WHERE id = product_id;
    
    -- Update product stock
    UPDATE products 
    SET stock_quantity = stock_quantity + quantity_change,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = product_id;
    
    -- Log the adjustment
    INSERT INTO stock_adjustments (product_id, adjustment_type, quantity, reason, adjusted_by)
    VALUES (
        product_id,
        CASE 
            WHEN quantity_change > 0 THEN 'in'
            WHEN quantity_change < 0 THEN 'out'
            ELSE 'correction'
        END,
        ABS(quantity_change),
        adjustment_reason,
        adjusted_by
    );
    
    -- Return success message
    SELECT CONCAT('Stock updated successfully. New stock: ', current_stock + quantity_change) as message;
END //
DELIMITER ;

-- Create triggers for audit logging

-- Trigger to log user changes
DELIMITER //
CREATE TRIGGER log_user_changes
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values)
    VALUES (
        NEW.id,
        'UPDATE',
        'users',
        NEW.id,
        JSON_OBJECT(
            'username', OLD.username,
            'email', OLD.email,
            'role', OLD.role
        ),
        JSON_OBJECT(
            'username', NEW.username,
            'email', NEW.email,
            'role', NEW.role
        )
    );
END //
DELIMITER ;

-- Trigger to log product changes
DELIMITER //
CREATE TRIGGER log_product_changes
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values)
    VALUES (
        NULL, -- System triggered
        'UPDATE',
        'products',
        NEW.id,
        JSON_OBJECT(
            'name', OLD.name,
            'price', OLD.price,
            'cost', OLD.cost,
            'stock_quantity', OLD.stock_quantity
        ),
        JSON_OBJECT(
            'name', NEW.name,
            'price', NEW.price,
            'cost', NEW.cost,
            'stock_quantity', NEW.stock_quantity
        )
    );
END //
DELIMITER ;

-- Create indexes for better performance
CREATE INDEX idx_sales_date_amount ON sales(sale_date, total_amount);
CREATE INDEX idx_products_price_category ON products(price, category);
CREATE INDEX idx_customers_type_name ON customers(customer_type, name);
CREATE INDEX idx_expenses_date_category ON expenses(expense_date, category);

-- Create backup user (for automated backups)
CREATE USER IF NOT EXISTS 'backup_user'@'localhost' IDENTIFIED BY 'backup_password';
GRANT SELECT, LOCK TABLES ON business_dashboard.* TO 'backup_user'@'localhost';
FLUSH PRIVILEGES;

-- Display success message
SELECT 'Database setup completed successfully!' as message;