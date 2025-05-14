import streamlit as st
import pandas as pd
import plotly.express as px

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie

#####  funcion para importarn animaciones ######
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def resumen(consignaciones,incidentes,saidi):

    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 2rem; /* Cambia el tamaño del valor */
            font-weight: bold; /* Cambia el grosor del texto */
            color: #f7760c; /* Cambia el color del texto */
        }
        [data-testid="stMetricLabel"] {
        font-size: 1.5rem; /* Cambia el tamaño del texto del label */
        color: #FFFFFF; /* Cambia el color del texto del label */
        }
        </style>
    """, unsafe_allow_html=True)
    

    # # Cargar la animación Lottie
    lottie_url ="https://lottie.host/d057d56c-37f1-4e41-86ee-b18bc4177110/yfFjsNUf6d.json"
    lottie_json = load_lottie_url(lottie_url)
    st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
    st.lottie(lottie_json, height=200, key="consigna")
    st.markdown("</div>", unsafe_allow_html=True)

    st.title("Resumen Datos")
    
    colum1, colum2, colum3 = st.columns(3)

    with colum1:
        st.metric(label=" :books: Consignaciones", value=consignaciones.shape[0])
    
    with colum2:
        st.metric(label=" :warning: Incidentes", value=incidentes.shape[0])
    
    with colum3:   
        st.metric(label=" :bar_chart: SAIDI", value=saidi.shape[0])
    

    st.subheader('Dashboard de consignaciones por zona')
    st.metric("Cantidad de datos en consignaciones", consignaciones.shape[0])  # Número de filas
    st.dataframe(consignaciones)
    st.subheader('Dashboard de incidentes por zona')
    st.metric("Cantidad de datos en Incidentes", incidentes.shape[0])  # Número de filas
    st.dataframe(incidentes)
    st.subheader('Dashboard de SAIDI por zona')
    st.metric("Cantidad de datos en SAIDI", saidi.shape[0])  # Número de filas
    st.dataframe(saidi)

    