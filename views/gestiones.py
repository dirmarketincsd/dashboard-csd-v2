import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

# ── Constantes ────────────────────────────────────────────────────────────────
SHEET_ID         = "1-YbA3jOuf33rWKNYk_r2_8sx-GYrGtoNgVRa7AWydL4"
CREDENTIALS_FILE = "credentials.json"
TAB_NAME         = "Gestiones"

ASESORES = ["Daniela", "Evelyn", "Carolina"]
TIPOS    = ["Llamada", "WhatsApp", "Email", "Reunión", "Otro"]
ESTADOS  = ["Contactado", "Interesado", "Cita agendada", "Cerrado", "No contesta", "Descartado"]
SEDES    = ["Madrid", "Barcelona", "Málaga", "Valencia", "Alicante", "Bilbao",
            "Dallas", "Houston", "New Jersey", "Orlando", "Los Angeles"]

# ── Conexión ──────────────────────────────────────────────────────────────────
def conectar_sheet():
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
    except Exception:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID)


# ── Lectura ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cargar_gestiones():
    try:
        sheet = conectar_sheet()
        ws    = sheet.worksheet(TAB_NAME)
        data  = ws.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Fecha", "Asesor", "Sede", "Lead", "Tipo", "Estado", "Notas"])
        df = pd.DataFrame(data)
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        return df
    except Exception as e:
        st.error(f"Error cargando gestiones: {e}")
        return pd.DataFrame()


# ── Escritura ─────────────────────────────────────────────────────────────────
def registrar_gestion(fecha, asesor, sede, lead, tipo, estado, notas):
    try:
        sheet = conectar_sheet()
        ws    = sheet.worksheet(TAB_NAME)
        ws.append_row([
            fecha.strftime("%Y-%m-%d"),
            asesor, sede, lead, tipo, estado, notas
        ])
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al registrar: {e}")
        return False


# ── Vista principal ───────────────────────────────────────────────────────────
def render():
    st.markdown("## 📋 Gestiones")
    st.markdown("Registro y seguimiento de gestiones del equipo comercial.")

    # ── Formulario de registro ─────────────────────────────────────────────
    with st.expander("➕ Registrar nueva gestión", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha  = st.date_input("Fecha", value=datetime.today())
            asesor = st.selectbox("Asesor", ASESORES)
        with col2:
            sede  = st.selectbox("Sede", SEDES)
            tipo  = st.selectbox("Tipo de gestión", TIPOS)
        with col3:
            estado = st.selectbox("Estado del lead", ESTADOS)
            lead   = st.text_input("Nombre del lead")

        notas = st.text_area("Notas", placeholder="Detalles de la gestión...")

        if st.button("💾 Guardar gestión", use_container_width=True):
            if not lead.strip():
                st.warning("Ingresa el nombre del lead.")
            else:
                ok = registrar_gestion(fecha, asesor, sede, lead.strip(), tipo, estado, notas)
                if ok:
                    st.success("✅ Gestión registrada correctamente.")

    st.markdown("---")

    # ── Filtros ────────────────────────────────────────────────────────────
    df = cargar_gestiones()

    if df.empty:
        st.info("No hay gestiones registradas aún.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_asesor = st.multiselect("Asesor", options=df["Asesor"].unique().tolist(), default=[])
    with col2:
        filtro_sede = st.multiselect("Sede", options=df["Sede"].unique().tolist(), default=[])
    with col3:
        filtro_estado = st.multiselect("Estado", options=df["Estado"].unique().tolist(), default=[])

    df_filtered = df.copy()
    if filtro_asesor:
        df_filtered = df_filtered[df_filtered["Asesor"].isin(filtro_asesor)]
    if filtro_sede:
        df_filtered = df_filtered[df_filtered["Sede"].isin(filtro_sede)]
    if filtro_estado:
        df_filtered = df_filtered[df_filtered["Estado"].isin(filtro_estado)]

    # ── KPIs rápidos ───────────────────────────────────────────────────────
    total      = len(df_filtered)
    cerradas   = len(df_filtered[df_filtered["Estado"] == "Cerrado"])
    agendadas  = len(df_filtered[df_filtered["Estado"] == "Cita agendada"])
    tasa_cierre = round((cerradas / total * 100), 1) if total > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total gestiones", total)
    k2.metric("Cerrados", cerradas)
    k3.metric("Citas agendadas", agendadas)
    k4.metric("Tasa de cierre", f"{tasa_cierre}%")

    st.markdown("---")

    # ── Tabla ──────────────────────────────────────────────────────────────
    st.markdown("### 📄 Historial de gestiones")
    st.dataframe(
        df_filtered.sort_values("Fecha", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400,
    )