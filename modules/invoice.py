# modules/invoice.py
import streamlit as st
import pandas as pd
from utils.gsheet import load_sheet
from header_mapper import load_header_map

def invoices_module():
    st.header("🧾 Invoices")

    headers = load_header_map()
    df = load_sheet("Invoices")
    items_df = load_sheet("InvoiceItems")

    status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df[headers["status"]].dropna().unique()))
    if status_filter != "All":
        df = df[df[headers["status"]] == status_filter]

    st.dataframe(df)

    with st.expander("📋 View Line Items"):
        selected_invoice = st.selectbox("Select Invoice", df[headers["invoice_id"]])
        filtered_items = items_df[items_df[headers["invoice_id"]] == selected_invoice]
        st.dataframe(filtered_items)
