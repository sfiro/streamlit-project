import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import os
import plotly.graph_objects as go
import numpy as np
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM
from pydataxm.pydataxm import ReadDB
from pydataxm import *          # Importa la libreria que fue instalada con pip install pydataxm o tambien desde GitHub
from xm import extraccionData, precioBolsa, barras
import plotly.express as px
import requests
import json


objetoAPI = pydataxm.ReadDB()     # Construir la clase que contiene los métodos de pydataxm


def datos_xm2():

    fecha_actual = dt.now().date()
    dia = fecha_actual.strftime("%d")
    mes = fecha_actual.strftime("%m")
    año = fecha_actual.strftime("%Y")

    
    fecha_fin = fecha_actual - timedelta(days=4)
    fecha_inicio = fecha_actual - timedelta(days=300)


    df_data_precio_bolsa, df_vol_util_filtrado, df_vol_energia_emb, suma_por_dia_VEnerg_celsia, df_Vol_Energ, porcentaje_vol_Energia, df_demanda_dia, df_export_dia, df_vert = extraccionData(fecha_inicio,fecha_fin)

    #metrica_personalizada(df_data_precio_bolsa, "💰 Precio de BOLSA TX1","COP/kWh", color="#F09001", tam_titulo="3.0rem", tam_valor="4.0rem", tam_delta="2.5rem", delta_pos="right")


    columna1, columna2= st.columns([1,1])

    with columna1:
        precioBolsa(df_data_precio_bolsa)
        barras(df_vert,"Vertimientos","GWh") 
        
    with columna2:
        barras(porcentaje_vol_Energia,  "🔋 Porcentaje Embalse Nacional","%")
        barras(df_demanda_dia,  "💡 Demanda Nacional","GWh")
        barras(df_export_dia, "🔌 Exportación de energia","GWh")

        
        


   



