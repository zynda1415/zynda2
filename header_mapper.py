# header_mapper.py
import gspread
import json
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
SHEET_NAME = "SheetConfig"

def get_credentials():
    with open("zyndasys1-2.json") as f:
        creds_dict = json.load(f)
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    return Credentials.from_service_account_info(creds_dict, scopes=scope)

def load_header_map():
    creds = get_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = pd.DataFrame(sheet.get_all_records())
    mapping = dict(zip(data["Key"], data["Column"]))
    return mapping
