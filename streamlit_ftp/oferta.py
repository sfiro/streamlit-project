import streamlit as st
from datetime import datetime
import pandas as pd
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
        st.title("Cargando información de la oferta...")
        try:
            st.write("Ruta del archivo:", Data["ruta"] + "\\" + Data["archivo"])
            with open(Data["ruta"] + "\\" + Data["archivo"], "r", encoding="utf-8") as file:
                contenido = file.readlines()

                
                Data["contenidoFTP"] = [linea.strip() for linea in contenido]
                Data['error']['Mensaje'] = ""
                Data['error']['Bandera'] = False
                df= pd.DataFrame(Data["contenidoFTP"])
                st.dataframe(df)
        except Exception as e:
            Data['error']['Mensaje'] = f"Error al cargar el archivo: {e}"
            Data['error']['Bandera'] = True
    else:
        if not Data["contenidoFTP"]:
            Data['error']['Mensaje'] = "No hay datos cargados. Por favor, recargue la información."
            Data['error']['Bandera'] = True
    return df