import streamlit as st
from config import HEADER_ALIASES
from data import load_clients_data

H = HEADER_ALIASES["Clients"]

def map_module():
    st.title("📍 Client Map View")
    df = load_clients_data()

    if "Latitude" in df.columns and "Longitude" in df.columns:
        st.map(df[["Latitude", "Longitude"]].dropna())
    else:
        st.warning("Missing Latitude and Longitude columns.")
