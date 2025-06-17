import streamlit as st
import pandas as pd
from data import connect_sheet  # ✅ use your secure function

@st.cache_data(ttl=300)
def get_header_map():
    try:
        sheet = connect_sheet().worksheet_by_title("SheetConfig")
        df = sheet.get_as_df().dropna()
    except Exception as e:
        st.error(f"Failed to load SheetConfig: {e}")
        return {}

    header_map = {}
    for _, row in df.iterrows():
        section = row["sheet"]
        field = row["field_key"]
        header = row["header name"]
        header_map.setdefault(section, {})[field] = header
    return header_map

def get_headers(sheet_name):
    return get_header_map().get(sheet_name, {})
