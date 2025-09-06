from django.db import connection

def set_admin_for_trigger(admin_id: int):
    """
    Устанавливает текущего админа в PostgreSQL для триггера.
    Нужно использовать внутри transaction.atomic().
    """
    with connection.cursor() as cursor:
        cursor.execute("SET LOCAL myapp.current_admin_id = %s;", [admin_id])