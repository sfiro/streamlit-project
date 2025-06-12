import streamlit as st
from datetime import datetime
def mostrar_pruebas(fecha):
    st.header("Pruebas")
    fechatext = fecha.strftime("%m%d")
    if fecha<=datetime.today().date():
        ruta='Redespacho/'
        archivo="rPru"+fechatext+".txt"
    else:
        ruta='DESPACHO/'
        archivo="dPru"+fechatext+".txt"
    ruta+= fecha.strftime("%Y-%m")
    Data={"seleccionado":"Pruebas","ruta":ruta,"archivo":archivo,
          "Notacion":{"A":"Pruebas autorizadas","NA":"Pruebas no autorizadas","":"Sin Prueba","R":"Regulación","D":"Dsiponibilidad"},
          "contenidoFTP":[],
          "error":{"Mensaje":"","Bandera":False}}
    return Data