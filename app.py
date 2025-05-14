
import streamlit as st
import pandas as pd
import plotly.express as px
from arranques import arranques
from disparos import disparos
from resumen import resumen
from señales import señales
from precios import precios
import requests  # Importar la librería para trabajar con APIs
import json  # Importar la librería para trabajar con JSON


def main():
    st.title('Aplicación de visualización de datos')
    st.subheader('Datos de ingreso')
    
    archivo_datos = st.file_uploader("subir CSV", type=["csv", "xlsx"])
    if archivo_datos is not None:
        try:
            detalle_archivo = {
                "Nombre del archivo": archivo_datos.name,
                "Tipo de archivo": archivo_datos.type,
                "Tamaño del archivo": archivo_datos.size
            }
            st.write(detalle_archivo)

            if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                datos = pd.read_excel(archivo_datos)
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                datos = pd.read_csv(archivo_datos)
            else:
                st.error("Formato de archivo no soportado.")
                return

            if datos.empty:
                st.warning("El archivo cargado está vacío.")
                return

            st.dataframe(datos.head(5))

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

    if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        datos = pd.read_excel(archivo_datos)
    elif detalle_archivo["Tipo de archivo"] == "text/csv":
        datos = pd.read_csv(archivo_datos)
    else:
        datos = pd.DataFrame()

    ##---------------------------------------------------------------
    st.sidebar.title("Menú lateral")
    opcion = st.sidebar.selectbox("Selecciona una opción", ["Resumen","señales","Arranques", "Disparos", "Precios"])

    # Mostrar contenido según la opción seleccionada
    if opcion == "Resumen":
        resumen(datos)

    if opcion == "señales":
        señales(datos)

    if opcion == "Arranques":
        arranques(datos)

    elif opcion == "Disparos":
        disparos(datos)

    elif opcion == "Precios":
        precios()

    ##---------------------------------------------------------------




  # Cargar datos de ejemplo
if __name__ == '__main__':
  main()