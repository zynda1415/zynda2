import pandas as pd
import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tempfile
import os

# Google Sheets Setup
SHEET_NAME = 'Inventory'
SPREADSHEET_ID = '1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M'
COLUMNS = ['Item Name', 'Category', 'Quantity', 'Purchase Price', 'Sale Price', 'Supplier', 'Notes', 'Image URL']

# Your Google Drive folder ID:
DRIVE_FOLDER_ID = '18kaAXbaCaP3JLfK1QwNx_g885995QR7P'

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

def edit_item(index, updated_item):
    df = load_data()
    df.loc[index] = updated_item
    save_data(df)

def delete_item(index):
    df = load_data()
    df = df.drop(index).reset_index(drop=True)
    save_data(df)

# Bulletproof Google Drive upload (no ServiceAccountAuth anymore)
def upload_image_to_drive(file):
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    
    # Save credentials json file temporarily (required for pydrive2 legacy interface)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_json:
        json.dump(creds_dict, tmp_json)
        tmp_json_path = tmp_json.name

    # Authenticate pydrive2
    gauth = GoogleAuth()
    gauth.LoadServiceConfigFile(tmp_json_path)
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    # Save uploaded file to temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name

    file_drive = drive.CreateFile({'title': file.name, 'parents': [{'id': DRIVE_FOLDER_ID}]})
    file_drive.SetContentFile(tmp_file_path)
    file_drive.Upload()

    os.remove(tmp_file_path)
    os.remove(tmp_json_path)

    # Public URL
    file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    file_url = f"https://drive.google.com/uc?id={file_drive['id']}"
    return file_url
