import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import json
import streamlit as st

# Load credentials from Streamlit secrets
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
client = gspread.authorize(creds)
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
sheet = client.open_by_key(SPREADSHEET_ID)

# Load inventory
def load_inventory():
    ws = sheet.worksheet("Inventory")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# Load clients
def load_clients():
    ws = sheet.worksheet("Clients")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# Load sales
def load_sales():
    ws = sheet.worksheet("Sales")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    return df

# Save new sales record
def save_sale(date, item, name, quantity_sold, unit_price, total_price):
    ws = sheet.worksheet("Sales")
    ws.append_row([date, item, name, quantity_sold, unit_price, total_price])
