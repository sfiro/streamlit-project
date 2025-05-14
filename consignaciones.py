
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import altair as alt

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

def consignaciones(datos):

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
    lottie_url ="https://lottie.host/6a17c74e-dca5-429a-a173-fdff3fa7942a/I7BnuU8RrT.json"
    lottie_json = load_lottie_url(lottie_url)
    st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
    st.lottie(lottie_json, height=200, key="consigna")
    st.markdown("</div>", unsafe_allow_html=True)

    st.title('Resumen visual de Consignaciones')

    st.subheader('Cantidad de consignaciones por zona')
    description_counts = datos.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')

    description_counts = description_counts.sort_values(by='count', ascending=False).head(10)

    st.dataframe(description_counts)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Pie chart in the first column
    with col1:
        fig_pie = px.pie(description_counts, values='count', names='SubstationName',title="Número de consignaciones por zona")
        st.plotly_chart(fig_pie)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(description_counts, x='SubstationName', y='count', title="Número de consignaciones por zona")
        st.plotly_chart(fig_bar)

    st.subheader('Dashboard de consignaciones por zona')

    st.dataframe(datos)

    col1, col2, col3, col4, col5 = st.columns(5)

    # Pie chart in the first column
    with col1:
        st.metric(label=description_counts['SubstationName'].iloc[0], value=description_counts['count'].iloc[0])
        grafico_torta(datos, description_counts['SubstationName'].iloc[0], key="grafico_torta_1")

    with col2:
        st.metric(label=description_counts['SubstationName'].iloc[1], value=description_counts['count'].iloc[1])
        grafico_torta(datos, description_counts['SubstationName'].iloc[1], key="grafico_torta_2")

    with col3:
        st.metric(label=description_counts['SubstationName'].iloc[2], value=description_counts['count'].iloc[2])
        grafico_torta(datos, description_counts['SubstationName'].iloc[2], key="grafico_torta_3")

    with col4:
        st.metric(label=description_counts['SubstationName'].iloc[3], value=description_counts['count'].iloc[3])
        grafico_torta(datos, description_counts['SubstationName'].iloc[3], key="grafico_torta_4")

    with col5:
        st.metric(label=description_counts['SubstationName'].iloc[4], value=description_counts['count'].iloc[4])
        grafico_torta(datos, description_counts['SubstationName'].iloc[4], key="grafico_torta_5")



 # Nuevo subheader para gráficos de donut

    col1, col2, col3, col4, col5 = st.columns(5)

    # Donut charts for the top 5 substations
    with col1:
        grafico_donut(datos, description_counts['SubstationName'].iloc[0])

    with col2:
        grafico_donut(datos, description_counts['SubstationName'].iloc[1])

    with col3:
        grafico_donut(datos, description_counts['SubstationName'].iloc[2])

    with col4:
        grafico_donut(datos, description_counts['SubstationName'].iloc[3])

    with col5:
        grafico_donut(datos, description_counts['SubstationName'].iloc[4])




def grafico_torta(datos,zona,key):
    # Filtrar los datos para "Tolima Norte"
    data = datos[datos['SubstationName'] == zona]

    # Agrupar los datos por estadoConsignacion y contar
    estado_counts = data.groupby('EstadoConsignacion')['EstadoConsignacion'].count().reset_index(name='count')

    # Crear el gráfico de torta
    fig_pie = px.pie(
        estado_counts,
        values='count',
        names='EstadoConsignacion',
        #title= zona
    )
    # Quitar las etiquetas de los colores (leyenda)
    #fig_pie.update_layout(showlegend=False)

    # Configurar la posición de la leyenda fuera del gráfico
    fig_pie.update_layout(
        legend=dict(
            orientation="h",  # Horizontal
            yanchor="bottom",  # Anclar en la parte inferior
            y=-0.2,  # Posición vertical (debajo del gráfico)
            xanchor="center",  # Centrar horizontalmente
            x=0.5  # Posición horizontal (centro)
        )
    )
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_pie, key=key)
    

def grafico_donut(datos, zona):
    # Filtrar los datos para la zona especificada
    zona_data = datos[datos['SubstationName'] == zona]

    # Agrupar los datos por EstadoConsignacion y contar
    estado_counts = zona_data.groupby('EstadoConsignacion')['EstadoConsignacion'].count().reset_index(name='count')

    #st.dataframe(estado_counts)
    # Crear el gráfico de donut
    fig_donut = px.pie(
        estado_counts,
        values='count',
        names='EstadoConsignacion',
        hole=0.7,  # Crear el efecto de donut
    )

    # Calcular la cantidad de consignaciones iniciadas
    consignaciones_iniciadas = estado_counts[estado_counts['EstadoConsignacion'] == 'Iniciadas'].loc[0]

    # Agregar texto interno al gráfico
    fig_donut.update_traces(
        textinfo='none',  # Ocultar etiquetas en las secciones
        hoverinfo='label+percent',  # Mostrar información al pasar el cursor
        textposition='inside',
        textfont_size=14,
        text=[f"{consignaciones_iniciadas['count']}"]
    )

    # Configurar la posición de la leyenda fuera del gráfico
    fig_donut.update_layout(
        legend=dict(
            orientation="h",  # Horizontal
            yanchor="bottom",  # Anclar en la parte inferior
            y=-0.2,  # Posición vertical (debajo del gráfico)
            xanchor="center",  # Centrar horizontalmente
            x=0.5  # Posición horizontal (centro)
        ),
        annotations=[
            dict(
                text=f"<b>{consignaciones_iniciadas['count']}</b>",  # Texto en el centro del donut
                x=0.5,  # Posición horizontal (centro del gráfico)
                y=0.5,  # Posición vertical (centro del gráfico)
                font_size=60,  # Tamaño de la fuente
                showarrow=False  # Sin flecha
            )
        ]

    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_donut)