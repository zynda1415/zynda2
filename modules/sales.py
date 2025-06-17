import streamlit as st
import pandas as pd
from modules.header_mapper import get_headers
from data import load_inventory_data, load_clients_data, load_invoice_data

H_items = get_headers("Inventory")
H_clients = get_headers("Clients")
H_invoices = get_headers("Invoices")

def sales_module():
    st.title("📈 Sales Summary")

    try:
        df_items = load_inventory_data()
        df_clients = load_clients_data()
        df_invoices = load_invoice_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return

    st.subheader("📦 Items Overview")
    st.dataframe(df_items[[H_items["name"], H_items["stock"], H_items["price"]]])

    st.subheader("👥 Client List")
    st.dataframe(df_clients[[H_clients["name"], H_clients["phone"], H_clients["type"]]])

    st.subheader("🧾 Recent Invoices")
    st.dataframe(df_invoices[[H_invoices["client"], H_invoices["amount"], H_invoices["status"]]])
