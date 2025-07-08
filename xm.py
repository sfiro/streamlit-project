import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
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

    fecha_actual = dt.now().date()
    dia = fecha_actual.strftime("%d")
    mes = fecha_actual.strftime("%m")
    año = fecha_actual.strftime("%Y")
    # Selector de fechas al inicio
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio", value=dt(int(año), 1, 1))
    with col2:
        # Fecha fin por defecto: 5 días antes de la fecha actual
        fecha_fin_default = fecha_actual - timedelta(days=0)
        fecha_fin = st.date_input("Fecha fin", value=fecha_fin_default)

    # Usar las fechas seleccionadas en los request
    # df_precio_bolsa = objetoAPI.request_data(
    #     "PrecBolsNaci", "Sistema", fecha_inicio, fecha_fin
    # )

    df_data_precio_bolsa, df_vol_util_filtrado, df_vol_energia_emb, suma_por_dia_VEnerg_celsia, df_Vol_Energ, porcentaje_vol_Energia, df_demanda_dia, df_export_dia, df_vert = extraccionData(fecha_inicio,fecha_fin)


    #metricas(df_data_precio_bolsa, "💰 Precio de BOLSA TX1", "COP/kWh")

    precioBolsa(df_data_precio_bolsa)

    
   



###---------------Volumen util EMBALSES CELSIA ----------

    
    plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO'] #
    #st.dataframe(plantas_filtrar)

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


###-------------------VOLUMEN UTIL DE ENERGÍA ----------------------------------------------------

    #metricas(df_Vol_Energ, "🔋 Energia Embalses Nacional", "GWh")
    
    barras(df_Vol_Energ,"Energia embalses Nacional", "GWh")


## ------------ Capacidad util ------------------

    #st.dataframe(objetoAPI.get_collections('CapaUtilDiarEner')) # Revisar los cruces disponibles para demanda comercial

    #metricas(porcentaje_vol_Energia, "🔋 Porcentaje Embalses", "%")

    barras(porcentaje_vol_Energia,"Porcentaje Embalses","[%]")


## -------------- Volumen de energía Celsia ---------------------

    #metricas(suma_por_dia_VEnerg_celsia, "⚡ Energia Embalses CELSIA", "GWh")

    barras(suma_por_dia_VEnerg_celsia,"Energia embalses CELSIA", "GWh")


###-------------------Demanda del sistema Nacional ----------------------------------------------------
     
    #metricas(df_demanda_dia,"💡 Demanda Nacional","GWh")
    barras(df_demanda_dia,"💡 Demanda Nacional","GWh")

## ---------------- Exportaciones de energía ----------------

    #metricas(df_export_dia,"🔌 Exportación de energia","GWh")
    barras(df_export_dia,"Exportaciones de energía","GWh")

## --------------- Vertimiento de energía ----------------

    #metricas(df_vert, "💧 Vertimientos", "GWh")
    barras(df_vert,"Vertimientos", "GWh")

    columna1, columna2 = st.columns(2)

    with columna1:
        metricas(df_data_precio_bolsa, "💰 Precio de BOLSA TX1", "COP/kWh")
        metricas(suma_por_dia_VEnerg_celsia, "⚡ Energia Embalses CELSIA", "GWh")
        metricas(df_export_dia,"🔌 Exportación de energia","GWh")
    with columna2:
        metricas(porcentaje_vol_Energia, "🔋 Porcentaje Embalses", "%")
        metricas(df_demanda_dia,"💡 Demanda Nacional","GWh")
        metricas(df_vert, "💧 Vertimientos", "GWh")




