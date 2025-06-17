import streamlit as st
from modules.header_mapper import get_headers
from data import load_clients_data

H = get_headers("Clients")

def map_module():
    st.title("📍 Client Map View")

    try:
        df = load_clients_data()
    except Exception as e:
        st.error(f"Failed to load client data: {e}")
        return

    if H["latitude"] in df.columns and H["longitude"] in df.columns:
        st.map(df[[H["latitude"], H["longitude"]]].dropna())
    else:
        st.warning("Latitude and Longitude columns are missing in the data.")
