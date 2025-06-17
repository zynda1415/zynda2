# modules/purchase_history.py
import streamlit as st
from utils.gsheet import load_sheet
from header_mapper import load_header_map

def purchase_history_module():
    st.header("📈 Purchase History")

    headers = load_header_map()
    df = load_sheet("PurchaseHistory")

    search = st.text_input("Search by Item").lower()
    if search:
        df = df[df[headers["item"]].astype(str).str.lower().str.contains(search)]

    st.dataframe(df)
