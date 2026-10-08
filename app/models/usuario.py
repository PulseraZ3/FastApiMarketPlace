from pydantic import BaseModel


class RegistroUsuario(BaseModel):
    email: str
    password: str
    username: str


class LoginUsuario(BaseModel):
    email: str
    password: str