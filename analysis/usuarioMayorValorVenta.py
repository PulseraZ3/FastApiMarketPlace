import pandas as pd
import matplotlib.pyplot as plt

publicaciones = pd.read_csv("./data/raw/listings.csv")
perfiles = pd.read_csv("./data/raw/profiles.csv")

usuarioMayor = publicaciones.merge(perfiles, left_on="user_id", right_on="id")
usuarioMayor = usuarioMayor.groupby("user_id")["price"].sum().reset_index(name="total_ventas")
usuarioMayor = usuarioMayor.head(5)
usuarioMayor = usuarioMayor.sort_values(by = "total_ventas",ascending = False)
#ahora quiero que en vez de que me muestre el id del usuario, me muestre el nombre del usuario, para eso hago un merge con el dataframe perfiles
usuarioMayor = usuarioMayor.merge(perfiles, left_on="user_id", right_on="id")


plt.pie(usuarioMayor["total_ventas"], labels=usuarioMayor["username"], autopct='%1.1f%%')
plt.title("Usuarios con mayor valor de venta")
plt.show()


