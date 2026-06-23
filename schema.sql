-- ============================================
-- A to Z Enterprises - Database Schema
-- Mobile Accessories & Repair Shop
-- ============================================

CREATE DATABASE IF NOT EXISTS atoz_enterprises;
USE atoz_enterprises;

-- ---------- Admin Users ----------
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Product Categories ----------
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    display_order INT DEFAULT 0
);

-- ---------- Products ----------
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    mrp DECIMAL(10,2) DEFAULT NULL,        -- original price for "discount" display
    image_url VARCHAR(500) DEFAULT NULL,
    in_stock BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ---------- Repair Services ----------
CREATE TABLE IF NOT EXISTS repair_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(150) NOT NULL,
    description TEXT,
    price_range VARCHAR(100) NOT NULL,     -- e.g. "Rs.500 - Rs.2500"
    estimated_time VARCHAR(50) DEFAULT NULL, -- e.g. "30 mins"
    icon_key VARCHAR(50) DEFAULT NULL,     -- maps to a frontend icon
    display_order INT DEFAULT 0
);

-- ---------- Customer Reviews ----------
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,     -- admin approves before it shows publicly
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------- Contact / Enquiry Messages (from website contact form) ----------
CREATE TABLE IF NOT EXISTS enquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    message TEXT,
    enquiry_type VARCHAR(50) DEFAULT 'general', -- general / repair / product
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Seed Data
-- ============================================

INSERT INTO categories (name, slug, display_order) VALUES
('Mobile Cases & Covers', 'cases-covers', 1),
('Chargers & Adapters', 'chargers', 2),
('Earphones & Headsets', 'earphones', 3),
('Power Banks', 'power-banks', 4),
('Cables', 'cables', 5),
('Screen Guards & Tempered Glass', 'screen-guards', 6),
('Bluetooth Speakers', 'speakers', 7),
('Mobile Holders & Stands', 'holders', 8);

INSERT INTO repair_services (service_name, description, price_range, estimated_time, icon_key, display_order) VALUES
('Screen / Display Repair', 'Cracked or dead display replacement for all major brands', 'Rs.800 - Rs.4500', '45 mins', 'screen', 1),
('Battery Replacement', 'Original quality battery replacement with 6 month warranty', 'Rs.500 - Rs.2000', '20 mins', 'battery', 2),
('Charging Port Repair', 'Fix loose or non-working charging port / connector issues', 'Rs.400 - Rs.1200', '30 mins', 'charging', 3),
('Speaker / Mic Repair', 'Speaker, earpiece and microphone repair or replacement', 'Rs.350 - Rs.1000', '25 mins', 'speaker', 4),
('Camera Repair', 'Front and back camera module repair / replacement', 'Rs.600 - Rs.3000', '40 mins', 'camera', 5),
('Water Damage Service', 'Complete cleaning and component-level water damage repair', 'Rs.500 - Rs.3500', '24-48 hrs', 'water', 6);

INSERT INTO products (category_id, name, description, price, mrp, in_stock, is_featured) VALUES
(1, 'Shockproof Back Cover', 'Military grade drop protection, all popular models available', 199.00, 399.00, TRUE, TRUE),
(1, 'Transparent TPU Case', 'Slim fit clear case with anti-yellowing coating', 149.00, 299.00, TRUE, FALSE),
(1, 'Leather Flip Cover', 'Premium PU leather with card slots', 299.00, 599.00, TRUE, FALSE),
(2, '20W Fast Charger', 'PD fast charging adapter, type-C output', 449.00, 899.00, TRUE, TRUE),
(2, '33W Multi-Port Adapter', 'Dual port charger for phone and accessories together', 599.00, 1199.00, TRUE, FALSE),
(3, 'Wired Earphones with Mic', 'Clear bass, in-line mic and remote', 199.00, 399.00, TRUE, FALSE),
(3, 'Bluetooth Neckband', '20 hours battery, fast charging, deep bass', 699.00, 1499.00, TRUE, TRUE),
(4, '10000mAh Power Bank', 'Dual output, fast charging support', 899.00, 1599.00, TRUE, TRUE),
(5, 'Type-C Fast Charging Cable', '1 meter braided cable, 3A fast charging', 99.00, 199.00, TRUE, FALSE),
(6, 'Tempered Glass 9H', 'Edge to edge protection, anti-fingerprint coating', 99.00, 249.00, TRUE, FALSE),
(7, 'Mini Bluetooth Speaker', 'Portable speaker with deep bass, 8 hr playback', 599.00, 1199.00, TRUE, FALSE),
(8, 'Car Mobile Holder', '360 degree rotating dashboard mount', 249.00, 499.00, TRUE, FALSE);

INSERT INTO reviews (customer_name, rating, review_text, is_approved) VALUES
('Karthik R', 5, 'Screen repair was quick and affordable. Phone works like new!', TRUE),
('Priya S', 5, 'Bought a power bank here, good quality and genuine pricing.', TRUE),
('Manoj Kumar', 4, 'Battery replacement done same day. Good service.', TRUE);
