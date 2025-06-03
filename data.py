import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
import streamlit as st

# Google Sheets Setup
SHEET_NAME = 'Inventory'
SPREADSHEET_ID = '1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M'
COLUMNS = ['Item Name', 'Category', 'Quantity', 'Purchase Price', 'Sale Price', 'Supplier', 'Notes', 'Image URL']

def connect_gsheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return sheet

@st.cache_data(ttl=60)
def load_data():
    sheet = connect_gsheets()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(columns=COLUMNS)
    return df

def save_data(df):
    sheet = connect_gsheets()
    sheet.clear()
    sheet.append_row(COLUMNS)
    values = df.astype(str).values.tolist()
    for row in values:
        sheet.append_row(row)

def add_item(new_item):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_item])], ignore_index=True)
    save_data(df)
