
import streamlit as st
import pandas as pd
import plotly.express as px

def señales(datos):

    #TOP 10 de cantidad de señales por tipo de descripción

    st.subheader('Top 10 Cantidad de señales por descripcion')

    description_counts = datos.groupby('description')['description'].count().reset_index(name='count')

    # Sort by count in descending order and take the top 10
    description_counts = description_counts.sort_values(by='count', ascending=False).head(10)

    st.dataframe(description_counts)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Pie chart in the first column
    with col1:
        fig_pie = px.pie(description_counts, values='count', names='description')
        st.plotly_chart(fig_pie)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(description_counts, x='description', y='count', title="Cantidad de señales")
        st.plotly_chart(fig_bar)
