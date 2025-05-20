import streamlit as st
import pandas as pd
import plotly.express as px

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
import utils

#####  funcion para importarn animaciones ######
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def resumen(consignaciones,incidentes,saidi):

    utils.local_css('estilo.css')
    
    col1, col2 = st.columns([1,3])
    with col1:
        # # Cargar la animación Lottie
        lottie_url ="https://lottie.host/d057d56c-37f1-4e41-86ee-b18bc4177110/yfFjsNUf6d.json"
        lottie_json = load_lottie_url(lottie_url)
        st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
        st.lottie(lottie_json, height=200, key="consigna")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.title('')
        st.markdown("<div class='centered-title'><h1>Resumen Datos</h1></div>", unsafe_allow_html=True)

    
    colum1, colum2, colum3 = st.columns(3)

    with colum1:
        st.metric( label=":books: Consignaciones ",value=consignaciones.shape[0])
    
    with colum2:
        st.metric(label=" :warning: Incidentes ", value=incidentes.shape[0])
    
    with colum3:   
        st.metric(label=" :bar_chart: SAIDI ", value=saidi.shape[0])
    

    st.subheader('Dashboard de consignaciones por zona')
    st.metric("Cantidad de datos en consignaciones", consignaciones.shape[0])  # Número de filas
    

    description_counts = consignaciones.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
    
    num_columns = len(description_counts)  # Número de columnas necesarias
    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan

    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubstationName'], value=row['count'])
    st.dataframe(consignaciones)

    st.subheader('Dashboard de incidentes por zona')
    st.metric("Cantidad de datos en Incidentes", incidentes.shape[0])  # Número de filas

    description_counts = incidentes.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')
      # Crear columnas dinámicamente
    num_columns = len(description_counts)  # Número de columnas necesarias
    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan
    # graficos de pie
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubregionName'], value=row['count'])
            
    st.dataframe(incidentes)


    st.subheader('Dashboard de SAIDI por zona')

#limpieza de datos
    # ------------- limpieza de los datos y coerencia
    # Limpiar la columna SAIDI (cambia comas por puntos, elimina espacios inicio final)
    saidi['SAIDI'] = saidi['SAIDI'].astype(str).str.replace(',', '.').str.strip()
    saidi['SAIDI'] = pd.to_numeric(saidi['SAIDI'], errors='coerce')
    saidi['SAIDI'] = saidi['SAIDI'].fillna(0)

    # ------------- Mostrar el DataFrame actualizado
    #st.dataframe(datos)

    st.metric("Cantidad de datos en SAIDI", saidi.shape[0])  # Número de filas
    
    description_counts = saidi.groupby('SubregionName')['SAIDI'].sum().reset_index(name='count')
    num_columns = len(description_counts)  # Número de columnas necesarias
    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan
    # graficos de pie
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubregionName'], value=row['count'])
    
    
    st.dataframe(saidi)

    