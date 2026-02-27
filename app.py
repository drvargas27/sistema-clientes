import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("📋 Sistema de Gestión de Clientes - Centro Estético")

# ------------------- CONEXIÓN BASE DE DATOS -------------------
conn = sqlite3.connect("clientes.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    telefono TEXT,
    fecha_cumple TEXT,
    fecha_inicio TEXT,
    fecha_procedimiento TEXT,
    tipo_servicio TEXT,
    variacion TEXT,
    proxima_cita TEXT,
    notas TEXT
)
""")
conn.commit()

# ------------------- MENÚ LATERAL -------------------
menu = st.sidebar.radio("Menú", ["➕ Agregar Cliente", "📋 Ver Clientes", "🎂 Cumpleaños del Mes", "🔔 Servicios Hoy"])

# ------------------- AGREGAR CLIENTE -------------------
if menu == "➕ Agregar Cliente":
    st.subheader("Nuevo Cliente")
    
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono")
    fecha_cumple = st.date_input("Fecha de cumpleaños")
    fecha_inicio = st.date_input("Fecha primera visita")
    fecha_procedimiento = st.date_input("Fecha del procedimiento")
    tipo_servicio = st.selectbox("Tipo de servicio", ["Depilación", "Cejas", "Pestañas", "Micropigmentación", "Otros"])
    variacion = st.text_input("Variación específica del servicio")
    proxima_cita = st.date_input("Próxima cita")
    notas = st.text_area("Notas adicionales")
    
    if st.button("Guardar Cliente"):
        c.execute("""
            INSERT INTO clientes 
            (nombre, telefono, fecha_cumple, fecha_inicio, fecha_procedimiento, tipo_servicio, variacion, proxima_cita, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, telefono, fecha_cumple, fecha_inicio, fecha_procedimiento, tipo_servicio, variacion, proxima_cita, notas))
        conn.commit()
        st.success("✅ Cliente guardado correctamente")

# ------------------- VER CLIENTES -------------------
elif menu == "📋 Ver Clientes":
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df.empty:
        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
        df["Años como cliente"] = (datetime.now() - df["fecha_inicio"]).dt.days // 365
        df["fecha_procedimiento"] = pd.to_datetime(df["fecha_procedimiento"])
        df["proxima_cita"] = pd.to_datetime(df["proxima_cita"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay clientes registrados")

# ------------------- CUMPLEAÑOS DEL MES -------------------
elif menu == "🎂 Cumpleaños del Mes":
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df.empty:
        df["fecha_cumple"] = pd.to_datetime(df["fecha_cumple"])
        mes_actual = datetime.now().month
        cumple_mes = df[df["fecha_cumple"].dt.month == mes_actual]
        st.dataframe(cumple_mes, use_container_width=True)
    else:
        st.info("No hay datos")

# ------------------- SERVICIOS DEL DÍA -------------------
elif menu == "🔔 Servicios Hoy":
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    if not df.empty:
        df["fecha_procedimiento"] = pd.to_datetime(df["fecha_procedimiento"])
        hoy = datetime.now().date()
        servicios_hoy = df[df["fecha_procedimiento"].dt.date == hoy]
        if not servicios_hoy.empty:
            st.subheader("Servicios programados para hoy")
            for i, row in servicios_hoy.iterrows():
                st.write(f"• {row['nombre']} → {row['tipo_servicio']} ({row['variacion']}) a las {row['fecha_procedimiento'].strftime('%d/%m/%Y')}")
        else:
            st.info("No hay servicios programados para hoy")
    else:
        st.info("No hay clientes registrados")