import pandas as pd
import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials

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

# FAST APPEND (faster adds)
def add_item(new_item):
    sheet = connect_gsheets()
    values = [new_item.get(col, "") for col in COLUMNS]
    sheet.append_row(values)

# Full rewrite for edit/delete
def save_data(df):
    sheet = connect_gsheets()
    sheet.clear()
    sheet.append_row(COLUMNS)
    values = df.astype(str).values.tolist()
    for row in values:
        sheet.append_row(row)

def edit_item(index, updated_item):
    df = load_data()
    df.loc[index] = updated_item
    save_data(df)

def delete_item(index):
    df = load_data()
    df = df.drop(index).reset_index(drop=True)
    save_data(df)
