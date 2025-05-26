import streamlit as st
import pandas as pd

def entrega(df):
    st.title("📊 Dashboard de Incidentes Eléctricos")

    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # 🔢 Métricas generales
    st.header("🔹 Resumen General")
    df_llamadas = df[df["Origen"] == "PhoneCallCreated"]
    df_eventos = df[df["Origen"] != "PhoneCallCreated"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total incidentes", len(df))
    col2.metric("📞 Llamadas", len(df_llamadas))
    col3.metric("🛠️ Eventos de campo", len(df_eventos))

    #st.markdown("---")

    # Agrupación por zona
    st.header("🔹 Total de incidentes por zona")
    incidentes_zona = df.groupby("SubregionName").size().reset_index(name="Cantidad de Incidentes")
    incidentes_zona = incidentes_zona.sort_values(by="Cantidad de Incidentes", ascending=False)
    st.dataframe(incidentes_zona)
    st.bar_chart(incidentes_zona.set_index("SubregionName"))

    st.markdown("---")

    # 🔌 Clientes sin servicio por zona (eventos)
    st.header("🔹 Clientes sin servicio por zona (eventos de campo)")
    eventos = df_eventos.groupby("SubregionName")["NumUnrestCustomers"].sum().reset_index()
    eventos = eventos.rename(columns={"NumUnrestCustomers": "Clientes sin servicio"})
    eventos = eventos.sort_values(by="Clientes sin servicio", ascending=False)

    st.dataframe(eventos)
    st.bar_chart(eventos.set_index("SubregionName"))

    st.markdown("---")

    # 📅 Detalles de eventos de campo por subregión
    st.header("🔹 Detalles de eventos de campo por subregión")

    # Asegurar que CreateTime es datetime y limpiar fechas inválidas
    df_eventos["Fecha"] = pd.to_datetime(df_eventos["CreateTime"], errors='coerce')
    df_eventos = df_eventos.dropna(subset=["Fecha"])
    df_eventos["Fecha"] = df_eventos["Fecha"].dt.strftime("%d/%m/%Y")

    # Renombrar columnas para mejor presentación
    df_eventos_detalle = df_eventos.rename(columns={
        "UID": "Incidente",
        "SubstationName": "Subestación",
        "FeederName": "Circuito",
        "Name": "BOL",
        "NumUnrestCustomers": "Clientes sin servicio"
    })[["Fecha", "Incidente", "Subestación", "Circuito", "Dispositivo", "BOL", "SubregionName", "Clientes sin servicio"]]

    # Mostrar una tabla por cada subregión
    for subregion in sorted(df_eventos_detalle["SubregionName"].dropna().unique()):
        st.subheader(f"📍 Subregión: {subregion}")
        tabla_subregion = df_eventos_detalle[df_eventos_detalle["SubregionName"] == subregion].drop(columns=["SubregionName"])
        st.dataframe(tabla_subregion)