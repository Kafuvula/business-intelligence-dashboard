-- Sample data for Business Intelligence Dashboard
-- Run this after setup.sql to populate the database with realistic data

USE business_dashboard;

-- Insert more sample customers (total 20 customers)
INSERT INTO customers (name, email, phone, address, customer_type) VALUES
('Emma Wilson', 'emma@example.com', '+265 884 112233', 'Lilongwe, Area 3', 'retail'),
('James Miller', 'james@example.com', '+265 995 223344', 'Blantyre, Nyambadwe', 'wholesale'),
('Sophia Davis', 'sophia@example.com', '+265 776 334455', 'Mzuzu, Katoto', 'retail'),
('Robert Garcia', 'robert@example.com', '+265 887 445566', 'Zomba, Chancellor College', 'business'),
('Olivia Martinez', 'olivia@example.com', '+265 998 556677', 'Salima, Beach Road', 'retail'),
('William Rodriguez', 'william@example.com', '+265 779 667788', 'Mangochi, Lake View', 'wholesale'),
('Ava Hernandez', 'ava@example.com', '+265 880 778899', 'Kasungu, Boma', 'retail'),
('Michael Lopez', 'michael@example.com', '+265 991 889900', 'Dedza, Trading Centre', 'business'),
('Isabella Gonzalez', 'isabella@example.com', '+265 772 990011', 'Nkhotakota, Beach', 'retail'),
('David Perez', 'david@example.com', '+265 883 001122', 'Mzimba, Boma', 'wholesale'),
('Mia Torres', 'mia@example.com', '+265 994 112233', 'Balaka, Trading Centre', 'retail'),
('Joseph Flores', 'joseph@example.com', '+265 775 223344', 'Mulanje, Boma', 'business'),
('Charlotte King', 'charlotte@example.com', '+265 886 334455', 'Thyolo, Boma', 'retail'),
('Charles Scott', 'charles@example.com', '+265 997 445566', 'Rumphi, Boma', 'wholesale'),
('Amelia Green', 'amelia@example.com', '+265 778 556677', 'Karonga, Boma', 'retail'),
('Thomas Adams', 'thomas@example.com', '+265 889 667788', 'Nkhata Bay, Beach', 'business'),
('Evelyn Nelson', 'evelyn@example.com', '+265 990 778899', 'Chitipa, Boma', 'retail'),
('Christopher Carter', 'christopher@example.com', '+265 771 889900', 'Phalombe, Trading Centre', 'wholesale'),
('Abigail Mitchell', 'abigail@example.com', '+265 882 990011', 'Chiradzulu, Boma', 'retail'),
('Daniel Perez', 'daniel@example.com', '+265 993 001122', 'Neno, Trading Centre', 'business');

