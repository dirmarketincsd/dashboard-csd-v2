import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import *

def conectar_sheet():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID)

def cargar_gestiones():
    try:
        sh = conectar_sheet()
        hoja = sh.worksheet(SHEET_GESTIONES)
        datos = hoja.get_all_records()
        df = pd.DataFrame(datos)
        if df.empty:
            return df
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error cargando gestiones: {e}")
        return pd.DataFrame()

def render():
    st.markdown("### 📋 Gestiones del Equipo")

    # ── FORMULARIO ────────────────────────────────────────────────────────────
    with st.expander("➕ Registrar nueva gestión", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            responsable = st.selectbox("Responsable", list(ASESORES.keys()))
        with col2:
            pais = st.selectbox("País", ["España", "USA"])
        with col3:
            sede_opciones = SEDES_ESPAÑA if pais == "España" else SEDES_USA
            sede = st.selectbox("Sede", sede_opciones)

        col4, col5, col6 = st.columns(3)
        with col4:
            valoraciones = st.number_input("Valoraciones", min_value=0, max_value=50, value=0)
        with col5:
            depositos = st.number_input("Depósitos", min_value=0, max_value=20, value=0)
        with col6:
            presupuestos = st.number_input("Presupuestos realizados", min_value=0, max_value=20, value=0)

        if st.button("💾 Guardar gestión", type="primary"):
            try:
                sh = conectar_sheet()
                hoja = sh.worksheet(SHEET_GESTIONES)
                ahora = datetime.now()
                dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                fila = [
                    ahora.strftime("%d/%m/%Y"),
                    dias[ahora.weekday()],
                    responsable,
                    pais,
                    sede,
                    valoraciones,
                    depositos,
                    presupuestos
                ]
                hoja.append_row(fila)
                st.success("✅ Gestión registrada correctamente")
                st.rerun()
            except Exception as e:
                st.error(f"Error guardando: {e}")

    # ── DATOS ─────────────────────────────────────────────────────────────────
    df = cargar_gestiones()

    if df.empty:
        st.warning("Sin registros aún.")
        return

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Valoraciones", int(df.get("VALORACIONES REALIZADAS", pd.Series([0])).sum()))
    with col2:
        st.metric("Total Depósitos", int(df.get("DEPOSITOS", pd.Series([0])).sum()))
    with col3:
        st.metric("Total Presupuestos", int(df.get("PRESUPUESTO REALIZADOS", pd.Series([0])).sum()))
    with col4:
        st.metric("Registros totales", len(df))

    # Tabla
    st.dataframe(df, use_container_width=True, hide_index=True)