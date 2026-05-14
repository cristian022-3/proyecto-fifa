"""
Vista del Chatbot — Solo interfaz de usuario.
"""
import streamlit as st
from src.core.gestor_chatbot import (
    inicializar_sesion,
    procesar_pregunta,
    limpiar_historial,
    agregar_mensaje,
    obtener_historial
)


def render_info_cards():
    """Renderiza las tarjetas de información del sistema."""
    st.markdown("""
    <div class="card" style="margin-top:4rem;">
        <p class="card-title">Sistema RAG</p>
        <p class="card-subtitle">Retrieval Augmented Generation</p>
        <p style="font-size:0.8rem; color:rgba(240,244,248,0.5); margin-top:0.8rem; line-height:1.6;">
            El chatbot consulta el reglamento oficial antes de responder, 
            garantizando precisión factual.
        </p>
    </div>
    <div class="card">
        <p class="card-title">Llama 3.1 8B</p>
        <p class="card-subtitle">Modelo de lenguaje via Groq</p>
        <p style="font-size:0.8rem; color:rgba(240,244,248,0.5); margin-top:0.8rem; line-height:1.6;">
            8 mil millones de parámetros. Respuesta en 1-3 segundos 
            con streaming visual.
        </p>
    </div>
    <div class="card">
        <p class="card-title">113 Chunks</p>
        <p class="card-subtitle">Fragmentos indexados con FAISS</p>
        <p style="font-size:0.8rem; color:rgba(240,244,248,0.5); margin-top:0.8rem; line-height:1.6;">
            El reglamento completo está vectorizado para búsqueda 
            semántica instantánea.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_historial():
    """Renderiza el historial de mensajes."""
    for mensaje in obtener_historial():
        with st.chat_message(mensaje["rol"]):
            st.write(mensaje["contenido"])
            if mensaje.get("fuente"):
                with st.expander("📖 Fragmento del reglamento"):
                    st.markdown(
                        '<div class="source-tag">📄 Reglamento IFAB 2025/26</div>',
                        unsafe_allow_html=True
                    )
                    st.caption(mensaje["fuente"])


def render_chatbot():
    """Renderiza la vista completa del chatbot."""
    inicializar_sesion()

    col_chat, col_info = st.columns([3, 1])

    with col_chat:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">💬</div>
            <div>
                <p class="section-title">Asistente Reglamentario</p>
                <p class="section-desc">
                    Basado en Reglas de Juego IFAB 2025/26 · Llama 3.1 8B
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Preguntas sugeridas
        st.markdown("""
        <p style="font-size:0.75rem; color:rgba(240,244,248,0.35); 
           text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
            Preguntas frecuentes
        </p>
        <div class="suggested-questions">
            <span class="question-chip">⏱ Duración del partido</span>
            <span class="question-chip">🚩 Fuera de juego</span>
            <span class="question-chip">🥅 Tiro penal</span>
            <span class="question-chip">🟥 Tarjeta roja</span>
            <span class="question-chip">📺 VAR</span>
            <span class="question-chip">🔄 Sustituciones</span>
        </div>
        """, unsafe_allow_html=True)

        # Historial
        render_historial()

        # Input
        pregunta = st.chat_input("Consulta sobre el reglamento FIFA...")

        if pregunta:
            agregar_mensaje("user", pregunta)
            with st.chat_message("user"):
                st.write(pregunta)

            with st.chat_message("assistant"):
                contenedor = st.empty()
                respuesta_completa = ""
                for fragmento in st.session_state.chatbot.responder_stream(pregunta):
                    respuesta_completa += fragmento
                    contenedor.write(respuesta_completa)

                fuente = st.session_state.chatbot.obtener_contexto_usado(pregunta)
                with st.expander("📖 Fragmento del reglamento"):
                    st.markdown(
                        '<div class="source-tag">📄 Reglamento IFAB 2025/26</div>',
                        unsafe_allow_html=True
                    )
                    st.caption(fuente)

            agregar_mensaje("assistant", respuesta_completa, fuente)

        if st.button("🗑 Limpiar conversación"):
            limpiar_historial()
            st.rerun()

    with col_info:
        render_info_cards()