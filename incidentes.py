
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

def incidentes(datos):
     # # Cargar la animación Lottie
    lottie_url ="https://lottie.host/2579f833-b415-4d91-b4a5-51da50e27882/bpUVUyMsgL.json"
    lottie_json = load_lottie_url(lottie_url)
    st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
    st.lottie(lottie_json, height=200, key="consigna")
    st.markdown("</div>", unsafe_allow_html=True)


    st.title('Resumen visual de Incidentes')
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
    #st.subheader('Incidentes actuales por zona')
    #st.dataframe(datos)

    st.subheader('Cantidad de Incidentes por zona')
    description_counts = datos.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')

    description_counts = description_counts.sort_values(by='count', ascending=False).head(10)

    st.dataframe(description_counts)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Pie chart in the first column
    with col1:
        fig_pie = px.pie(description_counts, values='count', names='SubregionName',title="Número de incidentes por zona")
        st.plotly_chart(fig_pie)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(description_counts, x='SubregionName', y='count', title="Número de incidentes por zona")
        st.plotly_chart(fig_bar)

    st.subheader('Dashboard de incidentes por zona')

    col1, col2, col3, col4 = st.columns(4)

    # Pie chart in the first column
    with col1:
        st.metric(label=description_counts['SubregionName'].iloc[0], value=description_counts['count'].iloc[0])
        grafico_torta(datos,description_counts['SubregionName'].iloc[0])

    with col2:
        st.metric(label=description_counts['SubregionName'].iloc[1], value=description_counts['count'].iloc[1])
        grafico_torta(datos,description_counts['SubregionName'].iloc[1])

    with col3:
        st.metric(label=description_counts['SubregionName'].iloc[2], value=description_counts['count'].iloc[2])
        grafico_torta(datos,description_counts['SubregionName'].iloc[2])

    with col4:
        st.metric(label=description_counts['SubregionName'].iloc[3], value=description_counts['count'].iloc[3])
        grafico_torta(datos,description_counts['SubregionName'].iloc[3])


 # Nuevo subheader para gráficos de donut

    col1, col2, col3, col4 = st.columns(4)

    # Donut charts for the top 5 substations
    with col1:
        grafico_donut(datos, description_counts['SubregionName'].iloc[0])

    with col2:
        grafico_donut(datos, description_counts['SubregionName'].iloc[1])

    with col3:
        grafico_donut(datos, description_counts['SubregionName'].iloc[2])

    with col4:
        grafico_donut(datos, description_counts['SubregionName'].iloc[3])

    
###------Cantidad de clientes afectados -------
    # Agrupar los datos por SubregionName y sumar la cantidad de usuarios afectados
    usuarios_afectados = datos.groupby('SubregionName')['NumCustomers'].sum().reset_index()

    st.dataframe(usuarios_afectados)

    # Crear el gráfico de barras
    fig_bar = px.bar(
        usuarios_afectados,
        x='SubregionName',  # Eje X: Subregiones
        y='NumCustomers',   # Eje Y: Usuarios afectados
        title="Usuarios afectados por subregión",
        labels={'SubregionName': 'Subregión', 'NumCustomers': 'Usuarios Afectados'},
        text='NumCustomers'  # Mostrar los valores en las barras
    )

    # Personalizar el diseño del gráfico
    fig_bar.update_traces(
        texttemplate='%{text:.2s}',  # Formato del texto en las barras
        textposition='outside'  # Mostrar valores fuera de las barras
    )
    fig_bar.update_layout(
        xaxis_title="Subregión",
        yaxis_title="Usuarios Afectados",
        xaxis_tickangle=-45,  # Rotar etiquetas del eje X para mejor legibilidad
        height=500,  # Altura del gráfico
        margin=dict(l=40, r=40, t=40, b=80)  # Márgenes del gráfico
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_bar)

# ----- Crear el gráfico de barras con colores de cantida de usuarios afectados por SubstationName
    fig_bar = px.bar(
        datos,
        x='SubregionName',  # Eje X: Subregiones
        y='NumCustomers',   # Eje Y: Usuarios afectados
        color='SubstationName',  # Colorear por SubstationName
        title="Usuarios afectados por subregión y subestación",
        labels={
            'SubregionName': 'Subregión',
            'NumCustomers': 'Usuarios Afectados',
            'SubstationName': 'Subestación'
        },
        text='NumCustomers'  # Mostrar los valores en las barras
    )

    # Personalizar el diseño del gráfico
    fig_bar.update_traces(
        texttemplate='%{text:.2s}',  # Formato del texto en las barras
        textposition='outside'  # Mostrar valores fuera de las barras
    )
    fig_bar.update_layout(
        xaxis_title="Subregión",
        yaxis_title="Usuarios Afectados",
        xaxis_tickangle=-45,  # Rotar etiquetas del eje X para mejor legibilidad
        height=600,  # Altura del gráfico
        margin=dict(l=40, r=40, t=40, b=80)  # Márgenes del gráfico
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_bar)

