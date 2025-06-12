import streamlit as st
import pandas as pd
import plotly.express as px

import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON
import altair as alt
from streamlit_lottie import st_lottie
import utils
import plotly.graph_objects as go

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

def dashboard(consignaciones,incidentes,saidi):
    # Cargamos archivo de estilos
    utils.local_css('estilo.css')
    
    # ------------ Título -----------------
    #col1, col2 = st.columns([1,3])
    #with col1:
    #    # # Cargar la animación Lottie
    #    lottie_url ="https://lottie.host/ee49ee8b-a13d-40bc-aade-3cde94a58a28/kOexocr7It.json"
    #    lottie_json = load_lottie_url(lottie_url)
    #    st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
    #    st.lottie(lottie_json, height=200, key="consigna")
    #    st.markdown("</div>", unsafe_allow_html=True)
    #with col2:
    #    st.title('')
    #    st.markdown("<div class='centered-title'><h1>Dashboard</h1></div>", unsafe_allow_html=True)

    # ------------ Resumen de datos -----------------
    # colum1, colum2, colum3 = st.columns(3)

    # with colum1:
    #     st.metric( label=":books: Consignaciones ",value=consignaciones.shape[0])
    
    # with colum2:
    #     st.metric(label=" :warning: Incidentes ", value=incidentes.shape[0])
    
    # with colum3:   
    #     st.metric(label=" :bar_chart: SAIDI ", value=saidi.shape[0])

    # ------------ Gráficos Incidentes -----------------
    #st.title('Incidentes')

    incidentes['SubregionName'] = incidentes['SubregionName'].replace('VALLE NORTE', 'Vn')
    incidentes['SubregionName'] = incidentes['SubregionName'].replace('VALLE SUR', 'Vs')
    incidentes['SubregionName'] = incidentes['SubregionName'].replace('TOLIMA NORTE', 'Tn')
    incidentes['SubregionName'] = incidentes['SubregionName'].replace('TOLIMA SUR', 'Ts')

    incidentesScada =  incidentes[incidentes['Origen'] == 'SCADACreated']
    incidentesLlamadas =  incidentes[incidentes['Origen'] == 'PhoneCallCreated']

    colum1, colum2, colum3, colum4 = st.columns(4)
    with colum1:
        incidentes_subregion_llamadas = incidentesLlamadas.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')
        incidentes_subregion_llamadas = incidentes_subregion_llamadas.sort_values(by='count', ascending=False)
        st.metric( label=":phone: Llamadas ",value=incidentesLlamadas.shape[0])
        if not incidentesLlamadas.empty:
            incidentesRadar(incidentes_subregion_llamadas, titulo="")

    with colum2:
        st.metric( label=" :zap: SCADA ",value=incidentesScada.shape[0])

        num_subregiones = incidentesScada['SubregionName'].nunique()
        incidentes_subregion_scada = incidentesScada.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')
        incidentes_subregion_scada = incidentes_subregion_scada.sort_values(by='count', ascending=False)

        if num_subregiones > 2:
            if  not incidentesScada.empty:
                incidentesRadar(incidentes_subregion_scada, titulo="")
        else:
            incidentesDonut(incidentes_subregion_scada, titulo="")  

    with colum3:
        st.metric(label=" :books: Consignaciones ", value=consignaciones.shape[0])
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('ISLAS', 'Tr')
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('TRANSMISION ANALISIS', 'Tr')
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('TOLIMA NORTE', 'Tn')
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('TOLIMA SUR', 'Ts')
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('VALLE NORTE', 'Vn')
        consignaciones['SubstationName'] = consignaciones['SubstationName'].replace('VALLE SUR', 'Vs')

        consignaciones_hoy = consignaciones
        if not consignaciones_hoy.empty:
            consignacionesRadar(consignaciones_hoy, titulo="")

    with colum4:
        st.metric(label=" :warning: SAIDI ", value=saidi.shape[0])
        usuarios_afectados = incidentes.groupby('SubregionName')['NumCustomers'].sum().reset_index()
        
        if not usuarios_afectados.empty:
            usuariosRadar(usuarios_afectados, titulo="Usuarios")


    # if  not incidentesScada.empty:
    #     incidentesGrafico(incidentesScada, "Incidentes SCADA")
    #     incidentesRadar(incidentesScada, titulo="Incidentes por Scada")

    # if not incidentesLlamadas.empty:
    #     incidentesGrafico(incidentesLlamadas, "Incidentes Llamadas")
    #     incidentesRadar(incidentesLlamadas, titulo="Incidentes llamadas")




