import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json


def precios():
    # Título de la sección
    st.title("Consulta de precios desde la API")

    # Selección de fechas con un calendario
    st.subheader("Selecciona el rango de fechas")
    start_date = st.date_input("Fecha de inicio", value=pd.to_datetime("2025-05-03"))
    end_date = st.date_input("Fecha de fin", value=pd.to_datetime("2025-05-03"))

    # Convertir las fechas seleccionadas a formato string (YYYY-MM-DD)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    
    # Parámetros de la API
    dataset_id = 'EC6945'
    columnDestinyName = 'null'  # Nombre de la columna destino a filtrar
    values = 'null'  # Valores para filtrar

    # Construir la URL de la API
    url = f"https://www.simem.co/backend-files/api/PublicData?startDate={start_date}&enddate={end_date}&datasetId={dataset_id}&columnDestinyName={columnDestinyName}&values={values}"

     # Realizar la solicitud a la API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        data = json.loads(response.content)  # Convertir la respuesta a JSON

        # Extraer los registros de la respuesta
        records = data.get("result", {}).get("records", [])
        if not records:
            st.warning("No se encontraron datos en la respuesta de la API.")
            return

        # Convertir los registros a un DataFrame
        df = pd.DataFrame(records)

        # Verificar si el DataFrame tiene datos
        if df.empty:
            st.warning("No se encontraron datos en la respuesta de la API.")
            return

        # Convertir la columna FechaHora a formato datetime
        df['FechaHora'] = pd.to_datetime(df['FechaHora'])


        # Mostrar los datos en un DataFrame interactivo
        st.subheader("Datos obtenidos desde la API")
        st.dataframe(df)

        # Graficar los datos
        st.subheader("Gráfico de precios por hora")
        fig = px.line(df, x='FechaHora', y='Valor', color='CodigoVariable',
                      title='Precios por Hora',
                      labels={'FechaHora': 'Fecha y Hora', 'Valor': 'Precio (COP/kWh)', 'CodigoVariable': 'Variable'})
        st.plotly_chart(fig)


        df_filtrado = df[df['CodigoVariable'] == 'PB_Nal']
        df_filtrado = df_filtrado[df_filtrado['Version'] == 'TX1']
        st.subheader("Gráfico de precios por hora (PB_Nal)")
        fig_filtrado = px.line(df_filtrado, x='FechaHora', y='Valor', color='CodigoVariable',
                               title='Precios por Hora (PB_Nal)',
                               labels={'FechaHora': 'Fecha y Hora', 'Valor': 'Precio (COP/kWh)', 'CodigoVariable': 'Variable'})
        st.plotly_chart(fig_filtrado)

        st.dataframe(df_filtrado)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos desde la API: {e}")
    except json.JSONDecodeError:
        st.error("Error al decodificar la respuesta de la API.")


