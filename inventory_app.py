import streamlit as st
import pandas as pd
import os
import datetime

# File paths
INVENTORY_FILE = 'inventory.csv'
SALES_FILE = 'sales.csv'

# Initialize files if they don't exist
def init_files():
    if not os.path.exists(INVENTORY_FILE):
        inventory_df = pd.DataFrame(columns=["Item Name", "Category", "Quantity", "Purchase Price", "Sale Price", "Supplier", "Notes"])
        inventory_df.to_csv(INVENTORY_FILE, index=False)
    if not os.path.exists(SALES_FILE):
        sales_df = pd.DataFrame(columns=["Date", "Item Name", "Quantity Sold", "Unit Price", "Total Price"])
        sales_df.to_csv(SALES_FILE, index=False)

# Load data functions
def load_inventory():
    return pd.read_csv(INVENTORY_FILE)

def load_sales():
    return pd.read_csv(SALES_FILE)

# Save data functions
def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def save_sales(df):
    df.to_csv(SALES_FILE, index=False)

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
    df.at[index, 'Quantity'] -= quantity_sold
    save_inventory(df)

# Initialize data files
init_files()

# Streamlit App
st.title("💼 Inventory + POS Management System")
menu = ["Add Inventory Item", "Point of Sale (POS)", "View Inventory", "Sales History", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

# 1. Add Inventory
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

# 2. POS
elif choice == "Point of Sale (POS)":
    st.header("Point of Sale")
    inventory_df = load_inventory()
    
    if inventory_df.empty:
        st.warning("No items in inventory!")
    else:
        cart = []
        item_selected = st.selectbox("Select Item", inventory_df['Item Name'].tolist())
        selected_item = inventory_df[inventory_df['Item Name'] == item_selected].iloc[0]
        available_stock = selected_item['Quantity']
        
        quantity_sold = st.number_input("Quantity to sell", min_value=1, max_value=int(available_stock), step=1)
        total_price = quantity_sold * selected_item['Sale Price']
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

# 3. View Inventory
elif choice == "View Inventory":
    st.header("Inventory List")
    inventory_df = load_inventory()
    search_query = st.text_input("Search Inventory")
    if search_query:
        inventory_df = inventory_df[inventory_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(inventory_df)

# 4. Sales History
elif choice == "Sales History":
    st.header("Sales History")
    sales_df = load_sales()
    st.dataframe(sales_df)

# 5. Statistics
elif choice == "Statistics":
    st.header("Statistics Summary")
    inventory_df = load_inventory()
    sales_df = load_sales()

    total_inventory_items = inventory_df.shape[0]
    total_stock_quantity = inventory_df['Quantity'].sum()
    total_stock_value = (inventory_df['Quantity'] * inventory_df['Purchase Price']).sum()
    potential_sales_value = (inventory_df['Quantity'] * inventory_df['Sale Price']).sum()
    total_sales_value = sales_df['Total Price'].sum()

    st.subheader("Inventory Stats")
    st.metric("Total Inventory Items", total_inventory_items)
    st.metric("Total Stock Quantity", total_stock_quantity)
    st.metric("Total Stock Purchase Value", f"${total_stock_value:,.2f}")
    st.metric("Potential Sales Value", f"${potential_sales_value:,.2f}")

    st.subheader("Sales Stats")
    st.metric("Total Sales Revenue", f"${total_sales_value:,.2f}")