#----------------Metricas y graficos -------------------------

    # colum1, colum2, colum3, colum4 = st.columns(4)
    # with colum1:
    #     st.metric( label=":books: Incidentes SCADA ",value=incidentesScada.shape[0])
    # with colum2:
    #     st.metric( label=":phone: Incidentes Llamadas ",value=incidentesLlamadas.shape[0])
    # with colum3:
    #     st.metric(label=" :warning: Consignaciones ", value=consignaciones.shape[0])
    # with colum4:
    #     st.metric(label=" :bar_chart: SAIDI ", value=saidi.shape[0])

    # if  not incidentesScada.empty:
    #     incidentesGrafico(incidentesScada, "Incidentes SCADA")
    #     incidentesRadar(incidentesScada, titulo="Incidentes por Scada")

    # if not incidentesLlamadas.empty:
    #     incidentesGrafico(incidentesLlamadas, "Incidentes Llamadas")
    #     incidentesRadar(incidentesLlamadas, titulo="Incidentes llamadas")
    
    # ------------ Gráficos consignaciones -----------------
    #st.title('Consignaciones')

    # Seleccion de consignaciones por fecha dia actual 

#     if 'StartDateTime' in consignaciones.columns:
#         consignaciones['StartDateTime'] = pd.to_datetime(consignaciones['StartDateTime'])
#         # Filtrar consignaciones cuyo StartDateTime es hoy (fecha del sistema)
#         hoy = pd.Timestamp.now().date()
#         consignaciones_hoy = consignaciones[consignaciones['StartDateTime'].dt.date == hoy]
    
#     #consignaciones_hoy = consignaciones   

#     if consignaciones_hoy.empty:
#         st.warning("No hay consignaciones para mostrar.")
#     else:
#         consignaciones_hoy['SubstationName'] = consignaciones_hoy['SubstationName'].replace('ISLAS', 'TRANSMISION ANALISIS')
#         description_counts = consignaciones_hoy.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
#         description_counts = description_counts.sort_values(by='count', ascending=False)

        
#         total = description_counts['count'].sum()
#         #st.metric(label="Total consignaciones", value=total)
#         st.title('Consignaciones'+ f" ({total})")
#         num_columns = len(description_counts)  # Número de columnas necesarias
#         columns = st.columns(num_columns)  # Crear tantas columnas como datos existan

#         # Nuevo subheader para gráficos de donut
#         for i, row in description_counts.iterrows():
#             with columns[i]:
#                 #st.metric(label=row['SubstationName'], value=row['count'])
#                 #grafico_donut(consignaciones, row['SubstationName'])
#                 st.plotly_chart(gauge_chart(row['count'], row['SubstationName'],
#                                             min_val=0, 
#                                             max_val=total), 
#                                             use_container_width=True,
#                                             key=f"gauge_{row['SubstationName']}")
                
#         consignacionesRadar(consignaciones_hoy, titulo="Consignaciones por zona")

    
    

# #--------------  Total de clientes afectados ------------------------------------
#     usuarios_afectados = incidentes.groupby('SubregionName')['NumCustomers'].sum().reset_index()
#     #st.dataframe(usuarios_afectados)
#     num_columns = len(usuarios_afectados)  # Número de columnas necesarias
#     total = usuarios_afectados['NumCustomers'].sum()
#     #st.metric(label="Total clientes afectados", value=total)
#     st.title('Clientes Afectados'+ f" ({total})")
#     columns = st.columns(num_columns)  # Crear tantas columnas como datos existan
#      # graficos de donut
#     for i, row in usuarios_afectados.iterrows():
#         with columns[i]:
#             #st.metric(label=row['SubregionName'], value=row['count'])
#             st.plotly_chart(gauge_chart(row['NumCustomers'], row['SubregionName'],min_val=0, max_val=total), use_container_width=True)

#     usuariosRadar(usuarios_afectados, titulo="Usuarios Afectados por Subregión")



def incidentesGrafico(datos, titulo="Incidentes"):
    # crea la grafica de incidentes dependiendo los datos filtrados
    inc = datos.groupby('SubregionName')['SubregionName'].count().reset_index(name='count')
    inc = inc.sort_values(by='count', ascending=False)

    num_columns = len(inc)  # Número de columnas necesarias
    total = inc['count'].sum()
    #st.metric(label=titulo, value=total)
    st.title(titulo + f" ({total})")

    columns = st.columns(num_columns)  # Crear tantas columnas como datos existan
     # graficos de donut
    for i, row in inc.iterrows():
        with columns[i]:
            #st.metric(label=row['SubregionName'], value=row['count'])
            st.plotly_chart(gauge_chart(row['count'], row['SubregionName'],min_val=0, max_val=total), use_container_width=True)


