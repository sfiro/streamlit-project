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


def datos_xm():

    fecha_actual = dt.now()
    dia = fecha_actual.strftime("%d")
    mes = fecha_actual.strftime("%m")
    año = fecha_actual.strftime("%Y")
    # Selector de fechas al inicio
    # col1, col2 = st.columns(2)
    # with col1:
    #     fecha_inicio = st.date_input("Fecha inicio", value=dt(int(año), 1, 1))
    # with col2:
    #     fecha_fin = st.date_input("Fecha fin", value=dt(int(año), int(mes), int(dia)))

    fecha_inicio = dt(int(año),1,1)
    fecha_fin = dt(int(año), int(mes), int(dia))

    # Usar las fechas seleccionadas en los request
    # df_precio_bolsa = objetoAPI.request_data(
    #     "PrecBolsNaci", "Sistema", fecha_inicio, fecha_fin
    # )

    df_data_precio_bolsa, df_vol_util_filtrado, df_vol_energia_emb, suma_por_dia_VEnerg_celsia, df_Vol_Energ, porcentaje_vol_Energia, df_demanda_dia, df_export_dia, df_vert = extraccionData(fecha_inicio,fecha_fin)


    columna1, columna2, columna3, columna4 = st.columns([1,10,10,1])

    with columna1:
        pass

    with columna2:
        #metricas(df_data_precio_bolsa, "💰 Precio de BOLSA TX1", "COP/kWh")
        metrica_personalizada(df_data_precio_bolsa, "💰 Precio de BOLSA TX1","COP/kWh", color="#F09001", tam_titulo="3.0rem", tam_valor="4.0rem", tam_delta="2.5rem", delta_pos="right")

        metrica_personalizada(suma_por_dia_VEnerg_celsia, "⚡ Energia Embalses CELSIA","GWh", color="#F09001")

        metrica_personalizada(df_export_dia, "🔌 Exportación de energia","GWh", color="#F09001")

    with columna3:
        
        metrica_personalizada(porcentaje_vol_Energia,  "🔋 Porcentaje Embalses","GWh", color="#F09001")

        metrica_personalizada(df_demanda_dia,  "💡 Demanda Nacional","GWh", color="#F09001")

        metrica_personalizada(df_vert,  "💧 Vertimiento","GWh", color="#F09001")
    with columna4:
        pass



def barras(datos,titulo, Yaxis="Energia [GWh]"):
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
        yaxis_title= Yaxis,
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True)


