"""
Gestor del Chatbot FIFA — Lógica de negocio separada de la interfaz.
"""
import streamlit as st
from src.chatbot.chatbot import ChatbotFIFA


@st.cache_resource
def cargar_chatbot() -> ChatbotFIFA:
    """Carga el chatbot una sola vez y lo mantiene en caché."""
    return ChatbotFIFA()


def inicializar_sesion():
    """Inicializa el estado de la sesión del chatbot."""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = cargar_chatbot()


def procesar_pregunta(pregunta: str) -> tuple[str, str]:
    """
    Procesa una pregunta y retorna la respuesta y la fuente.
    
    Returns:
        tuple: (respuesta_completa, fuente_del_reglamento)
    """
    respuesta_completa = ""
    for fragmento in st.session_state.chatbot.responder_stream(pregunta):
        respuesta_completa += fragmento
    fuente = st.session_state.chatbot.obtener_contexto_usado(pregunta)
    return respuesta_completa, fuente


def limpiar_historial():
    """Limpia el historial de conversación."""
    st.session_state.mensajes = []


def agregar_mensaje(rol: str, contenido: str, fuente: str = ""):
    """Agrega un mensaje al historial."""
    st.session_state.mensajes.append({
        "rol": rol,
        "contenido": contenido,
        "fuente": fuente
    })


def obtener_historial() -> list:
    """Retorna el historial de mensajes."""
    return st.session_state.get("mensajes", [])