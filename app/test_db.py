from database import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()

        print(resultado)