def grafico_donut(datos, zona):
    # Filtrar los datos para la zona especificada
    zona_data = datos[datos['SubstationName'] == zona]

    # Agrupar los datos por EstadoConsignacion y contar
    estado_counts = zona_data.groupby('EstadoConsignacion')['EstadoConsignacion'].count().reset_index(name='count')

    # Definir un mapa de colores para los estados
    color_map = {
        'Iniciadas': '#13A2E1',  
        'Sin Activar': '#59595B',  # Blanco
        'Pendientes': '#13A2E1', 
        'Canceladas': '#13A2E1', 
    }
    # Crear el gráfico de donut
    fig_donut = px.pie(
        estado_counts,
        values='count',
        names='EstadoConsignacion',
        hole=0.7,  # Crear el efecto de donut
        color='EstadoConsignacion',  # Columna para asignar colores
        color_discrete_map=color_map  # Mapa de colores definido
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
            'bar': {'color': color_map['Rojo']},  # Color de la barra
            'bgcolor': "white",  # Color de fondo
            'steps': [
                {'range': [min_val, (max_val - min_val) * 0.5 + min_val], 'color':color_map['Verde']},  # Rango bajo
                {'range': [(max_val - min_val) * 0.5 + min_val, (max_val - min_val) * 0.75 + min_val], 'color': color_map['Amarillo']},  # Rango medio
                {'range': [(max_val - min_val) * 0.75 + min_val, max_val], 'color': color_map['Rojo']}  # Rango alto
            ]
        }
    ))
    return fig

def incidentesDonut(datos, titulo="Incidentes por Subregión"):
    fig_donut = px.pie(
        datos,
        values='count',
        names='SubregionName',
        hole=0.6,  # Crear el efecto de donut
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
        width=80,
        height=380,
        title=dict(
            text="",  # Cambia el texto por el título que desees
            font=dict(size=30, color='#D5752D'),
            x=0.5,  # Centrado
            xanchor='center'
        ),
        legend=dict(
            orientation="h",  # Horizontal
            yanchor="bottom",  # Anclar en la parte inferior
            y=-0.2,  # Posición vertical (debajo del gráfico)
            xanchor="center",  # Centrar horizontalmente
            x=0.5,  # Posición horizontal (centro)
            font=dict(
                size=18           # Tamaño de fuente de la leyenda
            )
        ),
    )
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_donut)

