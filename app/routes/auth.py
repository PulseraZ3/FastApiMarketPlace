from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.supabase import supabase
from app.database import get_connection
from app.auth_dependencies import obtener_usuario_actual
from app.models.usuario import RegistroUsuario, LoginUsuario

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register")
def registrar_usuario(datos: RegistroUsuario):

    respuesta = supabase.auth.sign_up({
        "email": datos.email,
        "password": datos.password
    })

    usuario = respuesta.user

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO profiles (id, username)
                VALUES (%s, %s)
                """,
                (usuario.id, datos.username)
            )

        connection.commit()

    return {
        "mensaje": "Usuario registrado correctamente",
        "user_id": usuario.id
    }


@router.post("/login")
def iniciar_sesion(datos: LoginUsuario):

    respuesta = supabase.auth.sign_in_with_password({
        "email": datos.email,
        "password": datos.password
    })

    return {
        "mensaje": "Inicio de sesión correcto",
        "access_token": respuesta.session.access_token,
        "refresh_token": respuesta.session.refresh_token
    }


@router.get("/me")
def obtener_me(user=Depends(obtener_usuario_actual)):

    return {
        "user_id": user.id,
        "email": user.email
    }