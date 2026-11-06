import pandas as pd
import matplotlib.pyplot as plt


categorias = pd.read_csv("./data/raw/categories.csv")
publicaciones = pd.read_csv("./data/raw/listings.csv")
perfiles = pd.read_csv("./data/raw/profiles.csv")

#mean lo que hace es calcular el promedio de la columna "price" para cada categoría de producto, agrupando los datos por "category_id".
promedio = publicaciones.groupby("category_id")["price"].mean()

#merge lo que hace es combinar el dataframe promedio con el dataframe categorias, para obtener los nombres de las categorías correspondientes a cada category_id.
#combinamos promedio y categorias
promedio1 = pd.merge(promedio, categorias, left_on="category_id", right_on="id")

#para ordenar 
promedio1 = promedio1.sort_values(by = "price", ascending=True)
# print(promedio1)

serie = promedio1.groupby("name")["price"].mean()
plt.plot(serie.index, serie.values, marker='o')
plt.title("Precio promedio por categoría")
plt.xlabel("Categoría")
plt.ylabel("Precio promedio")
plt.xticks(rotation=45)
plt.show()


# df_completo = publicaciones.merge(categorias, left_on="category_id", right_on="id")
# # 2. Agrupar por nombre de categoría y sacar el promedio
# promedio = df_completo.groupby("name")["price"].mean().reset_index()

#okei me podrias explicar paso a paso como funciona lo de merge? o mejor dicho cada variable que le pasaste?