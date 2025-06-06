import streamlit as st
import data
import pandas as pd

def map_module():
    st.header("📍 Client Map View")

    clients_df = data.load_clients()

    map_df = pd.DataFrame({
        'lat': clients_df['Latitude'],
        'lon': clients_df['Longitude']
    })

    st.map(map_df)
