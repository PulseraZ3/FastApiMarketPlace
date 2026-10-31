
import random
from datetime import datetime, timedelta, timezone

from faker import Faker

from app.database import get_connection

fake = Faker("es_ES")

CANTIDAD_PUBLICACIONES = 300
CANTIDAD_RESENAS = 200

# --------------------------------------------------
# DATOS PARA PUBLICACIONES
# --------------------------------------------------

PRODUCTOS = {
    "Electrónica": [
        ("Monitor Samsung 24 pulgadas", 350, 650),
        ("Teclado mecánico RGB", 100, 280),
        ("Mouse Logitech inalámbrico", 40, 180),
        ("Audífonos Bluetooth", 50, 250),
        ("Smart TV 43 pulgadas", 700, 1400),
        ("Parlante portátil JBL", 80, 350),
    ],
    "Tecnología": [
        ("Smartwatch deportivo", 80, 350),
        ("Cámara de seguridad WiFi", 60, 250),
        ("Router WiFi", 80, 300),
        ("Proyector portátil", 250, 800),
    ],
    "Computación": [
        ("Laptop Lenovo Core i5", 1200, 2800),
        ("Memoria RAM DDR4 16GB", 100, 250),
        ("SSD NVMe 1TB", 180, 350),
        ("Tarjeta gráfica GTX 1660", 450, 900),
        ("Case gamer", 100, 400),
    ],
    "Celulares y accesorios": [
        ("iPhone 13", 1200, 1900),
        ("Samsung Galaxy A54", 500, 900),
        ("Cargador USB-C", 20, 90),
        ("Power bank 20000mAh", 50, 150),
    ],
    "Videojuegos": [
        ("Control Xbox inalámbrico", 120, 250),
        ("Juego físico para PS5", 100, 250),
        ("Auriculares gamer", 80, 300),
    ],
    "Consolas": [
        ("PlayStation 4 Slim", 650, 1000),
        ("Nintendo Switch", 700, 1200),
        ("Xbox Series S", 900, 1300),
    ],
    "Ropa": [
        ("Casaca deportiva", 50, 180),
        ("Polera oversize", 35, 100),
        ("Jean para hombre", 40, 120),
    ],
    "Calzado": [
        ("Zapatillas deportivas", 80, 300),
        ("Botines de fútbol", 70, 250),
    ],
    "Hogar": [
        ("Lámpara de escritorio", 30, 120),
        ("Organizador de habitación", 20, 100),
        ("Espejo decorativo", 40, 180),
    ],
    "Electrodomésticos": [
        ("Licuadora Oster", 100, 250),
        ("Microondas", 200, 450),
        ("Freidora de aire", 180, 400),
    ],
    "Muebles": [
        ("Escritorio para computadora", 150, 500),
        ("Silla ergonómica", 180, 650),
        ("Estantería de madera", 100, 350),
    ],
    "Deportes": [
        ("Balón de fútbol", 30, 120),
        ("Mancuernas ajustables", 100, 350),
        ("Bicicleta urbana", 300, 900),
    ],
    "Libros": [
        ("Libro de programación Python", 30, 100),
        ("Libro de matemáticas", 25, 90),
        ("Novela de ciencia ficción", 20, 70),
    ],
    "Música": [
        ("Parlante de estudio", 150, 500),
        ("Micrófono USB", 80, 300),
    ],
    "Instrumentos musicales": [
        ("Guitarra acústica", 200, 600),
        ("Teclado musical", 250, 800),
    ],
    "Belleza y cuidado personal": [
        ("Secadora de cabello", 50, 200),
        ("Plancha para cabello", 40, 180),
    ],
    "Juguetes": [
        ("Set de construcción", 30, 150),
        ("Carro a control remoto", 50, 180),
    ],
    "Coleccionables": [
        ("Figura de colección", 50, 300),
        ("Set de cartas coleccionables", 20, 150),
    ],
    "Automotriz": [
        ("Cámara para automóvil", 80, 250),
        ("Compresor portátil", 100, 300),
    ],
    "Herramientas": [
        ("Taladro inalámbrico", 120, 400),
        ("Juego de destornilladores", 30, 120),
    ],
    "Mascotas": [
        ("Transportadora para mascotas", 50, 180),
        ("Cama para perro", 40, 150),
    ],
    "Oficina y papelería": [
        ("Silla de oficina", 150, 500),
        ("Calculadora científica", 30, 100),
    ],
    "Fotografía": [
        ("Trípode profesional", 60, 250),
        ("Lente para cámara", 300, 1200),
    ],
    "Otros": [
        ("Producto de segunda mano", 20, 200),
        ("Artículo variado", 15, 150),
    ],
}