def barras(datos,titulo, Yaxis="Energia [GWh]"):
     # Calcular último valor promedio y delta
    ultimo_valor = datos['Value'].iloc[-1]
    valor_anterior = datos['Value'].iloc[-2]
    delta = ultimo_valor - valor_anterior
    flecha = '▲' if delta >= 0 else '▼'
    color_delta = 'green' if delta >= 0 else 'red'
    # Título y valor en la misma línea, delta debajo
    titulo_grafico = (
        f"<span style='font-size:1.2em; color:#F09001; font-weight:bold;'>{titulo} </span> "
        f"<span style='font-size:1.2em; color:#F09001; font-weight:bold;'>{ultimo_valor:,.2f} {Yaxis}</span>"
        f"<br><span style='color:{color_delta}; font-size:1em;'>{flecha} {delta:,.2f} {Yaxis}</span>"
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=datos['Date'],
        y=datos['Value'],
        name='Embalse naciona',
        marker_color='royalblue'
    ))
    fig.update_layout(
        title={
            'text': titulo_grafico,
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=32, color='#F09001')
        },
        xaxis_title='',
        yaxis_title=Yaxis,
        legend_title='',
        xaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=26)  # Aumenta el tamaño de los valores del eje X
        ),
        yaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=22)
        ),
        height=400,
        width=900
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def extraccionData(fecha_inicio, fecha_fin):
    #--- precios de bolsa -----
    # Consulta mensual para Precio de Bolsa
    try:
        # Convertir a fechas sin hora
        fecha_inicio = pd.to_datetime(fecha_inicio).date()
        #st.write(f"Fecha inicio: {fecha_inicio}")
        fecha_fin = pd.to_datetime(fecha_fin).date()
 
        # Siempre dividir en bloques mensuales para mayor robustez
        # Generar los cortes de mes (inicio de cada mes)
        fechas = list(pd.date_range(fecha_inicio, fecha_fin, freq='MS'))
        # Asegurar que la fecha de inicio esté incluida como primer bloque
        if fechas[0].date() != fecha_inicio:
            fechas = [pd.to_datetime(fecha_inicio)] + fechas
        # Asegurar que la fecha de fin esté incluida como último corte
        if fechas[-1].date() < fecha_fin:
            fechas.append(pd.to_datetime(fecha_fin))

         
        df_precio_bolsa = pd.DataFrame()
        for i in range(len(fechas)-1):
            f_ini = fechas[i].date()
            f_fin = (fechas[i+1] - pd.Timedelta(days=1)).date()
            if i == len(fechas)-2:
                f_fin = fecha_fin
            if f_ini < fecha_inicio:
                f_ini = fecha_inicio
            if f_fin > fecha_fin:
                f_fin = fecha_fin
            try:
                df_tmp = objetoAPI.request_data("PrecBolsNaci", "Sistema", f_ini, f_fin)
            except Exception as e:
                error_msg = f"Error al consultar Precio de Bolsa (bloque {f_ini} a {f_fin}): {e}"
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_msg += f"\nRespuesta de la API: {e.response.text}"
                    except Exception:
                        pass
                st.error(error_msg)
                continue
            if df_tmp is not None and not df_tmp.empty:
                df_precio_bolsa = pd.concat([df_precio_bolsa, df_tmp], ignore_index=True)
        if df_precio_bolsa.empty:
            st.warning("No se encontraron datos para Precio de Bolsa en el rango seleccionado.")
            return [None] * 9
        df_precio_bolsa.drop(columns=['Id', 'Values_code'], inplace=True)
        df_precio_bolsa.set_index('Date', inplace=True)
        df_data_precio_bolsa = df_precio_bolsa.aggregate(['mean', 'max', 'min'], axis=1)
        
        
        #st.title("precio de bolsa")
        #st.dataframe(df_data_precio_bolsa)

    except Exception as e:
        error_msg = f"Error general al consultar Precio de Bolsa: {e}"
        st.error(error_msg)
        return [None] * 9

    #---  Volumen útil  -----
    try:
        df_vol_util = objetoAPI.request_data('VoluUtilDiarMasa', 'Embalse', fecha_inicio, fecha_fin)
    except Exception as e:
        error_msg = f"Error al consultar Volumen Útil: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    if df_vol_util is None or df_vol_util.empty:
        st.warning("No se encontraron datos de Volumen Útil en el rango seleccionado.")
        return [None] * 9

    df_vol_util['Date'] = pd.to_datetime(df_vol_util['Date']).dt.date
    df_data_Vol_util = df_vol_util.groupby('Date')['Value'].sum().reset_index()
    plantas_filtrar = ['ALTOANCHICAYA', 'CALIMA1', 'SALVAJINA', 'PRADO']
    df_vol_util_filtrado = df_vol_util[df_vol_util['Name'].isin(plantas_filtrar)].copy()

    #st.title("volumen util CELSIA")
    #st.dataframe(df_vol_util_filtrado)

    # ---- Volumen útil de energía ----
    try:
        df_vol_energ = objetoAPI.request_data('VoluUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)
    except Exception as e:
        error_msg = f"Error al consultar Volumen Útil de Energía: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    if df_vol_energ is None or df_vol_energ.empty:
        st.warning("No se encontraron datos de Volumen Útil de Energía en el rango seleccionado.")
        return [None] * 9

    try:
        df_vol_energIA = objetoAPI.request_data('VoluUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)
    except Exception as e:
        error_msg = f"Error al consultar Volumen Útil de Energía (IA): {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    df_vol_energ['Date'] = pd.to_datetime(df_vol_energ['Date']).dt.date
    df_vol_energia_emb = df_vol_energ
    suma_por_dia_VEnerg = df_vol_energ.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg['Value'] = suma_por_dia_VEnerg['Value'] / 1_000_000

    #st.title("volumen util")
    #st.dataframe(suma_por_dia_VEnerg)

    # ----- volumen util energia celsia ---
    df_vol_util_celsia = df_vol_energia_emb[df_vol_energia_emb['Name'].isin(plantas_filtrar)].copy()
    
    suma_por_dia_VEnerg_celsia = df_vol_util_celsia.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_VEnerg_celsia['Value'] = suma_por_dia_VEnerg_celsia['Value'] / 1_000_000

    #st.title("Energia embalses CELSIA")
    #st.dataframe(suma_por_dia_VEnerg_celsia)

    # --- capacidad útil de energía ----
    try:
        df_cap_energ = objetoAPI.request_data('CapaUtilDiarEner', 'Embalse', fecha_inicio, fecha_fin)
    except Exception as e:
        error_msg = f"Error al consultar Capacidad Útil de Energía: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    if df_cap_energ is None or df_cap_energ.empty:
        st.warning("No se encontraron datos de Capacidad Útil de Energía en el rango seleccionado.")
        return [None] * 9

    df_cap_energ['Date'] = pd.to_datetime(df_cap_energ['Date']).dt.date
    suma_por_dia_CEnerg = df_cap_energ.groupby('Date')['Value'].sum().reset_index()
    suma_por_dia_CEnerg['Value'] = suma_por_dia_CEnerg['Value'] / 1_000_000
    porcentaje_vol_Energia = suma_por_dia_VEnerg.copy()
    porcentaje_vol_Energia['Value'] = (suma_por_dia_VEnerg['Value'] / suma_por_dia_CEnerg['Value']) * 100
    
    
    #st.title("Capacidad util embalses %")
    #st.dataframe(porcentaje_vol_Energia)

    # ------ Demanda de energía  -------
    try:
        df_demanda = objetoAPI.request_data('DemaReal', 'Sistema', fecha_inicio, fecha_fin)
    except Exception as e:
        error_msg = f"Error al consultar Demanda de Energía: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    if df_demanda is None or df_demanda.empty:
        st.warning("No se encontraron datos de Demanda de Energía en el rango seleccionado.")
        return [None] * 9

    df_demanda['Date'] = pd.to_datetime(df_demanda['Date']).dt.date
    df_demanda = df_demanda.drop(columns=['Id', 'Values_code'])
    cols_numericas = df_demanda.select_dtypes(include=[np.number]).columns
    df_demanda['Value'] = df_demanda[cols_numericas].sum(axis=1)
    df_demanda_dia = df_demanda.groupby('Date')['Value'].mean().reset_index()
    df_demanda_dia['Value'] = df_demanda_dia['Value'] / 1_000_000

    #st.title("demanda del pais diaria")
    #st.dataframe(df_demanda_dia)

    # -------- Exportaciones de energia ---------
    

    try:
        df_export = pd.DataFrame()
        for i in range(len(fechas)-1):
            f_ini = fechas[i].date()
            f_fin = (fechas[i+1] - pd.Timedelta(days=1)).date()
            if i == len(fechas)-2:
                f_fin = fecha_fin
            if f_ini < fecha_inicio:
                f_ini = fecha_inicio
            if f_fin > fecha_fin:
                f_fin = fecha_fin
            try:
                df_tmp = objetoAPI.request_data("ExpoEner", "Enlace", f_ini, f_fin)
            except Exception:
                # Silenciar el error, no mostrar nada en la interfaz
                continue
            if df_tmp is not None and not df_tmp.empty:
                df_export = pd.concat([df_export, df_tmp], ignore_index=True)
        if df_export.empty:
            st.warning("No se encontraron datos para exportaciones en el rango seleccionado.")
            return [None] * 9
        df_export = df_export.drop(columns=['Id', 'Values_code'], errors='ignore')
        cols_numericas = df_export.select_dtypes(include=[np.number]).columns
        df_export['Value'] = df_export[cols_numericas].sum(axis=1)
        df_export_dia = df_export.groupby('Date')['Value'].mean().reset_index()
        df_export_dia['Value'] = df_export_dia['Value'] / 1_000_000
        #st.title("exportacion de energía ")
        #st.dataframe(df_export_dia)
    except Exception as e:
        error_msg = f"Error general al consultar exportaciones: {e}"
        st.error(error_msg)
        return [None] * 9


    # -------- Vertimientos de energia ---------
    try:
        df_vert = objetoAPI.request_data('VertEner', 'Sistema', fecha_inicio, fecha_fin)
        df_vert = df_vert.drop(columns=['Id'])
        df_vert['Value'] = df_vert['Value'] / 1_000_000
    except Exception as e:
        error_msg = f"Error al consultar Vertimientos de Energía: {e}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_msg += f"\nRespuesta de la API: {e.response.text}"
            except Exception:
                pass
        st.error(error_msg)
        return [None] * 9
    if df_vert is None or df_vert.empty:
        st.warning("No se encontraron datos de Vertimientos de Energía en el rango seleccionado.")
        return [None] * 9

    

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

def precioBolsa(df_data_precio_bolsa):
     # Calcular último valor promedio y delta
    ultimo_valor = df_data_precio_bolsa['mean'].iloc[-1]
    valor_anterior = df_data_precio_bolsa['mean'].iloc[-2]
    delta = ultimo_valor - valor_anterior
    flecha = '▲' if delta >= 0 else '▼'
    color_delta = 'green' if delta >= 0 else 'red'
    # Título y valor en la misma línea, delta debajo
    titulo_grafico = (
        f"<span style='font-size:1.2em; color:#F09001; font-weight:bold;'>💰 Precio de BOLSA </span> "
        f"<span style='font-size:1.2em; color:#F09001; font-weight:bold;'>{ultimo_valor:,.2f} COP/kWh</span>"
        f"<br><span style='color:{color_delta}; font-size:1em;'>{flecha} {delta:,.2f} COP/kWh</span>"
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_data_precio_bolsa.index,
        y=df_data_precio_bolsa['mean'],
        mode='lines',
        name='',  # Sin etiqueta
        showlegend=False,
        line=dict(color='white')
    ))
    fig.add_trace(go.Scatter(
        x=df_data_precio_bolsa.index,
        y=df_data_precio_bolsa['max'],
        mode='lines',
        name='',  # Sin etiqueta
        showlegend=False,
        line=dict(color='red', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=df_data_precio_bolsa.index,
        y=df_data_precio_bolsa['min'],
        mode='lines',
        name='',  # Sin etiqueta
        showlegend=False,
        line=dict(color='cyan', dash='dash')
    ))
    fig.update_layout(
        title={
            'text': titulo_grafico,
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=32, color='#F09001')
        },
        xaxis_title='',
        yaxis_title='Precio en bolsa nacional [COP/kWh]',
        legend_title='Serie',
        xaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=26)  # Aumenta el tamaño de los valores del eje X
        ),
        yaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=22)
        ),
        height=400,
        width=900
    )
    fig.update_layout(title_font=dict(size=32, color='#F09001'))
    fig.update_layout(title={'text': titulo_grafico, 'y':0.92, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(size=32, color='#F09001')})
    fig.update_layout(title={'text': titulo_grafico, 'y':0.92, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, title_font=dict(size=32, color='#F09001'), title_x=0.5)
    fig.update_layout(title={'text': titulo_grafico, 'y':0.92, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': dict(size=32, color='#F09001')}, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})