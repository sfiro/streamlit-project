import streamlit as st
import pandas as pd
import plotly.express as px

def disparos(datos):
    # filtro de las señales de disparo de la base de datos

    st.subheader('Top 10 Cantidad de señales de disparo')

    disparos_df = datos[datos['description'].str.contains("disparo", case=False, na=False)]
    st.dataframe(disparos_df.head(5))

    # Extraer las horas de la columna FieldTime
    disparos_df['Hora'] = pd.to_datetime(disparos_df['FieldTime']).dt.hour
    # Contar registros por hora
    disparos_por_hora = disparos_df.groupby('Hora')['Hora'].count().reset_index(name='Cantidad')

#-------- resumen de señales en tres columnas
    st.subheader('Resumen de Señales')

    total_records = len(disparos_df)
    num_substations = disparos_df['substationName'].nunique()
    num_devices = disparos_df['deviceName'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total disparos", value=total_records)

    with col2:
        st.metric(label="Disparo por Subestaciones", value=num_substations)

    with col3:
        st.metric(label="Disparos por Dispositivos", value=num_devices)




    st.subheader('Cantidad de señales de disparos por zona')
    disparo_counts = disparos_df.groupby('subregionName')['subregionName'].count().reset_index(name='count1')
    st.dataframe(disparo_counts)

    st.subheader('Cantidad de disparos por elemento')

    # Agrupar y contar los disparos por 'deviceName'
    disparo_element_counts = disparos_df.groupby('deviceName')['deviceName'].count().reset_index(name='count1')

    # Ordenar los datos de mayor a menor según la columna 'count1'
    disparo_element_counts = disparo_element_counts.sort_values(by='count1', ascending=False)

    # Mostrar el DataFrame ordenado
    st.dataframe(disparo_element_counts.head(5))


    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Pie chart in the first column
    with col1:
        fig = px.pie(disparo_counts, values='count1', names='subregionName',title='Disparos por zona')
        fig.update_traces(
        textinfo='label+percent',
        customdata=disparo_counts['count1'],
        hovertemplate='%{label}<br>Cantidad: %{customdata}<br>Porcentaje: %{percent}<extra></extra>',
        textposition='inside'
        )
        st.plotly_chart(fig)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(disparo_counts, x='subregionName', y='count1', title="Disparos por zona")
        st.plotly_chart(fig_bar)

    
    # Mostrar el DataFrame con los conteos por hora
    st.subheader('Cantidad de disparos por hora')
    #st.dataframe(disparos_por_hora)

    # Graficar cantidad de disparos por hora
    fig = px.bar(disparos_por_hora, x='Hora', y='Cantidad', title='Cantidad de disparos por hora', labels={'Hora': 'Hora del día', 'Cantidad': 'Cantidad de disparos'})
    st.plotly_chart(fig)