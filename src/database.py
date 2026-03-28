import sqlite3
from pathlib import Path
import csv

DB_PATH = Path("business.db")
CLIENTES_CSV = Path("data/clientes.csv")
VENTAS_CSV = Path("data/ventas.csv")


def conectar():
    return sqlite3.connect(DB_PATH)


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            ingresos REAL,
            deudas REAL,
            score INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY,
            cliente_id INTEGER,
            producto TEXT,
            categoria TEXT,
            monto REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()


def cargar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    with open(CLIENTES_CSV, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cursor.execute("""
                INSERT INTO clientes (id, nombre, ingresos, deudas, score)
                VALUES (?, ?, ?, ?, ?)
            """, (
                int(fila["id"]),
                fila["nombre"],
                float(fila["ingresos"]),
                float(fila["deudas"]),
                int(fila["score"])
            ))

    conn.commit()
    conn.close()


def cargar_ventas():
    conn = conectar()
    cursor = conn.cursor()

    with open(VENTAS_CSV, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cursor.execute("""
                INSERT INTO ventas (id, cliente_id, producto, categoria, monto)
                VALUES (?, ?, ?, ?, ?)
            """, (
                int(fila["id"]),
                int(fila["cliente_id"]),
                fila["producto"],
                fila["categoria"],
                float(fila["monto"])
            ))

    conn.commit()
    conn.close()


def inicializar():
    crear_tablas()
    cargar_clientes()
    cargar_ventas()


if __name__ == "__main__":
    inicializar()
    print("Base de datos creada correctamente.")
