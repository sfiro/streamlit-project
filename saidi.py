
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd

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

def saidi(datos):
    # # Cargar la animación Lottie
    lottie_url ="https://lottie.host/dd1f24a2-7702-4f57-81ec-67f5d048e457/b1oz4hndQO.json"
    lottie_json = load_lottie_url(lottie_url)
    st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
    st.lottie(lottie_json, height=200, key="consigna")
    st.markdown("</div>", unsafe_allow_html=True)


    st.title("Resumen visual de SAIDI")
    
    #st.dataframe(datos)

    # ------------- limpieza de los datos y coerencia
    # Limpiar la columna SAIDI (cambia comas por puntos, elimina espacios inicio final)
    datos['SAIDI'] = datos['SAIDI'].astype(str).str.replace(',', '.').str.strip()
    datos['SAIDI'] = pd.to_numeric(datos['SAIDI'], errors='coerce')
    datos['SAIDI'] = datos['SAIDI'].fillna(0)

    # ------------- Mostrar el DataFrame actualizado
    #st.dataframe(datos)


    fig_bar = px.bar(datos, x='UID', y='SAIDI', color='SubregionName', title="Incidentes impacto SAIDI por zona")
    st.plotly_chart(fig_bar)


    data_vnorte =  datos[datos['SubregionName'] == 'VALLE NORTE']
    data_vsur = datos[datos['SubregionName'] == 'VALLE SUR']
    data_tnorte = datos[datos['SubregionName'] == 'TOLIMA NORTE']
    data_tsur = datos[datos['SubregionName'] == 'TOLIMA SUR']

    data_vnorte = data_vnorte.sort_values(by='SAIDI', ascending=False).head(5)
    fig_bar = px.bar(data_vnorte, y='UID', x='SAIDI',orientation='h', title="Valle norte Incidentes impacto SAIDI")
    st.plotly_chart(fig_bar)

    data_vsur = data_vsur.sort_values(by='SAIDI', ascending=False).head(5)
    fig_bar = px.bar(data_vsur, y='UID', x='SAIDI',orientation='h', title="Valle sur Incidentes impacto SAIDI")
    st.plotly_chart(fig_bar)

    data_tnorte = data_tnorte.sort_values(by='SAIDI', ascending=False).head(5)
    fig_bar = px.bar(data_tnorte, y='UID', x='SAIDI',orientation='h', title="Tolima norte Incidentes impacto SAIDI")
    st.plotly_chart(fig_bar)

    data_tsur = data_tsur.sort_values(by='SAIDI', ascending=False).head(5)
    fig_bar = px.bar(data_tsur, y='UID', x='SAIDI',orientation='h', title="Tolima sur Incidentes impacto SAIDI")
    st.plotly_chart(fig_bar)



    ### treemap

    #uid_por_zona = datos.groupby('SubregionName')['SAIDI'].sum()
    #uid_por_zona = uid_por_zona.sort_values(by='SAIDI', ascending=False)  # Ordenar por cantidad de UID

    # Crear el gráfico de Treemap
    fig_treemap = px.treemap(
        datos,
        path=['SubregionName'],  # Jerarquía: FeederName
        values='SAIDI',         # Tamaño de las cajas basado en la cantidad de UID
        title="Impacto de SAIDI por zona"
    )

    # Personalizar el diseño del Treemap
    fig_treemap.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),  # Márgenes del gráfico
        height=600  # Altura del gráfico
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_treemap)