CONDICIONES = [
    "Nuevo",
    "Como nuevo",
    "Buen estado",
    "Estado regular",
]

ESTADOS = [
    "active",
    "active",
    "active",
    "sold",
]


def fecha_aleatoria():
    ahora = datetime.now(timezone.utc)
    dias_atras = random.randint(0, 180)

    return ahora - timedelta(
        days=dias_atras,
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )


def obtener_datos():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT id, username
                FROM profiles
            """)
            perfiles = cursor.fetchall()

            cursor.execute("""
                SELECT id, name
                FROM categories
            """)
            categorias = cursor.fetchall()

    if len(perfiles) < 2:
        raise ValueError("Se necesitan al menos dos perfiles.")

    if not categorias:
        raise ValueError("No existen categorías.")

    return perfiles, categorias


def generar_publicaciones(perfiles, categorias):
    categorias_dict = {
        nombre: categoria_id
        for categoria_id, nombre in categorias
    }

    publicaciones = []

    for _ in range(CANTIDAD_PUBLICACIONES):
        perfil = random.choice(perfiles)
        categoria_id, nombre_categoria = random.choice(categorias)

        productos = PRODUCTOS.get(
            nombre_categoria,
            PRODUCTOS["Otros"]
        )

        titulo, precio_minimo, precio_maximo = random.choice(productos)

        descripcion = fake.paragraph(nb_sentences=3)

        publicaciones.append((
            perfil[0],
            categoria_id,
            titulo,
            descripcion,
            round(random.uniform(precio_minimo, precio_maximo), 2),
            random.choice(CONDICIONES),
            random.choice(ESTADOS),
            fecha_aleatoria()
        ))

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany("""
                INSERT INTO listings (
                    user_id,
                    category_id,
                    title,
                    description,
                    price,
                    condition,
                    status,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, publicaciones)

        connection.commit()

    print(f"{len(publicaciones)} publicaciones creadas.")


def generar_resenas(perfiles):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id
                FROM listings
            """)
            publicaciones = cursor.fetchall()

    resenas = []

    for _ in range(CANTIDAD_RESENAS):
        reviewer = random.choice(perfiles)[0]

        # Aproximadamente 60% de reseñas asociadas
        # a una publicación y 40% directas al usuario.
        if publicaciones and random.random() < 0.60:
            listing_id, seller_id = random.choice(publicaciones)

            if reviewer == seller_id:
                continue

            resenas.append((
                reviewer,
                seller_id,
                listing_id,
                random.randint(1, 5),
                fake.sentence(nb_words=12),
                fecha_aleatoria()
            ))

        else:
            seller = random.choice(perfiles)[0]

            if reviewer == seller:
                continue

            resenas.append((
                reviewer,
                seller,
                None,
                random.randint(1, 5),
                fake.sentence(nb_words=12),
                fecha_aleatoria()
            ))

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany("""
                INSERT INTO reviews (
                    reviewer_id,
                    reviewed_user_id,
                    listing_id,
                    rating,
                    comment,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, resenas)

        connection.commit()

    print(f"{len(resenas)} reseñas creadas.")


def main():
    perfiles, categorias = obtener_datos()

    print(f"Perfiles encontrados: {len(perfiles)}")
    print(f"Categorías encontradas: {len(categorias)}")

    generar_publicaciones(perfiles, categorias)

    # Actualizar la lista de publicaciones para generar reseñas.
    generar_resenas(perfiles)

    print("Generación de datos finalizada.")


if __name__ == "__main__":
    main()
