import streamlit as st
import pandas as pd

def get_inventory_df(sheet_data):
    """
    Retrieves the inventory DataFrame.
    """
    return sheet_data.get("Inventory", pd.DataFrame())

def display_inventory_data(inventory_df, mappings):
    """
    Displays the inventory data using Streamlit.
    """
    st.subheader("Inventory List")
    if not inventory_df.empty:
        # Displaying a subset of columns or mapping them for better readability
        display_cols = [
            mappings['inventory']['item_name'],
            mappings['inventory']['barcode'],
            mappings['inventory']['category'],
            mappings['inventory']['quantity'],
            mappings['inventory']['sell_price'],
            mappings['inventory']['free_quantity']
        ]
        # Filter dataframe to only show columns that actually exist
        existing_cols = [col for col in display_cols if col in inventory_df.columns]
        st.dataframe(inventory_df[existing_cols])
    else:
        st.info("No inventory data available.")

def add_inventory_item(gspread_client, spreadsheet_url, new_item_data, mappings):
    """
    Adds a new item to the Inventory sheet.
    new_item_data is a dictionary with logical keys and their values.
    """
    st.subheader("Add New Item")
    with st.form("add_item_form"):
        # Create input fields using logical keys but display them nicely
        item_name = st.text_input(f"{mappings['inventory']['item_name'].replace('_', ' ').title()}")
        barcode = st.text_input(f"{mappings['inventory']['barcode'].replace('_', ' ').title()}")
        category = st.text_input(f"{mappings['inventory']['category'].replace('_', ' ').title()}")
        quantity = st.number_input(f"{mappings['inventory']['quantity'].replace('_', ' ').title()}", min_value=0, value=0)
        sell_price = st.number_input(f"{mappings['inventory']['sell_price'].replace('_', ' ').title()}", min_value=0.0, value=0.0)
        wholesale_price = st.number_input(f"{mappings['inventory']['wholesale_price'].replace('_', ' ').title()}", min_value=0.0, value=0.0)
        last_purchase_price = st.number_input(f"{mappings['inventory']['last_purchase_price'].replace('_', ' ').title()}", min_value=0.0, value=0.0)
        last_purchase_date = st.date_input(f"{mappings['inventory']['last_purchase_date'].replace('_', ' ').title()}")
        expiry_date = st.date_input(f"{mappings['inventory']['expiry_date'].replace('_', ' ').title()}")
        supplier = st.text_input(f"{mappings['inventory']['supplier'].replace('_', ' ').title()}")
        image_url = st.text_input(f"{mappings['inventory']['image_url'].replace('_', ' ').title()}")
        notes = st.text_area(f"{mappings['inventory']['notes'].replace('_', ' ').title()}")
        free_quantity = st.number_input(f"{mappings['inventory']['free_quantity'].replace('_', ' ').title()}", min_value=0, value=0)

        submitted = st.form_submit_button("Add Item")
        if submitted:
            # Map logical keys to actual column headers for the row to append
            new_row = {
                mappings['inventory']['item_name']: item_name,
                mappings['inventory']['barcode']: barcode,
                mappings['inventory']['category']: category,
                mappings['inventory']['quantity']: quantity,
                mappings['inventory']['sell_price']: sell_price,
                mappings['inventory']['wholesale_price']: wholesale_price,
                mappings['inventory']['last_purchase_price']: last_purchase_price,
                mappings['inventory']['last_purchase_date']: last_purchase_date.strftime("%Y-%m-%d"),
                mappings['inventory']['expiry_date']: expiry_date.strftime("%Y-%m-%d"),
                mappings['inventory']['supplier']: supplier,
                mappings['inventory']['image_url']: image_url,
                mappings['inventory']['notes']: notes,
                mappings['inventory']['free_quantity']: free_quantity
            }
            try:
                spreadsheet = gspread_client.open_by_url(spreadsheet_url)
                inventory_sheet = spreadsheet.worksheet("Inventory") # Assuming "Inventory" is the sheet name
                
                # Append row - ensure the order of values matches the sheet's column order
                # This requires getting all headers from the sheet first to match the order
                sheet_headers = inventory_sheet.row_values(1) # Get first row (headers)
                row_to_append = [new_row.get(header, '') for header in sheet_headers] # Create list in sheet order

                inventory_sheet.append_row(row_to_append)
                st.success(f"Item '{item_name}' added successfully!")
                st.experimental_rerun() # Rerun to refresh data
            except Exception as e:
                st.error(f"Error adding item: {e}")

# You would add functions for update_inventory_item and delete_inventory_item similarly
# They would need to fetch the row, modify it, and then use update_cells or delete_rows methods of gspread.Worksheet
