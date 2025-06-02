import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

# Google Sheets Setup
SHEET_NAME = 'Inventory'  # Name of your Google Sheet tab
SPREADSHEET_ID = '1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M'

# Define inventory columns
COLUMNS = ['Item Name', 'Category', 'Quantity', 'Purchase Price', 'Sale Price', 'Supplier', 'Notes']

# Connect to Google Sheets using Streamlit secrets
def connect_gsheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return sheet

# Load data from Google Sheets
@st.cache_data(ttl=60)
def load_data():
    sheet = connect_gsheets()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(columns=COLUMNS)
    return df

# Save dataframe to Google Sheets
def save_data(df):
    sheet = connect_gsheets()
    sheet.clear()
    sheet.append_row(COLUMNS)
    values = df.astype(str).values.tolist()  # <-- The magic fix
    for row in values:
        sheet.append_row(row)


# Add a new item
def add_item(new_item):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_item])], ignore_index=True)
    save_data(df)

# Edit an existing item
def edit_item(index, updated_item):
    df = load_data()
    df.loc[index] = updated_item
    save_data(df)

# Delete an item
def delete_item(index):
    df = load_data()
    df = df.drop(index).reset_index(drop=True)
    save_data(df)

# Show statistics
def show_statistics():
    df = load_data()
    total_items = len(df)
    total_quantity = df['Quantity'].sum() if not df.empty else 0
    total_value = (df['Quantity'] * df['Sale Price']).sum() if not df.empty else 0

    st.subheader("Inventory Statistics")
    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")

# Main Streamlit app
st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 Inventory Management System")

# Load data
df = load_data()

# Sidebar menu
menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics"])

if menu == "View Inventory":
    st.subheader("Inventory List")
    
    # Filtering options
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['Category'].dropna().unique()))

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]

    st.dataframe(filtered_df, use_container_width=True)

elif menu == "Item":
    # Sub-menu for Item management
    item_action = st.sidebar.radio("Item Actions", ["Add Item", "Edit Item", "Delete Item"])

    if item_action == "Add Item":
        st.subheader("Add New Item")
        
        with st.form("add_form"):
            item_name = st.text_input("Item Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
            sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01)
            supplier = st.text_input("Supplier")
            notes = st.text_area("Notes")
            
            submitted = st.form_submit_button("Add Item")
            
            if submitted:
                new_item = {
                    'Item Name': item_name,
                    'Category': category,
                    'Quantity': quantity,
                    'Purchase Price': purchase_price,
                    'Sale Price': sale_price,
                    'Supplier': supplier,
                    'Notes': notes
                }
                add_item(new_item)
                st.success("Item added successfully!")

    elif item_action == "Edit Item":
        st.subheader("Edit Existing Item")
        
        if df.empty:
            st.warning("No items to edit.")
        else:
            item_to_edit = st.selectbox("Select Item to Edit", df.index, format_func=lambda x: df.loc[x, 'Item Name'])
            selected_row = df.loc[item_to_edit]
            
            with st.form("edit_form"):
                item_name = st.text_input("Item Name", value=selected_row['Item Name'])
                category = st.text_input("Category", value=selected_row['Category'])
                quantity = st.number_input("Quantity", min_value=0, step=1, value=int(selected_row['Quantity']))
                purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01, value=float(selected_row['Purchase Price']))
                sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01, value=float(selected_row['Sale Price']))
                supplier = st.text_input("Supplier", value=selected_row['Supplier'])
                notes = st.text_area("Notes", value=selected_row['Notes'])
                
                submitted = st.form_submit_button("Save Changes")
                
                if submitted:
                    updated_item = {
                        'Item Name': item_name,
                        'Category': category,
                        'Quantity': quantity,
                        'Purchase Price': purchase_price,
                        'Sale Price': sale_price,
                        'Supplier': supplier,
                        'Notes': notes
                    }
                    edit_item(item_to_edit, updated_item)
                    st.success("Item updated successfully!")

    elif item_action == "Delete Item":
        st.subheader("Delete Item")
        
        if df.empty:
            st.warning("No items to delete.")
        else:
            item_to_delete = st.selectbox("Select Item to Delete", df.index, format_func=lambda x: df.loc[x, 'Item Name'])
            if st.button("Delete"):
                delete_item(item_to_delete)
                st.success("Item deleted successfully!")

elif menu == "Statistics":
    show_statistics()
