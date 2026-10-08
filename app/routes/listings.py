from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.database import get_connection
from app.models.listing import CrearPublicacion
from app.core.supabase import supabase
from app.auth_dependencies import obtener_usuario_actual


router = APIRouter(prefix="/listings", tags=["Listings"])


@router.post("/")
def crear_publicacion(
    datos: CrearPublicacion,
    usuario=Depends(obtener_usuario_actual)
):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO listings
                (user_id, category_id, title, description, price, condition)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, category_id, title, description, price, condition, status, created_at
                """,
                (
                    usuario.id,
                    datos.category_id,
                    datos.title,
                    datos.description,
                    datos.price,
                    datos.condition
                )
            )

            publicacion = cursor.fetchone()

        connection.commit()

    return {
        "id": publicacion[0],
        "category_id": publicacion[1],
        "title": publicacion[2],
        "description": publicacion[3],
        "price": publicacion[4],
        "condition": publicacion[5],
        "status": publicacion[6],
        "created_at": publicacion[7]
    }
@router.get("/")
def obtener_publicaciones():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    category_id,
                    title,
                    description,
                    price,
                    condition,
                    status,
                    created_at
                FROM listings
                ORDER BY created_at DESC
                """
            )
            publicaciones = cursor.fetchall()
    return [
        {
            "id": publicacion[0],
            "category_id": publicacion[1],
            "title": publicacion[2],
            "description": publicacion[3],
            "price": publicacion[4],
            "condition": publicacion[5],
            "status": publicacion[6],
            "created_at": publicacion[7]
        }
        for publicacion in publicaciones
    ]

@router.get("/category/{category_id}")
def obtener_publicaciones_por_categoria(category_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    category_id,
                    title,
                    description,
                    price,
                    condition,
                    status,
                    created_at
                FROM listings
                WHERE category_id = %s
                ORDER BY created_at DESC
                """,
                (category_id,)
            )

            publicaciones = cursor.fetchall()

    return [
        {
            "id": publicacion[0],
            "category_id": publicacion[1],
            "title": publicacion[2],
            "description": publicacion[3],
            "price": publicacion[4],
            "condition": publicacion[5],
            "status": publicacion[6],
            "created_at": publicacion[7]
        }
        for publicacion in publicaciones
    ]
@router.post("/{listing_id}/images")
def subir_imagen(
    listing_id: int,
    file: UploadFile = File(...),
    usuario=Depends(obtener_usuario_actual)
):

    # Verificación de la imagen
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen"
        )

    # Conexión a la base de datos
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM listings
                WHERE id = %s AND user_id = %s
                """,
                (listing_id, usuario.id)
            )

            publicacion = cursor.fetchone()

            if not publicacion:
                raise HTTPException(
                    status_code=404,
                    detail="Publicación no encontrada"
                )

    finally:
        conn.close()

    # Leer la imagen
    contenido = file.file.read()

    # Ruta dentro de Storage
    ruta = f"{listing_id}/{file.filename}"

    # Subir imagen
    try:
        supabase.storage.from_("listing-images").upload(
            ruta,
            contenido,
            {
                "content-type": file.content_type
            }
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir la imagen: {str(error)}"
        )

    # Obtener URL pública
    url = supabase.storage.from_("listing-images").get_public_url(ruta)

    # Guardar URL en PostgreSQL
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO listing_images (listing_id, image_url)
                VALUES (%s, %s)
                RETURNING id, listing_id, image_url
                """,
                (listing_id, url)
            )

            imagen = cursor.fetchone()

        conn.commit()

        return {
            "id": imagen[0],
            "listing_id": imagen[1],
            "image_url": imagen[2]
        }

    finally:
        conn.close()