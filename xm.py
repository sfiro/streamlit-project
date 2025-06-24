import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.graph_objects as go
import numpy as np
from pydataxm.pydatasimem import ReadSIMEM, CatalogSIMEM
from pydataxm.pydataxm import ReadDB



def xm_data():
    # Importación
    

    # Crear una instancia de catalogo con el tipo
    catalogo_vbles = CatalogSIMEM('variables')

    # Extraer información a utilizar
    print("Nombre: ", catalogo_vbles.get_name())
    print("Metadata: ", catalogo_vbles.get_metadata())
    print("Columnas: ", catalogo_vbles.get_columns())

    # Dataframe con información de las variables
    data = catalogo_vbles.get_data()
    st.write(data)


    # Buscar el id del conjunto de datos
    catalogo = CatalogSIMEM('Datasets')
    data_catalogo = catalogo.get_data()
    print(data_catalogo.query("nombreConjuntoDatos.str.contains('Generación Real')"))

    # Crear una instancia de ReadSIMEM
    dataset_id = 'b7917a'
    fecha_inicio = '2025-06-20'
    fecha_fin = '2025-06-24'
    generacion = ReadSIMEM(dataset_id, fecha_inicio, fecha_fin)

    # Recuperar datos
    data = generacion.main(filter=False)
    st.write(data)