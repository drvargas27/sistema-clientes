import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

conn = sqlite3.connect("clientes.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    telefono TEXT,
    fecha_cumple TEXT,
    fecha_inicio TEXT
)
""")
conn.commit()

st.title("📋 Sistema de Gestión de Clientes")

menu = st.sidebar.radio("Menú", ["➕ Agregar Cliente", "📋 Ver Clientes", "🎂 Cumpleaños del Mes"])

if menu == "➕ Agregar Cliente":
    st.subheader("Nuevo Cliente")

    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono")
    fecha_cumple = st.date_input("Fecha de cumpleaños")
    fecha_inicio = st.date_input("Fecha primera visita")

    if st.button("Guardar Cliente"):
        c.execute("INSERT INTO clientes (nombre, telefono, fecha_cumple, fecha_inicio) VALUES (?, ?, ?, ?)",
                  (nombre, telefono, fecha_cumple, fecha_inicio))
        conn.commit()
        st.success("✅ Cliente guardado correctamente")

if menu == "📋 Ver Clientes":
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df.empty:
        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
        df["Años como cliente"] = (datetime.now() - df["fecha_inicio"]).dt.days // 365
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay clientes registrados")

if menu == "🎂 Cumpleaños del Mes":
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df.empty:
        df["fecha_cumple"] = pd.to_datetime(df["fecha_cumple"])
        mes_actual = datetime.now().month
        cumple_mes = df[df["fecha_cumple"].dt.month == mes_actual]
        st.dataframe(cumple_mes, use_container_width=True)
    else:
        st.info("No hay datos")