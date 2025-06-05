# ZYNDA_SYSTEM v1.8
# Full Clean Base Structure

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

# ----------- data.py -----------
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = 'your_spreadsheet_id_here'
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

def connect_gsheets():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID)

def load_inventory():
    sheet = connect_gsheets().worksheet('Inventory')
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_inventory(df):
    sheet = connect_gsheets().worksheet('Inventory')
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Similar functions for Clients and Sales

def load_clients():
    sheet = connect_gsheets().worksheet('Clients')
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_clients(df):
    sheet = connect_gsheets().worksheet('Clients')
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

def load_sales():
    sheet = connect_gsheets().worksheet('Sales')
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_sales(df):
    sheet = connect_gsheets().worksheet('Sales')
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# ----------- item.py -----------
import streamlit as st
import data

def item_management():
    st.header("Item Management")
    df = data.load_inventory()
    
    action = st.radio("Item Actions", ["Add Item", "Edit Item", "Delete Item"])
    
    if action == "Add Item":
        with st.form("add_form"):
            name = st.text_input("Item Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", 0)
            purchase_price = st.number_input("Purchase Price", 0.0)
            sale_price = st.number_input("Sale Price", 0.0)
            supplier = st.text_input("Supplier")
            notes = st.text_input("Notes")
            image_url = st.text_input("Image URL")
            submitted = st.form_submit_button("Add")
            if submitted:
                new_row = pd.DataFrame([[name, category, quantity, purchase_price, sale_price, supplier, notes, image_url]],
                                        columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                data.save_inventory(df)
                st.success("Item Added Successfully!")
