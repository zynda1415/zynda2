# ---------- app.py ----------
import streamlit as st
import pandas as pd
from datetime import datetime
from data import load_inventory, load_clients, load_sales, save_sales, save_inventory, save_clients
from item import item_management

st.set_page_config(page_title="ZYNDA SYSTEM v1.8", layout="wide")
menu = st.sidebar.radio("Menu", [
    "View Inventory", "Item", "Statistics", "Catalog View", "Map", "Sales", "Clients"])

# View Inventory
if menu == "View Inventory":
    st.header("Inventory Table View")
    df = load_inventory()
    st.dataframe(df)

# Item Management
elif menu == "Item":
    item_management()  # Call the function from item.py

# Statistics
elif menu == "Statistics":
    st.header("Inventory Statistics")
    df = load_inventory()
    total_items = len(df)
    total_quantity = df['Quantity'].sum()
    total_value = (df['Quantity'] * df['Sale Price']).sum()
    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")

# Catalog View
elif menu == "Catalog View":
    st.header("Catalog View")
    df = load_inventory()
    search = st.text_input("Search Item")
    category_filter = st.selectbox("Category", ["All"] + list(df['Category'].unique()))
    columns = st.slider("Columns per row", 1, 5, 3)
    filtered_df = df[df['Item Name'].str.contains(search, case=False)] if search else df
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    for i in range(0, len(filtered_df), columns):
        cols = st.columns(columns)
        for col, row in zip(cols, filtered_df.iloc[i:i+columns].itertuples()):
            with col:
                st.image(row.Image_URL, width=150)
                st.write(row.Item_Name)
                st.write(f"Category: {row.Category}")
                st.write(f"Price: ${row.Sale_Price}")
                st.write(f"Quantity: {row.Quantity}")

# Client Map
elif menu == "Map":
    st.header("Client Map View")
    df = load_clients()
    if not df.empty:
        st.map(df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}))
    else:
        st.warning("No clients found.")

# Sales
elif menu == "Sales":
    st.header("Sales Management")
    inventory_df = load_inventory()
    sales_df = load_sales()

    with st.form("sales_form"):
        item = st.selectbox("Item", options=inventory_df['Item Name'])
        qty = st.number_input("Quantity Sold", 1)
        unit_price = st.number_input("Unit Price", 0.0)
        date = st.date_input("Date", value=datetime.now())
        submitted = st.form_submit_button("Add Sale")

        if submitted:
            total_price = qty * unit_price
            new_sale = pd.DataFrame([[date.strftime("%Y-%m-%d"), item, qty, unit_price, total_price]],
                                     columns=sales_df.columns)
            sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
            save_sales(sales_df)
            st.success("Sale recorded!")
            inventory_df.loc[inventory_df['Item Name'] == item, 'Quantity'] -= qty
            save_inventory(inventory_df)

# Clients
elif menu == "Clients":
    st.header("Clients Management")
    df = load_clients()
    with st.form("client_form"):
        client_id = st.number_input("Client ID", 0)
        name = st.text_input("Client Name")
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        lat = st.number_input("Latitude", 0.0)
        lon = st.number_input("Longitude", 0.0)
        submitted = st.form_submit_button("Add Client")
        if submitted:
            new_row = pd.DataFrame([[client_id, name, phone, address, lat, lon]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_clients(df)
            st.success("Client Added Successfully!")
