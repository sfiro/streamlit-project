import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Título de la app

def mapas(datos):
    st.title("Mapa de Incidentes - Valle del Cauca")

    # Cargar el archivo GeoJSON (usa la URL raw de GitHub)
    #url = "https://raw.githubusercontent.com/finiterank/mapa-colombia-js/master/colombia-municipios.json"

    #st.dataframe(datos)
    Inc_substation = datos.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
    #EstadoInc_counts = EstadoInc_counts.sort_values(by='count', ascending=False)
    #st.dataframe(Inc_substation)

    # Cargar el GeoJSON en un GeoDataFrame
    #gdf = gpd.read_file(url)

    colombia_map = gpd.read_file("\\Users\\accontrol\\Documents\\streamlit\\streamlit-project\\datos\\municipios_GeoJSON.geojson\\Colombia.geo.json")

    # Filtrar solo Valle del Cauca y Tolima
    departments = ["VALLE DEL CAUCA", "TOLIMA"]
    colombia_filtered = colombia_map[colombia_map['NOMBRE_DPT'].isin(departments)]

     # Convertir el GeoDataFrame filtrado a formato GeoJSON
 
    # Leer Subestaciones.csv de forma robusta y mostrar primeras líneas para depuración
    subestaciones_path = os.path.join("datos", "Subestaciones.csv")

    try:
        Subestaciones = pd.read_csv(subestaciones_path, on_bad_lines='skip', encoding='utf-8')
        if list(Subestaciones.columns)[0] == Subestaciones.columns.name or Subestaciones.shape[1] == 1:
            # Intentar con delimitador punto y coma
            Subestaciones = pd.read_csv(subestaciones_path, on_bad_lines='skip', encoding='utf-8', delimiter=';')
    except UnicodeDecodeError:
        Subestaciones = pd.read_csv(subestaciones_path, on_bad_lines='skip', encoding='latin1')
    except Exception as e:
        st.error(f"Error al leer Subestaciones.csv: {e}")
        #Subestaciones = pd.DataFrame()

    # Convertir LATITUDE y LONGITUDE a float, reemplazando coma por punto si es necesario
    if not Subestaciones.empty and 'LATITUDE' in Subestaciones.columns and 'LONGITUDE' in Subestaciones.columns:
        Subestaciones['LATITUDE'] = Subestaciones['LATITUDE'].astype(str).str.replace(',', '.', regex=False)
        Subestaciones['LONGITUDE'] = Subestaciones['LONGITUDE'].astype(str).str.replace(',', '.', regex=False)
        Subestaciones['LATITUDE'] = pd.to_numeric(Subestaciones['LATITUDE'], errors='coerce')
        Subestaciones['LONGITUDE'] = pd.to_numeric(Subestaciones['LONGITUDE'], errors='coerce')

    #st.dataframe(Subestaciones)

    # --- Agregar LATITUDE y LONGITUDE a Inc_substation por coincidencia aproximada con ALIAS ---
    def match_lat_lon(substation_name, subestaciones_df):
        # Tomar las primeras 2 palabras del nombre de la subestación para el match
        key = str(substation_name).split()[:2]
        key = ' '.join(key).lower()
        for _, row in subestaciones_df.iterrows():
            alias = str(row['ALIAS']).lower()
            if alias.startswith(key):
                return row['LATITUDE'], row['LONGITUDE']
        return None, None

    if 'SubstationName' in Inc_substation.columns and 'ALIAS' in Subestaciones.columns:
        latitudes = []
        longitudes = []
        for name in Inc_substation['SubstationName']:
            lat, lon = match_lat_lon(name, Subestaciones)
            latitudes.append(lat)
            longitudes.append(lon)
        Inc_substation['LATITUDE'] = latitudes
        Inc_substation['LONGITUDE'] = longitudes
        #st.dataframe(Inc_substation)

    # Crear GeoDataFrame de las ciudades
    subestation_gdf = gpd.GeoDataFrame(
        Inc_substation,
        geometry=gpd.points_from_xy(Inc_substation.LONGITUDE, Inc_substation.LATITUDE),
        crs="EPSG:4326"
    )

    # Graficar
    fig, ax = plt.subplots(figsize=(8, 10))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Dibujar mapa base con fondo oscuro
    colombia_filtered.plot(ax=ax, color='#222222', edgecolor="#F78400")

    subestation_gdf.plot(
        ax=ax,
        markersize=Inc_substation['count']*10,  # ajusta esta escala si quieres
        color='red',
        alpha=0.7,
        edgecolor='black'
    )

    # Anotar nombres de las ciudades en blanco
    for x, y, label in zip(subestation_gdf.geometry.x, subestation_gdf.geometry.y, Inc_substation['SubstationName']):
        ax.text(x, y, label, color='white', fontsize=3, ha='right', va='bottom')

    # Título y visualización
    plt.title("Valle y Tolima", fontsize=14, color='white')
    plt.axis('off')
    st.pyplot(fig)




