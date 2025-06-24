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

    # Cargar datos
   
    #st.title("Mapa de Incidentes - Valle del Cauca")

    # Cargar el archivo GeoJSON (usa la URL raw de GitHub)
    #url = "https://raw.githubusercontent.com/finiterank/mapa-colombia-js/master/colombia-municipios.json"

    #st.dataframe(datos)
    Inc_substation = datos.groupby('SubstationName')['SubstationName'].count().reset_index(name='count')
    #st.dataframe(Inc_substation)

    # Cargar el GeoJSON en un GeoDataFrame
    #gdf = gpd.read_file(url)

    base_path = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(base_path, "datos", "Mapa", "Colombia.geo.json")
    colombia_map = gpd.read_file(geojson_path)

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

    
    # --- Agregar LATITUDE y LONGITUDE a Inc_substation por coincidencia exacta con ALIAS ---
    def match_lat_lon(substation_name, subestaciones_df):
        # Coincidencia exacta (ignorando mayúsculas/minúsculas y espacios)
        key = str(substation_name).strip().lower()
        for _, row in subestaciones_df.iterrows():
            alias = str(row['SUBESTACION']).strip().lower()
            if alias == key:
                return row['LATITUDE'], row['LONGITUDE']
        return None, None

    if 'SubstationName' in Inc_substation.columns and 'SUBESTACION' in Subestaciones.columns:
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

    #st.dataframe(Inc_substation)

    column1, column2 = st.columns([1,1])

    with column1:
        # Graficar
        fig, ax = plt.subplots(figsize=(8, 10))
        fig.patch.set_facecolor('#0E1117')   ##0E1117
        ax.set_facecolor('black')

        # Dibujar mapa base con fondo oscuro
        colombia_filtered.plot(ax=ax, color="#707072", edgecolor="#D5752D")
        #color= '#D5752D'
        #    color='#59595B',
        
        # Ordenar por 'count' descendente y tomar los tres primeros
        top3 = Inc_substation.sort_values(by='count', ascending=False).head(3)

        #st.dataframe(top3)
    
        collection = subestation_gdf.plot(
            ax=ax,
            markersize=Inc_substation['count']*30,   # Tamaño proporcional
            column='count',                          # Color según la columna 'count'
            cmap='OrRd',                             # Puedes usar otros colormaps como 'viridis', 'plasma', etc.
            alpha=0.7,
            edgecolor='#D5752D',
            legend=True                              # Muestra la leyenda de colores
        )
        # Hacer la barra de color más pequeña
        if hasattr(collection, 'get_figure'):
            cbar = collection.get_figure().axes[1]  # El colorbar es el último eje
            cbar.set_position([0.75, 0.33, 0.03, 0.3])  # [left, bottom, width, height] (ajusta a tu gusto)


        for x, y in zip(subestation_gdf.geometry.x, subestation_gdf.geometry.y):
            ax.text(x, y, "", color='white', fontsize=10, ha='right', va='bottom')
        # Título y visualización

        # Anotar solo los tres con más datos
        for _, row in top3.iterrows():
            x = row['LONGITUDE']
            y = row['LATITUDE']
            label = row['SubstationName']
            ax.text(x, y, label, color='white', fontsize=10, ha='right', va='bottom', fontweight='bold')


        plt.title(
            "Incidentes",
            fontsize=22,
            color='#D5752D',
            fontname='Arial',
            fontweight='bold'
        )
        plt.axis('off')
        st.pyplot(fig)

    ##------------prueba de mapa con pydeck----------------
    with column2:         

        # Crear DataFrame para pydeck
        map_data = Inc_substation[['LATITUDE', 'LONGITUDE', 'count', 'SubstationName']].rename(
            columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'}
        )

        with st.container(border=True):
            #st.subheader("🟣 Mapa de Operaciones en Tiempo Real")
            
            # Configurar vista inicial centrada entre Valle del Cauca y Tolima
            view_state = pdk.ViewState(
                latitude=4.2,   # Aproximadamente entre ambos departamentos
                longitude=-75.5,
                zoom=7,
                pitch=0,
            )

            # Capa de puntos de calor
            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=map_data,
                get_position='[lon, lat]',
                get_weight="count",
                radius_pixels=50,
                aggregation='"SUM"',
                threshold=0.10,
            )

            # Capa de puntos (opcional, para ver las subestaciones)
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position='[lon, lat]',
                get_radius=200,
                get_fill_color='[255, 140, 0, 160]',
                pickable=True,
                tooltip=True,
            )

            #st.subheader("🟣 Mapa de incidentes por subestación (Valle del Cauca y Tolima)")
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v11",
                    #map_style="mapbox://styles/mapbox/light-v11",
                    initial_view_state=view_state,
                    layers=[heatmap_layer, scatter_layer],
                    tooltip={"text": "{SubstationName}\nIncidentes: {count}"}
                ),
                use_container_width=True,
            )