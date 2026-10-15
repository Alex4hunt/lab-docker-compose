CREATE TABLE IF NOT EXISTS ads (
    id SERIAL PRIMARY KEY,
    seller VARCHAR(100) NOT NULL DEFAULT 'Иван',
    title VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    original_price INTEGER NOT NULL,
    age_months INTEGER NOT NULL,
    condition VARCHAR(20) NOT NULL,
    recommended_price INTEGER
);

INSERT INTO ads (seller, title, category, original_price, age_months, condition) VALUES
('Иван', 'Смартфон Samsung Galaxy', 'electronics', 800, 18, 'good'),
('Иван', 'Ноутбук Lenovo', 'electronics', 1200, 30, 'fair'),
('Иван', 'Диван угловой', 'furniture', 600, 24, 'good'),
('Иван', 'Куртка зимняя', 'clothes', 150, 12, 'excellent'),
('Иван', 'Велосипед горный', 'other', 400, 36, 'poor');