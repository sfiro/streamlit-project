import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import altair as alt

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

def consignaciones(datos):
    
    datos['SubstationName'] = datos['SubstationName'].replace('ISLAS', 'TRANSMISION ANALISIS')
    # Convertir StartDateTime a tipo datetime
    if 'StartDateTime' in datos.columns:
        datos['StartDateTime'] = pd.to_datetime(datos['StartDateTime'])
        # Filtrar consignaciones cuyo StartDateTime es hoy (fecha del sistema)
        hoy = pd.Timestamp.now().date()
        consignaciones_hoy = datos[datos['StartDateTime'].dt.date == hoy]
    
    utils.local_css('estilo.css')

# ------------------------------ Animación y Titulo de la pagina  -----------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        # # Cargar la animación Lottie
        lottie_url ="https://lottie.host/395bdf05-eaae-44c1-8c97-e27afbea5abd/hoMc41cPw0.json"
        lottie_json = load_lottie_url(lottie_url)
        st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
        st.lottie(lottie_json, height=200, key="consigna")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.title('')
        st.markdown("<div class='centered-title'><h1>Consignaciones</h1></div>", unsafe_allow_html=True)

# ------------------------------ Tabla de consignaciones por zona  -----------------------------------------
    st.subheader('Cantidad de consignaciones por zona')
    description_counts = datos.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
    description_counts = description_counts.sort_values(by='count', ascending=False).head(10)
    st.dataframe(description_counts)


# ------------------------------ Graficos de consignaciones por zona  -----------------------------------------
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

# ------------------------------ Tabla de consignaciones  -----------------------------------------
    st.subheader('Dashboard de consignaciones por zona')
    st.dataframe(datos)


# ------------------------------ GRaficos de torta cantidad de consignaciones por zona y estado  -----------------------------------------
    # Crear columnas dinámicamente
    num_columns = len(description_counts)  # Número de columnas necesarias
    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan

    # Nuevo subheader para gráficos de torta
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubstationName'], value=row['count'])
            grafico_torta(datos, row['SubstationName'], key="grafico_torta_" + str(i))

# ------------------------------ GRaficos de donut cantidad de consignaciones por zona y estado  -----------------------------------------
    # Nuevo subheader para gráficos de donut
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubstationName'], value=row['count'])
            grafico_donut(datos, row['SubstationName'], key="grafico_donut_" + str(i))


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
    

def grafico_donut(datos, zona, key):
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
    if "Iniciadas" in estado_counts['EstadoConsignacion'].values:
        # Existe el estado "Iniciadas"
        consignaciones_iniciadas = int(estado_counts[estado_counts['EstadoConsignacion'] == 'Iniciadas']['count'].iloc[0])
    else:
        consignaciones_iniciadas = 0
        


    # Agregar texto interno al gráfico
    fig_donut.update_traces(
        textinfo='none',  # Ocultar etiquetas en las secciones
        hoverinfo='label+percent',  # Mostrar información al pasar el cursor
        textposition='inside',
        textfont_size=14,
        text=[f"{consignaciones_iniciadas}"]
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
                text=f"<b>{consignaciones_iniciadas}</b>",  # Texto en el centro del donut
                x=0.5,  # Posición horizontal (centro del gráfico)
                y=0.5,  # Posición vertical (centro del gráfico)
                font_size=60,  # Tamaño de la fuente
                showarrow=False  # Sin flecha
            )
        ]

    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_donut, key=key)