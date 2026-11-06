import pandas as pd
import matplotlib.pyplot as plt


categorias = pd.read_csv("./data/raw/categories.csv")
publicaciones = pd.read_csv("./data/raw/listings.csv")
perfiles = pd.read_csv("./data/raw/profiles.csv")
# con esto lee los arcvhivos csv y los guarda en dataframes de pandas, que son estructuras de datos muy útiles para análisis de datos.
# publicaciones = publicaciones.merge(categorias, on='left', on='category_id', on='id')

#que producto se vendio mas
categorias_ventas = publicaciones.groupby('category_id').size().reset_index(name='ventas')
print("categorias con mas ventas:")
print(categorias_ventas.sort_values('ventas', ascending=False))

#Categorias con mas ventas

categorias_nombres = categorias[['id', 'name']]

#groupy hace un agrupamiento de los datos segun la columna que le pases.
categorias_ventas = publicaciones.groupby('category_id')

#size() cuenta el número de publicaciones en cada categoría.
categorias_ventas = categorias_ventas.size()

#reset_index(name='ventas') convierte la serie resultante en un dataframe y le da un nombre a la columna de conteo.
categorias_ventas = categorias_ventas.reset_index(name='ventas')

#merge combina dos dataframes según una columna común, en este caso 'category_id' y 'id', para obtener los nombres de las categorías.
categorias_ventas = categorias_ventas.merge(categorias_nombres, left_on='category_id', right_on='id')

# print("categorias con mas ventas:")
# print(categorias_ventas.sort_values('ventas', ascending=False))

serie = categorias_ventas.groupby("name")["ventas"].sum()
plt.bar(serie.index, serie.values)
plt.title("Ventas por categoría")
plt.show()