import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.graph_objects as go

plantas_hidro = [
            "ALTO TULUA",
            "AMAIME",
            "BAJO TULUA",
            "HIDROMONTAÑITAS",
            "NIMA",
            "PRADO IV",
            "RIO CALI",
            "RIO PIEDRAS",
            "SAN ANDRES DE CUERQUIA"
        ]
cogeneradores = [
    "ARGOS CARTAGENA",
    "ARGOS TOLUVIEJO",
    "ARGOS YUMBO",
    "MAYAGUEZ 1",
    "SAN CARLOS 1"
]
solares = [
    "ALUMINA",
    "BOLIVAR",
    "BUGA I GRASAS",
    "BUGA I SOLLA",
    "CARMELO",
    "CERRITOS",
    "DULIMA",
    "ESPINAL",
    "FLANDES",
    "HARINAS",
    "LA MEDINA",
    "LA PAILA",
    "LA VICTORIA I",
    "LA VICTORIA II",
    "MELGAR - LANCEROS",
    "LEVAPAN (Tulua)",
    "LOS CABALLEROS",
    "MONTELIBANO",
    "PALMIRA 3 AMCOR",
    "PALMIRA 3 ZONA FRANCA",
    "PETALO DEL MAGDALENA",
    "SAN FELIPE",
    "SINCE",
    "TUCANES (BAYUNCA)",
    "YUMA",
    "YUMBO",
    "PLANETA RICA",
    "GD ALFEREZ",
    "GD BASILICA",
    "GD CHICORAL",
    "GD EL BANCO",
    "GD LA URIBE",
    "GD LOS CHORROS",
    "GD LA HONDA",
    "GD PALERMO",
    "BUGALAGRANDE",
    "PUERTO TEJADA",
    "GD CHIMBI",
    "PALMIRA II BERRY",
    "TECNOQUIMICAS JAMUNDI",
    "BOCAS DEL PALO",
    "PALMASECA 1",
    "PALMASECA 2",
    "MOLINO SANTA MARTA",
    "AUTOG COMOLSA",
    "AUTOG QBCO"
]

termicas = [
    "MERILECTRICA",
    "TESORITO"
]

plantas_mayor_gen = [
     "Unnamed: 2",
    "Unnamed: 5", 
    "Unnamed: 8", 
    "Unnamed: 11", 
    "Unnamed: 14", 
    "Unnamed: 17", 
]

plantas_mayor = [
     "ALTO ANCHICAYA",
    "BAJO ANCHICAYA", 
    "CALIMA", 
    "SALVAJINA", 
    "PRADO", 
    "CUCUANA", 
]


def gen():

    fecha_actual = datetime.now()
    mes = fecha_actual.strftime("%m")
    año = fecha_actual.strftime("%Y")
    nombre_archivo = f"GENERACION Y NIVELES {mes}-{año}.xlsm"
    #ruta_base = r"C:\Users\accontrol\OneDrive - CELSIA S.A E.S.P\CSM_BACKUP\GENERACION TOTAL Y NIVELES PLANTAS\2025"
    ruta_base = r"C:\Users\gestioncc\OneDrive - CELSIA S.A E.S.P\CSM_BACKUP\GENERACION TOTAL Y NIVELES PLANTAS\2025"
  
    ruta_completa = fr"{ruta_base}\{nombre_archivo}"

    if os.path.exists(ruta_completa):
        df_plantas = pd.read_excel(ruta_completa, sheet_name="Plantas")
        df_cogeneradores = pd.read_excel(ruta_completa, sheet_name="Cogeneradores CELSIA")
        #st.dataframe(df_plantas)
        #st.dataframe(df_cogeneradores)

        # Reemplaza saltos de línea y cambia la coma por punto antes de convertir a float
        df_cogeneradores.iloc[:, 1:] = df_cogeneradores.iloc[:, 1:].applymap(
            lambda x: str(x).replace('\n', '').replace(',', '.')
        )
        lineas(df_cogeneradores,"Generación diaria")

        # Filtrar las plantas de interés
        df_hidro = filtrado(df_cogeneradores,plantas_hidro,"pequeñas hidro")
        df_coge = filtrado(df_cogeneradores,cogeneradores,"cogeneradores")
        df_sol = filtrado(df_cogeneradores,solares,"solar")
        df_term = filtrado(df_cogeneradores,termicas,"Termicas")

        df_resultado = pd.concat([df_term, df_hidro, df_coge,df_sol], ignore_index=True)
        
        lineas(df_resultado,"Generacion Cogeneradores")
        area(df_resultado)
        
        plantas_mayores=df_plantas[plantas_mayor_gen]
        plantas_mayores = plantas_mayores.iloc[1:].reset_index(drop=True)
        plantas_mayores.columns = plantas_mayor
        #st.dataframe(plantas_mayores)
        #lineas(plantas_mayores.T,"Generacion plantas")
        
        #st.dataframe(plantas_mayores.T)
        lineasGeneracion(plantas_mayores,"key")

    else:
        st.error(f"El archivo no existe: {ruta_completa}")



def lineas(datos,key):
    nombre_columna = datos.columns[0]    
    periodos = datos.columns[1:]

    fig = go.Figure()

    for idx, row in datos.iterrows():
        fig.add_trace(go.Scatter(
            x=periodos,
            y=row[1:],  # Todos los valores excepto el nombre de la planta
            mode='lines+markers',
            name=row[nombre_columna]
        ))

    fig.update_layout(
        title=key,
        xaxis_title="Periodo",
        yaxis_title="Energía",
        legend_title="Planta"
    )

    st.plotly_chart(fig,key=key)

def filtrado(data,plantas,titulo):
    #filtrado y seleccion de plantas y suma de sus aportes energeticos
    df_plantas = data[data[data.columns[0]].isin(plantas)].copy()
    suma = df_plantas.iloc[:, 1:].astype(float).sum(axis=0)
    df_suma = pd.DataFrame([suma.values], columns=suma.index)
    df_suma.insert(0, data.columns[0], titulo)
    return df_suma


def area(data):
    nombre_columna = data.columns[0]
    periodos = data.columns[1:]

    fig = go.Figure()

    for idx, row in data.iterrows():
        fig.add_trace(go.Scatter(
            x=periodos,
            y=row[1:].astype(float),
            mode='lines',
            stackgroup='one',  # Esto hace el área apilada
            name=row[nombre_columna]
        ))

    fig.update_layout(
        title="Gráfico de área apilada de generación",
        xaxis_title="Periodo",
        yaxis_title="Energía",
        legend_title="Planta"
    )

    st.plotly_chart(fig)


def lineasGeneracion(datos,key):
    x_vals = list(range(len(datos)))

    fig = go.Figure()

    for col in datos.columns:
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=datos[col].astype(float),
            mode='lines+markers',
            name=str(col)
        ))

    fig.update_layout(
        title=key,
        xaxis_title="Periodo",
        yaxis_title="Energía",
        legend_title="Planta"
    )

    st.plotly_chart(fig, key=key)

def area(data):
    nombre_columna = data.columns[0]
    periodos = data.columns[1:]

    fig = go.Figure()

    for idx, row in data.iterrows():
        fig.add_trace(go.Scatter(
            x=periodos,
            y=row[1:].astype(float),
            mode='lines',
            stackgroup='one',  # Esto hace el área apilada
            name=row[nombre_columna]
        ))

    fig.update_layout(
        title="Gráfico de área apilada de generación",
        xaxis_title="Periodo",
        yaxis_title="Energía",
        legend_title="Planta"
    )

    st.plotly_chart(fig)