# modules/clients.py
import streamlit as st
import pandas as pd
from utils.gsheet import load_sheet
from header_mapper import load_header_map

def clients_module():
    st.header("👥 Clients")

    headers = load_header_map()
    df = load_sheet("Clients")

    # Optional Filters
    client_type = st.selectbox("Filter by Type", ["All"] + sorted(df[headers["type"]].dropna().unique()))
    if client_type != "All":
        df = df[df[headers["type"]] == client_type]

    search = st.text_input("🔍 Search by Name or Phone").lower()
    if search:
        df = df[df[headers["name"]].astype(str).str.lower().str.contains(search) |
                df[headers["phone"]].astype(str).str.lower().str.contains(search)]

    # Display Table
    st.dataframe(df)

    # Coordinates Check
    if headers.get("latitude") in df.columns and headers.get("longitude") in df.columns:
        st.success("✅ Coordinates found — ready for map view")
    else:
        st.warning("⚠️ Latitude and Longitude fields not found in sheet")
