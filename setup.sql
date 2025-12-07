-- =====================================================
-- THE BHARAT COLLECTIONS - SUPABASE DATABASE SCHEMA
-- Backend Mediator Admin Interface
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- PRODUCTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    collection VARCHAR(50),
    manufacturer VARCHAR(100),
    made_in VARCHAR(100),
    qikink_product_id VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_qikink_id ON products(qikink_product_id);

-- =====================================================
-- VARIANTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS variants (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    size VARCHAR(20),
    color VARCHAR(50),
    stock INT DEFAULT 0,
    qikink_variant_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_variants_product_id ON variants(product_id);
CREATE INDEX IF NOT EXISTS idx_variants_qikink_id ON variants(qikink_variant_id);

-- =====================================================
-- ORDERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255),
    customer_phone VARCHAR(20),
    shipping_address TEXT NOT NULL,
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_pincode VARCHAR(10),
    items JSONB NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    qikink_order_id VARCHAR(100),
    qikink_shipment_id VARCHAR(100),
    razorpay_order_id VARCHAR(100),
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_orders_order_id ON orders(order_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_razorpay_order_id ON orders(razorpay_order_id);
CREATE INDEX IF NOT EXISTS idx_orders_qikink_order_id ON orders(qikink_order_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);

-- =====================================================
-- PAYMENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    razorpay_payment_id VARCHAR(100),
    razorpay_order_id VARCHAR(100) NOT NULL,
    razorpay_signature TEXT,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(50) DEFAULT 'created',
    payment_method VARCHAR(50),
    webhook_processed BOOLEAN DEFAULT FALSE,
    idempotency_key VARCHAR(100) UNIQUE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id);
CREATE INDEX IF NOT EXISTS idx_payments_idempotency_key ON payments(idempotency_key);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

-- =====================================================
-- TRACKING LOGS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS tracking_logs (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    qikink_order_id VARCHAR(100),
    tracking_number VARCHAR(100),
    status VARCHAR(50),
    location VARCHAR(255),
    description TEXT,
    event_timestamp TIMESTAMP WITH TIME ZONE,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_tracking_logs_order_id ON tracking_logs(order_id);
CREATE INDEX IF NOT EXISTS idx_tracking_logs_qikink_order_id ON tracking_logs(qikink_order_id);
CREATE INDEX IF NOT EXISTS idx_tracking_logs_event_timestamp ON tracking_logs(event_timestamp DESC);

-- =====================================================
-- ADMIN USERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS admin_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);

-- =====================================================
-- USERS TABLE (Customer Accounts)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- =====================================================
-- FAILED JOBS QUEUE TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS failed_jobs (
    id BIGSERIAL PRIMARY KEY,
    job_type VARCHAR(50) NOT NULL,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    payload JSONB,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    status VARCHAR(50) DEFAULT 'pending',
    next_retry_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_failed_jobs_status ON failed_jobs(status);
CREATE INDEX IF NOT EXISTS idx_failed_jobs_next_retry ON failed_jobs(next_retry_at);
CREATE INDEX IF NOT EXISTS idx_failed_jobs_order_id ON failed_jobs(order_id);

-- =====================================================
-- WEBHOOK LOGS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS webhook_logs (
    id BIGSERIAL PRIMARY KEY,
    webhook_type VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    signature TEXT,
    status VARCHAR(50) DEFAULT 'received',
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_webhook_logs_webhook_type ON webhook_logs(webhook_type);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_status ON webhook_logs(status);
CREATE INDEX IF NOT EXISTS idx_webhook_logs_created_at ON webhook_logs(created_at DESC);

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_variants_updated_at BEFORE UPDATE ON variants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_admin_users_updated_at BEFORE UPDATE ON admin_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_failed_jobs_updated_at BEFORE UPDATE ON failed_jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE tracking_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE failed_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE webhook_logs ENABLE ROW LEVEL SECURITY;

-- Public read access for products and variants
CREATE POLICY "Public can view products" ON products FOR SELECT USING (true);
CREATE POLICY "Public can view variants" ON variants FOR SELECT USING (true);

-- Service role can do everything (for backend API)
CREATE POLICY "Service role can manage products" ON products FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage variants" ON variants FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage orders" ON orders FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage payments" ON payments FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage tracking" ON tracking_logs FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage admins" ON admin_users FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage users" ON users FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage failed jobs" ON failed_jobs FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role can manage webhooks" ON webhook_logs FOR ALL USING (auth.role() = 'service_role');

-- =====================================================
-- INITIAL DATA (OPTIONAL)
-- =====================================================

-- Insert default admin user (password: admin123 - CHANGE IN PRODUCTION!)
-- Password hash generated with bcrypt
INSERT INTO admin_users (username, email, password_hash, role)
VALUES (
    'admin',
    'admin@bharatcollections.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLHJ4tXu',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- =====================================================
-- VIEWS FOR ANALYTICS
-- =====================================================

-- Order statistics view
CREATE OR REPLACE VIEW order_statistics AS
SELECT 
    COUNT(*) as total_orders,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders,
    COUNT(CASE WHEN status = 'payment_verified' THEN 1 END) as payment_verified,
    COUNT(CASE WHEN status = 'qikink_submitted' THEN 1 END) as qikink_submitted,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as average_order_value
FROM orders;

-- Daily order summary view
CREATE OR REPLACE VIEW daily_order_summary AS
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as order_count,
    SUM(total_amount) as daily_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
GROUP BY DATE(created_at)
ORDER BY order_date DESC;

-- Failed jobs summary view
CREATE OR REPLACE VIEW failed_jobs_summary AS
SELECT 
    job_type,
    status,
    COUNT(*) as count,
    MAX(created_at) as last_failure
FROM failed_jobs
GROUP BY job_type, status;

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON TABLE products IS 'Product catalog with Qikink mapping';
COMMENT ON TABLE variants IS 'Product variants (size, color) with Qikink mapping';
COMMENT ON TABLE orders IS 'Customer orders with Razorpay and Qikink integration';
COMMENT ON TABLE payments IS 'Payment records with Razorpay integration and idempotency';
COMMENT ON TABLE tracking_logs IS 'Order tracking events from Qikink';
COMMENT ON TABLE admin_users IS 'Admin users for backend management';
COMMENT ON TABLE users IS 'Customer user accounts for the e-commerce platform';
COMMENT ON TABLE failed_jobs IS 'Queue for failed API calls with retry logic';
COMMENT ON TABLE webhook_logs IS 'Webhook event logs for debugging';

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Supabase database schema created successfully!';
    RAISE NOTICE '📊 Tables created: products, variants, orders, payments, tracking_logs, admin_users, users, failed_jobs, webhook_logs';
    RAISE NOTICE '🔐 Row Level Security enabled on all tables';
    RAISE NOTICE '👤 Default admin user created (username: admin, password: admin123)';
    RAISE NOTICE '⚠️  IMPORTANT: Change the default admin password in production!';
END $$;
