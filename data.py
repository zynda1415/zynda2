import streamlit as st
import pandas as pd
import json
import pygsheets

# === Setup ===
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"

@st.cache_data(ttl=60)
def connect_sheet():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    client = pygsheets.authorize(service_account_info=creds_dict)
    return client.open_by_key(SPREADSHEET_ID)

# === Inventory ===
def load_inventory_data():
    sheet = connect_sheet().worksheet_by_title("Items")
    return sheet.get_as_df()

def save_inventory_data(df):
    sheet = connect_sheet().worksheet_by_title("Items")
    sheet.clear()
    sheet.set_dataframe(df, start=(1, 1))

# === Invoices ===
def load_invoice_data():
    sheet = connect_sheet().worksheet_by_title("Invoices")
    return sheet.get_as_df()

def save_invoice_data(df):
    sheet = connect_sheet().worksheet_by_title("Invoices")
    sheet.clear()
    sheet.set_dataframe(df, start=(1, 1))

# === Clients ===
def load_clients_data():
    sheet = connect_sheet().worksheet_by_title("Clients")
    return sheet.get_as_df()

def save_clients_data(df):
    sheet = connect_sheet().worksheet_by_title("Clients")
    sheet.clear()
    sheet.set_dataframe(df, start=(1, 1))
