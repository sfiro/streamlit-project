import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd

def gestion():
    
    st.title('Datos de ingreso')
    
    archivo_datos = st.file_uploader("subir CSV", type=["csv", "xlsx"])
    if archivo_datos is not None:
        try:
            detalle_archivo = {
                "Nombre del archivo": archivo_datos.name,
                "Tipo de archivo": archivo_datos.type,
                "Tamaño del archivo": archivo_datos.size
            }
            #st.write(detalle_archivo)

            if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                datos = pd.read_excel(archivo_datos, engine="openpyxl")
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                datos = pd.read_csv(archivo_datos, sep=';', skiprows=3)
            else:
                st.error("Formato de archivo no soportado.")
                return

            if datos.empty:
                st.warning("El archivo cargado está vacío.")
                return

            st.dataframe(datos)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    
    # Eliminar los excluibles
    df_incidentes = df_incidentes[~df_incidentes['Causa'].str.startswith('Exc_')]