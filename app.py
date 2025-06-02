import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Upload your service account file
SPREADSHEET_ID = 'your-google-sheet-id-here'

# Authenticate with Google Sheets
def connect_gsheet():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)
    return sh

# Load sheets
def load_inventory():
    sheet = connect_gsheet().worksheet('Inventory')
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def load_sales():
    sheet = connect_gsheet().worksheet('Sales')
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_inventory(df):
    sheet = connect_gsheet().worksheet('Inventory')
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

def save_sales(df):
    sheet = connect_gsheet().worksheet('Sales')
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Add inventory item
def add_inventory_item(item):
    df = load_inventory()
    df = pd.concat([df, pd.DataFrame([item])], ignore_index=True)
    save_inventory(df)

# Record sale transaction
def record_sale(sales):
    df = load_sales()
    df = pd.concat([df, pd.DataFrame(sales)], ignore_index=True)
    save_sales(df)

# Update inventory after sale
def update_inventory_after_sale(item_name, quantity_sold):
    df = load_inventory()
    index = df[df['Item Name'] == item_name].index[0]
    df.at[index, 'Quantity'] = int(df.at[index, 'Quantity']) - quantity_sold
    save_inventory(df)

# Streamlit App
st.title("💼 Inventory + POS Management System (Google Sheets)")
menu = ["Add Inventory Item", "Point of Sale (POS)", "View Inventory", "Sales History", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Inventory Item":
    st.header("Add New Inventory Item")
    with st.form("Add Form"):
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
        sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01)
        supplier = st.text_input("Supplier")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Item")
        
        if submit:
            item = {
                "Item Name": item_name,
                "Category": category,
                "Quantity": quantity,
                "Purchase Price": purchase_price,
                "Sale Price": sale_price,
                "Supplier": supplier,
                "Notes": notes
            }
            add_inventory_item(item)
            st.success("Item added successfully!")

elif choice == "Point of Sale (POS)":
    st.header("Point of Sale")
    inventory_df = load_inventory()
    
    if inventory_df.empty:
        st.warning("No items in inventory!")
    else:
        item_selected = st.selectbox("Select Item", inventory_df['Item Name'].tolist())
        selected_item = inventory_df[inventory_df['Item Name'] == item_selected].iloc[0]
        available_stock = int(selected_item['Quantity'])
        
        quantity_sold = st.number_input("Quantity to sell", min_value=1, max_value=available_stock, step=1)
        total_price = quantity_sold * float(selected_item['Sale Price'])
        st.write(f"Total Price: ${total_price:.2f}")
        
        if st.button("Confirm Sale"):
            sale_record = [{
                "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Item Name": item_selected,
                "Quantity Sold": quantity_sold,
                "Unit Price": selected_item['Sale Price'],
                "Total Price": total_price
            }]
            record_sale(sale_record)
            update_inventory_after_sale(item_selected, quantity_sold)
            st.success("Sale recorded and inventory updated!")

elif choice == "View Inventory":
    st.header("Inventory List")
    inventory_df = load_inventory()
    search_query = st.text_input("Search Inventory")
    if search_query:
        inventory_df = inventory_df[inventory_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(inventory_df)

elif choice == "Sales History":
    st.header("Sales History")
    sales_df = load_sales()
    st.dataframe(sales_df)

elif choice == "Statistics":
    st.header("Statistics Summary")
    inventory_df = load_inventory()
    sales_df = load_sales()

    total_inventory_items = inventory_df.shape[0]
    total_stock_quantity = inventory_df['Quantity'].astype(int).sum()
    total_stock_value = (inventory_df['Quantity'].astype(float) * inventory_df['Purchase Price'].astype(float)).sum()
    potential_sales_value = (inventory_df['Quantity'].astype(float) * inventory_df['Sale Price'].astype(float)).sum()
    total_sales_value = sales_df['Total Price'].astype(float).sum()

    st.subheader("Inventory Stats")
    st.metric("Total Inventory Items", total_inventory_items)
    st.metric("Total Stock Quantity", total_stock_quantity)
    st.metric("Total Stock Purchase Value", f"${total_stock_value:,.2f}")
    st.metric("Potential Sales Value", f"${potential_sales_value:,.2f}")

    st.subheader("Sales Stats")
    st.metric("Total Sales Revenue", f"${total_sales_value:,.2f}")
