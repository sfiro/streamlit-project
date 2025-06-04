import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import requests
import geopandas as gpd
import matplotlib.pyplot as plt

# Título de la app

def mapas():
    st.title("Mapa de Incidentes - Valle del Cauca")

    import geopandas as gpd
    import matplotlib.pyplot as plt

    # Cargar el archivo GeoJSON (usa la URL raw de GitHub)
    #url = "https://raw.githubusercontent.com/finiterank/mapa-colombia-js/master/colombia-municipios.json"

    # Cargar el GeoJSON en un GeoDataFrame
    #gdf = gpd.read_file(url)

    gdf = gpd.read_file("\\Users\\accontrol\\Documents\\streamlit\\streamlit-project\\datos\\municipios_GeoJSON.geojson\\municipios_GeoJSON.geojson")

    # Mostrar las columnas disponibles en Streamlit para depuración
    st.write('Columnas disponibles:', gdf.columns.tolist())

    # Filtrar por el departamento "Valle del Cauca" usando la columna correcta
    gdf_valle = gdf[gdf['dpt'] == 'VALLE DEL CAUCA']
    gdf_tolima = gdf[gdf['dpt'] == 'TOLIMA']
    st.write('Filtrado por dpt == VALLE DEL CAUCA:', gdf_valle)
    st.write(gdf.crs)

  
    gdf_todo=pd.concat([gdf_valle, gdf_tolima], ignore_index=True)
     # Convertir el GeoDataFrame filtrado a formato GeoJSON
 


    # Datos ficticios de incidentes
    
    data = pd.DataFrame([
        {"lugar": "Cali", "lat": 3.4516, "lon": -76.5320, "cantidad": 12},
        {"lugar": "Palmira", "lat": 3.5394, "lon": -76.3033, "cantidad": 4},
        {"lugar": "Buenaventura", "lat": 3.8801, "lon": -77.0312, "cantidad": 6},
        {"lugar": "Tuluá", "lat": 4.0847, "lon": -76.1954, "cantidad": 3},
    ])

    #Graficar el polígono de los departamentos y los incidentes como círculos
    if not gdf_todo.empty:
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf_todo.plot(ax=ax, edgecolor='black', cmap='Dark2')
        # Graficar los incidentes como círculos
        plt.title(f"Polígonos y puntos de incidentes")
        plt.axis('off')
        plt.legend()
        st.pyplot(fig)
    else:
        st.warning('No se encontró el municipio solicitado en el GeoDataFrame.')

    # if not gdf_todo.empty:
    #     fig, ax = plt.subplots(figsize=(10, 10))
    #     gdf_todo.plot(ax=ax, edgecolor='black', facecolor='lightgray')

    #     # Agregar los puntos de incidentes
    #     ax.scatter(data["lon"], data["lat"], s=data["cantidad"]*2, color="red", alpha=0.6, edgecolor="black", label="Incidentes")

    #     plt.title("Mapa de Municipios y Puntos de Incidentes")
    #     plt.axis('off')
    #     ax.legend()
    #     st.pyplot(fig)
    # else:
    #     st.warning('No se encontró el municipio solicitado en el GeoDataFrame.')
    

