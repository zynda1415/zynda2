import streamlit as st
import pydeck as pdk
import data

def client_map():
    st.header("Client Map View")
    df = data.load_clients()

    if not df.empty:
        st.map(df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}))
    else:
        st.warning("No clients found.")
