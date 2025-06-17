import streamlit as st

# ✅ MUST BE FIRST
st.set_page_config(page_title="ZYNDA_SYSTEM Inventory Management", layout="wide")

# === Import views/modules ===
from modules import item, clients, sales, invoice, mapview
from views import (
    inventory_view,
    statistics_view,
    catalog_view,
    sheet_info_view,
    sales_charts
)

# === Sidebar navigation ===
st.sidebar.title("🧭 ZYNDA_SYSTEM Menu")
page = st.sidebar.radio("Select a section:", [
    "📦 View Inventory",
    "🧾 Invoices",
    "👥 Clients Management",
    "📘 View Catalog",
    "📊 Statistics",
    "🗺️ Map",
    "📈 Sales",
    "📉 Sales Summary",
    "📊 Sales Charts",
    "🛠️ Sheet Info"
])

# === Page routing ===
if page == "📦 View Inventory":
    inventory_view.inventory_view_module()

elif page == "🧾 Invoices":
    invoice.render_invoice_section()

elif page == "👥 Clients Management":
    clients.render_client_section()

elif page == "📘 View Catalog":
    catalog_view.catalog_module()

elif page == "📊 Statistics":
    statistics_view.statistics_view()

elif page == "🗺️ Map":
    mapview.map_module()

elif page == "📈 Sales":
    sales.sales_module()

elif page == "📉 Sales Summary":
    sales.sales_module()  # optional: separate summary module

elif page == "📊 Sales Charts":
    sales_charts.sales_charts_module()

elif page == "🛠️ Sheet Info":
    sheet_info_view.sheet_info_module()
