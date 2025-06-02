import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"

# Connect to Google Sheets
def connect_gsheets():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    return sheet

# Load Inventory and Sales
@st.cache_data(ttl=60)
def load_data():
    sheet = connect_gsheets()
    inventory = pd.DataFrame(sheet.worksheet("Inventory").get_all_records())
    sales = pd.DataFrame(sheet.worksheet("Sales").get_all_records())
    return sheet, inventory, sales

# Save Inventory
def save_inventory(df):
    sheet = connect_gsheets()
    worksheet = sheet.worksheet("Inventory")
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# Append Sale
def append_sale(sale_record):
    sheet = connect_gsheets()
    worksheet = sheet.worksheet("Sales")
    worksheet.append_row(sale_record)
