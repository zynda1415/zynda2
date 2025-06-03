### app.py

import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
import item

# Google Sheets Setup
SHEET_NAME = 'Inventory'
SPREADSHEET_ID = '1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M'
COLUMNS = ['Item Name', 'Category', 'Quantity', 'Purchase Price', 'Sale Price', 'Supplier', 'Notes', 'Image URL']

# Connect to Google Sheets using Streamlit secrets
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

def show_statistics():
    df = load_data()
    total_items = len(df)
    total_quantity = df['Quantity'].sum() if not df.empty else 0
    total_value = (df['Quantity'] * df['Sale Price']).sum() if not df.empty else 0

    st.subheader("Inventory Statistics")
    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")

st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 Inventory Management System")

df = load_data()
menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics"])

if menu == "View Inventory":
    st.subheader("Inventory List")
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['Category'].dropna().unique()))
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    st.dataframe(filtered_df, use_container_width=True)

elif menu == "Item":
    item.render_item_section(df, add_item, edit_item, delete_item)

elif menu == "Statistics":
    show_statistics()
