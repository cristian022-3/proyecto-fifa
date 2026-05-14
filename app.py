"""
FIFA Analytics — Punto de entrada principal.
Solo configuración e importación de vistas.
"""
import streamlit as st
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(".")

from views.vista_chatbot import render_chatbot
from views.vista_sentimiento import render_sentimiento
from views.vista_dashboard import render_dashboard

# ── Configuración ──────────────────────────────────────────
st.set_page_config(
    page_title="FIFA Analytics — IA Deportiva",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilos ────────────────────────────────────────────────
from styles.estilos import CSS_GLOBAL
st.markdown(CSS_GLOBAL, unsafe_allow_html=True)

# ── Hero Section ───────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">⚡ Sistema IA Deportiva · IFAB 2025/26</div>
    <h1 class="hero-title">
        FIFA
        <span>Analytics</span>
    </h1>
    <p class="hero-subtitle">
        Análisis de sentimiento en tiempo real · Asistente reglamentario oficial
    </p>
    <div class="hero-stats">
        <div class="stat-item">
            <span class="stat-number">81%</span>
            <span class="stat-label">Precisión F1</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">3.6K</span>
            <span class="stat-label">Datos entrenamiento</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">113</span>
            <span class="stat-label">Chunks reglamento</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">17</span>
            <span class="stat-label">Reglas FIFA</span>
        </div>
    </div>
</div>
<div class="warning-banner">
    ⚠️ Sistema experimental — Las clasificaciones y respuestas no constituyen fuentes oficiales
</div>
""", unsafe_allow_html=True)

# ── Navegación ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "⚽  Chatbot Reglamentario",
    "🎭  Análisis de Sentimiento",
    "📊  Dashboard de Tendencias"
])

with tab1:
    render_chatbot()

with tab2:
    render_sentimiento()

with tab3:
    render_dashboard()