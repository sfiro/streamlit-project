
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard centro de control",
    # page_icon="🏂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from consignaciones import consignaciones
from incidentes import incidentes
from saidi import saidi
from resumenApp2 import resumen
from entrega import entrega
from Dashboard import dashboard
from gestion import gestion
from mapa import mapas
from generacion import gen
from xm import xm_data
from xmData import datos_xm
from xmData2 import datos_xm2

import os
import time
import sys

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
from streamlit_autorefresh import st_autorefresh
import utils

sys.path.append(os.path.join(os.path.dirname(__file__),'streamlit_ftp'))

from streamlit_ftp import app as app_ftp

#######################
# Page configuration

alt.themes.enable("dark")
# alt.themes.enable("default")



#######################  Carga de base de datos  ####################
@st.cache_data(ttl=10) 
def cargar_datos():
    #base_path = os.path.dirname(os.path.abspath(__file__))
    #print(base_path)
    #base_path = "\\Users\\gestioncc\\OneDrive - CELSIA S.A E.S.P"
    # base_path dinámico para cualquier usuario
    base_path = os.path.expanduser("~")
    consignaciones_path = os.path.join(base_path,'OneDrive - CELSIA S.A E.S.P', 'BICC', 'Consignaciones.csv')
    incidentes_path = os.path.join(base_path,'OneDrive - CELSIA S.A E.S.P','BICC', 'IncidentesActual.csv')
    saidi_path = os.path.join(base_path, 'OneDrive - CELSIA S.A E.S.P','BICC', 'SAIDIPendientes.csv')
    #consignaciones_path = os.path.join(base_path,'datos', 'BICC', 'Consignaciones.csv')
    #incidentes_path = os.path.join(base_path,'datos','BICC', 'IncidentesActual.csv')
    #saidi_path = os.path.join(base_path,'datos', 'BICC', 'SAIDIPendientes.csv')

  

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

    count = st_autorefresh(interval=300000, key="fizzbuzzcounter")

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
        #opcion = st.sidebar.selectbox("Selecciona una opción", ["Dashboard","Mapa","Resumen","Consignaciones","Incidentes", "Saidi", "Entrega turno","Gestion"])
        opcion = st.sidebar.selectbox("Selecciona una opción", ["Dashboard","Mapa","XM","Consignaciones", "Saidi", "Entrega turno","Gestion","FTP","Generación"])


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

    if opcion == "XM":
        xm_data()

    if opcion == "Incidentes":
        incidentes(incidentes_datos)

    if opcion == "Saidi":
        saidi(saidi_datos)

    if opcion == "Entrega turno":
        entrega(incidentes_datos)

    if opcion == "Gestion":
        gestion()

    if opcion == "Mapa":
        mapas(incidentes_datos)

    if opcion =="FTP":
        # Aquí puedes llamar a la función de tu aplicación FTP
        app_ftp.app()

    if opcion =="Generación":
        # Aquí puedes llamar a la función de tu aplicación FTP
        gen()



  # Cargar datos de ejemplo
if __name__ == '__main__':
  
    page = st.query_params.get("page")

    # Contenido dinámico
    if page is None:
        main()
    elif page == "dashboard":
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 1.05; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        dashboard(consignaciones_datos, incidentes_datos, saidi_datos)
    elif page == "mapa":
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 1.05; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        mapas(incidentes_datos)
    elif page == "generacion":
        #consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 0.95; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        gen()
    
    elif page == "iconosGen":
        #consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 0.95; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        pass
        

    elif page == "xm":
        #consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 0.95; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        datos_xm()
    
    elif page == "xm2":
        #consignaciones_datos, incidentes_datos, saidi_datos, consignaciones_last_modified, incidentes_last_modified, saidi_last_modified = cargar_datos()
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                zoom: 0.95; /* Cambia este valor para simular zoom (1.0 = 100%) */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        datos_xm2()
    else:
        st.title("Página no encontrada")
        st.write("El valor en la URL no es válido.")