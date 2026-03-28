import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Dashboard de Clientes y Ventas")

# Conectar a la base de datos
conn = sqlite3.connect("business.db")

# Query
query = """
SELECT c.nombre, SUM(v.monto) as total
FROM clientes c
JOIN ventas v ON c.id = v.cliente_id
GROUP BY c.nombre
"""

df = pd.read_sql_query(query, conn)

# Mostrar tabla
st.subheader("Ventas por Cliente")
st.dataframe(df)

# Gráfico
st.subheader("Gráfico de Ventas")
st.bar_chart(df.set_index("nombre"))


