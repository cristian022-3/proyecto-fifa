"""
Estilos globales de la aplicación FIFA Analytics.
Separados de la lógica para mejor mantenimiento.
"""

CSS_GLOBAL = """
<style>
/* ── ANIMACIONES ──────────────────────────────── */

    /* Contador animado para estadísticas */
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Entrada suave del hero */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Entrada desde izquierda */
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Pulso verde */
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 5px rgba(0,212,94,0.2); }
        50% { box-shadow: 0 0 25px rgba(0,212,94,0.6), 0 0 50px rgba(0,212,94,0.2); }
    }

    /* Rotación del balón */
    @keyframes rotateBall {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Línea de progreso animada */
    @keyframes slideIn {
        from { width: 0; }
        to { width: 100%; }
    }

    /* Partículas flotantes */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.8; }
    }

    @keyframes float2 {
        0%, 100% { transform: translateY(0px) rotate(45deg); opacity: 0.2; }
        50% { transform: translateY(-15px) rotate(225deg); opacity: 0.6; }
    }

    /* Shimmer para cards */
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    /* Typing cursor */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }

    /* ── APLICAR ANIMACIONES ──────────────────────── */

    .hero-section {
        animation: fadeInDown 0.8s ease forwards;
    }

    .hero-badge {
        animation: fadeInLeft 0.6s ease 0.2s both;
    }

    .hero-title {
        animation: fadeInLeft 0.6s ease 0.3s both;
    }

    .hero-subtitle {
        animation: fadeInLeft 0.6s ease 0.4s both;
    }

    .stat-item:nth-child(1) { animation: countUp 0.6s ease 0.5s both; }
    .stat-item:nth-child(2) { animation: countUp 0.6s ease 0.6s both; }
    .stat-item:nth-child(3) { animation: countUp 0.6s ease 0.7s both; }
    .stat-item:nth-child(4) { animation: countUp 0.6s ease 0.8s both; }

    /* Cards con hover shimmer */
    .card {
        background: linear-gradient(
            135deg,
            var(--gris-oscuro) 0%,
            #1a2128 50%,
            var(--gris-oscuro) 100%
        );
        transition: all 0.3s ease;
    }

    .card:hover {
        border-color: rgba(0, 212, 94, 0.4) !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 20px rgba(0,212,94,0.05);
    }

    /* Botón con efecto de onda */
    .stButton > button {
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::after {
        content: '' !important;
        position: absolute !important;
        top: 50% !important; left: 50% !important;
        width: 0 !important; height: 0 !important;
        background: rgba(255,255,255,0.2) !important;
        border-radius: 50% !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.4s, height 0.4s !important;
    }

    .stButton > button:active::after {
        width: 200px !important;
        height: 200px !important;
    }

    /* Resultado de sentimiento con animación */
    .resultado-positivo, .resultado-negativo, .resultado-neutral {
        animation: fadeInDown 0.4s ease forwards;
    }

    .resultado-positivo {
        animation: fadeInDown 0.4s ease, glowPulse 3s ease-in-out infinite;
    }

    /* Tabs con transición */
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease !important;
        position: relative !important;
    }

    .stTabs [data-baseweb="tab"]::after {
        content: '' !important;
        position: absolute !important;
        bottom: 0 !important; left: 50% !important;
        width: 0 !important; height: 3px !important;
        background: var(--verde-fifa) !important;
        transition: all 0.3s ease !important;
        transform: translateX(-50%) !important;
    }

    .stTabs [data-baseweb="tab"]:hover::after {
        width: 100% !important;
    }

    /* Section header con línea animada */
    .section-header {
        animation: fadeInLeft 0.5s ease forwards;
    }

    .section-header::after {
        content: '';
        display: block;
        height: 1px;
        background: linear-gradient(90deg, rgba(0,212,94,0.5), transparent);
        animation: slideIn 0.8s ease 0.3s both;
        margin-top: 1rem;
    }

    /* Métricas con brillo */
    [data-testid="metric-container"] {
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="metric-container"]:hover {
        border-color: rgba(0,212,94,0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }

    [data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important; left: -100% !important;
        width: 100% !important; height: 100% !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(0,212,94,0.05),
            transparent
        ) !important;
        transition: left 0.5s ease !important;
    }

    [data-testid="metric-container"]:hover::before {
        left: 100% !important;
    }

    /* Chat input animado */
    .stChatInput {
        transition: all 0.3s ease !important;
    }

    .stChatInput:focus-within {
        border-color: rgba(0,212,94,0.5) !important;
        box-shadow: 0 0 0 3px rgba(0,212,94,0.1) !important;
    }

    /* Chips de preguntas con hover */
    .question-chip {
        transition: all 0.2s ease !important;
    }

    .question-chip:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,212,94,0.2) !important;
    }

    /* Source tag con pulso */
    .source-tag {
        animation: glowPulse 3s ease-in-out infinite;
    }

    /* Progress bar animada */
    .stProgress > div {
        transition: all 0.3s ease !important;
    }

    /* File uploader con hover */
    [data-testid="stFileUploader"] {
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0,212,94,0.4) !important;
        background: rgba(0,212,94,0.03) !important;
    }

    /* Scrollbar animada */
    ::-webkit-scrollbar-thumb {
        transition: background 0.3s ease !important;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0,212,94,0.6) !important;
    }
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