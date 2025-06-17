import streamlit as st
from config import HEADER_ALIASES, SHEET_NAMES
from data import load_clients_data

H = HEADER_ALIASES["Clients"]

def map_module():
    st.title("📍 Client Map View")

    try:
        df = load_clients_data()

        if H["latitude"] in df.columns and H["longitude"] in df.columns:
            st.map(df[[H["latitude"], H["longitude"]]].dropna())
        else:
            st.warning("Latitude and Longitude columns are missing in the selected sheet.")

    except Exception as e:
        st.error(f"Failed to load map view: {e}")
