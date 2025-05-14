import streamlit as st
import pandas as pd
import plotly.express as px

def resumen(datos):

    # resumen de señales en tres columnas
    st.subheader('Resumen de Señales')

    total_records = len(datos)
    num_substations = datos['substationName'].nunique()
    num_devices = datos['deviceName'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total de Registros", value=total_records)

    with col2:
        st.metric(label="Subestaciones", value=num_substations)

    with col3:
        st.metric(label="Dispositivos", value=num_devices)


# Grafico de barras de cantidad de señales por zona
    st.subheader('Cantidad de señales por zona y circuito')
    x_axis = datos["subregionName"]
    y_axis = datos["description"]
    grafico = px.bar(datos, x="subregionName", y="description", color="feederName", title = "Cantidad de señales por Zona")
    st.plotly_chart(grafico)
