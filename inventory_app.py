import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"
SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"

# Connect to Google Sheets
def connect_gsheets():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    return sheet

# Load Inventory and Sales
@st.cache_data(ttl=60)
def load_data():
    sheet = connect_gsheets()
    inventory = pd.DataFrame(sheet.worksheet("Inventory").get_all_records())
    sales = pd.DataFrame(sheet.worksheet("Sales").get_all_records())
    return sheet, inventory, sales

# Save Inventory
def save_inventory(df):
    sheet = connect_gsheets()
    worksheet = sheet.worksheet("Inventory")
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# Append Sale
def append_sale(sale_record):
    sheet = connect_gsheets()
    worksheet = sheet.worksheet("Sales")
    worksheet.append_row(sale_record)

# Streamlit App
st.title("💼 Inventory + POS (Google Sheets) + Catalog")
menu = ["Add Inventory Item", "Point of Sale (POS)", "View Inventory", "Sales History", "Statistics", "View Catalog"]
choice = st.sidebar.selectbox("Menu", menu)

sheet, inventory_df, sales_df = load_data()

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
        image_url = st.text_input("Image URL (optional)")
        submit = st.form_submit_button("Add Item")
        
        if submit:
            new_row = pd.DataFrame([{
                "Item Name": item_name,
                "Category": category,
                "Quantity": quantity,
                "Purchase Price": purchase_price,
                "Sale Price": sale_price,
                "Supplier": supplier,
                "Notes": notes,
                "Image URL": image_url
            }])
            inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
            save_inventory(inventory_df)
            st.success("Item added successfully!")

elif choice == "Point of Sale (POS)":
    st.header("Point of Sale")
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
            idx = inventory_df[inventory_df['Item Name'] == item_selected].index[0]
            inventory_df.at[idx, 'Quantity'] -= quantity_sold
            save_inventory(inventory_df)
            
            sale_record = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                item_selected,
                quantity_sold,
                selected_item['Sale Price'],
                total_price
            ]
            append_sale(sale_record)
            
            st.success("Sale recorded and inventory updated!")

elif choice == "View Inventory":
    st.header("Inventory List")
    search_query = st.text_input("Search Inventory")
    df_display = inventory_df
    if search_query:
        df_display = df_display[df_display.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(df_display)

elif choice == "Sales History":
    st.header("Sales History")
    st.dataframe(sales_df)

elif choice == "Statistics":
    st.header("Statistics Summary")
    
    inventory_df["Quantity"] = inventory_df["Quantity"].astype(float)
    inventory_df["Purchase Price"] = inventory_df["Purchase Price"].astype(float)
    inventory_df["Sale Price"] = inventory_df["Sale Price"].astype(float)
    
    total_inventory_items = inventory_df.shape[0]
    total_stock_quantity = inventory_df['Quantity'].sum()
    total_stock_value = (inventory_df['Quantity'] * inventory_df['Purchase Price']).sum()
    potential_sales_value = (inventory_df['Quantity'] * inventory_df['Sale Price']).sum()
    total_sales_value = sales_df['Total Price'].astype(float).sum()

    st.subheader("Inventory Stats")
    st.metric("Total Inventory Items", total_inventory_items)
    st.metric("Total Stock Quantity", total_stock_quantity)
    st.metric("Total Stock Purchase Value", f"${total_stock_value:,.2f}")
    st.metric("Potential Sales Value", f"${potential_sales_value:,.2f}")

    st.subheader("Sales Stats")
    st.metric("Total Sales Revenue", f"${total_sales_value:,.2f}")

elif choice == "View Catalog":
    st.header("📖 Product Catalog")
    
    if inventory_df.empty:
        st.warning("No items in inventory!")
    else:
        cols = st.columns(4)
        for idx, row in inventory_df.iterrows():
            col = cols[idx % 4]
            with col:
                if row['Image URL']:
                    st.image(row['Image URL'], use_container_width=True)
                else:
                    st.write("No Image")
                st.write(f"**{row['Item Name']}**")
                st.write(f"Barcode: {row.get('Barcode', 'N/A')}")
                st.write(f"Price: ${row['Sale Price']}")
                st.write(f"Quantity: {row['Quantity']}")
