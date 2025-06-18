import streamlit as st
from datetime import datetime
import pandas as pd


nombres_filtrar = [
    "ALBAN", "ALTOANCHICAYA1", "ALTOANCHICAYA2", "ALTOANCHICAYA3",
    "BAJOANCHICAYA1", "BAJOANCHICAYA2", "BAJOANCHICAYA3", "BAJOANCHICAYA4",
    "SALVAJINA", "SALVAJINA1", "SALVAJINA2", "SALVAJINA3",
    "CALIMA", "CALIMA1", "CALIMA2", "CALIMA3", "CALIMA4",
    "PRADO", "PRADO1", "PRADO2", "PRADO3",
    "CUCUANA", "CUCUANA1", "CUCUANA2",
    "MERILECTRICA1",
    "TESORITO", "TESORITO1", "TESORITO2", "TESORITO3", "TESORITO4",
    "TESORITO5", "TESORITO6", "TESORITO7", "TESORITO8", "TESORITO9",
    "TESORITO10", "TESORITO11"
]

def mostrar_oferta(fecha):
    st.header("Oferta")
    fechatext = fecha.strftime("%m%d")
    ruta='\\\\EPSAMMAP\\Infomercado\\Oferta\\'
    archivo="epsg"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    Data={"seleccionado":"Redespacho","ruta":ruta,"archivo":archivo,
        "contenido":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data


def CargarInformacionOferta(Data,force_reload):
    #cargar contenido de la oferta en el archivo plano de la ruta
    df=pd.DataFrame()
    if force_reload:
        try:
            st.write("Ruta del archivo:", Data["ruta"] + "\\" + Data["archivo"])
            with open(Data["ruta"] + "\\" + Data["archivo"], "r", encoding="utf-8") as file:
                contenido = file.readlines()

                
                Data["contenidoFTP"] = [linea.strip() for linea in contenido]
                Data['error']['Mensaje'] = ""
                Data['error']['Bandera'] = False

                # Separar cada línea por comas
                filas = [linea.split(',') for linea in Data["contenidoFTP"]]
                df = pd.DataFrame(filas)

                columnas = ['Nombre', 'Tipo'] + [f'H{i}' for i in range(1, df.shape[1] - 1)]
                df.columns = columnas

                #st.dataframe(df)
                #df_filtrado = df[df['Nombre'].str.contains('ALBAN', case=False, na=False)]
                df_filtrado = df[df['Nombre'].isin(nombres_filtrar)]
                st.dataframe(df_filtrado)
        except Exception as e:
            Data['error']['Mensaje'] = f"Error al cargar el archivo: {e}"
            Data['error']['Bandera'] = True
    else:
        if not Data["contenidoFTP"]:
            Data['error']['Mensaje'] = "No hay datos cargados. Por favor, recargue la información."
            Data['error']['Bandera'] = True
    return df