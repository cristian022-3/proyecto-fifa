"""
Estilos globales de la aplicación FIFA Analytics.
Separados de la lógica para mejor mantenimiento.
"""

CSS_GLOBAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --verde-fifa: #00D45E;
        --negro: #080C0F;
        --gris-oscuro: #0F1518;
        --gris-medio: #1A2128;
        --blanco: #F0F4F8;
        --acento: #FFD700;
        --rojo: #FF3B3B;
        --azul: #00A8FF;
    }

    .stApp { background: var(--negro); font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    .hero-section {
        background: linear-gradient(135deg, #080C0F 0%, #0F1F15 50%, #080C0F 100%);
        padding: 3rem 4rem 2rem;
        border-bottom: 1px solid rgba(0, 212, 94, 0.2);
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(0,212,94,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(0, 212, 94, 0.1);
        border: 1px solid rgba(0, 212, 94, 0.3);
        border-radius: 20px; padding: 4px 14px;
        font-size: 0.7rem; font-weight: 600;
        color: var(--verde-fifa);
        text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 5rem; line-height: 0.9;
        color: var(--blanco); margin: 0; letter-spacing: 2px;
    }
    .hero-title span { color: var(--verde-fifa); display: block; }
    .hero-subtitle {
        font-size: 1rem; color: rgba(240,244,248,0.5);
        margin-top: 1rem; font-weight: 300; letter-spacing: 0.5px;
    }
    .hero-stats { display: flex; gap: 3rem; margin-top: 2rem; }
    .stat-item { display: flex; flex-direction: column; }
    .stat-number {
        font-family: 'Bebas Neue', cursive;
        font-size: 2.5rem; color: var(--verde-fifa); line-height: 1;
    }
    .stat-label {
        font-size: 0.7rem; color: rgba(240,244,248,0.4);
        text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;
    }
    .warning-banner {
        background: rgba(255, 215, 0, 0.05);
        border-left: 3px solid var(--acento);
        padding: 0.6rem 1rem; margin: 1.5rem 4rem 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.78rem; color: rgba(240,244,248,0.5);
    }
    .stTabs [data-baseweb="tab-list"] {
        background: transparent; border-bottom: none; gap: 0; padding: 0 3rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border: none;
        border-bottom: 3px solid transparent;
        color: rgba(240,244,248,0.4);
        font-family: 'Inter', sans-serif; font-weight: 500;
        font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px;
        padding: 1.2rem 2rem; transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--verde-fifa); background: rgba(0, 212, 94, 0.05);
    }
    .stTabs [aria-selected="true"] {
        color: var(--verde-fifa) !important;
        border-bottom: 3px solid var(--verde-fifa) !important;
        background: rgba(0, 212, 94, 0.05) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--negro); padding: 2rem 3rem;
    }
    .card {
        background: var(--gris-oscuro);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
        transition: border-color 0.2s;
    }
    .card:hover { border-color: rgba(0, 212, 94, 0.2); }
    .card-title {
        font-family: 'Bebas Neue', cursive; font-size: 1.3rem;
        color: var(--blanco); letter-spacing: 1px; margin-bottom: 0.3rem;
    }
    .card-subtitle {
        font-size: 0.75rem; color: rgba(240,244,248,0.35);
        text-transform: uppercase; letter-spacing: 1px;
    }
    .resultado-positivo {
        background: linear-gradient(135deg, rgba(0,212,94,0.1), rgba(0,212,94,0.05));
        border: 1px solid rgba(0,212,94,0.3);
        border-radius: 12px; padding: 1.5rem; text-align: center;
    }
    .resultado-negativo {
        background: linear-gradient(135deg, rgba(255,59,59,0.1), rgba(255,59,59,0.05));
        border: 1px solid rgba(255,59,59,0.3);
        border-radius: 12px; padding: 1.5rem; text-align: center;
    }
    .resultado-neutral {
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 12px; padding: 1.5rem; text-align: center;
    }
    .sentimiento-label {
        font-family: 'Bebas Neue', cursive;
        font-size: 3rem; line-height: 1; letter-spacing: 3px;
    }
    .confianza-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem; opacity: 0.6; margin-top: 0.3rem;
    }
    .section-header {
        display: flex; align-items: center; gap: 1rem;
        margin-bottom: 1.5rem; padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .section-icon {
        width: 40px; height: 40px;
        background: rgba(0,212,94,0.1);
        border: 1px solid rgba(0,212,94,0.2);
        border-radius: 10px;
        display: flex; align-items: center;
        justify-content: center; font-size: 1.2rem;
    }
    .section-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 1.8rem; color: var(--blanco);
        letter-spacing: 2px; margin: 0;
    }
    .section-desc {
        font-size: 0.75rem; color: rgba(240,244,248,0.35);
        text-transform: uppercase; letter-spacing: 1px; margin: 0;
    }
    .source-tag {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(0,168,255,0.08);
        border: 1px solid rgba(0,168,255,0.2);
        border-radius: 6px; padding: 3px 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; color: var(--azul); margin-bottom: 0.5rem;
    }
    .suggested-questions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
    .question-chip {
        background: rgba(0,212,94,0.08);
        border: 1px solid rgba(0,212,94,0.2);
        border-radius: 20px; padding: 4px 12px;
        font-size: 0.75rem; color: rgba(240,244,248,0.6);
        cursor: pointer; transition: all 0.2s;
    }
    .question-chip:hover { background: rgba(0,212,94,0.15); color: var(--verde-fifa); }
    .stButton > button {
        background: var(--verde-fifa) !important;
        color: var(--negro) !important; border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 0.85rem !important;
        text-transform: uppercase !important; letter-spacing: 1px !important;
        padding: 0.6rem 1.5rem !important; transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #00FF72 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(0,212,94,0.3) !important;
    }
    .stTextArea textarea {
        background: var(--gris-medio) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important; color: var(--blanco) !important;
        font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(0,212,94,0.4) !important;
        box-shadow: 0 0 0 2px rgba(0,212,94,0.1) !important;
    }
    .stRadio label { color: rgba(240,244,248,0.7) !important; font-size: 0.85rem !important; }
    [data-testid="metric-container"] {
        background: var(--gris-medio) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important; padding: 1rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--verde-fifa) !important;
        font-family: 'Bebas Neue', cursive !important; font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: rgba(240,244,248,0.4) !important;
        font-size: 0.7rem !important; text-transform: uppercase !important; letter-spacing: 1px !important;
    }
    .stProgress > div > div { background: var(--verde-fifa) !important; }
    .streamlit-expanderHeader {
        background: var(--gris-medio) !important; border-radius: 8px !important;
        color: rgba(240,244,248,0.5) !important; font-size: 0.8rem !important;
    }
    [data-testid="stFileUploader"] {
        background: var(--gris-medio) !important;
        border: 2px dashed rgba(0,212,94,0.2) !important; border-radius: 12px !important;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--negro); }
    ::-webkit-scrollbar-thumb { background: rgba(0,212,94,0.3); border-radius: 3px; }
</style>
"""