##----------
     # Agrupar los datos por FeederName y contar la cantidad de UID
    uid_por_feeder = datos.groupby('FeederName')['UID'].count().reset_index()
    uid_por_feeder = uid_por_feeder.sort_values(by='UID', ascending=False)  # Ordenar por cantidad de UID

    # Crear el gráfico de barras
    fig_bar = px.bar(
        uid_por_feeder,
        x='FeederName',  # Eje X: FeederName
        y='UID',         # Eje Y: Cantidad de UID
        title="Cantidad de UID por FeederName",
        labels={'FeederName': 'Nombre del Alimentador', 'UID': 'Cantidad de UID'},
        text='UID'  # Mostrar los valores en las barras
    )

    # Personalizar el diseño del gráfico
    fig_bar.update_traces(
        texttemplate='%{text}',  # Mostrar los valores exactos en las barras
        textposition='outside'  # Mostrar valores fuera de las barras
    )

    
    fig_bar.update_layout(
        xaxis_title="Nombre del Alimentador",
        yaxis_title="Cantidad de UID",
        xaxis_tickangle=-45,  # Rotar etiquetas del eje X para mejor legibilidad
        height=600,  # Altura del gráfico
        margin=dict(l=40, r=40, t=40, b=80)  # Márgenes del gráfico
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_bar)
#------grafico treemap
    # Agrupar los datos por FeederName y contar la cantidad de UID
    uid_por_feeder = datos.groupby('FeederName')['UID'].count().reset_index()
    uid_por_feeder = uid_por_feeder.sort_values(by='UID', ascending=False)  # Ordenar por cantidad de UID

    # Crear el gráfico de Treemap
    fig_treemap = px.treemap(
        uid_por_feeder,
        path=['FeederName'],  # Jerarquía: FeederName
        values='UID',         # Tamaño de las cajas basado en la cantidad de UID
        title="Cantidad de incidentes por circuito",
        labels={'FeederName': 'Nombre del Alimentador', 'UID': 'Cantidad de UID'}
    )

    # Personalizar el diseño del Treemap
    fig_treemap.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),  # Márgenes del gráfico
        height=600  # Altura del gráfico
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_treemap)


    




def grafico_torta(datos,zona):
    # Filtrar los datos para "Tolima Norte"
    data = datos[datos['SubregionName'] == zona]

    # Agrupar los datos por estadoConsignacion y contar
    estado_counts = data.groupby('EstadoInc')['EstadoInc'].count().reset_index(name='count')


    # Crear el gráfico de torta
    fig_pie = px.pie(
        estado_counts,
        values='count',
        names='EstadoInc',
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
    st.plotly_chart(fig_pie)
    

def grafico_donut(datos, zona):
    # Filtrar los datos para la zona especificada
    zona_data = datos[datos['SubregionName'] == zona]

    #st.dataframe(zona_data)
    # Agrupar los datos por EstadoConsignacion y contar
    estado_counts = zona_data.groupby('EstadoInc')['EstadoInc'].count().reset_index(name='count')
    #st.dataframe(estado_counts)

    # Verificar si hay filas con 'Pendiente'
    if not estado_counts[estado_counts['EstadoInc'] == 'Pendiente'].empty:
        consignaciones_iniciadas = estado_counts[estado_counts['EstadoInc'] == 'Pendiente'].iloc[0]
        count_iniciadas = consignaciones_iniciadas['count']
    else:
        count_iniciadas = 0
        consignaciones_iniciadas = {'EstadoInc': 'Pendiente', 'count': 0}

    # Mostrar la métrica
    #st.metric(label="Incidentes Pendientes", value=count_iniciadas)

    
    # Crear el gráfico de donut
    fig_donut = px.pie(
        estado_counts,
        values='count',
        names='EstadoInc',
        hole=0.7,  # Crear el efecto de donut
    )

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