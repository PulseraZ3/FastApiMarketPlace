from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.supabase import supabase


security = HTTPBearer()


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        respuesta = supabase.auth.get_user(token)

        if respuesta.user is None:
            raise HTTPException(
                status_code=401,
                detail="Usuario no autenticado"
            )

        return respuesta.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )