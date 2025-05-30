import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
import utils

color_map = {
        'Naraja': '#D5752D',  
        'Gris': '#59595B',  # Blanco
        'Azul': '#13A2E1', 
        'Verde': '#00BE91',
        'Amarillo': '#FFF65E',
        'Azul oscuro': '#003FA2',
        'Rojo': '#CA0045',
    }
#####  funcion para importarn animaciones ######
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def incidentes(datos):

    # Cargamos archivo de estilos
    utils.local_css('estilo.css')

#--------------  Incidentes animación y titulo  ------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        # # Cargar la animación Lottie
        lottie_url ="https://lottie.host/2579f833-b415-4d91-b4a5-51da50e27882/bpUVUyMsgL.json"
        lottie_json = load_lottie_url(lottie_url)
        st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
        st.lottie(lottie_json, height=200, key="consigna")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.title('')
        st.markdown("<div class='centered-title'><h1>Incidentes</h1></div>", unsafe_allow_html=True)

#--------------  Tabla de incidentes en el sistema por sector  ------------------------------------
    st.subheader('Cantidad de Incidentes por zona')
    description_counts = datos.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')
    description_counts = description_counts.sort_values(by='count', ascending=False).head(10)
    st.dataframe(description_counts)

#-------------- Grafico de tipo dona donde se muestran los incidentes por zona --------------------
    st.title("Incidentes por zona")
    # Crear el gráfico de donut
    fig_donut = px.pie(
        description_counts,
        values='count',
        names='SubregionName',
        hole=0.5,  # Crear el efecto de donut
        color='SubregionName',
        color_discrete_map=color_map
    )

     # Configurar el gráfico para mostrar valores absolutos
    fig_donut.update_traces(
        textinfo='value',  # Mostrar valores absolutos en lugar de porcentajes
        hoverinfo='label+value',  # Mostrar etiqueta y valor al pasar el cursor
        textposition='inside',  # Posición del texto dentro de las secciones
        textfont_size=30
    )
    # Configurar la posición de la leyenda fuera del gráfico
    fig_donut.update_layout(
        legend=dict(
            orientation="v",  # Horizontal
            yanchor="middle",  # Anclar en la parte inferior
            y=0.5,  # Posición vertical (debajo del gráfico)
            xanchor="left",  # Centrar horizontalmente
            x=1,  # Posición horizontal (centro)
            font=dict(
                size=30           # Tamaño de fuente de la leyenda
            )
        ),

    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_donut)

#--------------  Grafico de incidentes por zona tipo torta y barras ------------------------------------

    # Create two columns for layout
    col1, col2 = st.columns(2)


    # Pie chart in the first column
    with col1:
        fig_pie = px.pie(description_counts, 
                         values='count', 
                         names='SubregionName',
                         title="",
                         color='SubregionName',
                        color_discrete_map=color_map)
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(fig_pie)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(description_counts, 
                         x='SubregionName', 
                         y='count', 
                         title="",
                         color='SubregionName',  # Colorea cada barra diferente
                        labels={'SubregionName': 'Zona', 'count': 'Cantidad de Incidentes'},
                        color_discrete_map=color_map,
    )
    
        fig_bar.update_layout(
                font=dict(size=50),  # <-- Aumenta el tamaño general de los textos (ejes, leyenda)
                xaxis_title_font=dict(size=20),  # Tamaño del título del eje X
                yaxis_title_font=dict(size=20),  # Tamaño del título del eje Y
        )
        
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar)

#--------------  Metricas de estados de incidentes y zonas  ------------------------------------
    st.subheader('Dashboard de Estado de incidentes por zona')

    #col1, col2, col3, col4 = st.columns(4)
    EstadoInc_counts = datos.groupby('EstadoInc')['SubregionName'].count().reset_index(name='count')
    EstadoInc_counts = EstadoInc_counts.sort_values(by='count', ascending=False)
    #st.dataframe(EstadoInc_counts)

    # Agrupa por SubregionName y EstadoInc, y cuenta la cantidad de incidentes en cada combinación
    estado_por_subregion = datos.groupby(['SubregionName', 'EstadoInc']).size().reset_index(name='count')

    # Opcional: mostrar la tabla en Streamlit
    #st.dataframe(estado_por_subregion)

    # Obtén las subregiones únicas que quieres graficar
    subregiones = estado_por_subregion['SubregionName'].unique()
    num_columns = len(subregiones)
    columns = st.columns(num_columns)  # Crear tantas columnas como subregiones existan

    # graficos de pie
    for i, subregion in enumerate(subregiones):
        with columns[i]:
            st.subheader(subregion)
            grafico_torta(datos, subregion, key=f"Estado_Incidentes_{i}")
 
#--------------  Metricas de total de incidentes y zonas  ------------------------------------
    st.subheader('Dashboard de incidentes por zona')

    #col1, col2, col3, col4 = st.columns(4)

      # Crear columnas dinámicamente
    num_columns = len(description_counts)  # Número de columnas necesarias
    total = description_counts['count'].sum()
    st.metric(label="Total de incidentes", value=total)

    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan

    # graficos de pie
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubregionName'], value=row['count'])
            grafico_torta(datos,row['SubregionName'], key=f"grafico_torta_{i}")
            st.plotly_chart(gauge_chart(row['count'], row['SubregionName'],min_val=0, max_val=total), use_container_width=True)

     # graficos de donut
    for i, row in description_counts.iterrows():
        with columns[i]:
            st.metric(label=row['SubregionName'], value=row['count'])
            grafico_donut(datos,row['SubregionName'], key=f"grafico_donut_{i}")

    
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


    




def grafico_torta(datos,zona, key):
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
    st.plotly_chart(fig_pie, key=key)
    

def grafico_donut(datos, zona, key):
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
    st.plotly_chart(fig_donut, key=key)



def gauge_chart(value, titulo="SAIDI", min_val=0, max_val=100):
    """
    Crea un gráfico de tipo gauge (indicador).

    Parámetros:
    - value: Valor actual que se mostrará en el indicador.
    - titulo: Título del gráfico.
    - min_val: Valor mínimo del rango del indicador.
    - max_val: Valor máximo del rango del indicador.

    Retorna:
    - fig: Objeto de tipo Plotly Figure con el gráfico de gauge.
    """
    # Crear el gráfico de gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",  # Modo: indicador con número
        value=value,  # Valor actual
        title={'text': titulo},  # Título del gráfico
        domain={'x': [0, 1], 'y': [0, 1]},  # Posición del gráfico
        gauge={
            'axis': {'range': [min_val, max_val]},  # Rango del eje
            'bar': {'color': "red"},  # Color de la barra
            'bgcolor': "white",  # Color de fondo
            'steps': [
                {'range': [min_val, (max_val - min_val) * 0.5 + min_val], 'color': "green"},  # Rango bajo
                {'range': [(max_val - min_val) * 0.5 + min_val, (max_val - min_val) * 0.75 + min_val], 'color': "yellow"},  # Rango medio
                {'range': [(max_val - min_val) * 0.75 + min_val, max_val], 'color': "red"}  # Rango alto
            ]
        }
    ))
    return fig