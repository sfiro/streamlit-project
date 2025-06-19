import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.graph_objects as go
import numpy as np

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
     "ALTO ANCHICAYA GENERACION",
    "BAJO ANCHICAYA GENERACION", 
    "CALIMA GENERACION",  
    "SALVAJINA GENERACION",
    "PRADO GENERACION",
    "CUCUANA GENERACION",
]

plantas_mayor = [
     "ALTO ANCHICAYA",
    "BAJO ANCHICAYA", 
    "CALIMA", 
    "SALVAJINA", 
    "PRADO", 
    "CUCUANA", 
]

Columnas_plantas = [
    "DIA",
    "ALTO ANCHICAYA NIVEL",
    "ALTO ANCHICAYA GENERACION",
    "ALTO ANCHICAYA CAUDAL",
    "BAJO ANCHICAYA NIVEL",
    "BAJO ANCHICAYA GENERACION",
    "BAJO ANCHICAYA CAUDAL", 
    "CALIMA NIVEL",
    "CALIMA GENERACION", 
    "CALIMA CAUDAL", 
    "SALVAJINA NIVEL",
    "SALVAJINA GENERACION",
    "SALVAJINA CAUDAL", 
    "PRADO NIVEL",
    "PRADO GENERACION",
    "PRADO CAUDAL",
    "CUCUANA NIVEL",
    "CUCUANA GENERACION",
    "CUCUANA CAUDAL",
    "CUCUANA CAUDAL RIO",
    "CUCUANA CAUDAL EN SITIO",
    "CUCUANA VOLUMEN UTILIZADO",
    "CUCUANA VOLUMEN AGUA VERTIDA",
    "CUCUANA CAUDAL ECOLOGICO",
    "CUCUANA RIO SAN MARCOS CAUDAL DESVIADO",
    "CUCUANA RIO SAN MARCOS CAUDAL ECOLOGICO",
    "CUCUANA RIO SAN MARCOS CAUDAL NATURAL",
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
        
        df_plantas.columns = Columnas_plantas
        df_plantas = df_plantas.iloc[1:].reset_index(drop=True)
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
        plantas_mayores.columns = plantas_mayor
        #st.dataframe(plantas_mayores)
        #lineas(plantas_mayores.T,"Generacion plantas")
        
        #st.dataframe(plantas_mayores.T)
        lineasGeneracion(plantas_mayores,"Generación por planta mayor")

        # 1. Eliminar columnas cuya suma es cero
        plantas_mayores_filtrado = plantas_mayores.loc[:, plantas_mayores.sum(axis=0) != 0]

        # 2. Ordenar columnas por la suma de sus valores en orden descendente
        suma_columnas = plantas_mayores_filtrado.sum(axis=0)
        columnas_ordenadas = suma_columnas.sort_values(ascending=True).index
        plantas_mayores_ordenado = plantas_mayores_filtrado[columnas_ordenadas]

        areaGen(plantas_mayores_ordenado,"prueba")

        dia_actual = datetime.now().day  # Día del mes (1-31)

        columna1, columna2 = st.columns([1,5])
        with columna1:
            st.image(r"C:\Users\gestioncc\Documents\proyecto_streamlit\streamlit-project\logo\solar.png", width=200)
            
        with columna2:
            color = "#FFD700"
            barras(df_sol,dia_actual,"sol", color)

        ## plantas termicas

        columna1, columna2 = st.columns([1,5])
        with columna1:
            st.image(r"C:\Users\gestioncc\Documents\proyecto_streamlit\streamlit-project\logo\energia-hidro.png", width=200)
            
        with columna2:
            color = "#095AF1"
            barras(df_hidro,dia_actual,"hidro", color)


        ## plantas cogeneradoras

        columna1, columna2 = st.columns([1,5])
        with columna1:
            st.image(r"C:\Users\gestioncc\Documents\proyecto_streamlit\streamlit-project\logo\sustainable-energy.png", width=200)
            
        with columna2:
            color = "#F18509"
            barras(df_coge,dia_actual,"coge", color)

        
        ## plantas termicas
        
        columna1, columna2 = st.columns([1,5])
        with columna1:
            st.image(r"C:\Users\gestioncc\Documents\proyecto_streamlit\streamlit-project\logo\industria.png", width=200)
            
        with columna2:
            color = "#FFFFFF"
            #st.dataframe(df_term)
            barras(df_term,dia_actual,"term", color)

            

            
            

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
        xaxis_title="Día",
        yaxis_title="Energía kWh",
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

     # Define una lista de colores (puedes personalizarla)
    colores = [
        "#FF5733", "#13A2E1", "#F5F6FA", "#FFD700", "#33FF57", "#3357FF",
        "#D5752D", "#8A2BE2", "#00CED1", "#FF1493", "#228B22", "#DC143C"
    ]

    fig = go.Figure()

    for idx, row in data.iterrows():
        color = colores[idx % len(colores)]  # Asigna un color por fila
        fig.add_trace(go.Scatter(
            x=periodos,
            y=row[1:].astype(float),
            mode='lines',
            stackgroup='one',  # Esto hace el área apilada
            name=row[nombre_columna],
            line=dict(color=color)
        ))

    fig.update_layout(
        title="Gráfico de área apilada de generación",
        xaxis_title="Día",
        yaxis_title="Energía kWh",
        legend_title="Planta"
    )

    st.plotly_chart(fig)


def lineasGeneracion(datos,key):
    x_vals = list(range(1,len(datos)+1))

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
        xaxis_title="Día",
        yaxis_title="Energía kWh",
        legend_title="Planta"
    )

    st.plotly_chart(fig, key=key)

def areaGen(data,key):
    nombre_columna = data.columns
    periodos = list(range(1, len(data) + 1))
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=periodos,
            y=data[col].astype(float),
            mode='lines',
            stackgroup='one',  # Esto hace el área apilada
            name=col
        ))

    fig.update_layout(
        title="Gráfico de área apilada de generación",
        xaxis_title="Día",
        yaxis_title="Energía kWh",
        legend_title="Planta"
    )

    st.plotly_chart(fig, key=key)


def barras(data,dia,key, color):
    data = data.iloc[0, 1:][data.iloc[0, 1:] > 0]
    if data.eq(0).all():
        pass
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data.index,   # Nombres de las columnas
            y=data.values,  # Valores numéricos
            name='Generación solar > 0',
            marker_color=color          # Amarillo
        ))
        # Agrega el número como anotación centrada arriba
        fig.add_annotation(
            text=f"<b>{data.iloc[-1]:.0f} kWh</b>",  # HTML para negrita
            xref="paper", yref="paper",
            x=0.5, y=1.15,  # Ajusta y para que quede fuera del área del gráfico
            showarrow=False,
            font=dict(size=32, color=color, family="Arial"),
            align="center"
        )
        fig.update_layout(
            title="",
            xaxis_title="Día",
            yaxis_title="kWh",
            width=300,   # Ancho en píxeles
            height=250,   # Alto en píxeles
            plot_bgcolor='rgba(0,0,0,0)',   # Fondo del área de datos transparente
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo total de la figura transparente
            margin=dict(t=50, b=10, l=10, r=10)  # Márgenes pequeños
        )
        st.plotly_chart(fig,use_container_width=False)