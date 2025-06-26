import streamlit as st
import pandas as pd
from datetime import datetime as dt
import os
import plotly.graph_objects as go
import numpy as np
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM
from pydataxm.pydataxm import ReadDB
from pydataxm import *          # Importa la libreria que fue instalada con pip install pydataxm o tambien desde GitHub
import plotly.express as px
import requests
import json


objetoAPI = pydataxm.ReadDB()     # Construir la clase que contiene los métodos de pydataxm

def xm_data():

    
    # Importación

    #objetoAPI.get_collections('DemaCome') # Revisar los cruces disponibles para demanda comercial
    
    # st.write(objetoAPI.get_collections('DemaCome'))

    # df_demanda = objetoAPI.request_data('DemaCome',
    #                                 'MercadoComercializacion',
    #                                 dt(2025, 6, 1).date(),
    #                                 dt(2025, 6, 25).date())
    
    # st.dataframe(df_demanda)

    # df_demanda['demanda_diaria'] = df_demanda.sum(axis=1, skipna=True, numeric_only=True) #Cálculo diario de la demanda
    # cols_numericas = df_demanda.select_dtypes(include=[np.number]).columns
    # st.write(cols_numericas)
    # df_demanda['demanda_diaria'] = df_demanda[cols_numericas].sum(axis=1, skipna=True)
    # #Cálculo mensual de la demanda
    # # ...existing code...
    # cols_numericas = df_demanda.select_dtypes(include=[np.number]).columns

    # # Agrupa y suma solo columnas numéricas
    # df_demanda_grouped = df_demanda.groupby('Values_code')[cols_numericas].sum()

    # # Si solo quieres la suma de 'demanda_diaria' por 'Values_code':
    # df_demanda_suma = df_demanda_grouped['demanda_diaria']

    # df_demanda_porcentaje = (df_demanda_suma * 100 / df_demanda_suma.sum()).round(2).sort_values(ascending=True)
    # st.dataframe(df_demanda_porcentaje)
    # # ...existing code...

    # df_demanda_porcentaje = (df_demanda_suma * 100 / df_demanda_suma.sum()).round(2).sort_values(ascending=True)
    # st.dataframe(df_demanda_porcentaje)

    # # Gráfico de barras horizontal con Plotly
    # fig = px.bar(
    #     df_demanda_porcentaje,
    #     x=df_demanda_porcentaje.values,
    #     y=df_demanda_porcentaje.index,
    #     orientation='h',
    #     labels={'x': 'Porcentaje de demanda mensual [%]', 'y': 'Región'},
    #     title='Porcentaje de demanda por región respecto al total de la demanda'
    # )
    # st.plotly_chart(fig, use_container_width=True)

    df_precio_bolsa = objetoAPI.request_data("PrecBolsNaci", "Sistema", dt(2025, 1, 1).date(), dt(2025, 12, 31).date()) #consulta de la variable precio de bolsa nacional por sistema  
    df_precio_bolsa.drop(columns=['Id', 'Values_code'], inplace=True)             #Eliminación de columnas innecesarias para los cálculos requeridos
    df_precio_bolsa.set_index('Date', inplace=True)                               #Uso de la columna de 'Date' como índice
    df_resumen_anual = df_precio_bolsa.aggregate(['mean', 'max', 'min'], axis=1)  #Cálculo del promedio, máximo y mínimo del precio de bolsa nacional
    #st.dataframe(df_resumen_anual)


    ultimo_valor = df_resumen_anual['mean'].iloc[-1]
    valor_anterior = df_resumen_anual['mean'].iloc[-2]
    fecha = df_resumen_anual.index[-1] 
    delta = ultimo_valor - valor_anterior

    st.metric(
        "💰 Precio de BOLSA TX1",
        f"{ultimo_valor:,.2f} COP/kWh",
        delta=f"{delta:+.2f} COP/kWh",
        help=f"Fecha: {fecha}"
    )
    #st.dataframe(df_precio_bolsa)
    #st.dataframe(df_resumen_anual)

    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_resumen_anual.index,
        y=df_resumen_anual['mean'],
        mode='lines',
        name='Promedio diario del precio de bolsa nacional',
        line=dict(color='white')
    ))
    fig.add_trace(go.Scatter(
        x=df_resumen_anual.index,
        y=df_resumen_anual['max'],
        mode='lines',
        name='Máximo diario del precio de bolsa nacional',
        line=dict(color='red', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=df_resumen_anual.index,
        y=df_resumen_anual['min'],
        mode='lines',
        name='Mínimo diario del precio de bolsa nacional',
        line=dict(color='cyan', dash='dash')
    ))
    fig.update_layout(
        title='Máximo, mínimo y promedio diario del precio de bolsa nacional durante el año 2025',
        xaxis_title='Tiempo',
        yaxis_title='Precio en bolsa nacional [COP/kWh]',
        legend_title='Serie',
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)


    #----------precios de bolsa horarios --------------------------
    # Concatenar todos los valores de todas las filas en un solo array
    # precios_concatenados = df_precio_bolsa.values.flatten()
    # #st.dataframe(precios_concatenados)

    # # Crear un eje X con la cantidad de puntos concatenados
    # x = list(range(1, len(precios_concatenados) + 1))

    # # Graficar la serie única
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(
    #     x=x,
    #     y=precios_concatenados,
    #     mode='lines',
    #     name='Precio bolsa nacional (serie única)'
    # ))
    # fig.update_layout(
    #     title='Serie única de precios horarios de bolsa nacional durante el año 2025',
    #     xaxis_title='Intervalo horario acumulado',
    #     yaxis_title='Precio en bolsa nacional [COP/kWh]',
    #     height=400,
    #     width=900
    # )
    # st.plotly_chart(fig, use_container_width=True)



###---------------EMBALSES NACIONAL ----------
    #st.dataframe(objetoAPI.get_collections('VoluUtilDiarMasa')) # Revisar los cruces disponibles para demanda comercial

    df_vol_util = objetoAPI.request_data('VoluUtilDiarMasa', 'Embalse',
                                    dt(2025, 1, 1).date(),
                                    dt(2025, 6, 25).date())
    #st.dataframe(df_vol_util)

    df_vol_util['Date'] = pd.to_datetime(df_vol_util['Date']).dt.date

    suma_por_dia_Vutil = df_vol_util.groupby('Date')['Value'].sum().reset_index()
    #st.dataframe(suma_por_dia_Vutil)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=suma_por_dia_Vutil['Date'],
        y=suma_por_dia_Vutil['Value'],
        mode='lines',
        name='Embalse naciona',
            line=dict(
            color="#080CE7",   # Verde neón
            width=4,           # Más grueso para resaltar
        )
    ))
    fig.update_layout(
        title='Embalse Nacional',
        xaxis_title='Fecha',
        yaxis_title='Embalse [m3]',
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)


    ### --------------EMBALSES CELSIA  -------------

    # plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO']
    # df_vol_util_filtrado = df_vol_util[df_vol_util['Name'].isin(plantas_filtrar)].copy()
    # #st.dataframe(df_vol_util_filtrado)

    # fig = go.Figure()
    # for planta in plantas_filtrar:
    #     fig.add_trace(go.Scatter(
    #         x=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Date'],
    #         y=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Value'],
    #         mode='lines',
    #         name=planta
    #     ))
    # fig.update_layout(
    #     title='Embalses CELSIA',
    #     xaxis_title='Fecha',
    #     yaxis_title='Celsia Embalse [m3]',
    #     height=400,
    #     width=900
    # )
    # st.plotly_chart(fig, use_container_width=True)

    plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO']
    df_vol_util_filtrado = df_vol_util[df_vol_util['Name'].isin(plantas_filtrar)].copy()
    #st.dataframe(df_vol_util_filtrado)

    fig = go.Figure()
    for planta in plantas_filtrar:
        fig.add_trace(go.Scatter(
            x=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Date'],
            y=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Value'],
            mode='lines',
            stackgroup='one',  # Área apilada
            name=planta
        ))
    fig.update_layout(
        title='Embalses CELSIA - Evolución Niveles',
        xaxis_title='Fecha',
        yaxis_title='Nivel Embalse [m3]',
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    for planta in plantas_filtrar:
        fig.add_trace(go.Scatter(
            x=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Date'],
            y=df_vol_util_filtrado[df_vol_util_filtrado['Name'] == planta]['Value'],
            mode='lines+markers',
            name=planta
        ))
    fig.update_layout(
        title='Embalses CELSIA - Evolución Niveles',
        xaxis_title='Fecha',
        yaxis_title='Nivel Embalse [m3]',
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)



###-------------------VOLUMEN UTIL DE ENERGÍA ----------------------------------------------------

    #st.dataframe(objetoAPI.get_collections('VoluUtilDiarEner')) # Revisar los cruces disponibles para demanda comercial

    df_vol_energ = objetoAPI.request_data('VoluUtilDiarEner', 'Embalse',
                                    dt(2025, 1, 1).date(),
                                    dt(2025, 6, 25).date())
    #st.dataframe(df_vol_energ)

    df_vol_energ['Date'] = pd.to_datetime(df_vol_energ['Date']).dt.date

    suma_por_dia_VEnerg = df_vol_energ.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg['Value'] = suma_por_dia_VEnerg['Value'] / 1000000
    
## -----------------METRICA DE ULTIMO VALOR DE ENERGÍA -------------------
    # Mostrar la última energía diaria como métrica
    ultimo_valor = suma_por_dia_VEnerg.iloc[-1]
    valor_anterior = suma_por_dia_VEnerg.iloc[-2]['Value']
    delta = ultimo_valor['Value'] - valor_anterior

    st.metric(
        "🔋 Energia Embalses Nacional",
        f"{ultimo_valor['Value']:,.2f} GWh",
        delta=f"{delta:+.2f} GWh",
        help=f"Fecha: {ultimo_valor['Date']}"
    )
    #st.dataframe(suma_por_dia_Vutil)

    barras(suma_por_dia_VEnerg,"Energia embalses Nacional")

## -------------- Volumen de energía Celsia ---------------------

    
    plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO']
    df_vol_util_celsia= df_vol_energ[df_vol_energ['Name'].isin(plantas_filtrar)].copy()
    suma_por_dia_VEnerg_celsia = df_vol_util_celsia.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg_celsia['Value'] = suma_por_dia_VEnerg_celsia['Value'] / 1000000
    #st.dataframe(suma_por_dia_VEnerg_celsia)
    

    # Mostrar la última energía diaria como métrica
    ultimo_valor = suma_por_dia_VEnerg_celsia.iloc[-1]
    valor_anterior = suma_por_dia_VEnerg_celsia.iloc[-2]['Value']
    delta = ultimo_valor['Value'] - valor_anterior

    st.metric(
        "🔋 Energia Embalses CELSIA",
        f"{ultimo_valor['Value']:,.2f} GWh",
        delta=f"{delta:+.2f} GWh",
        help=f"Fecha: {ultimo_valor['Date']}"
    )

    barras(suma_por_dia_VEnerg_celsia,"Energia embalses CELSIA")

    


###-------------------Demanda del sistema Nacional ----------------------------------------------------
    
    #st.dataframe(objetoAPI.get_collections('DemaReal')) # Revisar los cruces disponibles para demanda comercial

    df_demanda = objetoAPI.request_data('DemaReal', 'Sistema',
                                    dt(2025, 1, 1).date(),
                                    dt(2025, 6, 25).date())
    #st.dataframe(df_demanda)

    df_demanda['Date'] = pd.to_datetime(df_demanda['Date']).dt.date
    df_demanda = df_demanda.drop(columns=['Id', 'Values_code'])
    #st.dataframe(df_demanda)

    # Selecciona solo las columnas numéricas (las 24 de datos)
    cols_numericas = df_demanda.select_dtypes(include=[np.number]).columns

    # Calcula el promedio diario de todas las columnas numéricas
    df_demanda['Value'] = df_demanda[cols_numericas].sum(axis=1)

    # Agrupa por fecha y calcula el promedio (en este caso, será igual al promedio_diario por fila)
    df_demanda_dia = df_demanda.groupby('Date')['Value'].mean().reset_index()

    # Si quieres mostrar en GWh (si tus datos están en kWh)
    df_demanda_dia['Value'] = df_demanda_dia['Value'] / 1_000_000

    #st.dataframe(df_demanda_dia)
    
  
    
## -----------------METRICA DE ULTIMO VALOR DE Demanda nacional -------------------
    # Mostrar la última energía diaria como métrica
    ultimo_valor = df_demanda_dia.iloc[-1]
    valor_anterior = df_demanda_dia.iloc[-2]['Value']
    delta = ultimo_valor['Value'] - valor_anterior

    st.metric(
        "💡 Demanda Nacional",
        f"{ultimo_valor['Value']:,.2f} GWh",
        delta=f"{delta:+.2f} GWh",
        help=f"Fecha: {ultimo_valor['Date']}"
    )

    barras(df_demanda_dia,"Demanda nacional")



 

def barras(datos,titulo):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=datos['Date'],
        y=datos['Value'],
        name='Embalse naciona',
        marker_color='royalblue'
    ))
    fig.update_layout(
        title=titulo,
        xaxis_title='Fecha',
        yaxis_title='Energia [GWh]',
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)