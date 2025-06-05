# ---------- data.py ----------
import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

# Setup Google Sheets
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
