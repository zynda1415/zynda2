# utils/gsheet.py
import gspread
import json
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1XbtuO9E-cmckDQcqCIPuytpr-RrB-XKLUinXZqWR0Wc"

def get_credentials():
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    return Credentials.from_service_account_info(creds_dict, scopes=scope)

def load_sheet(sheet_name):
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    return pd.DataFrame(sheet.get_all_records())

def write_sheet(sheet_name, df):
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
