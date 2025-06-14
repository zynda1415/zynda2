import streamlit as st
from config import HEADER_ALIASES
from data import load_inventory_data

H = HEADER_ALIASES["Inventory"]

def sales_module():
    st.title("💰 Sales Entry")
    df = load_inventory_data()

    st.selectbox("Select Item", df[H["name"]].dropna().unique())
    st.dataframe(df[[H["name"], H["price"], H.get("stock", "")]].dropna())
