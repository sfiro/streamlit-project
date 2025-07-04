import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import os
import plotly.graph_objects as go
import numpy as np
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM
from pydataxm.pydataxm import ReadDB
from pydataxm import *          # Importa la libreria que fue instalada con pip install pydataxm o tambien desde GitHub

from xm import extraccionData

import plotly.express as px
import requests
import json


objetoAPI = pydataxm.ReadDB()     # Construir la clase que contiene los métodos de pydataxm


def datos_xm():

    fecha_actual = dt.now().date()
    dia = fecha_actual.strftime("%d")
    mes = fecha_actual.strftime("%m")
    año = fecha_actual.strftime("%Y")
  

    fecha_inicio = dt(int(año),1,1)
    fecha_fin = fecha_actual - timedelta(days=4)
    


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
        
        metrica_personalizada(porcentaje_vol_Energia,  "🔋 Porcentaje Embalses","%", color="#F09001")

        metrica_personalizada(df_demanda_dia,  "💡 Demanda Nacional","GWh", color="#F09001")

        metrica_personalizada(df_vert,  "💧 Vertimiento","GWh", color="#F09001")

    with columna4:
        pass




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