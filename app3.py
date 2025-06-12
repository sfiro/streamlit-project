import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Avanzado de Control de Energía",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- IMPORTACIÓN DE LIBRERÍAS ADICIONALES (con manejo de errores) ---
try:
    import pydeck as pdk
except ImportError:
    st.error("Error: La librería Pydeck no está instalada. Por favor, ejecute 'pip install pydeck' en su terminal.")
    st.stop()

# --- DICCIONARIO DE ICONOS (SVG de Lucide Icons para mejor calidad) ---
icons = {
    "alerta": "https://lucide.dev/icons/siren.svg",
    "clientes": "https://lucide.dev/icons/users.svg",
    "disponibilidad": "https://lucide.dev/icons/check-check.svg",
    "riesgo": "https://lucide.dev/icons/shield-alert.svg",
    "reparacion": "https://lucide.dev/icons/wrench.svg",
    "solar": "https://lucide.dev/icons/sun.svg",
    "eolica": "https://lucide.dev/icons/wind.svg",
    "termica": "https://lucide.dev/icons/factory.svg",
    "hidraulica": "https://lucide.dev/icons/waves.svg",
    "incidentes": "https://lucide.dev/icons/hard-hat.svg",
    "llamadas": "https://lucide.dev/icons/phone.svg",
    "calidad": "https://lucide.dev/icons/award.svg",
    "hoja": "https://lucide.dev/icons/leaf.svg",
    "balance": "https://lucide.dev/icons/scale.svg",
}

# --- ESTILOS CSS PERSONALIZADOS ---
def load_css():
    """Carga estilos CSS para un tema oscuro y tecnológico."""
    st.markdown(f"""
        <style>
            /* Fuente y Colores Base */
            html, body, [class*="st-"] {{
                font-family: 'Inter', sans-serif;
                color: #E0E0E0;
            }}
            body {{ background-color: #0A0A0A; }}
            .stApp {{ background-color: #0A0A0A; }}

            /* Ocultar elementos de Streamlit */
            .st-emotion-cache-16txtl3, footer, header {{ display: none; }}
            
            /* Títulos de sección */
            h2, h3 {{
                color: #FFFFFF;
                font-weight: 700;
            }}
            h3 {{
                border-bottom: 2px solid #00A8E8;
                padding-bottom: 8px;
                margin-top: 20px;
            }}

            /* Tarjetas de Métricas */
            .metric-card {{
                background-color: #1E1E1E;
                border: 1px solid #2D2D2D;
                border-radius: 12px;
                padding: 1.5rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
            }}
            .metric-card-title {{
                font-size: 1.1rem;
                color: #A0A0A0;
                display: flex;
                align-items: center;
                font-weight: 600;
            }}
            .metric-card-title img {{
                width: 24px;
                height: 24px;
                margin-right: 10px;
                filter: invert(80%);
            }}
            .metric-card-value {{
                font-size: 2.5rem;
                font-weight: 700;
                color: #FFFFFF;
                text-align: right;
            }}
            
            /* Panel de Alertas */
            .alert-panel {{
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 1rem;
            }}
            .alert-critical {{ background-color: rgba(255, 71, 87, 0.15); border-left: 5px solid #FF4757; }}
            .alert-warning {{ background-color: rgba(255, 165, 2, 0.15); border-left: 5px solid #FFA502; }}
            .alert-title {{ font-weight: 700; margin-bottom: 5px; color: #FFFFFF; }}
            .alert-time {{ font-size: 0.8rem; color: #A0A0A0; }}

            /* Indicador de Estado del Sistema */
            .status-banner {{
                padding: 1rem;
                border-radius: 12px;
                text-align: center;
                font-size: 1.8rem;
                font-weight: 700;
                color: #FFFFFF;
                border: 2px solid;
            }}
            .status-normal {{ background-color: rgba(46, 204, 113, 0.2); border-color: #2ECC71; }}
            .status-alerta {{ background-color: rgba(255, 165, 2, 0.2); border-color: #FFA502; }}
            .status-critico {{ background-color: rgba(255, 71, 87, 0.2); border-color: #FF4757; }}
        </style>
    """, unsafe_allow_html=True)

load_css()

