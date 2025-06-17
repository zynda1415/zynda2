# modules/returns.py
import streamlit as st
from utils.gsheet import load_sheet
from header_mapper import load_header_map

def returns_module():
    st.header("↩️ Returns")

    headers = load_header_map()
    df = load_sheet("Returns")

    search = st.text_input("Search by Invoice ID or Item").lower()
    if search:
        df = df[df[headers["invoice_id"]].astype(str).str.lower().str.contains(search) |
                df[headers["item"]].astype(str).str.lower().str.contains(search)]

    st.dataframe(df)
