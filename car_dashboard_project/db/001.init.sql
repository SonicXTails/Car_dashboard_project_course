CREATE DATABASE car_dashboard_db;
CREATE USER adminitrator_chase WITH PASSWORD 'werawera00!';
ALTER ROLE adminitrator_chase SET client_encoding TO 'utf8';
ALTER ROLE adminitrator_chase SET default_transaction_isolation TO 'read committed';
ALTER ROLE adminitrator_chase SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE car_dashboard_db TO adminitrator_chase;

-- права на базу
GRANT ALL PRIVILEGES ON DATABASE car_dashboard_db TO adminitrator_chase;

-- права на схему public
GRANT ALL PRIVILEGES ON SCHEMA public TO adminitrator_chase;

-- права на все таблицы
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO adminitrator_chase;