import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config(layout="wide", page_title="Centro de Control Eléctrico", page_icon="⚡")
st.markdown("""
    <style>
    body {background-color: #121212; color: white;}
    .main {background-color: #121212;}
    h1, h2, h3, h4 {color: white; font-family: 'Segoe UI', sans-serif;}
    .block-container {padding-top: 1rem;}
    .metric-label, .metric-value {color: white;}
    img.icon-svg {height: 40px;}
    </style>
""", unsafe_allow_html=True)

# -------- Función para mostrar iconos SVG seguros --------
def show_svg_icon(url, alt="icon"):
    try:
        st.image(url, width=40)
    except Exception as e:
        st.text(f"[icono no disponible]")

# -------- Sección 1: Indicadores de Operación del Sistema Eléctrico --------
st.markdown("## 🟠 Indicadores de Operación del Sistema Eléctrico")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    show_svg_icon("https://www.svgrepo.com/show/13685/alert.svg")
    st.metric("Incidentes Activos", "8", "+2")
with col2:
    show_svg_icon("https://www.svgrepo.com/show/503185/error-alert.svg")
    st.metric("Criticidad Alta", "3")
with col3:
    show_svg_icon("https://www.svgrepo.com/show/354171/clock-time.svg")
    st.metric("MTTR (h)", "2.4h")
with col4:
    show_svg_icon("https://www.svgrepo.com/show/11889/group.svg")
    st.metric("Clientes Afectados", "12,400")
with col5:
    show_svg_icon("https://www.svgrepo.com/show/309077/check-shield.svg")
    st.metric("% Red Operativa", "96.5%")

# -------- Sección 2: Atención al Cliente --------
st.markdown("## 🟡 Atención al Cliente / Reportes")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📞 Reportes Hoy", "1,230")
col2.metric("⏳ Tiempo Promedio Atención", "3.8 min")
col3.metric("📋 En Cola", "124")
col4.metric("✔️ Confirmados Reales", "68%")

# -------- Sección 3: Calidad del Servicio Eléctrico --------
st.markdown("## 🟢 Indicadores de Calidad del Servicio Eléctrico")
col1, col2, col3, col4 = st.columns(4)
col1.metric("SAIDI", "1.2h")
col2.metric("SAIFI", "1.8")
col3.metric("ENS (MWh)", "54")
col4.metric("✅ Cumplimiento Normas", "92%")

# -------- Sección 4: Generación por Tipo --------
st.markdown("## 🔵 Generación Eléctrica por Tipo")
col1, col2 = st.columns([2, 3])

# Datos ficticios
fuentes = ["Solar ☀️", "Eólica 🌬️", "Térmica 🔥", "Hidráulica 💧"]
valores = [320, 180, 450, 520]
total = sum(valores)
porcentajes = [v/total*100 for v in valores]

# Donut chart
fig = go.Figure(data=[go.Pie(labels=fuentes, values=valores, hole=.5,
                             marker=dict(colors=['#FFD700','#1E90FF','#FF6347','#20B2AA']))])
fig.update_layout(paper_bgcolor='#121212', font_color='white', showlegend=True)
col1.plotly_chart(fig, use_container_width=True)

# KPIs complementarios
col2.markdown("### ⚡ Detalles")
col2.write(f"🔆 Solar: {valores[0]} MW ({porcentajes[0]:.1f}%)")
col2.write(f"🌬️ Eólica: {valores[1]} MW ({porcentajes[1]:.1f}%)")
col2.write(f"🔥 Térmica: {valores[2]} MW ({porcentajes[2]:.1f}%)")
col2.write(f"💧 Hidráulica: {valores[3]} MW ({porcentajes[3]:.1f}%)")
col2.write("📈 Demanda Pico Estimada: 1,500 MW")

# -------- Sección 5: Mapa Georreferenciado --------
st.markdown("## 🟣 Mapa Georreferenciado del Valle del Cauca")
data = pd.DataFrame({
    'Ciudad': ['Cali', 'Palmira', 'Tuluá', 'Buenaventura', 'Yumbo', 'Cartago'],
    'Lat': [3.4516, 3.5394, 4.0847, 3.8801, 3.5858, 4.7464],
    'Lon': [-76.5320, -76.3035, -76.1954, -77.0311, -76.4950, -75.9117],
    'Incidentes': [18, 12, 9, 15, 6, 8]
})
fig_map = px.scatter_mapbox(
    data, lat="Lat", lon="Lon", size="Incidentes", color="Incidentes",
    hover_name="Ciudad", color_continuous_scale="thermal", size_max=30, zoom=8,
    mapbox_style="carto-positron"
)
fig_map.update_layout(paper_bgcolor='#121212', margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# -------- Sección 6: Indicadores Estratégicos --------
st.markdown("## ⚫ Indicadores Estratégicos")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📶 Disponibilidad Sistema", "98.9%")
col2.metric("⚠️ Riesgo Operacional", "12.3%")
col3.metric("⚖️ Energía Balanceada", "✔️")
col4.metric("🌱 Emisiones Evitadas", "320 tCO2")

# Footer
st.markdown("""
---
Centro de Control de Energía | Visualización dinámica de indicadores clave. Diseño optimizado para video wall.
""")
