import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

SHEET_NAME = 'Clients'
SPREADSHEET_ID = '1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M'

def load_clients_data():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "")
    return df

def render_map():
    st.subheader("📍 Client Map View")
    df = load_clients_data()

    if 'latitude' in df.columns and 'longitude' in df.columns:
        map_data = df[['latitude', 'longitude']]
        map_data['latitude'] = pd.to_numeric(map_data['latitude'], errors='coerce')
        map_data['longitude'] = pd.to_numeric(map_data['longitude'], errors='coerce')
        map_data = map_data.dropna()

        if not map_data.empty:
            st.map(map_data)
        else:
            st.warning("Latitude/Longitude columns exist but no valid coordinates found.")
    else:
        st.warning("No Latitude/Longitude columns found in your Clients sheet.")
