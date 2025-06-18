import streamlit as st
import pandas as pd

def get_returns_df(sheet_data):
    """
    Retrieves the Returns DataFrame.
    """
    return sheet_data.get("Returns", pd.DataFrame())

def display_returns_data(returns_df, mappings):
    """
    Displays the returns data.
    """
    st.subheader("Returns Log")
    if not returns_df.empty:
        display_cols = [
            mappings['returns']['return_id'],
            mappings['returns']['invoice_id'],
            mappings['returns']['item_name'],
            mappings['returns']['quantity'],
            mappings['returns']['return_date'],
            mappings['returns']['reason']
        ]
        existing_cols = [col for col in display_cols if col in returns_df.columns]
        st.dataframe(returns_df[existing_cols])
    else:
        st.info("No returns data available.")

def log_return(gspread_client, spreadsheet_url, new_return_data, mappings):
    """
    Logs a new return to the Returns sheet.
    """
    st.subheader("Log New Return")
    with st.form("log_return_form"):
        return_id = st.text_input(f"{mappings['returns']['return_id'].replace('_', ' ').title()}")
        invoice_id = st.text_input(f"{mappings['returns']['invoice_id'].replace('_', ' ').title()}")
        item_name = st.text_input(f"{mappings['returns']['item_name'].replace('_', ' ').title()}")
        quantity = st.number_input(f"{mappings['returns']['quantity'].replace('_', ' ').title()}", min_value=1, value=1)
        return_date = st.date_input(f"{mappings['returns']['return_date'].replace('_', ' ').title()}")
        reason = st.text_area(f"{mappings['returns']['reason'].replace('_', ' ').title()}")

        submitted = st.form_submit_button("Log Return")
        if submitted:
            new_row = {
                mappings['returns']['return_id']: return_id,
                mappings['returns']['invoice_id']: invoice_id,
                mappings['returns']['item_name']: item_name,
                mappings['returns']['quantity']: quantity,
                mappings['returns']['return_date']: return_date.strftime("%Y-%m-%d"),
                mappings['returns']['reason']: reason
            }
            try:
                spreadsheet = gspread_client.open_by_url(spreadsheet_url)
                returns_sheet = spreadsheet.worksheet("Returns")

                sheet_headers = returns_sheet.row_values(1)
                row_to_append = [new_row.get(header, '') for header in sheet_headers]

                returns_sheet.append_row(row_to_append)
                st.success(f"Return '{return_id}' logged successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error logging return: {e}")

# Functions for updating/deleting returns would go here.
