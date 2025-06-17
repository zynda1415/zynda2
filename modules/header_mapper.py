# modules/header_mapper.py
import streamlit as st
import pandas as pd
from data import connect_sheet

@st.cache_data(ttl=300)
def get_header_map():
    sheet = connect_sheet().worksheet_by_title("SheetConfig")
    df = sheet.get_as_df()
    grouped = df.groupby("sheet")
    result = {}
    for sheet_name, group in grouped:
        mapping = dict(zip(group["field_key"], group["header"]))
        result[sheet_name] = mapping
    return result

def get_headers(sheet_name):
    return get_header_map().get(sheet_name, {})
