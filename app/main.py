from fastapi import FastAPI

from app.routes import auth
from app.routes import listings


app = FastAPI()

app.include_router(auth.router)
app.include_router(listings.router)


@app.get("/")
def inicio():
    return {"mensaje": "Marketplace funcionando"}