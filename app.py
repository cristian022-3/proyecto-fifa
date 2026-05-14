import streamlit as st
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()
sys.path.append(".")

# ── Configuración de la página ─────────────────────────────
st.set_page_config(
    page_title="Sistema FIFA — Análisis y Chatbot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .titulo-principal {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a472a;
        text-align: center;
        padding: 1rem;
    }
    .subtitulo {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metrica-card {
        background: #f0f7f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #1a472a;
    }
    .positivo { color: #2e7d32; font-weight: bold; font-size: 1.3rem; }
    .negativo { color: #c62828; font-weight: bold; font-size: 1.3rem; }
    .neutral  { color: #f57f17; font-weight: bold; font-size: 1.3rem; }
    .advertencia {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 0.8rem;
        border-radius: 5px;
        font-size: 0.9rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# ── Cargar modelos con caché ───────────────────────────────
@st.cache_resource
def cargar_analizador():
    from src.sentimiento.analizador import AnalizadorSentimiento
    return AnalizadorSentimiento()

@st.cache_resource
def cargar_chatbot():
    from src.chatbot.chatbot import ChatbotFIFA
    return ChatbotFIFA()

# ── Header principal ───────────────────────────────────────
st.markdown(
    '<div class="titulo-principal">⚽ Sistema FIFA — Análisis y Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitulo">Análisis de sentimiento de aficionados · Chatbot reglamentario oficial</div>',
    unsafe_allow_html=True
)
st.markdown("""
<div class="advertencia">
⚠️ Este sistema es experimental. Las clasificaciones de sentimiento y respuestas 
reglamentarias no constituyen fuentes oficiales y pueden contener errores.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Navegación por pestañas ────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "💬 Chatbot Reglamentario",
    "🎭 Análisis de Sentimiento",
    "📊 Dashboard de Tendencias"
])

# ══════════════════════════════════════════════════════════
# PESTAÑA 1 — CHATBOT
# ══════════════════════════════════════════════════════════
with tab1:
    st.header("💬 Asistente Reglamentario FIFA")
    st.caption("Consulta cualquier duda sobre las Reglas de Juego IFAB 2025/26")

    # Inicializar historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    if "chatbot" not in st.session_state:
        with st.spinner("Cargando asistente..."):
            st.session_state.chatbot = cargar_chatbot()

    # Mostrar historial
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["rol"]):
            st.write(mensaje["contenido"])
            if "fuente" in mensaje and mensaje["fuente"]:
                with st.expander("📖 Fragmento del reglamento usado"):
                    st.caption(mensaje["fuente"])

    # Input del usuario
    pregunta = st.chat_input("Escribe tu pregunta sobre el reglamento FIFA...")

    if pregunta:
        # Mostrar pregunta
        with st.chat_message("user"):
            st.write(pregunta)
        st.session_state.mensajes.append({
            "rol": "user",
            "contenido": pregunta
        })

        # Generar respuesta con streaming
        with st.chat_message("assistant"):
            contenedor = st.empty()
            respuesta_completa = ""

            for fragmento in st.session_state.chatbot.responder_stream(pregunta):
                respuesta_completa += fragmento
                contenedor.write(respuesta_completa)

            # Mostrar fuente
            fuente = st.session_state.chatbot.obtener_contexto_usado(pregunta)
            with st.expander("📖 Fragmento del reglamento usado"):
                st.caption(fuente)

        st.session_state.mensajes.append({
            "rol": "assistant",
            "contenido": respuesta_completa,
            "fuente": fuente
        })

    # Botón limpiar chat
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

# ══════════════════════════════════════════════════════════
# PESTAÑA 2 — ANÁLISIS DE SENTIMIENTO
# ══════════════════════════════════════════════════════════
with tab2:
    st.header("🎭 Análisis de Sentimiento")

    if "analizador" not in st.session_state:
        with st.spinner("Cargando modelo de sentimiento..."):
            st.session_state.analizador = cargar_analizador()

    modo = st.radio(
        "Modo de análisis:",
        ["Comentario individual", "Análisis por lotes (CSV)"],
        horizontal=True,
        key="modo_analisis"
    )

    if modo == "Comentario individual":
        st.subheader("Analizar un comentario")
        comentario = st.text_area(
            "Escribe el comentario a analizar:",
            placeholder="Ej: ¡Golazo histórico, campeones del mundo!",
            height=100,
            key="input_sentimiento"
        )

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            analizar_btn = st.button(
                "🔍 Analizar sentimiento",
                type="primary",
                key="btn_analizar"
            )

        if analizar_btn:
            if comentario.strip():
                with st.spinner("Analizando..."):
                    resultado = st.session_state.analizador.analizar(comentario)

                col1, col2, col3 = st.columns(3)

                etiqueta = resultado["etiqueta"]
                confianza = resultado["confianza"] * 100
                probs = resultado["probabilidades"]

                with col1:
                    if etiqueta == "positivo":
                        st.markdown('<div class="positivo">😊 POSITIVO</div>', unsafe_allow_html=True)
                    elif etiqueta == "negativo":
                        st.markdown('<div class="negativo">😠 NEGATIVO</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="neutral">😐 NEUTRAL</div>', unsafe_allow_html=True)
                    st.caption(f"Confianza: {confianza:.1f}%")

                with col2:
                    fig = go.Figure(go.Bar(
                        x=["Negativo", "Neutral", "Positivo"],
                        y=[probs["negativo"]*100, probs["neutral"]*100, probs["positivo"]*100],
                        marker_color=["#c62828", "#f57f17", "#2e7d32"]
                    ))
                    fig.update_layout(
                        title="Probabilidades (%)",
                        height=250,
                        showlegend=False,
                        margin=dict(t=40, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col3:
                    st.metric("Negativo", f"{probs['negativo']*100:.1f}%")
                    st.metric("Neutral", f"{probs['neutral']*100:.1f}%")
                    st.metric("Positivo", f"{probs['positivo']*100:.1f}%")
            else:
                st.warning("Por favor escribe un comentario.")

    else:
        st.subheader("Análisis por lotes")
        st.caption("Sube un CSV con una columna llamada 'texto'")

        archivo = st.file_uploader("Cargar archivo CSV", type=["csv"])

        if archivo:
            df = pd.read_csv(archivo)

            if "texto" not in df.columns:
                st.error("El CSV debe tener una columna llamada 'texto'")
            else:
                st.info(f"Archivo cargado: {len(df)} comentarios")

                if st.button("🔍 Analizar todos", type="primary"):
                    barra = st.progress(0)
                    resultados = []

                    for i, texto in enumerate(df["texto"].tolist()):
                        resultado = st.session_state.analizador.analizar(str(texto))
                        resultados.append(resultado["etiqueta"])
                        barra.progress((i + 1) / len(df))

                    df["sentimiento"] = resultados

                    conteo = df["sentimiento"].value_counts()
                    fig = px.pie(
                        values=conteo.values,
                        names=conteo.index,
                        title="Distribución de Sentimientos",
                        color=conteo.index,
                        color_discrete_map={
                            "positivo": "#2e7d32",
                            "negativo": "#c62828",
                            "neutral": "#f57f17"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.dataframe(df[["texto", "sentimiento"]], use_container_width=True)
                    st.success(f"✅ {len(df)} comentarios analizados")
# ══════════════════════════════════════════════════════════
# PESTAÑA 3 — DASHBOARD
# ══════════════════════════════════════════════════════════
with tab3:
    st.header("📊 Dashboard de Tendencias")
    st.caption("Visualiza la evolución del sentimiento durante un partido")

    archivo_dash = st.file_uploader(
        "Cargar CSV con comentarios del partido",
        type=["csv"],
        key="dashboard"
    )

    if archivo_dash:
        df_dash = pd.read_csv(archivo_dash)

        if "texto" not in df_dash.columns:
            st.error("El CSV debe tener una columna llamada 'texto'")
        else:
            if "analizador" not in st.session_state:
                st.session_state.analizador = cargar_analizador()

            if st.button("📊 Generar dashboard", type="primary"):
                barra = st.progress(0)
                sentimientos = []

                for i, texto in enumerate(df_dash["texto"].tolist()):
                    resultado = st.session_state.analizador.analizar(str(texto))
                    sentimientos.append(resultado["etiqueta"])
                    barra.progress((i + 1) / len(df_dash))

                df_dash["sentimiento"] = sentimientos

                col1, col2, col3 = st.columns(3)
                total = len(df_dash)
                pos = (df_dash["sentimiento"] == "positivo").sum()
                neg = (df_dash["sentimiento"] == "negativo").sum()
                neu = (df_dash["sentimiento"] == "neutral").sum()

                with col1:
                    st.metric("😊 Positivos", f"{pos}", f"{pos/total*100:.1f}%")
                with col2:
                    st.metric("😠 Negativos", f"{neg}", f"{neg/total*100:.1f}%")
                with col3:
                    st.metric("😐 Neutrales", f"{neu}", f"{neu/total*100:.1f}%")

                # Gráfico de evolución
                df_dash["indice"] = range(len(df_dash))
                df_dash["valor"] = df_dash["sentimiento"].map({
                    "positivo": 1, "neutral": 0, "negativo": -1
                })
                df_dash["promedio_movil"] = df_dash["valor"].rolling(
                    window=10, min_periods=1
                ).mean()

                fig = px.line(
                    df_dash,
                    x="indice",
                    y="promedio_movil",
                    title="Evolución del Sentimiento durante el Partido",
                    labels={"indice": "Comentario #", "promedio_movil": "Sentimiento"},
                    color_discrete_sequence=["#1a472a"]
                )
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                # Gráfico de torta
                fig2 = px.pie(
                    values=[pos, neg, neu],
                    names=["Positivo", "Negativo", "Neutral"],
                    title="Distribución Total",
                    color_discrete_sequence=["#2e7d32", "#c62828", "#f57f17"]
                )
                st.plotly_chart(fig2, use_container_width=True)

                st.dataframe(
                    df_dash[["texto", "sentimiento"]],
                    use_container_width=True
                )
    else:
        st.info("Carga un archivo CSV con comentarios para generar el dashboard.")
        st.caption("Puedes usar el archivo data/raw/dataset_youtube_etiquetado.csv como ejemplo.")