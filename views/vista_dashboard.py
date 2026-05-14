"""
Vista del Dashboard — Solo interfaz de usuario.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.core.gestor_sentimiento import (
    inicializar_analizador,
    analizar_comentario,
    calcular_estadisticas
)


def render_dashboard():
    """Renderiza la vista completa del dashboard de tendencias."""
    inicializar_analizador()

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div>
            <p class="section-title">Dashboard de Tendencias</p>
            <p class="section-desc">
                Evolución del sentimiento durante un partido · Datos reales
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    archivo = st.file_uploader(
        "",
        type=["csv"],
        key="dashboard",
        label_visibility="collapsed"
    )
    st.caption("💡 Usa el archivo `data/raw/dataset_youtube_etiquetado.csv` como ejemplo")

    if not archivo:
        st.markdown("""
        <div style="height:300px; display:flex; align-items:center; 
            justify-content:center; flex-direction:column; gap:1rem; opacity:0.3;">
            <div style="font-size:4rem;">📊</div>
            <p style="font-size:0.85rem; color:rgba(240,244,248,0.5);">
                Carga un archivo CSV para generar el dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.read_csv(archivo)

    if "texto" not in df.columns:
        st.error("El CSV debe tener una columna llamada 'texto'")
        return

    if not st.button("📊 Generar Dashboard", type="primary"):
        return

    barra = st.progress(0, text="Procesando comentarios...")
    sentimientos = []

    for i, texto in enumerate(df["texto"].tolist()):
        resultado = analizar_comentario(str(texto))
        sentimientos.append(resultado["etiqueta"])
        barra.progress((i + 1) / len(df), text=f"Procesando {i+1}/{len(df)}...")

    df["sentimiento"] = sentimientos
    barra.empty()

    stats = calcular_estadisticas(df)

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total comentarios", stats["total"])
    with col2:
        st.metric("😊 Positivos", stats["positivo"]["count"], f"{stats['positivo']['pct']:.1f}%")
    with col3:
        st.metric("😠 Negativos", stats["negativo"]["count"], f"{stats['negativo']['pct']:.1f}%")
    with col4:
        st.metric("😐 Neutrales", stats["neutral"]["count"], f"{stats['neutral']['pct']:.1f}%")

    st.divider()

    # Gráfico de evolución
    df["indice"] = range(len(df))
    df["valor"] = df["sentimiento"].map({"positivo": 1, "neutral": 0, "negativo": -1})
    df["promedio"] = df["valor"].rolling(window=15, min_periods=1).mean()

    fig_linea = go.Figure()
    fig_linea.add_trace(go.Scatter(
        x=df["indice"],
        y=df["promedio"],
        fill="tozeroy",
        fillcolor="rgba(0,212,94,0.05)",
        line=dict(color="rgba(0,212,94,0.8)", width=2),
        name="Tendencia",
        hovertemplate="Comentario %{x}<br>Sentimiento: %{y:.2f}<extra></extra>"
    ))
    fig_linea.add_hline(
        y=0, line_dash="dash",
        line_color="rgba(255,255,255,0.15)",
        annotation_text="Neutro",
        annotation_font_color="rgba(255,255,255,0.3)"
    )
    fig_linea.update_layout(
        title=dict(
            text="Evolución del Sentimiento durante el Partido",
            font=dict(family="Bebas Neue", size=20, color="rgba(240,244,248,0.8)"),
            x=0
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="rgba(240,244,248,0.3)"),
            title=dict(text="Número de comentario", font=dict(color="rgba(240,244,248,0.3)", size=11))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="rgba(240,244,248,0.3)"),
            range=[-1.2, 1.2],
            tickvals=[-1, 0, 1],
            ticktext=["Negativo", "Neutral", "Positivo"]
        ),
        height=350,
        margin=dict(t=50, b=40, l=80, r=20),
        showlegend=False
    )
    st.plotly_chart(fig_linea, use_container_width=True, config={"displayModeBar": False})

    # Distribución
    col_bar, col_pie = st.columns([3, 2])
    conteo = df["sentimiento"].value_counts()

    with col_bar:
        fig_bar = go.Figure(go.Bar(
            x=conteo.index,
            y=conteo.values,
            marker_color=[
                "#00D45E" if x == "positivo" else "#FF3B3B" if x == "negativo" else "#FFD700"
                for x in conteo.index
            ],
            marker_opacity=0.85,
            text=conteo.values,
            textposition="outside",
            textfont=dict(color="rgba(240,244,248,0.7)")
        ))
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(t=20, b=20),
            xaxis=dict(tickfont=dict(color="rgba(240,244,248,0.5)")),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_pie:
        fig_pie = px.pie(
            values=conteo.values,
            names=conteo.index,
            hole=0.7,
            color=conteo.index,
            color_discrete_map={
                "positivo": "#00D45E",
                "negativo": "#FF3B3B",
                "neutral": "#FFD700"
            }
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(t=10, b=10),
            legend=dict(font=dict(color="rgba(240,244,248,0.5)", size=10))
        )
        fig_pie.update_traces(textfont_color="white")
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.dataframe(df[["texto", "sentimiento"]], use_container_width=True, height=250)