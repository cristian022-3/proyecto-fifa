"""
Gestor del Analizador de Sentimiento — Lógica de negocio separada.
"""
import streamlit as st
import pandas as pd
from src.sentimiento.analizador import AnalizadorSentimiento


@st.cache_resource
def cargar_analizador() -> AnalizadorSentimiento:
    """Carga el analizador una sola vez y lo mantiene en caché."""
    return AnalizadorSentimiento()


def inicializar_analizador():
    """Inicializa el analizador en la sesión."""
    if "analizador" not in st.session_state:
        st.session_state.analizador = cargar_analizador()


def analizar_comentario(texto: str) -> dict:
    """
    Analiza el sentimiento de un comentario individual.
    
    Returns:
        dict con etiqueta, confianza y probabilidades
    """
    inicializar_analizador()
    return st.session_state.analizador.analizar(texto)


def analizar_dataframe(df: pd.DataFrame, columna: str = "texto") -> pd.DataFrame:
    """
    Analiza el sentimiento de todos los comentarios en un DataFrame.
    
    Returns:
        DataFrame con columna 'sentimiento' agregada
    """
    inicializar_analizador()
    resultados = []
    for texto in df[columna].tolist():
        resultado = st.session_state.analizador.analizar(str(texto))
        resultados.append(resultado["etiqueta"])
    df = df.copy()
    df["sentimiento"] = resultados
    return df


def calcular_estadisticas(df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas del análisis de sentimiento.
    
    Returns:
        dict con conteos y porcentajes por clase
    """
    total = len(df)
    pos = (df["sentimiento"] == "positivo").sum()
    neg = (df["sentimiento"] == "negativo").sum()
    neu = (df["sentimiento"] == "neutral").sum()

    return {
        "total": total,
        "positivo": {"count": pos, "pct": pos/total*100},
        "negativo": {"count": neg, "pct": neg/total*100},
        "neutral": {"count": neu, "pct": neu/total*100}
    }