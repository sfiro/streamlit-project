import streamlit as st
import plotly.graph_objects as go

# Configurar página
st.set_page_config(page_title="Dashboard de Incidentes", layout="wide")

# Mapa de colores
color_map = {
    'Naraja': '#D5752D',
    'Gris': '#59595B',
    'Azul': '#13A2E1',
    'Verde': '#00BE91',
    'Amarillo': '#FFF65E',
    'Azul oscuro': '#003FA2',
    'Rojo': '#CA0045',
}

# Estilos
st.markdown("""
    <style>
    .big-font {
        font-size:32px !important;
        font-weight: bold;
    }
    .card {
        padding: 30px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Datos por KPI
zonas = ['Valle Norte', 'Valle Sur', 'Tolima Norte', 'Tolima Sur']
datos_kpi = {
    "Llamadas": {
        "color": color_map["Azul oscuro"],
        "icono": "📞",
        "valor": 125,
        "zonas": [40, 35, 25, 25]
    },
    "SCADA": {
        "color": color_map["Naraja"],
        "icono": "⚡",
        "valor": 15,
        "zonas": [3, 5, 4, 3]
    },
    "Consignaciones": {
        "color": color_map["Gris"],
        "icono": "📝",
        "valor": 78,
        "zonas": [20, 18, 25, 15]
    },
    "Clientes Afectados": {
        "color": color_map["Rojo"],
        "icono": "🚨",
        "valor": 2340,
        "zonas": [800, 700, 500, 340]
    }
}

# KPIs en tarjetas
col1, col2, col3, col4 = st.columns(4)
columnas = [col1, col2, col3, col4]

for col, kpi in zip(columnas, datos_kpi.keys()):
    datos = datos_kpi[kpi]
    col.markdown(
        f'<div class="card" style="background-color:{datos["color"]}">'
        f'{datos["icono"]}<br>{kpi}<br>'
        f'<span class="big-font">{datos["valor"]}</span></div>',
        unsafe_allow_html=True
    )

# Título
st.markdown("## Radar de Incidentes por Zona")

# Función para crear radar
def crear_grafico_radar(nombre, color, valores):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores + [valores[0]],
        theta=zonas + [zonas[0]],
        fill='toself',
        name=nombre,
        line_color=color,
        fillcolor=color,
        opacity=0.6
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=False,
        paper_bgcolor="#0F172A",
        font_color="white",
        margin=dict(l=30, r=30, t=30, b=30),
        height=350
    )
    return fig

# Mostrar gráficos en filas
kpis = list(datos_kpi.keys())
for i in range(0, len(kpis), 2):
    col_a, col_b = st.columns(2)
    for j, col in enumerate([col_a, col_b]):
        if i + j < len(kpis):
            kpi = kpis[i + j]
            datos = datos_kpi[kpi]
            col.subheader(f'{datos["icono"]} {kpi}')
            col.plotly_chart(crear_grafico_radar(kpi, datos["color"], datos["zonas"]), use_container_width=True)
