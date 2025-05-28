import pandas as pd
import plotly.express as px
import streamlit as st

# Título
st.title("Análisis de Vehículos")

# Cargar
car_data = pd.read_csv('notebooks/vehicles_us.csv')

# Crear check-boxes
show_histogram = st.checkbox('Histograma de kilometraje')
show_scatter   = st.checkbox('Diagrama de dispersión (Kilometraje vs Precio)')

# Crear histograma
if show_histogram:
    st.write('### Histograma de kilometraje')
    fig_hist = px.histogram(
        car_data,
        x="odometer",
        title="Distribución del kilometraje",
        labels={"odometer": "Kilometraje (millas)"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Crear diagrama de dispersión
if show_scatter:
    st.write('### Dispersión de kilometraje vs precio')
    fig_scatter = px.scatter(
        car_data,
        x="odometer",
        y="price",
        title="Kilometraje vs Precio",
        labels={"odometer": "Kilometraje (millas)", "price": "Precio (USD)"},
        hover_data=["model_year", "model", "condition"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
