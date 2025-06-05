# ----------- app.py -----------
import streamlit as st
from item import item_management
from preview import catalog_view
from statistics_module import show_statistics
from mapview import client_map
from sales import sales_management
from clients import clients_management

st.set_page_config(page_title="Inventory Management System", layout="wide")

menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics", "Catalog View", "Map", "Sales", "Clients"])

if menu == "View Inventory":
    catalog_view()

elif menu == "Item":
    item_management()

elif menu == "Statistics":
    show_statistics()

elif menu == "Map":
    client_map()

elif menu == "Sales":
    sales_management()

elif menu == "Clients":
    clients_management()
