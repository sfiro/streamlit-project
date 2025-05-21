
import streamlit as st
import pandas as pd
import plotly.express as px
from consignaciones import consignaciones
from incidentes import incidentes
from saidi import saidi
from resumenApp2 import resumen
from entrega import entrega
from Dashboard import dashboard
import os
import time

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
from streamlit_autorefresh import st_autorefresh
import utils



#######################
# Page configuration
st.set_page_config(
    page_title="Dashboard centro de control",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

#alt.themes.enable("dark")
alt.themes.enable("default")

#######################

#######################
# # Agregar un temporizador de recarga automática en el frontend
# st.markdown("""
#     <script>
#         function reloadPage() {
#             setTimeout(function() {
#                 window.location.reload();
#             }, 10000);  // Recargar cada 10 segundos
#         }
#         reloadPage();
#     </script>
# """, unsafe_allow_html=True)



#######################  Carga de base de datos  ####################
@st.cache_data(ttl=10) 
def cargar_datos():
    #base_path = os.path.dirname(os.path.abspath(__file__))
    #print(base_path)
    base_path = "\\Users\\accontrol\\OneDrive - CELSIA S.A E.S.P"
    consignaciones_path = os.path.join(base_path, 'BICC', 'Consignaciones.csv')
    incidentes_path = os.path.join(base_path,'BICC', 'IncidentesActual.csv')
    saidi_path = os.path.join(base_path, 'BICC', 'SAIDIPendientes.csv')

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
    utils.local_css('estilo.css')

    count = st_autorefresh(interval=60000, limit=100, key="fizzbuzzcounter")

    last_update_time = time.time()

    # Formatear la fecha y hora de la última actualización
    formatted_last_update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_update_time))


    #######################
    # Cargar datos
    consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()

    
   ##---------------------------------------------------------------
    
    with st.sidebar:
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, 'logo', 'logoCelsia.png')
   
        st.image(logo_path, width=150)  # Cambia la ruta a tu imagen
        opcion = st.sidebar.selectbox("Selecciona una opción", ["Dashboard","Resumen","Consignaciones","Incidentes", "Saidi", "Entrega turno","IA"])

        st.markdown("---")  # Línea divisoria
        st.write("Última actualización:")
        st.write(formatted_last_update_time)
    # Mostrar contenido según la opción seleccionada
    if opcion == "Dashboard":
        dashboard(consignaciones_datos, incidentes_datos, saidi_datos)

    if opcion == "Resumen":
        resumen(consignaciones_datos, incidentes_datos, saidi_datos)
    #    resumen(datos)

    if opcion == "Consignaciones":
        consignaciones(consignaciones_datos)

    if opcion == "Incidentes":
        incidentes(incidentes_datos)

    if opcion == "Saidi":
        saidi(saidi_datos)

    if opcion == "Entrega turno":
        entrega(incidentes_datos)
    
    if opcion == "IA":
        pass
        #gemini.chat()
    

  # Cargar datos de ejemplo
if __name__ == '__main__':
  main()