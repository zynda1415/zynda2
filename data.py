import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import json
import streamlit as st

# Google Sheets API setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
client = gspread.authorize(creds)

# Your main spreadsheet
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
sheet = client.open_by_key(SPREADSHEET_ID)

# Inventory functions
def load_inventory():
    ws = sheet.worksheet("Inventory")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# Clients functions
def load_clients():
    ws = sheet.worksheet("Clients")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# Sales functions
def load_sales():
    ws = sheet.worksheet("Sales")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

def save_sale(date, item, name, quantity_sold, unit_price, total_price):
    ws = sheet.worksheet("Sales")
    ws.append_row([date, item, name, quantity_sold, unit_price, total_price])

def load_invoices():
    ws = sheet.worksheet("Invoices")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

def add_invoice(invoice_data):
    ws = sheet.worksheet("Invoices")
    ws.append_row(list(invoice_data.values()))

