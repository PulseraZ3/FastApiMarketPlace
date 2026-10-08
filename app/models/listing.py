from pydantic import BaseModel


class CrearPublicacion(BaseModel):
    category_id: int
    title: str
    description: str
    price: float
    condition: str