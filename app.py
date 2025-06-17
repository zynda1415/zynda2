# app.py
import streamlit as st

# Import from folders
from modules import item, clients, invoice, returns, purchase_history
from views import catalog_view, mapview

st.set_page_config(page_title="ZYNDA SYSTEM", layout="wide")

# Sidebar Navigation
st.sidebar.title("ZYNDA SYSTEM")
tab = st.sidebar.radio("📁 Select Module", [
    "📦 Inventory",
    "👥 Clients",
    "🧾 Invoices",
    "↩️ Returns",
    "📈 Purchase History",
    "📘 View Catalog",
    "🗺️ Map View"
])

# Route to each module
if tab == "📦 Inventory":
    item.inventory_module()

elif tab == "👥 Clients":
    clients.clients_module()

elif tab == "🧾 Invoices":
    invoice.invoices_module()

elif tab == "↩️ Returns":
    returns.returns_module()

elif tab == "📈 Purchase History":
    purchase_history.purchase_history_module()

elif tab == "📘 View Catalog":
    catalog_view.catalog_module()

elif tab == "🗺️ Map View":
    mapview.map_module()