def extraccionData(fecha_inicio,fecha_fin):
   
   #--- precios de bolsa -----
    df_precio_bolsa = objetoAPI.request_data("PrecBolsNaci", "Sistema", fecha_inicio, fecha_fin) #consulta de la variable precio de bolsa nacional por sistema  
    df_precio_bolsa.drop(columns=['Id', 'Values_code'], inplace=True)             #Eliminación de columnas innecesarias para los cálculos requeridos
    df_precio_bolsa.set_index('Date', inplace=True)                               #Uso de la columna de 'Date' como índice
    df_data_precio_bolsa = df_precio_bolsa.aggregate(['mean', 'max', 'min'], axis=1)  #Cálculo del promedio, máximo y mínimo del precio de bolsa nacional
   
    #---  Volumen útil  -----
    df_vol_util = objetoAPI.request_data('VoluUtilDiarMasa', 'Embalse',fecha_inicio, fecha_fin)
    df_vol_util['Date'] = pd.to_datetime(df_vol_util['Date']).dt.date
    df_data_Vol_util = df_vol_util.groupby('Date')['Value'].sum().reset_index()

    plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO'] 
    df_vol_util_filtrado = df_vol_util[df_vol_util['Name'].isin(plantas_filtrar)].copy()

    # ---- Volumen útil de energía ----
    df_vol_energ = objetoAPI.request_data('VoluUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)
    df_vol_energIA = objetoAPI.request_data('VoluUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)

    df_vol_energ['Date'] = pd.to_datetime(df_vol_energ['Date']).dt.date

    df_vol_energia_emb = df_vol_energ
    suma_por_dia_VEnerg = df_vol_energ.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg['Value'] = suma_por_dia_VEnerg['Value'] / 1_000_000

    # ----- volumen util energia celsia ---
    df_vol_util_celsia= df_vol_energia_emb[df_vol_energia_emb['Name'].isin(plantas_filtrar)].copy()
    suma_por_dia_VEnerg_celsia = df_vol_util_celsia.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg_celsia['Value'] = suma_por_dia_VEnerg_celsia['Value'] / 1_000_000
    
   

    # --- capacidad útil de energía ----
    df_cap_energ = objetoAPI.request_data('CapaUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)
    df_cap_energ['Date'] = pd.to_datetime(df_cap_energ['Date']).dt.date

    suma_por_dia_CEnerg = df_cap_energ.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_CEnerg['Value'] = suma_por_dia_CEnerg['Value'] / 1_000_000

    #st.dataframe(suma_por_dia_CEnerg)
    porcentaje_vol_Energia = suma_por_dia_VEnerg
    porcentaje_vol_Energia['Value'] = (suma_por_dia_VEnerg['Value']/suma_por_dia_CEnerg['Value'])*100


    # ------ Demanda de energía  -------

    df_demanda = objetoAPI.request_data('DemaReal', 'Sistema', fecha_inicio, fecha_fin)
    df_demanda['Date'] = pd.to_datetime(df_demanda['Date']).dt.date
    df_demanda = df_demanda.drop(columns=['Id', 'Values_code'])
    cols_numericas = df_demanda.select_dtypes(include=[np.number]).columns
    df_demanda['Value'] = df_demanda[cols_numericas].sum(axis=1)
    df_demanda_dia = df_demanda.groupby('Date')['Value'].mean().reset_index()
    df_demanda_dia['Value'] = df_demanda_dia['Value'] / 1_000_000


    # -------- Exportaciones de energia ---------

    df_export = objetoAPI.request_data('ExpoEner', 'Enlace', fecha_inicio, fecha_fin)
    df_export = df_export.drop(columns=['Id', 'Values_code'])
    cols_numericas = df_export.select_dtypes(include=[np.number]).columns
    df_export['Value'] = df_export[cols_numericas].sum(axis=1)
    df_export_dia = df_export.groupby('Date')['Value'].mean().reset_index()
    df_export_dia['Value'] = df_export_dia['Value'] / 1_000_000


    # -------- Vertimientos de energia ---------
    df_vert = objetoAPI.request_data('VertEner', 'Sistema', fecha_inicio, fecha_fin)
    df_vert = df_vert.drop(columns=['Id'])
    df_vert['Value'] = df_vert['Value']/1_000_000
    
    


    return df_data_precio_bolsa, df_vol_util_filtrado, df_vol_energia_emb, suma_por_dia_VEnerg_celsia, suma_por_dia_VEnerg, porcentaje_vol_Energia, df_demanda_dia, df_export_dia, df_vert


def metricas(df_data, Titulo="Precio de BOLSA TX1", unidad="COP/kWh"):
    
    if 'mean' in df_data.columns:
        ultimo_valor = df_data['mean'].iloc[-1]
        valor_anterior = df_data['mean'].iloc[-2]
        fecha = df_data.index[-1] 
        delta = ultimo_valor - valor_anterior
    else:
        #los datos en la demanda nacional tiene un error en los ultimos dos valores
        # se hace el condicional de demanda para saltar este error
        if "demanda" in Titulo.lower():  
            ultimo_valor = df_data['Value'].iloc[-3]
            valor_anterior = df_data['Value'].iloc[-4]
            delta = ultimo_valor - valor_anterior
            fecha = df_data['Date'].iloc[-1]
        else:
            ultimo_valor = df_data['Value'].iloc[-1]
            valor_anterior = df_data['Value'].iloc[-2]
            delta = ultimo_valor - valor_anterior
            fecha = df_data['Date'].iloc[-1]

    st.metric(
        Titulo,
        f"{ultimo_valor:,.2f} {unidad}",
        delta=f"{delta:+.2f} {unidad}",
        help=f"Fecha: {fecha}"
    )

def metrica_personalizada(df_data, titulo, unidad, color="#383838", tam_titulo="3.0rem", tam_valor="4.2rem", tam_delta="2.5rem", delta_pos="right"):
    # delta_pos puede ser "right" o "below"

    if 'mean' in df_data.columns:
        ultimo_valor = df_data['mean'].iloc[-1]
        valor_anterior = df_data['mean'].iloc[-2]
        fecha = df_data.index[-1] 
        delta = ultimo_valor - valor_anterior
    else:
        #los datos en la demanda nacional tiene un error en los ultimos dos valores
        # se hace el condicional de demanda para saltar este error
        if "demanda" in titulo.lower():  
            ultimo_valor = df_data['Value'].iloc[-3]
            valor_anterior = df_data['Value'].iloc[-4]
            delta = ultimo_valor - valor_anterior
            fecha = df_data['Date'].iloc[-1]
        else:
            ultimo_valor = df_data['Value'].iloc[-1]
            valor_anterior = df_data['Value'].iloc[-2]
            delta = ultimo_valor - valor_anterior
            fecha = df_data['Date'].iloc[-1]

        
    valor = ultimo_valor

    delta_html = f"""
        <span style='color:{"green" if delta>=0 else "red"}; font-size:{tam_delta};'>
            {'▲' if delta>=0 else '▼'} {abs(delta):,.2f} {unidad}
        </span>
    """
    if delta_pos == "right":
        html = f"""
        <div style='
            margin-bottom:18px;
            text-align:center;
            background-color:#383838;
            border-radius:12px;
            box-shadow:0 2px 8px rgba(0,0,0,0.07);
            padding:8px 8px 12px 8px;
            display:flex;
            flex-direction:column;
            align-items:center;
        '>
            <span style='font-size:{tam_titulo}; color:{color}; font-weight:bold;'>{titulo}</span><br>
            <span style='font-size:{tam_valor}; font-weight:bold;'>{valor:,.2f} {unidad}</span>
            {delta_html}
            
        </div>
        """
    else:  # delta abajo
        html = f"""
        <div style='
            margin-bottom:18px;
            text-align:center;
            background-color:#383838;
            border-radius:12px;
            box-shadow:0 2px 8px rgba(0,0,0,0.07);
            padding:8px 8px 12px 8px;
            display:flex;
            flex-direction:column;
            align-items:center;
        '>
            <span style='font-size:{tam_titulo}; color:{color}; font-weight:bold;'>{titulo}</span><br>
            <span style='font-size:{tam_valor}; font-weight:bold;'>{valor:,.2f} {unidad}</span><br>
            {delta_html}
   
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)