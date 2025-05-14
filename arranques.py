
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd

def arranques(datos):

    #TOP 10 de cantidad de señales por tipo de descripción

    st.subheader('Top 10 de arranques')

    arranques_df = datos[datos['description'].str.contains("arranque", case=False, na=False)]
    st.dataframe(arranques_df.head(5))

    arranque_counts = arranques_df.groupby('description')['description'].count().reset_index(name='count')

    # Sort by count in descending order and take the top 10
    arranque_counts = arranque_counts.sort_values(by='count', ascending=False).head(10)

    st.dataframe(arranque_counts)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Pie chart in the first column
    with col1:
        fig_pie = px.pie(arranque_counts, values='count', names='description', title="Arranques")
        st.plotly_chart(fig_pie)

    # Bar chart in the second column
    with col2:
        fig_bar = px.bar(arranque_counts, x='description', y='count', title="Arranques")
        st.plotly_chart(fig_bar)
