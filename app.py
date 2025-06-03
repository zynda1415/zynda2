import streamlit as st
import item
import item_catalog

st.set_page_config(page_title="ZYNDA_SYSTEM v1.6 Catalog v2", layout="wide")

st.sidebar.title("📦 ZYNDA SYSTEM")
page = st.sidebar.radio("Choose page:", ["Item Management", "Catalog View"])

if page == "Item Management":
    item.render_item_section()
elif page == "Catalog View":
    item_catalog.render_catalog_view()
