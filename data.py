import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"  # your service account json file
SPREADSHEET_ID = "18Kr780POh7zCa4DUTOMipimg4_f65eKOSueU2DeDpL8"  # your Google Sheet

# Connect to Google Sheets
def connect_gsheets():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    return sheet

# Load Items DataFrame
def load_items():
    sheet = connect_gsheets()
    worksheet = sheet.worksheet('Items')  # exact name of your sheet tab
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df
