"""
Vista del Analizador de Sentimiento — Solo interfaz de usuario.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.core.gestor_sentimiento import (
    inicializar_analizador,
    analizar_comentario,
    analizar_dataframe,
    calcular_estadisticas
)


def render_resultado(resultado: dict):
    """Renderiza el resultado del análisis de sentimiento."""
    etiqueta = resultado["etiqueta"]
    confianza = resultado["confianza"] * 100
    probs = resultado["probabilidades"]

    if etiqueta == "positivo":
        emoji, clase, color = "😊", "resultado-positivo", "#00D45E"
    elif etiqueta == "negativo":
        emoji, clase, color = "😠", "resultado-negativo", "#FF3B3B"
    else:
        emoji, clase, color = "😐", "resultado-neutral", "#FFD700"

    st.markdown(f"""
    <div class="{clase}" style="margin-bottom:1rem;">
        <div style="font-size:3rem;">{emoji}</div>
        <div class="sentimiento-label" style="color:{color};">
            {etiqueta.upper()}
        </div>
        <div class="confianza-text">Confianza: {confianza:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    categorias = ["Negativo", "Neutral", "Positivo"]
    valores = [probs["negativo"]*100, probs["neutral"]*100, probs["positivo"]*100]
    colores = ["#FF3B3B", "#FFD700", "#00D45E"]

    for cat, val, col in zip(categorias, valores, colores):
        fig.add_trace(go.Bar(
            x=[cat], y=[val],
            marker_color=col,
            marker_opacity=0.85,
            showlegend=False,
            text=f"{val:.1f}%",
            textposition="outside",
            textfont=dict(
                color="rgba(240,244,248,0.7)",
                size=11,
                family="JetBrains Mono"
            )
        ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=10, l=10, r=10),
        height=200,
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, 120]),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="rgba(240,244,248,0.5)", size=11)
        ),
        bargap=0.4
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_analisis_individual():
    """Renderiza el modo de análisis individual."""
    col_input, col_resultado = st.columns([1, 1])

    with col_input:
        st.markdown("""
        <p style="font-size:0.75rem; color:rgba(240,244,248,0.4); 
           text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
            Comentario a analizar
        </p>
        """, unsafe_allow_html=True)

        comentario = st.text_area(
            "",
            placeholder="Ej: ¡Golazo histórico, campeones del mundo!",
            height=150,
            key="input_sentimiento",
            label_visibility="collapsed"
        )

        st.markdown("""
        <p style="font-size:0.7rem; color:rgba(240,244,248,0.3); margin-top:0.5rem;">
            Ejemplos rápidos:
        </p>
        """, unsafe_allow_html=True)

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            if st.button("😊 Positivo", use_container_width=True):
                st.session_state.ejemplo = "¡Golazo histórico, campeones del mundo!"
        with col_e2:
            if st.button("😠 Negativo", use_container_width=True):
                st.session_state.ejemplo = "Qué robo de árbitro, gol invalidado injustamente"
        with col_e3:
            if st.button("😐 Neutral", use_container_width=True):
                st.session_state.ejemplo = "Colombia tuvo 60% de posesión en el primer tiempo"

        analizar_btn = st.button(
            "🔍 Analizar sentimiento",
            type="primary",
            use_container_width=True,
            key="btn_analizar"
        )

    with col_resultado:
        texto = comentario or st.session_state.get("ejemplo", "")

        if analizar_btn and texto.strip():
            with st.spinner("Analizando..."):
                resultado = analizar_comentario(texto)
            render_resultado(resultado)
        else:
            st.markdown("""
            <div style="height:300px; display:flex; align-items:center; 
                justify-content:center; flex-direction:column; gap:1rem; opacity:0.3;">
                <div style="font-size:4rem;">🎭</div>
                <p style="font-size:0.85rem; color:rgba(240,244,248,0.5);">
                    Escribe un comentario para analizar
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_analisis_lotes():
    """Renderiza el modo de análisis por lotes."""
    st.markdown("""
    <p style="font-size:0.75rem; color:rgba(240,244,248,0.4); 
       text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
        Cargar archivo CSV con columna "texto"
    </p>
    """, unsafe_allow_html=True)

    archivo = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if archivo:
        df = pd.read_csv(archivo)

        if "texto" not in df.columns:
            st.error("El CSV debe tener una columna llamada 'texto'")
            return

        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.metric("Comentarios cargados", len(df))
        with col_i2:
            st.metric("Columnas detectadas", len(df.columns))

        if st.button("🔍 Analizar todos los comentarios", type="primary"):
            barra = st.progress(0, text="Analizando comentarios...")
            resultados = []

            for i, texto in enumerate(df["texto"].tolist()):
                resultado = analizar_comentario(str(texto))
                resultados.append(resultado["etiqueta"])
                barra.progress((i + 1) / len(df), text=f"Analizando {i+1}/{len(df)}...")

            df["sentimiento"] = resultados
            barra.empty()

            stats = calcular_estadisticas(df)

            col_g1, col_g2 = st.columns([1, 1])

            with col_g1:
                conteo = df["sentimiento"].value_counts()
                fig = px.pie(
                    values=conteo.values,
                    names=conteo.index,
                    hole=0.6,
                    color=conteo.index,
                    color_discrete_map={
                        "positivo": "#00D45E",
                        "negativo": "#FF3B3B",
                        "neutral": "#FFD700"
                    }
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="rgba(240,244,248,0.7)"),
                    legend=dict(font=dict(color="rgba(240,244,248,0.5)", size=11)),
                    margin=dict(t=20, b=20),
                    height=280
                )
                fig.update_traces(textfont_color="white")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            with col_g2:
                st.metric("😊 Positivos", stats["positivo"]["count"], f"{stats['positivo']['pct']:.1f}%")
                st.metric("😠 Negativos", stats["negativo"]["count"], f"{stats['negativo']['pct']:.1f}%")
                st.metric("😐 Neutrales", stats["neutral"]["count"], f"{stats['neutral']['pct']:.1f}%")

            st.dataframe(df[["texto", "sentimiento"]], use_container_width=True, height=300)
            st.success(f"✅ {len(df)} comentarios analizados correctamente")


def render_sentimiento():
    """Renderiza la vista completa del analizador de sentimiento."""
    inicializar_analizador()

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎭</div>
        <div>
            <p class="section-title">Análisis de Sentimiento</p>
            <p class="section-desc">
                XLM-RoBERTa · F1=0.81 · Entrenado con datos reales de YouTube
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    modo = st.radio(
        "",
        ["💬 Comentario individual", "📁 Análisis por lotes (CSV)"],
        horizontal=True,
        key="modo_analisis"
    )

    if modo == "💬 Comentario individual":
        render_analisis_individual()
    else:
        render_analisis_lotes()