# --- GENERACIÓN DE DATOS SIMULADOS ---
@st.cache_data
def get_mock_data():
    """Genera datos aleatorios para simular un entorno en tiempo real."""
    
    # --- Datos de Series de Tiempo para Demanda ---
    now = datetime.now()
    timestamps = pd.to_datetime([now - timedelta(hours=i) for i in range(24)]).sort_values()
    base_demand = 2000 + 500 * np.sin(np.linspace(0, 2 * np.pi, 24))
    demanda_real = base_demand + np.random.normal(0, 50, 24)
    demanda_proyectada = base_demand * np.random.uniform(0.98, 1.02, 24)
    demand_df = pd.DataFrame({
        'Hora': timestamps,
        'Demanda Real (MW)': demanda_real,
        'Demanda Proyectada (MW)': demanda_proyectada
    }).set_index('Hora')

    # --- Incidentes y Operación ---
    incidentes = {'interrupciones': np.random.randint(1, 5), 'fallas': np.random.randint(0, 3), 'mantenimientos': np.random.randint(5, 15)}
    total_incidentes = sum(incidentes.values())
    clientes_afectados = incidentes['interrupciones'] * np.random.randint(50, 200) + incidentes['fallas'] * np.random.randint(100, 300)
    
    # --- Generación ---
    generacion = {'Solar ☀️': np.random.uniform(150, 300), 'Eólica 🌬️': np.random.uniform(200, 400), 'Térmica 🔥': np.random.uniform(500, 800), 'Hidráulica 💧': np.random.uniform(800, 1200)}
    total_generacion = sum(generacion.values())

    # --- Mapa ---
    map_data_incidentes = pd.DataFrame({'lat': np.random.normal(4.65, 0.1, 20), 'lon': np.random.normal(-74.08, 0.1, 20), 'weight': np.random.randint(1, 5, 20)})
    map_data_brigadas = pd.DataFrame({'lat': np.random.normal(4.65, 0.08, 8), 'lon': np.random.normal(-74.08, 0.08, 8)})

    # --- Alertas ---
    alerts = [
        {"level": "critical", "title": "Sobrecarga en Subestación Central", "time": "Hace 5 min"},
        {"level": "warning", "title": "Baja producción eólica por falta de viento", "time": "Hace 25 min"},
        {"level": "critical", "title": "Falla detectada en línea de transmisión Norte", "time": "Hace 45 min"}
    ]
    
    # --- Estado del Sistema ---
    riesgo = np.random.uniform(5, 45)
    system_status = "NORMAL"
    if riesgo > 35 or incidentes['fallas'] > 1:
        system_status = "CRÍTICO"
    elif riesgo > 20 or total_incidentes > 15:
        system_status = "ALERTA"
        
    return {
        'system_status': system_status,
        'incidentes': incidentes, 'total_incidentes': total_incidentes,
        'mttr': f"{np.random.uniform(1.5, 4.0):.2f}h",
        'clientes_afectados': int(clientes_afectados),
        'disponibilidad_sistema': f"{np.random.uniform(99.8, 99.99):.2f}%",
        'riesgo_sobrecarga': f"{riesgo:.1f}%",
        'llamadas_dia': np.random.randint(800, 1500), 'aht': f"{np.random.randint(180, 300)}s", 'reportes_cola': np.random.randint(5, 50),
        'saidi': np.random.uniform(1.0, 2.5), 'saifi': np.random.uniform(0.8, 1.5), 'ens': np.random.uniform(50, 150),
        'cumplimiento_normativo': np.random.uniform(98.0, 99.8),
        'generacion': generacion, 'total_generacion': total_generacion,
        'demand_df': demand_df,
        'emisiones_evitadas': np.random.uniform(500, 1200),
        'map_data_incidentes': map_data_incidentes, 'map_data_brigadas': map_data_brigadas,
        'alerts': alerts
    }

data = get_mock_data()


# --- FUNCIÓN PARA RENDERIZAR TARJETAS DE MÉTRICAS ---
def render_metric(title, value, icon_url):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-title">
                <img src="{icon_url}" class="icon">
                {title}
            </div>
            <div class="metric-card-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- LAYOUT DEL DASHBOARD ---

