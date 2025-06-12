import streamlit as st
from datetime import datetime
def mostrar_agc(fecha):
    st.header("AGC")
    fechatext = fecha.strftime("%m%d")
    if fecha<=datetime.today().date():
        ruta='Redespacho/'
        archivo="rAGC"+fechatext+".txt"
    else:
        ruta='DESPACHO/'
        archivo="dAGC"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    Data={"seleccionado":"AGC","ruta":ruta,"archivo":archivo,
        "contenidoFTP":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data
def mostrar_agc_unidad(fecha):
    st.header("AGC por Unidad")
    fechatext = fecha.strftime("%m%d")
    if fecha<=datetime.today().date():
        ruta='Redespacho/'
        archivo="rAGCUNIDAD"+fechatext+".txt"
    else:
        ruta='DESPACHO/'
        archivo="dAGCUNIDAD"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    Data={"seleccionado":"AGC_Unidad","ruta":ruta,"archivo":archivo,
        "contenidoFTP":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data