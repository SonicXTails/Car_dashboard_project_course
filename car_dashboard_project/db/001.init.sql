CREATE DATABASE car_dashboard_db;
CREATE USER adminitrator_chase WITH PASSWORD 'werawera00!';
ALTER ROLE adminitrator_chase SET client_encoding TO 'utf8';
ALTER ROLE adminitrator_chase SET default_transaction_isolation TO 'read committed';
ALTER ROLE adminitrator_chase SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE car_dashboard_db TO adminitrator_chase;
GRANT ALL PRIVILEGES ON SCHEMA public TO adminitrator_chase;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO adminitrator_chase;

-- 1. Функция для логирования
-- Функция для логирования действий админа
CREATE OR REPLACE FUNCTION log_admin_action()
RETURNS TRIGGER AS $$
DECLARE
    admin_id integer;
    action_text text;
BEGIN
    BEGIN
        admin_id := current_setting('myapp.current_admin_id')::int;
    EXCEPTION WHEN others THEN
        admin_id := NULL;
    END;

    IF TG_OP = 'INSERT' THEN
        action_text := 'create';
        INSERT INTO main_adminlog(admin, action, target_table, target_id)
        VALUES (admin_id, action_text, TG_TABLE_NAME, NEW.id);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        action_text := 'update';
        INSERT INTO main_adminlog(admin, action, target_table, target_id)
        VALUES (admin_id, action_text, TG_TABLE_NAME, NEW.id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        action_text := 'delete';
        INSERT INTO main_adminlog(admin, action, target_table, target_id)
        VALUES (admin_id, action_text, TG_TABLE_NAME, OLD.id);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Привязываем триггер к таблицам
CREATE TRIGGER card_crud_log
AFTER INSERT OR UPDATE OR DELETE ON main_card
FOR EACH ROW EXECUTE FUNCTION log_admin_action();

CREATE TRIGGER user_crud_log
AFTER INSERT OR UPDATE OR DELETE ON main_customuser
FOR EACH ROW EXECUTE FUNCTION log_admin_action();