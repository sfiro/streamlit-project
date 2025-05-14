
import streamlit as st
import pandas as pd
import plotly.express as px
from consignaciones import consignaciones
from incidentes import incidentes
from saidi import saidi
from resumenApp2 import resumen
from entrega import entrega
import os
import time

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
from streamlit_autorefresh import st_autorefresh


# Capturar el tiempo de inicio
start_time = time.time()

#######################
# Page configuration
st.set_page_config(
    page_title="Dashboard centro de control",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################

#######################
# Agregar un temporizador de recarga automática en el frontend
st.markdown("""
    <script>
        function reloadPage() {
            setTimeout(function() {
                window.location.reload();
            }, 10000);  // Recargar cada 10 segundos
        }
        reloadPage();
    </script>
""", unsafe_allow_html=True)

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################  Carga de base de datos  ####################
@st.cache_data(ttl=10) 
def cargar_datos():
    consignaciones_path = '/Users/debbiearredondo/Desktop/streamlit project/datos/BICC/Consignaciones.csv'
    incidentes_path = '/Users/debbiearredondo/Desktop/streamlit project/datos/BICC/IncidentesActual.csv'
    saidi_path = '/Users/debbiearredondo/Desktop/streamlit project/datos/BICC/SAIDIPendientes.csv'

    # Obtener la última fecha de modificación de los archivos
    consignaciones_last_modified = os.path.getmtime(consignaciones_path)
    incidentes_last_modified = os.path.getmtime(incidentes_path)
    saidi_last_modified = os.path.getmtime(saidi_path)

    # Cargar los datos
    consignaciones_datos = pd.read_csv(consignaciones_path, encoding='utf-16')
    incidentes_datos = pd.read_csv(incidentes_path, encoding='utf-16')
    saidi_datos = pd.read_csv(saidi_path, encoding='utf-16')

    return consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified

#####  funcion para importarn animaciones ######
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    count = st_autorefresh(interval=3000, limit=100, key="fizzbuzzcounter")
    #st.metric("Contador", count)

    #######################
    # Cargar datos
    consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()

    st.write("Última actualización:") 
    st.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(incidentes_last_modified)))
   ##---------------------------------------------------------------
    st.sidebar.title("Menú lateral")
    opcion = st.sidebar.selectbox("Selecciona una opción", ["Resumen","consignaciones","incidentes", "Saidi", "Entrega"])

    # Mostrar contenido según la opción seleccionada
    if opcion == "Resumen":
        resumen(consignaciones_datos, incidentes_datos, saidi_datos)
    #    resumen(datos)

    if opcion == "consignaciones":
        consignaciones(consignaciones_datos)

    if opcion == "incidentes":
        incidentes(incidentes_datos)

    if opcion == "Saidi":
        saidi(saidi_datos)

    if opcion == "Entrega":
        entrega(incidentes_datos)
    

    ##---------------------------------------------------------------




  # Cargar datos de ejemplo
if __name__ == '__main__':
  main()