import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Control de Energía",
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


# --- ESTILOS CSS PERSONALIZADOS ---
def load_css():
    """Carga estilos CSS para un tema oscuro y tecnológico."""
    st.markdown("""
        <style>
            /* Reset y configuración base */
            html, body, [class*="st-"] {
                font-family: 'Inter', sans-serif;
                color: #E0E0E0;
            }
            body {
                background-color: #121212;
            }
            .stApp {
                background-color: #121212;
            }

            /* Estilo de las tarjetas (contenedores) */
            .stMetric, [data-testid="stMetric"], .st-emotion-cache-z5fcl4 {
                background-color: #1E1E1E;
                border: 1px solid #2D2D2D;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 12px 0 rgba(0,0,0,0.1);
            }
            
            /* Títulos de las tarjetas y KPIs */
            .stMetricLabel, [data-testid="stMetricLabel"] {
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                color: #A0A0A0 !important; /* Color gris suave para etiquetas */
            }

            .stMetricValue, [data-testid="stMetricValue"] {
                font-size: 2.5rem !important;
                font-weight: 700 !important;
                color: #FFFFFF !important;
            }

            .stMetricDelta, [data-testid="stMetricDelta"] {
                font-size: 1rem !important;
                font-weight: 600 !important;
            }
            
            /* Títulos de sección */
            h2, h3 {
                color: #FFFFFF;
                font-weight: 700;
            }
            
            h3 {
                border-bottom: 2px solid #00A8E8;
                padding-bottom: 8px;
            }

            /* Ocultar elementos innecesarios de Streamlit */
            .st-emotion-cache-16txtl3 {
                display: none;
            }
            footer {
                visibility: hidden;
            }
            header {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

load_css()

# --- GENERACIÓN DE DATOS SIMULADOS ---
@st.cache_data
def get_mock_data():
    """Genera datos aleatorios para simular un entorno en tiempo real."""
    
    # Operación del sistema
    incidentes = {
        'interrupciones': np.random.randint(1, 5),
        'fallas': np.random.randint(0, 3),
        'mantenimientos': np.random.randint(5, 15)
    }
    total_incidentes = sum(incidentes.values())
    clientes_afectados = incidentes['interrupciones'] * np.random.randint(50, 200) + incidentes['fallas'] * np.random.randint(100, 300)
    
    # Generación eléctrica
    generacion = {
        'Solar ☀️': np.random.uniform(150, 300),
        'Eólica 🌬️': np.random.uniform(200, 400),
        'Térmica 🔥': np.random.uniform(500, 800),
        'Hidráulica 💧': np.random.uniform(800, 1200)
    }
    total_generacion = sum(generacion.values())
    demanda_actual = total_generacion * np.random.uniform(0.85, 0.98)

    # Mapa
    num_puntos_incidentes = np.random.randint(10, 30)
    map_data_incidentes = pd.DataFrame({
        'lat': np.random.normal(4.65, 0.1, num_puntos_incidentes),
        'lon': np.random.normal(-74.08, 0.1, num_puntos_incidentes),
        'weight': np.random.randint(1, 5, size=num_puntos_incidentes) # Criticidad del incidente
    })

    num_brigadas = np.random.randint(5, 10)
    map_data_brigadas = pd.DataFrame({
        'lat': np.random.normal(4.65, 0.08, num_brigadas),
        'lon': np.random.normal(-74.08, 0.08, num_brigadas)
    })

    return {
        'incidentes': incidentes,
        'total_incidentes': total_incidentes,
        'mttr': f"{np.random.uniform(1.5, 4.0):.2f}h",
        'clientes_afectados': int(clientes_afectados),
        'confiabilidad_red': f"{np.random.uniform(99.5, 99.98):.2f}%",
        'llamadas_dia': np.random.randint(800, 1500),
        'aht': f"{np.random.randint(180, 300)}s",
        'reportes_cola': np.random.randint(5, 50),
        'confirmados_reales': f"{np.random.uniform(75, 95):.1f}%",
        'saidi': np.random.uniform(1.0, 2.5),
        'saifi': np.random.uniform(0.8, 1.5),
        'ens': np.random.uniform(50, 150),
        'cumplimiento_normativo': np.random.uniform(98.0, 99.8),
        'generacion': generacion,
        'total_generacion': total_generacion,
        'demanda_actual': demanda_actual,
        'disponibilidad_sistema': f"{np.random.uniform(99.8, 99.99):.2f}%",
        'riesgo_sobrecarga': f"{np.random.uniform(5, 25):.1f}%",
        'emisiones_evitadas': np.random.uniform(500, 1200),
        'map_data_incidentes': map_data_incidentes,
        'map_data_brigadas': map_data_brigadas
    }

data = get_mock_data()

# --- LAYOUT DEL DASHBOARD ---

# Título y última actualización
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("⚡ Dashboard de Control del Sistema Eléctrico")
with header_col2:
    st.markdown(f"""
    <div style="text-align: right; font-size: 0.9rem; color: #A0A0A0;">
        <p>Última actualización:<br><b>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</b></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Contenedor principal
main_grid = st.container()
with main_grid:
    # FILA 1: KPIs Principales
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            label="Incidentes Activos",
            value=data['total_incidentes'],
            delta=f"{np.random.randint(-5, 5)} en la última hora",
            delta_color="inverse"
        )
    with col2:
        st.metric(
            label="Clientes Afectados",
            value=f"{data['clientes_afectados']:,}",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            label="Disponibilidad del Sistema",
            value=data['disponibilidad_sistema']
        )
    with col4:
        st.metric(
            label="MTTR (Tiempo Medio Reparación)",
            value=data['mttr']
        )
    with col5:
        st.metric(
            label="Riesgo de Sobrecarga",
            value=data['riesgo_sobrecarga'],
            delta_color="inverse"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # FILA 2: Generación, Mapa e Incidentes
    col1, col2 = st.columns([2, 3])
    with col1:
        # --- SECCIÓN DE GENERACIÓN ELÉCTRICA ---
        with st.container(border=True):
            st.subheader("🔵 Generación Eléctrica en Tiempo Real")
            
            # Gráfico Donut de Generación
            gen_df = pd.DataFrame(list(data['generacion'].items()), columns=['Fuente', 'MW'])
            fig_donut = px.pie(
                gen_df,
                values='MW',
                names='Fuente',
                hole=0.6,
                color_discrete_map={
                    'Solar ☀️': '#FFC300', 'Eólica 🌬️': '#00A8E8',
                    'Térmica 🔥': '#FF5733', 'Hidráulica 💧': '#335BFF'
                },
                title=f"Total Generado: {data['total_generacion']:.2f} MW"
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E0E0E0',
                title_font_size=20,
                title_x=0.5,
                height=350,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            # Gráfico de Barra (Generación vs Demanda)
            fig_gauge = go.Figure()
            fig_gauge.add_trace(go.Bar(
                y=['Balance'], x=[data['total_generacion']], name='Generación',
                orientation='h', marker_color='#00A8E8'
            ))
            fig_gauge.add_trace(go.Bar(
                y=['Balance'], x=[data['demanda_actual']], name='Demanda',
                orientation='h', marker_color='#FF5733'
            ))
            fig_gauge.update_layout(
                barmode='overlay',
                title_text="Generación vs. Demanda",
                xaxis_title="MW",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E0E0E0', height=150,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # --- SECCIÓN DE MAPA GEORREFERENCIADO ---
        with st.container(border=True):
            st.subheader("🟣 Mapa de Operaciones en Tiempo Real")
            
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=4.65,
                        longitude=-74.08,
                        zoom=9,
                        pitch=50,
                    ),
                    layers=[
                        pdk.Layer(
                           'HeatmapLayer',
                           data=data['map_data_incidentes'],
                           get_position='[lon, lat]',
                           opacity=0.9,
                           get_weight="weight",
                           threshold=0.1,
                           radius_pixels=40,
                        ),
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=data['map_data_brigadas'],
                            get_position='[lon, lat]',
                            get_color='[0, 200, 255, 200]', # Azul brillante para brigadas
                            get_radius=200,
                            pickable=True,
                        ),
                    ],
                    tooltip={"text": "Brigada Operativa"}
                ),
                use_container_width=True,
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # FILA 3: Desglose de KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # --- OPERACIÓN DEL SISTEMA ---
        with st.container(border=True, height=350):
            st.subheader("🟠 Operación del Sistema")
            for tipo, num in data['incidentes'].items():
                color = "normal"
                if tipo == "fallas": color = "inverse"
                if tipo == "interrupciones": color = "off"
                st.metric(label=f"Incidentes: {tipo.capitalize()}", value=num, delta_color=color)

    with col2:
        # --- ATENCIÓN AL CLIENTE ---
        with st.container(border=True, height=350):
            st.subheader("🟡 Atención al Cliente / Reportes")
            st.metric(label="Llamadas Recibidas (Día)", value=f"{data['llamadas_dia']:,}")
            st.metric(label="Tiempo Promedio Atención (AHT)", value=data['aht'])
            st.metric(label="Reportes en Cola", value=data['reportes_cola'], delta_color="inverse")
            st.metric(label="% Confirmados Reales", value=data['confirmados_reales'])

    with col3:
        # --- CALIDAD DE SERVICIO (REGULATORIO) ---
        with st.container(border=True, height=350):
            st.subheader("🟢 Calidad del Servicio (Regulatorio)")
            st.metric(label="SAIDI (Duración Prom. Interrupción)", value=f"{data['saidi']:.2f}")
            st.metric(label="SAIFI (Frecuencia Prom. Interrupción)", value=f"{data['saifi']:.2f}")
            st.metric(label="ENS (Energía No Suministrada)", value=f"{data['ens']:.2f} MWh")
            st.markdown("Nivel de Cumplimiento Normativo:")
            st.progress(int(data['cumplimiento_normativo']), text=f"{data['cumplimiento_normativo']:.1f}%")

# --- LÓGICA DE ACTUALIZACIÓN AUTOMÁTICA ---
# Forzamos un refresh de la página cada 15 segundos para simular datos en tiempo real.
time.sleep(15)
st.rerun()

