from faker import Faker

from app.core.supbase_admin import supabase_admin
from app.database import get_connection

fake = Faker("es_ES")
CANTIDAD = 50
for i in range(CANTIDAD):
    username= f"usuario_{i+1:03d}"
    email= f"usuario_{i+1:03d}@example.com"
    try:
        respuesta = supabase_admin.auth.admin.create_user({
            "email":email,
            "password":"Prueba123456!",
            "email_confirm": True
        })
        usuario = respuesta.user
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO profiles (id, username)
                    VALUES (%s, %s)
                    """,
                    (usuario.id, username)
                )

            connection.commit()

        print(f"Usuario creado: {username}")

    except Exception as error:
        print(f"Error creando {username}: {error}")