# Título y última actualización
st.title("Dashboard Avanzado de Control del Sistema Eléctrico")
st.markdown(f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

st.markdown("<br>", unsafe_allow_html=True)

# --- Fila 0: Estado del Sistema ---
status_map = {"NORMAL": "status-normal", "ALERTA": "status-alerta", "CRÍTICO": "status-critico"}
status_class = status_map.get(data['system_status'], "status-normal")
st.markdown(f"""
    <div class="status-banner {status_class}">
        ESTADO DEL SISTEMA: <strong>{data['system_status']}</strong>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- FILA 1: KPIs Principales ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1: render_metric("Incidentes Activos", data['total_incidentes'], icons['alerta'])
with col2: render_metric("Clientes Afectados", f"{data['clientes_afectados']:,}", icons['clientes'])
with col3: render_metric("Disponibilidad Sistema", data['disponibilidad_sistema'], icons['disponibilidad'])
with col4: render_metric("Riesgo de Sobrecarga", data['riesgo_sobrecarga'], icons['riesgo'])
with col5: render_metric("Tiempo Medio Reparación", data['mttr'], icons['reparacion'])

st.markdown("<br>", unsafe_allow_html=True)

# --- FILA 2: Generación, Demanda y Mapa ---
col1, col2 = st.columns([2, 3])

with col1:
    with st.container(border=True):
        st.subheader("Generación y Demanda")
        
        # Gráfico Donut de Generación
        gen_df = pd.DataFrame(list(data['generacion'].items()), columns=['Fuente', 'MW'])
        fig_donut = px.pie(
            gen_df, values='MW', names='Fuente', hole=0.6,
            color_discrete_map={'Solar ☀️': '#FFC300', 'Eólica 🌬️': '#00A8E8', 'Térmica 🔥': '#FF5733', 'Hidráulica 💧': '#335BFF'},
            title=f"Mix de Generación (Total: {data['total_generacion']:.0f} MW)"
        )
        fig_donut.update_traces(textinfo='percent', showlegend=True)
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E0E0E0', height=280, margin=dict(t=50, b=20), legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # Gráfico de Líneas de Demanda
        fig_demand = go.Figure()
        fig_demand.add_trace(go.Scatter(x=data['demand_df'].index, y=data['demand_df']['Demanda Real (MW)'], name='Demanda Real', line=dict(color='#00A8E8', width=3)))
        fig_demand.add_trace(go.Scatter(x=data['demand_df'].index, y=data['demand_df']['Demanda Proyectada (MW)'], name='Demanda Proyectada', line=dict(color='#A0A0A0', width=2, dash='dash')))
        fig_demand.update_layout(
            title_text="Tendencia de Demanda (Últimas 24h)",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E0E0E0', height=280,
            xaxis_title="", yaxis_title="MW", margin=dict(t=50), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_demand, use_container_width=True)

with col2:
    with st.container(border=True):
        st.subheader("Mapa de Operaciones en Tiempo Real")
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v11",
                initial_view_state=pdk.ViewState(latitude=4.65, longitude=-74.08, zoom=9.5, pitch=50),
                layers=[
                    pdk.Layer('HeatmapLayer', data=data['map_data_incidentes'], get_position='[lon, lat]', opacity=0.9, get_weight="weight", radius_pixels=40),
                    pdk.Layer('ScatterplotLayer', data=data['map_data_brigadas'], get_position='[lon, lat]', get_color='[0, 200, 255, 200]', get_radius=250, pickable=True)
                ],
                tooltip={"html": "<b>Brigada Operativa</b><br/>ID: {index}"}
            ), use_container_width=True
        )

# --- FILA 3: Desglose de KPIs y Alertas ---
col1, col2, col3 = st.columns((2, 2, 2.2))

with col1:
    with st.container(border=True, height=400):
        st.subheader("Detalle de Operación")
        for tipo, num in data['incidentes'].items():
            color = "normal"
            if tipo == "fallas": color = "inverse"
            if tipo == "interrupciones": color = "off"
            st.metric(label=f"Incidentes: {tipo.capitalize()}", value=num, delta_color=color)

with col2:
    with st.container(border=True, height=400):
        st.subheader("Atención al Cliente")
        st.metric(label="Llamadas Recibidas (Día)", value=f"{data['llamadas_dia']:,}")
        st.metric(label="Tiempo Promedio Atención (AHT)", value=data['aht'])
        st.metric(label="Reportes en Cola", value=data['reportes_cola'], delta_color="inverse")

with col3:
    with st.container(border=True, height=400):
        st.subheader("Alertas Críticas")
        for alert in data['alerts']:
            alert_class = f"alert-{alert['level']}"
            st.markdown(f"""
                <div class="alert-panel {alert_class}">
                    <div class="alert-title">{alert['title']}</div>
                    <div class="alert-time">{alert['time']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- FILA 4: Indicadores Regulatorios y Estratégicos ---
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("Calidad de Servicio (Regulatorio)")
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="SAIDI (Duración Prom. Interrupción)", value=f"{data['saidi']:.2f}")
        kpi2.metric(label="SAIFI (Frecuencia Prom. Interrupción)", value=f"{data['saifi']:.2f}")
        st.metric(label="ENS (Energía No Suministrada)", value=f"{data['ens']:.2f} MWh")
        st.markdown("**Nivel de Cumplimiento Normativo:**")
        st.progress(int(data['cumplimiento_normativo']), text=f"{data['cumplimiento_normativo']:.1f}%")

with col2:
     with st.container(border=True):
        st.subheader("Indicadores Estratégicos y Ambientales")
        st.metric(label="Emisiones de CO2 Evitadas (hoy)", value=f"{data['emisiones_evitadas']:.1f} Toneladas")
        st.metric(label="Balance Generación vs Demanda", value=f"{(data['total_generacion'] - data['demand_df']['Demanda Real (MW)'].iloc[-1]):.0f} MW")


# --- LÓGICA DE ACTUALIZACIÓN AUTOMÁTICA ---
time.sleep(20)
st.rerun()

