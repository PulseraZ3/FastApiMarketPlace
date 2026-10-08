from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.supabase import supabase


security = HTTPBearer()


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    respuesta = supabase.auth.get_user(token)

    return respuesta.user