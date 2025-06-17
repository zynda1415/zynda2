# views/mapview.py
import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.gsheet import load_sheet
from header_mapper import load_header_map

def map_module():
    st.header("🗺️ Client Map View")

    headers = load_header_map()
    df = load_sheet("Clients")

    lat_col = headers["latitude"]
    lon_col = headers["longitude"]

    if lat_col in df.columns and lon_col in df.columns:
        df = df.dropna(subset=[lat_col, lon_col])
        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=df[lat_col].mean(),
                longitude=df[lon_col].mean(),
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=[lon_col, lat_col],
                    get_color='[200, 30, 0, 160]',
                    get_radius=100,
                ),
            ],
        ))
    else:
        st.warning("❗ Missing latitude/longitude headers in config or data.")
