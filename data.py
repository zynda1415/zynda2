import streamlit as st
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

# === Setup ===
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
scope = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_data(ttl=60)
def connect_sheet():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID)

# === Inventory ===
def load_inventory_data():
    sheet = connect_sheet().worksheet("Items")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_inventory_data(df):
    sheet = connect_sheet().worksheet("Items")
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# === Invoices ===
def load_invoice_data():
    sheet = connect_sheet().worksheet("Invoices")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_invoice_data(df):
    sheet = connect_sheet().worksheet("Invoices")
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# === Clients ===
def load_clients_data():
    sheet = connect_sheet().worksheet("Clients")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_clients_data(df):
    sheet = connect_sheet().worksheet("Clients")
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
