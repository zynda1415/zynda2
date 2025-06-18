import streamlit as st
import pandas as pd

def get_purchase_history_df(sheet_data):
    """
    Retrieves the PurchaseHistory DataFrame.
    """
    return sheet_data.get("PurchaseHistory", pd.DataFrame())

def display_purchase_history_data(purchase_history_df, mappings):
    """
    Displays the purchase history data.
    """
    st.subheader("Purchase History Log")
    if not purchase_history_df.empty:
        display_cols = [
            mappings['purchase_history']['item_name'],
            mappings['purchase_history']['last_buy_price'],
            mappings['purchase_history']['last_sell_price'],
            mappings['purchase_history']['last_wholesale_price'],
            mappings['purchase_history']['last_transaction_date']
        ]
        existing_cols = [col for col in display_cols if col in purchase_history_df.columns]
        st.dataframe(purchase_history_df[existing_cols])
    else:
        st.info("No purchase history data available.")

# You would add functions here to update purchase history based on sales or purchases.
# For instance, a function that takes an item, price, and type (buy/sell/wholesale)
# and updates the last known price and date for that item in the sheet.
def update_purchase_history(gspread_client, spreadsheet_url, item_name, price_type, price, transaction_date, mappings):
    """
    Updates the purchase history for a specific item.
    This is a conceptual function; actual implementation would involve finding the row
    for the item and updating specific cells.
    """
    st.info(f"Conceptual: Updating purchase history for {item_name} with {price_type} price {price} on {transaction_date}")
    # Full implementation would:
    # 1. Open the 'PurchaseHistory' worksheet.
    # 2. Find the row for the given item_name (using the mapped 'item_name' column).
    # 3. Update the cell corresponding to price_type (e.g., 'last_buy_price') and 'last_transaction_date'.
    try:
        spreadsheet = gspread_client.open_by_url(spreadsheet_url)
        history_sheet = spreadsheet.worksheet("PurchaseHistory")

        item_name_col_header = mappings['purchase_history']['item_name']
        # Find item row by item name
        # This is simplified. In a real app, you might use get_all_records() and then find the row index.
        # Or you might iterate through rows directly if the sheet is small.
        # Example (simplified, for actual use consider efficiency):
        all_records = history_sheet.get_all_records()
        df = pd.DataFrame(all_records)
        
        if item_name_col_header in df.columns:
            target_row_index = df[df[item_name_col_header] == item_name].index
            if not target_row_index.empty:
                row_num = target_row_index[0] + 2 # +2 because pandas index is 0-based and sheets are 1-based, plus header row
                
                # Get the actual column header for the price type
                actual_price_col = mappings['purchase_history'][price_type] # e.g., 'last_buy_price' maps to 'Last Buy Price'
                actual_date_col = mappings['purchase_history']['last_transaction_date']

                # Find the column index for the price type and date
                headers = history_sheet.row_values(1)
                try:
                    price_col_idx = headers.index(actual_price_col) + 1 # +1 for gspread col indexing
                    date_col_idx = headers.index(actual_date_col) + 1
                    
                    history_sheet.update_cell(row_num, price_col_idx, price)
                    history_sheet.update_cell(row_num, date_col_idx, transaction_date.strftime("%Y-%m-%d"))
                    st.success(f"Purchase history updated for '{item_name}'.")
                    st.experimental_rerun()
                except ValueError:
                    st.error(f"Error: Could not find column '{actual_price_col}' or '{actual_date_col}' in PurchaseHistory sheet.")
            else:
                st.warning(f"Item '{item_name}' not found in purchase history. Consider adding it first.")
        else:
            st.error(f"Error: Mapped item name column '{item_name_col_header}' not found in PurchaseHistory sheet.")
    except Exception as e:
        st.error(f"Error updating purchase history: {e}")
