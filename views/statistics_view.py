import streamlit as st
import pandas as pd
from config import HEADER_ALIASES
from data import load_inventory_data

H = HEADER_ALIASES["Inventory"]

def statistics_module():
    st.title("📊 Inventory Statistics")
    df = load_inventory_data()

    st.metric("Total Items", len(df))

    if H["brand"] in df.columns:
        brand_counts = df[H["brand"]].value_counts()
        st.bar_chart(brand_counts)
    else:
        st.warning("Brand column not found in dataset.")
