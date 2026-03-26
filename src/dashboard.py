import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a la base de datos
conn = sqlite3.connect("business.db")

# Consulta SQL
query = """
SELECT c.nombre, SUM(v.monto) as total
FROM clientes c
JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.nombre
"""

df = pd.read_sql_query(query, conn)

# Mostrar datos
print(df)

# Gráfico
plt.bar(df["nombre"], df["total"])
plt.title("Ventas por Cliente")
plt.xlabel("Cliente")
plt.ylabel("Total Compras")

plt.show()
