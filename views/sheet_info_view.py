import streamlit as st
import data

def sheet_info_module():
    st.title("📋 Sheet Info")

    sheets = {
        "Inventory": data.load_inventory(),
        "Clients": data.load_clients(),
        "Sales": data.load_sales(),
        "Invoices": data.load_invoices()
    }

    for name, df in sheets.items():
        with st.expander(f"🗂 {name} Columns"):
            st.write(df.columns.tolist())
