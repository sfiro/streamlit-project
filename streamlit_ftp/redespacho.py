import streamlit as st
from datetime import datetime
def mostrar_redespacho(fecha):
    st.header("Resdespacho")
    fechatext = fecha.strftime("%m%d")
    if fecha<=datetime.today().date():
        ruta='Redespacho/'
        archivo="rDec"+fechatext+".txt"
    else:
        ruta='DESPACHO/'
        archivo="dDec"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    Data={"seleccionado":"Redespacho","ruta":ruta,"archivo":archivo,
        "contenidoFTP":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data

def mostrar_despacho(fecha):
    #st.header("Despacho")
    fechatext = fecha.strftime("%m%d")
    
    ruta='DESPACHO/'
    archivo="dDEC"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    #st.write("Ruta del archivo:", ruta)
    Data={"seleccionado":"Despacho","ruta":ruta,"archivo":archivo,
        "contenidoFTP":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data

def mostrar_agc(fecha):
    #st.header("Despacho")
    fechatext = fecha.strftime("%m%d")
    
    ruta='DESPACHO/'
    archivo="dAGC"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    #st.write("Ruta del archivo:", ruta)
    Data={"seleccionado":"Despacho","ruta":ruta,"archivo":archivo,
        "contenidoFTP":[],
        "error":{"Mensaje":"","Bandera":False}}
    return Data


