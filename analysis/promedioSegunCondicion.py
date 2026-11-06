import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el archivo de publicaciones
publicaciones = pd.read_csv("./data/raw/listings.csv")

# 2. Agrupar por la condición del producto y calcular el promedio del precio
promedio_condicion = publicaciones.groupby("condition")["price"].mean().reset_index(name="precio_promedio")

# 3. Ordenar de mayor a menor por el precio promedio y redondear a 2 decimales
resultado = promedio_condicion.sort_values(by="precio_promedio", ascending=False)
resultado["precio_promedio"] = resultado["precio_promedio"].round(2)

# print(resultado)


plt.pie(resultado["precio_promedio"], labels=resultado["condition"], autopct='%1.1f%%')
plt.title("Precio promedio por condición del producto")
plt.show()

plt.bar(resultado["condition"], resultado["precio_promedio"])
plt.title("Precio promedio por condición del producto")
plt.xlabel("Condición")
plt.ylabel("Precio Promedio")
plt.show()