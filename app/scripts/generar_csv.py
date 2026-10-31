import pandas as pd

from app.database import get_connection
from pathlib import Path


# Tablas que queremos exportar
TABLAS = [
    "profiles",
    "categories",
    "listings",
    "reviews"
]

# Directorio de destino
DIRECTORIO = Path("data/raw")
DIRECTORIO.mkdir(parents=True, exist_ok=True)


def exportar_tabla(nombre_tabla):

    with get_connection() as connection:

        consulta = f"SELECT * FROM {nombre_tabla}"

        df = pd.read_sql_query(consulta, connection)

        ruta = DIRECTORIO / f"{nombre_tabla}.csv"

        df.to_csv(
            ruta,
            index=False,
            encoding="utf-8"
        )

        print(f"{nombre_tabla}.csv exportado: {len(df)} registros")


def main():

    for tabla in TABLAS:
        exportar_tabla(tabla)

    print("\nExportación finalizada.")


if __name__ == "__main__":
    main()