-- Insert more sample products (total 25 products)
INSERT INTO products (name, description, category, price, cost, stock_quantity, min_stock) VALUES
('Smartphone Samsung A54', '5G smartphone with 128GB storage', 'Electronics', 850000.00, 650000.00, 20, 8),
('Tablet iPad 10th Gen', '10.9-inch tablet with Apple Pencil support', 'Electronics', 950000.00, 750000.00, 8, 3),
('Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 'Electronics', 35000.00, 20000.00, 35, 15),
('Power Bank 20000mAh', 'Fast charging power bank with dual output', 'Electronics', 45000.00, 28000.00, 40, 20),
('Laptop Bag', 'Waterproof laptop bag with USB charging port', 'Accessories', 25000.00, 15000.00, 50, 25),
('Wireless Earbuds', 'True wireless earbuds with charging case', 'Electronics', 55000.00, 35000.00, 30, 12),
('External Hard Drive 1TB', 'Portable SSD hard drive USB 3.0', 'Electronics', 120000.00, 85000.00, 15, 6),
('Webcam HD', '1080p HD webcam with microphone', 'Electronics', 40000.00, 25000.00, 25, 10),
('Desk Organizer', 'Wooden desk organizer with compartments', 'Office', 18000.00, 10000.00, 60, 30),
('Stapler', 'Heavy duty stapler with staple remover', 'Stationery', 8000.00, 4000.00, 100, 50),
('Calculator', 'Scientific calculator with 240 functions', 'Electronics', 15000.00, 8000.00, 45, 20),
('File Cabinet', '2-drawer metal file cabinet', 'Furniture', 120000.00, 80000.00, 10, 4),
('Whiteboard 4x3 ft', 'Magnetic whiteboard with markers', 'Office', 55000.00, 35000.00, 18, 8),
('Projector', 'HD projector with 3000 lumens', 'Electronics', 450000.00, 350000.00, 5, 2),
('Router WiFi 6', 'Dual-band WiFi 6 router', 'Electronics', 95000.00, 65000.00, 12, 5),
('Air Conditioner 1.5HP', 'Inverter split AC with installation', 'Appliances', 850000.00, 650000.00, 6, 2),
('Refrigerator 300L', 'Double door refrigerator with freezer', 'Appliances', 1200000.00, 900000.00, 4, 1),
('Microwave Oven', '20L microwave with grill function', 'Appliances', 180000.00, 120000.00, 10, 4),
('Toaster', '4-slice toaster with defrost function', 'Appliances', 45000.00, 30000.00, 20, 8),
('Blender', '600W blender with 1.5L jug', 'Appliances', 55000.00, 35000.00, 25, 10),
('Vacuum Cleaner', 'Bagless vacuum cleaner with HEPA filter', 'Appliances', 85000.00, 55000.00, 15, 6),
('Iron', 'Steam iron with ceramic soleplate', 'Appliances', 35000.00, 22000.00, 30, 12),
('First Aid Kit', '50-piece first aid kit', 'Health', 25000.00, 15000.00, 40, 20),
('Fire Extinguisher', '5kg dry powder fire extinguisher', 'Safety', 45000.00, 30000.00, 20, 8),
('Tool Kit', '65-piece household tool kit', 'Tools', 75000.00, 50000.00, 15, 6);

-- Insert sample sales for March 2024 (30 days of sales data)
-- March 1-10
INSERT INTO sales (invoice_number, customer_id, sale_date, total_amount, discount, tax, payment_method) VALUES
('INV-20240301-001', 1, '2024-03-01 09:15:00', 1215000.00, 0, 15000.00, 'cash'),
('INV-20240301-002', 2, '2024-03-01 10:30:00', 195000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240301-003', 3, '2024-03-01 11:45:00', 270000.00, 0, 20000.00, 'card'),
('INV-20240302-001', 4, '2024-03-02 09:00:00', 45000.00, 0, 0, 'mobile_money'),
('INV-20240302-002', 5, '2024-03-02 14:20:00', 120000.00, 10000.00, 0, 'cash'),
('INV-20240303-001', 6, '2024-03-03 10:00:00', 33000.00, 0, 3000.00, 'card'),
('INV-20240303-002', 7, '2024-03-03 15:30:00', 180000.00, 0, 0, 'bank_transfer'),
('INV-20240304-001', 8, '2024-03-04 11:00:00', 85000.00, 5000.00, 0, 'cash'),
('INV-20240304-002', 9, '2024-03-04 16:45:00', 24000.00, 0, 0, 'mobile_money'),
('INV-20240305-001', 10, '2024-03-05 09:30:00', 195000.00, 0, 15000.00, 'card');

-- March 6-15
INSERT INTO sales (invoice_number, customer_id, sale_date, total_amount, discount, tax, payment_method) VALUES
('INV-20240306-001', 11, '2024-03-06 10:15:00', 85000.00, 5000.00, 0, 'cash'),
('INV-20240306-002', 12, '2024-03-06 14:30:00', 125000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240307-001', 13, '2024-03-07 09:45:00', 45000.00, 0, 0, 'mobile_money'),
('INV-20240307-002', 14, '2024-03-07 16:20:00', 320000.00, 20000.00, 0, 'card'),
('INV-20240308-001', 15, '2024-03-08 11:00:00', 75000.00, 0, 5000.00, 'cash'),
('INV-20240308-002', 16, '2024-03-08 15:30:00', 180000.00, 10000.00, 0, 'bank_transfer'),
('INV-20240309-001', 17, '2024-03-09 10:00:00', 55000.00, 0, 0, 'mobile_money'),
('INV-20240309-002', 18, '2024-03-09 14:45:00', 95000.00, 5000.00, 0, 'card'),
('INV-20240310-001', 19, '2024-03-10 09:30:00', 120000.00, 0, 10000.00, 'cash'),
('INV-20240310-002', 20, '2024-03-10 16:00:00', 280000.00, 20000.00, 0, 'bank_transfer');

-- March 11-20
INSERT INTO sales (invoice_number, customer_id, sale_date, total_amount, discount, tax, payment_method) VALUES
('INV-20240311-001', 1, '2024-03-11 10:15:00', 65000.00, 0, 5000.00, 'card'),
('INV-20240311-002', 2, '2024-03-11 14:30:00', 185000.00, 15000.00, 0, 'cash'),
('INV-20240312-001', 3, '2024-03-12 09:45:00', 75000.00, 0, 0, 'mobile_money'),
('INV-20240312-002', 4, '2024-03-12 15:20:00', 220000.00, 20000.00, 0, 'bank_transfer'),
('INV-20240313-001', 5, '2024-03-13 11:00:00', 45000.00, 0, 5000.00, 'card'),
('INV-20240313-002', 6, '2024-03-13 16:30:00', 160000.00, 10000.00, 0, 'cash'),
('INV-20240314-001', 7, '2024-03-14 10:00:00', 85000.00, 0, 0, 'mobile_money'),
('INV-20240314-002', 8, '2024-03-14 14:45:00', 125000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240315-001', 9, '2024-03-15 09:30:00', 35000.00, 0, 3000.00, 'card'),
('INV-20240315-002', 10, '2024-03-15 16:00:00', 195000.00, 15000.00, 0, 'cash');

-- March 16-25
INSERT INTO sales (invoice_number, customer_id, sale_date, total_amount, discount, tax, payment_method) VALUES
('INV-20240316-001', 11, '2024-03-16 10:15:00', 95000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240316-002', 12, '2024-03-16 14:30:00', 280000.00, 0, 20000.00, 'card'),
('INV-20240317-001', 13, '2024-03-17 09:45:00', 55000.00, 0, 0, 'cash'),
('INV-20240317-002', 14, '2024-03-17 15:20:00', 185000.00, 15000.00, 0, 'mobile_money'),
('INV-20240318-001', 15, '2024-03-18 11:00:00', 75000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240318-002', 16, '2024-03-18 16:30:00', 220000.00, 20000.00, 0, 'card'),
('INV-20240319-001', 17, '2024-03-19 10:00:00', 45000.00, 0, 0, 'cash'),
('INV-20240319-002', 18, '2024-03-19 14:45:00', 160000.00, 10000.00, 0, 'mobile_money'),
('INV-20240320-001', 19, '2024-03-20 09:30:00', 85000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240320-002', 20, '2024-03-20 16:00:00', 125000.00, 5000.00, 0, 'card');

-- March 21-31
INSERT INTO sales (invoice_number, customer_id, sale_date, total_amount, discount, tax, payment_method) VALUES
('INV-20240321-001', 1, '2024-03-21 10:15:00', 35000.00, 0, 3000.00, 'cash'),
('INV-20240321-002', 2, '2024-03-21 14:30:00', 195000.00, 15000.00, 0, 'mobile_money'),
('INV-20240322-001', 3, '2024-03-22 09:45:00', 95000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240322-002', 4, '2024-03-22 15:20:00', 280000.00, 0, 20000.00, 'card'),
('INV-20240323-001', 5, '2024-03-23 11:00:00', 55000.00, 0, 0, 'cash'),
('INV-20240323-002', 6, '2024-03-23 16:30:00', 185000.00, 15000.00, 0, 'mobile_money'),
('INV-20240324-001', 7, '2024-03-24 10:00:00', 75000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240324-002', 8, '2024-03-24 14:45:00', 220000.00, 20000.00, 0, 'card'),
('INV-20240325-001', 9, '2024-03-25 09:30:00', 45000.00, 0, 0, 'cash'),
('INV-20240325-002', 10, '2024-03-25 16:00:00', 160000.00, 10000.00, 0, 'mobile_money'),
('INV-20240326-001', 11, '2024-03-26 10:15:00', 85000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240326-002', 12, '2024-03-26 14:30:00', 125000.00, 5000.00, 0, 'card'),
('INV-20240327-001', 13, '2024-03-27 09:45:00', 35000.00, 0, 3000.00, 'cash'),
('INV-20240327-002', 14, '2024-03-27 15:20:00', 195000.00, 15000.00, 0, 'mobile_money'),
('INV-20240328-001', 15, '2024-03-28 11:00:00', 95000.00, 5000.00, 0, 'bank_transfer'),
('INV-20240328-002', 16, '2024-03-28 16:30:00', 280000.00, 0, 20000.00, 'card'),
('INV-20240329-001', 17, '2024-03-29 10:00:00', 55000.00, 0, 0, 'cash'),
('INV-20240329-002', 18, '2024-03-29 14:45:00', 185000.00, 15000.00, 0, 'mobile_money'),
('INV-20240330-001', 19, '2024-03-30 09:30:00', 75000.00, 0, 5000.00, 'bank_transfer'),
('INV-20240330-002', 20, '2024-03-30 16:00:00', 220000.00, 20000.00, 0, 'card'),
('INV-20240331-001', 1, '2024-03-31 10:15:00', 45000.00, 0, 0, 'cash'),
('INV-20240331-002', 2, '2024-03-31 14:30:00', 160000.00, 10000.00, 0, 'mobile_money');

-- Insert sale items for all sales (sample items for first 10 invoices)
-- This is a simplified version - in reality, each sale would have multiple items
INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 1200000.00, 1200000.00), (1, 2, 1, 15000.00, 15000.00),
(2, 11, 2, 45000.00, 90000.00), (2, 12, 1, 180000.00, 180000.00),
(3, 13, 2, 85000.00, 170000.00), (3, 14, 1, 12000.00, 12000.00),
(4, 15, 5, 8000.00, 40000.00), (4, 16, 1, 15000.00, 15000.00),
(5, 17, 1, 65000.00, 65000.00), (5, 18, 2, 9000.00, 18000.00),
(6, 19, 3, 35000.00, 105000.00), (6, 20, 1, 25000.00, 25000.00),
(7, 21, 1, 850000.00, 850000.00), (7, 22, 1, 950000.00, 950000.00),
(8, 23, 2, 35000.00, 70000.00), (8, 24, 1, 45000.00, 45000.00),
(9, 25, 1, 25000.00, 25000.00), (9, 1, 1, 55000.00, 55000.00),
(10, 2, 1, 120000.00, 120000.00), (10, 3, 1, 15000.00, 15000.00);

-- Insert more expenses for March 2024
INSERT INTO expenses (category, description, amount, expense_date, payment_method) VALUES
('Salaries', 'Part-time staff wages', 250000.00, '2024-03-08', 'bank_transfer'),
('Marketing', 'Google Ads campaign', 75000.00, '2024-03-12', 'card'),
('Maintenance', 'Computer repairs', 35000.00, '2024-03-15', 'cash'),
('Insurance', 'Business insurance premium', 120000.00, '2024-03-18', 'bank_transfer'),
('Training', 'Staff training workshop', 45000.00, '2024-03-22', 'card'),
('Software', 'Monthly software subscriptions', 25000.00, '2024-03-25', 'bank_transfer'),
('Cleaning', 'Office cleaning services', 18000.00, '2024-03-28', 'cash'),
('Bank Charges', 'Monthly bank charges', 15000.00, '2024-03-30', 'bank_transfer');

-- Insert stock adjustments
INSERT INTO stock_adjustments (product_id, adjustment_type, quantity, reason, adjusted_by) VALUES
(1, 'in', 10, 'New stock received', 1),
(2, 'out', 5, 'Sold to customer', 1),
(3, 'correction', 2, 'Stock count correction', 2),
(4, 'in', 20, 'Bulk purchase', 1),
(5, 'out', 8, 'Regular sales', 2),
(6, 'in', 15, 'New supplier', 1),
(7, 'out', 3, 'Corporate order', 2),
(8, 'correction', 1, 'Damaged item removed', 1);

-- Insert audit log entries
INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values, ip_address) VALUES
(1, 'LOGIN', 'users', 1, NULL, '{"action": "login"}', '192.168.1.100'),
(2, 'CREATE', 'products', 11, NULL, '{"name": "Smartphone Samsung A54", "price": 850000}', '192.168.1.101'),
(1, 'UPDATE', 'customers', 3, '{"phone": "+265 776 334455"}', '{"phone": "+265 776 334466"}', '192.168.1.100'),
(2, 'DELETE', 'expenses', 1, '{"amount": 250000, "category": "Rent"}', NULL, '192.168.1.101'),
(1, 'EXPORT', 'reports', NULL, NULL, '{"report": "sales_summary", "format": "csv"}', '192.168.1.100');

-- Update product stock based on sales (simplified calculation)
UPDATE products p
SET stock_quantity = (
    SELECT initial_stock - COALESCE(sold_quantity, 0)
    FROM (
        SELECT 
            p.id,
            p.stock_quantity as initial_stock,
            SUM(si.quantity) as sold_quantity
        FROM products p
        LEFT JOIN sale_items si ON p.id = si.product_id
        GROUP BY p.id
    ) as stock_calc
    WHERE stock_calc.id = p.id
);

-- Display statistics after data insertion
SELECT 
    (SELECT COUNT(*) FROM customers) as total_customers,
    (SELECT COUNT(*) FROM products) as total_products,
    (SELECT COUNT(*) FROM sales) as total_sales,
    (SELECT SUM(total_amount) FROM sales) as total_revenue,
    (SELECT SUM(amount) FROM expenses) as total_expenses,
    (SELECT SUM(stock_quantity * cost) FROM products) as inventory_value;

-- Create a summary report view
CREATE OR REPLACE VIEW monthly_summary AS
SELECT 
    'March 2024' as period,
    COUNT(DISTINCT s.id) as total_transactions,
    COUNT(DISTINCT s.customer_id) as unique_customers,
    SUM(s.total_amount) as total_revenue,
    SUM(s.discount) as total_discount,
    SUM(s.tax) as total_tax,
    SUM(e.amount) as total_expenses,
    (SUM(s.total_amount) - SUM(e.amount)) as net_profit,
    AVG(s.total_amount) as avg_transaction_value
FROM sales s
CROSS JOIN (SELECT SUM(amount) as amount FROM expenses WHERE MONTH(expense_date) = 3) e
WHERE MONTH(s.sale_date) = 3;

-- Display the monthly summary
SELECT * FROM monthly_summary;

SELECT 'Sample data inserted successfully! Ready for testing.' as message;