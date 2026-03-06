-- Sirio TPV Database Schema
-- Para Vercel Postgres

-- Table: transactions
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    items JSONB NOT NULL DEFAULT '[]',
    subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
    tax DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    payment_method VARCHAR(50) DEFAULT 'card',
    status VARCHAR(50) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    created_ip VARCHAR(45)
);

-- Table: products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(5, 2) DEFAULT 21.00,
    stock INT DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'cashier',
    active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: audit_logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: invoices
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(id),
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    series_code VARCHAR(10),
    tax_identification_number VARCHAR(20),
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    items JSONB NOT NULL,
    subtotal DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    total DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'draft',
    aeat_status VARCHAR(50),
    qr_code TEXT,
    digital_signature TEXT,
    issued_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_products_code ON products(code);
CREATE INDEX idx_products_active ON products(active);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_invoices_transaction_id ON invoices(transaction_id);
CREATE INDEX idx_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_status ON invoices(status);

-- Sequence
CREATE SEQUENCE IF NOT EXISTS invoice_number_seq START 1000;

-- Initial data
INSERT INTO products (code, name, description, price, tax_rate, stock, active) 
VALUES 
  ('BEER001', 'Cerveza Caña', 'Cerveza pequeña', 3.50, 21.00, 100, true),
  ('BEER002', 'Cerveza Pinta', 'Cerveza grande', 5.50, 21.00, 80, true),
  ('WINE001', 'Vino Tinto', 'Vino tinto de la casa', 8.00, 21.00, 50, true),
  ('WINE002', 'Vino Blanco', 'Vino blanco de la casa', 8.00, 21.00, 40, true),
  ('WATER001', 'Agua Mineral', 'Botella de agua', 2.00, 21.00, 200, true),
  ('COFFEE001', 'Café Espresso', 'Café solo', 1.50, 21.00, 500, true),
  ('TAPAS001', 'Jamón Ibérico', 'Tabla de jamón', 12.00, 21.00, 20, true),
  ('TAPAS002', 'Queso Manchego', 'Tabla de queso', 10.00, 21.00, 25, true)
ON CONFLICT (code) DO NOTHING;

-- Usuarios de prueba
INSERT INTO users (username, email, password_hash, role, active)
VALUES 
  ('admin', 'admin@sirio.local', 'hash_admin', 'admin', true),
  ('cashier1', 'cashier1@sirio.local', 'hash_cashier', 'cashier', true),
  ('manager1', 'manager1@sirio.local', 'hash_manager', 'manager', true)
ON CONFLICT (username) DO NOTHING;

-- Tabla de configuración
CREATE TABLE IF NOT EXISTS config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO config (key, value) VALUES
  ('app_version', '1.0.0'),
  ('app_name', 'Sirio TPV'),
  ('default_tax_rate', '21.00'),
  ('invoice_series', 'SIR'),
  ('receipt_printer', 'disabled'),
  ('display_decimals', '2')
ON CONFLICT (key) DO NOTHING;
