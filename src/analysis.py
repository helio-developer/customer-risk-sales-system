import sqlite3
from pathlib import Path

DB_PATH = Path("business.db")


def conectar():
    return sqlite3.connect(DB_PATH)


def ventas_por_cliente():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.nombre, SUM(v.monto) as total_compras
        FROM clientes c
        JOIN ventas v ON c.id = v.cliente_id
        GROUP BY c.nombre
    """)

    resultados = cursor.fetchall()

    print("\n--- Ventas por Cliente ---")
    for r in resultados:
        print(f"{r[0]}: ${r[1]:,.0f}")

    conn.close()


def clientes_riesgosos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre, ingresos, deudas
        FROM clientes
        WHERE deudas > ingresos * 0.4
    """)

    resultados = cursor.fetchall()

    print("\n--- Clientes Riesgosos ---")
    for r in resultados:
        print(f"{r[0]} | Ingresos: {r[1]} | Deudas: {r[2]}")

    conn.close()


def mejor_cliente():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.nombre, SUM(v.monto) as total
        FROM clientes c
        JOIN ventas v ON c.id = v.cliente_id
        GROUP BY c.nombre
        ORDER BY total DESC
        LIMIT 1
    """)

    resultado = cursor.fetchone()

    print("\n--- Mejor Cliente ---")
    print(f"{resultado[0]} con compras de ${resultado[1]:,.0f}")

    conn.close()

def generar_reporte():
    conn = conectar()
    cursor = conn.cursor()

    with open("reports/resumen.txt", "w", encoding="utf-8") as f:

        f.write("REPORTE DE ANALISIS\n")
        f.write("====================\n\n")

        # Mejor cliente
        cursor.execute("""
            SELECT c.nombre, SUM(v.monto) as total
            FROM clientes c
            JOIN ventas v ON c.id = v.cliente_id
            GROUP BY c.nombre
            ORDER BY total DESC
            LIMIT 1
        """)
        mejor = cursor.fetchone()

        f.write(f"Mejor cliente: {mejor[0]} (${mejor[1]:,.0f})\n\n")

        # Clientes riesgosos
        cursor.execute("""
            SELECT nombre, ingresos, deudas
            FROM clientes
            WHERE deudas > ingresos * 0.4
        """)

        riesgos = cursor.fetchall()

        f.write("Clientes riesgosos:\n")
        for r in riesgos:
            f.write(f"- {r[0]} (Deuda: {r[2]})\n")

    conn.close()


if __name__ == "__main__":
    ventas_por_cliente()
    clientes_riesgosos()
    mejor_cliente()
    generar_reporte()


