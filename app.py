import streamlit as st
from config import COLOR_GOLD, COLOR_DARK

st.set_page_config(
    page_title="CSD Dashboard",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo global
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f5;
        border-radius: 8px;
        color: #666;
        padding: 8px 20px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #C9A84C !important;
        color: #fff !important;
        font-weight: 700;
        border: none !important;
    }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3 { color: #C9A84C !important; }
    .stMetric { 
        background-color: #fffbf0; 
        border: 1px solid #C9A84C33;
        border-radius: 10px;
        padding: 12px;
    }
    .stMetricLabel { color: #888 !important; }
    .stMetricValue { color: #C9A84C !important; }
    .stDataFrame { border: 1px solid #e0e0e0; border-radius: 10px; }
    .stButton button {
        background-color: #C9A84C !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .stExpander {
        border: 1px solid #C9A84C44 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stInfo"] {
        background-color: #fffbf0;
        border-left: 4px solid #C9A84C;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Header con logo
import base64

def get_logo_base64():
    try:
        with open("static/Marca de agua 2026.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:70px;">' if logo_b64 else "✦"

st.markdown(f"""
<div style="display:flex; align-items:center; gap:20px; padding:10px 0 20px 0; 
            border-bottom:1px solid #C9A84C33; margin-bottom:20px;">
    {logo_html}
    <div>
        <div style="color:#C9A84C; font-weight:700; font-size:16px;">Dashboard Comercial</div>
        <div style="color:#999; font-size:12px;">Panel de control · Equipo comercial</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Resumen",
    "📣 Campañas Meta",
    "🔻 Embudo CRM",
    "📋 Gestiones",
    "📅 Agenda"
])

with tab1:
    st.info("🔧 Resumen — en construcción")

with tab2:
    st.info("🔧 Campañas Meta — en construcción")

with tab3:
    st.info("🔧 Embudo CRM — en construcción")

with tab4:
    from views.gestiones import render as render_gestiones
    render_gestiones()

with tab5:
    st.info("🔧 Agenda — en construcción")