def incidentesRadar(inc, titulo="Incidentes por Subregión"):
    # Agrupa los datos por subregión y cuenta los incidentes

    # Prepara los datos para el radar
    categorias = inc['SubregionName'].tolist()
    valores = inc['count'].tolist()
    # Para cerrar el radar, repetimos el primer valor al final
    categorias += [categorias[0]]
    valores += [valores[0]]

    #print(categorias, valores)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name=titulo,
        marker=dict(color='#13A2E1'),
        line=dict(width=3)
    ))
    
    dtick=3,  # Ticks entero
    if max(valores) >= 20:  # Solo si el valor máximo es mayor a 10
        dtick=int(max(valores)/5)  # <-- Solo ticks enteros

    fig.update_layout(
        width=300,
        height=400,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, max(valores)],
                tickfont=dict(size=20),
                dtick=dtick,  # Ajuste de los ticks
            ),
            angularaxis=dict(
                tickfont=dict(size=18),
                tickangle=0
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del área de la gráfica transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del "papel" transparente
        showlegend=False,
        title=dict(
            text=titulo,
            font=dict(size=30, color='#D5752D'),
            x=0.5,  # <-- Centra el título
            xanchor='center'
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def consignacionesRadar(datos, titulo="Incidentes por Subregión"):
    # Definir categorías base con todas las subestaciones posibles
    categorias_base = sorted(datos['SubstationName'].unique().tolist())
    fig = go.Figure()

    # --- Consignaciones del día actual ---
    categorias = []
    valores = []
    if 'StartDateTime' in datos.columns:
        datos['StartDateTime'] = pd.to_datetime(datos['StartDateTime'])
        hoy = pd.Timestamp.now().date()
        consignaciones_hoy = datos[datos['StartDateTime'].dt.date == hoy]
        if not consignaciones_hoy.empty:
            consignaciones_hoy = consignaciones_hoy.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
            consignaciones_hoy = consignaciones_hoy.set_index('SubstationName').reindex(categorias_base, fill_value=0).reset_index()
            categorias = consignaciones_hoy['SubstationName'].tolist()
            valores = consignaciones_hoy['count'].tolist()
        else:
            categorias = categorias_base
            valores = [0] * len(categorias_base)
    else:
        categorias = categorias_base
        valores = [0] * len(categorias_base)

    # Cerrar el radar
    categorias_cierre = categorias + [categorias[0]]
    valores_cierre = valores + [valores[0]]

    # --- Consignaciones Iniciadas ---
    consignaciones_en_ejecucion = datos[datos['EstadoConsignacion'] == 'Iniciadas']
    if not consignaciones_en_ejecucion.empty:
        iniciado = consignaciones_en_ejecucion.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
        iniciado = iniciado.set_index('SubstationName').reindex(categorias[:-1], fill_value=0).reset_index()
        categoriasIniciado = iniciado['SubstationName'].tolist()
        valoresIniciado = iniciado['count'].tolist()
    else:
        categoriasIniciado = categorias.copy()
        valoresIniciado = [0] * len(categorias)

    categoriasIniciado_cierre = categoriasIniciado + [categoriasIniciado[0]]
    valoresIniciado_cierre = valoresIniciado + [valoresIniciado[0]]

    # --- Graficar ambas líneas ---
    fig.add_trace(go.Scatterpolar(
        r=valores_cierre,
        theta=categorias_cierre,
        fill='none',
        name="hoy",
        marker=dict(color="#EE8D0E"),
        line=dict(width=3)
    ))
    fig.add_trace(go.Scatterpolar(
        r=valoresIniciado_cierre,
        theta=categoriasIniciado_cierre,
        fill='none',
        name='Iniciadas',
        marker=dict(color="#13A2E1"),
        line=dict(width=3)
    ))

    max_radar = max(max(valores_cierre), max(valoresIniciado_cierre))
    if max_radar == 0:
        max_radar = 1  # Para evitar rango cero y que el radar sea visible
    # Ajuste de los ticks
    dtick = 3
    if max_radar > 10:
        dtick = int((max_radar)/5) 

    fig.update_layout(
        width=300,
        height=400,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, max_radar],
                tickfont=dict(size=20),
                dtick=dtick,
            ),
            angularaxis=dict(
                tickfont=dict(size=18),
                rotation=0
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",      # Horizontal
            yanchor="bottom",     # Anclar en la parte inferior
            y=-0.3,               # Debajo del gráfico
            xanchor="center",     # Centrar horizontalmente
            x=0.5,                # Posición horizontal (centro)
            font=dict(size=16)
        ),
        title=dict(
            text=titulo,
            font=dict(size=30, color='#D5752D'),
            x=0.5,
            xanchor='center'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def usuariosRadar(datos, titulo="Incidentes por Subregión"):


    # Agrupa los datos por subregión y cuenta los incidentes
    inc = datos.groupby('SubregionName')['NumCustomers'].sum().reset_index(name='count')
    inc = inc.sort_values(by='count', ascending=False)

    # Prepara los datos para el radar
    categorias = inc['SubregionName'].tolist()
    valores = inc['count'].tolist()
    # Para cerrar el radar, repetimos el primer valor al final
    categorias += [categorias[0]]
    valores += [valores[0]]

    #print(categorias, valores)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name=titulo,
        marker=dict(color="#36E713"),
        line=dict(width=3)
    ))
    if max(valores) < 20:  # Solo si el valor máximo es mayor a 10
        dtick=1,  # Ticks entero
    else:
        dtick=int(max(valores)/5)  # <-- Solo ticks enteros

    fig.update_layout(
        width=300,
        height=400,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, max(valores)],
                tickfont=dict(size=20),
                dtick=dtick,  # Ajuste de los ticks
            ),
            angularaxis=dict(
                tickfont=dict(size=18)
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del área de la gráfica transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del "papel" transparente
        showlegend=False,
        title=dict(
            text=titulo,
            font=dict(size=30, color="#D5752D"),
            x=0.5,  # <-- Centra el título
            xanchor='center'
        )
    )

    st.plotly_chart(fig, use_container_width=True)