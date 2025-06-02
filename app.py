import streamlit as st
import datetime
import pandas as pd
import os

from database.gsheets import load_data, save_inventory, append_sale
from export.pdf_generator import generate_catalog_pdf
from utils.drive_converter import convert_drive_link

# Load data from Google Sheets
sheet, inventory_df, sales_df = load_data()

# Streamlit App UI
st.title("💼 Inventory + POS (Google Sheets) + Catalog + PDF Export")

menu = ["Add Inventory Item", "Point of Sale (POS)", "View Inventory", "Sales History", "Statistics", "View Catalog"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Inventory
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

# POS
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

# View Inventory
elif choice == "View Inventory":
    st.header("Inventory List")
    search_query = st.text_input("Search Inventory")
    df_display = inventory_df
    if search_query:
        df_display = df_display[df_display.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(df_display)

# Sales History
elif choice == "Sales History":
    st.header("Sales History")
    st.dataframe(sales_df)

# Statistics
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

# View Catalog + PDF Export
elif choice == "View Catalog":
    st.header("📖 Product Catalog")

    if inventory_df.empty:
        st.warning("No items in inventory!")
    else:
        cols = st.columns(4)
        for idx, row in inventory_df.iterrows():
            col = cols[idx % 4]
            with col:
                image_url = row['Image URL']
                if image_url:
                    image_url = convert_drive_link(image_url)
                    st.image(image_url, use_container_width=True)
                else:
                    st.write("No Image")
                st.write(f"**{row['Item Name']}**")
                st.write(f"Barcode: {row.get('Barcode', 'N/A')}")
                st.write(f"Price: ${row['Sale Price']}")
                st.write(f"Quantity: {row['Quantity']}")

        st.divider()
        st.subheader("📄 Export This Catalog To PDF")
        if st.button("Generate Catalog PDF"):
            pdf_filename = generate_catalog_pdf(inventory_df)
            with open(pdf_filename, "rb") as f:
                st.download_button("Download Catalog PDF", f, file_name="catalog.pdf", mime="application/pdf")
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
