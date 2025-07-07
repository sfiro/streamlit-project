import os
import streamlit as st
import pandas as pd
from pydataxm.pydataxm import ReadDB

# Título
st.title("🔌 Consulta API XM con Streamlit y pydataxm")

# Proxy opcional
proxy = os.getenv("HTTP_PROXY")
if proxy:
    st.info(f"🌍 Usando proxy: {proxy}")

# Inicializar API
try:
    api = ReadDB(proxy=proxy) if proxy else ReadDB()
    collections = api.get_collections()
    st.success("✅ Conectado a la API XM")
except Exception as e:
    st.error(f"Error conexión API: {e}")
    st.stop()

# Selectboxes dinámicos
metric_list = list(collections.keys())
st.dataframe(metric_list)
metric = st.selectbox("Métrica (MetricId)", metric_list)

entities = [c[1] for c in collections[metric]]  # ejemplo: "Sistema", "Recurso", etc.
entity = st.selectbox("Cruce (Entity)", entities)

# Fechas
start = st.date_input("Fecha inicio")
end = st.date_input("Fecha fin")

# Filtro si aplica
filters = []
if entity != "Sistema":
    available_filters = [f[0] for f in collections[metric] if f[1] == entity]
    sel = st.multiselect("Filtros disponibles", options=available_filters)
    filters = sel

# Botón de consulta
if st.button("📥 Consultar datos"):
    try:
        df = api.request_data(metric, entity, start, end, filters or None)
        if df.empty:
            st.warning("⚠️ No se encontraron datos.")
        else:
            st.dataframe(df)
            csv = df.to_csv(index=False).encode()
            st.download_button("Descargar CSV", csv, file_name="xm_data.csv")
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
