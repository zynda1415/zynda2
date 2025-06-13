import gspread
import pandas as pd
import json
import streamlit as st
from google.oauth2.service_account import Credentials

# 🔐 Google Sheets API Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
client = gspread.authorize(creds)

# 📊 Spreadsheet connection
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
sheet = client.open_by_key(SPREADSHEET_ID)

# 🔄 Loaders
def load_inventory():
    return pd.DataFrame(sheet.worksheet("Inventory").get_all_records())

def load_clients():
    return pd.DataFrame(sheet.worksheet("Clients").get_all_records())

def load_sales():
    return pd.DataFrame(sheet.worksheet("Sales").get_all_records())

def load_invoices():
    return pd.DataFrame(sheet.worksheet("Invoices").get_all_records())

# 📥 Writers
def save_sale(date, item, name, quantity_sold, unit_price, total_price):
    ws = sheet.worksheet("Sales")
    ws.append_row([date, item, name, quantity_sold, unit_price, total_price])

def add_invoice(invoice_data):
    ws = sheet.worksheet("Invoices")
    ws.append_row(list(invoice_data.values()))
