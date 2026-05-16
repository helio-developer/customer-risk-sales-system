import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Configuración página
st.set_page_config(
    
    page_title="Customer Risk & Sales Dashboard",
    layout="wide"
)

# Sidebar
st.sidebar.title("📌 Panel de Control")
st.sidebar.markdown("Dashboard de análisis de clientes y ventas")



# Conexión DB
conn = sqlite3.connect("business.db")

# Leer datos
df = pd.read_sql_query("""
SELECT clientes.nombre, ventas.producto, ventas.monto
FROM ventas
JOIN clientes
ON ventas.cliente_id = clientes.id
""", conn)

# Filtro de ventas
min_venta = int(df["monto"].min())
max_venta = int(df["monto"].max())

rango_ventas = st.sidebar.slider(
    "💰 Rango de Ventas",
    min_venta,
    max_venta,
    (min_venta, max_venta)
)

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

# Filtro cliente
clientes = df["nombre"].unique()

cliente_seleccionado = st.selectbox(
    "🔎 Selecciona un cliente",
    clientes
)

df_filtrado = df[
    (df["nombre"] == cliente_seleccionado) &
    (df["monto"] >= rango_ventas[0]) &
    (df["monto"] <= rango_ventas[1])
]

st.dataframe(df_filtrado, width='stretch')


# Gráfico
st.subheader("📈 Ventas por Cliente")

ventas_cliente = (
    df_filtrado.groupby("nombre")["monto"]
    .sum()
    .reset_index()
)

fig = px.bar(
    ventas_cliente,
    x="nombre",
    y="monto",
    text_auto=True,
    title="Ventas Totales"
)

st.plotly_chart(fig, width='stretch')

# Pie Chart
st.subheader("🥧 Distribución de Ventas")

fig_pie = px.pie(
    df,
    names="nombre",
    values="monto",
    title="Participación de Clientes"
)

st.plotly_chart(fig_pie, width='stretch')