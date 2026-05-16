import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Configuración página
st.set_page_config(
    page_title="Customer Risk & Sales Dashboard",
    layout="wide"
)

# Conexión DB
conn = sqlite3.connect("business.db")

# Leer datos
df = pd.read_sql_query("""
SELECT clientes.nombre, ventas.producto, ventas.monto
FROM ventas
JOIN clientes
ON ventas.cliente_id = clientes.id
""", conn)

# KPIs
ventas_totales = df["monto"].sum()
clientes_totales = df["nombre"].nunique()
mejor_cliente = df.groupby("nombre")["monto"].sum().idxmax()
promedio = df["monto"].mean()

# Título
st.title("📊 Customer Risk & Sales Dashboard")

# KPIs visuales
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Ventas Totales", f"${ventas_totales:,.0f}")
col2.metric("👥 Clientes", clientes_totales)
col3.metric("🏆 Mejor Cliente", mejor_cliente)
col4.metric("📈 Promedio", f"${promedio:,.0f}")

st.divider()

# Tabla
st.subheader("📋 Datos de Ventas")
st.dataframe(df, use_container_width=True)

# Gráfico
st.subheader("📈 Ventas por Cliente")

ventas_cliente = df.groupby("nombre")["monto"].sum()

fig, ax = plt.subplots(figsize=(8,4))
ventas_cliente.plot(kind="bar", ax=ax)

plt.xticks(rotation=0)

st.pyplot(fig)