import streamlit as st
import pandas as pd

def get_invoices_df(sheet_data):
    """
    Retrieves the Invoices DataFrame.
    """
    return sheet_data.get("Invoices", pd.DataFrame())

def get_invoice_items_df(sheet_data):
    """
    Retrieves the InvoiceItems DataFrame.
    """
    return sheet_data.get("InvoiceItems", pd.DataFrame())

def display_invoices(invoices_df, mappings):
    """
    Displays the invoices data.
    """
    st.subheader("Invoices List")
    if not invoices_df.empty:
        display_cols = [
            mappings['invoices']['invoice_id'],
            mappings['invoices']['client'],
            mappings['invoices']['amount'],
            mappings['invoices']['due_date'],
            mappings['invoices']['status'],
            mappings['invoices']['type']
        ]
        existing_cols = [col for col in display_cols if col in invoices_df.columns]
        st.dataframe(invoices_df[existing_cols])
    else:
        st.info("No invoice data available.")

def display_invoice_items(invoice_items_df, mappings):
    """
    Displays the invoice items data.
    """
    st.subheader("Invoice Line Items")
    if not invoice_items_df.empty:
        display_cols = [
            mappings['invoice_items']['invoice_id'],
            mappings['invoice_items']['item_name'],
            mappings['invoice_items']['quantity'],
            mappings['invoice_items']['unit_price'],
            mappings['invoice_items']['total_price'],
            mappings['invoice_items']['free_quantity']
        ]
        existing_cols = [col for col in display_cols if col in invoice_items_df.columns]
        st.dataframe(invoice_items_df[existing_cols])
    else:
        st.info("No invoice item data available.")

def add_invoice(gspread_client, spreadsheet_url, new_invoice_data, mappings):
    """
    Adds a new invoice to the Invoices sheet.
    """
    st.subheader("Add New Invoice")
    with st.form("add_invoice_form"):
        invoice_id = st.text_input(f"{mappings['invoices']['invoice_id'].replace('_', ' ').title()}")
        client = st.text_input(f"{mappings['invoices']['client'].replace('_', ' ').title()}")
        amount = st.number_input(f"{mappings['invoices']['amount'].replace('_', ' ').title()}", min_value=0.0, value=0.0)
        due_date = st.date_input(f"{mappings['invoices']['due_date'].replace('_', ' ').title()}")
        status = st.selectbox(f"{mappings['invoices']['status'].replace('_', ' ').title()}", ["Pending", "Paid", "Overdue"])
        invoice_type = st.selectbox(f"{mappings['invoices']['type'].replace('_', ' ').title()}", ["Sale", "Return"])

        submitted = st.form_submit_button("Add Invoice")
        if submitted:
            new_row = {
                mappings['invoices']['invoice_id']: invoice_id,
                mappings['invoices']['client']: client,
                mappings['invoices']['amount']: amount,
                mappings['invoices']['due_date']: due_date.strftime("%Y-%m-%d"),
                mappings['invoices']['status']: status,
                mappings['invoices']['type']: invoice_type
            }
            try:
                spreadsheet = gspread_client.open_by_url(spreadsheet_url)
                invoices_sheet = spreadsheet.worksheet("Invoices")
                
                sheet_headers = invoices_sheet.row_values(1)
                row_to_append = [new_row.get(header, '') for header in sheet_headers]

                invoices_sheet.append_row(row_to_append)
                st.success(f"Invoice '{invoice_id}' added successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error adding invoice: {e}")

def add_invoice_item(gspread_client, spreadsheet_url, new_invoice_item_data, mappings):
    """
    Adds a new invoice item to the InvoiceItems sheet.
    """
    st.subheader("Add New Invoice Item")
    with st.form("add_invoice_item_form"):
        invoice_id = st.text_input(f"{mappings['invoice_items']['invoice_id'].replace('_', ' ').title()}")
        item_name = st.text_input(f"{mappings['invoice_items']['item_name'].replace('_', ' ').title()}")
        quantity = st.number_input(f"{mappings['invoice_items']['quantity'].replace('_', ' ').title()}", min_value=1, value=1)
        unit_price = st.number_input(f"{mappings['invoice_items']['unit_price'].replace('_', ' ').title()}", min_value=0.0, value=0.0)
        free_quantity = st.number_input(f"{mappings['invoice_items']['free_quantity'].replace('_', ' ').title()}", min_value=0, value=0)

        submitted = st.form_submit_button("Add Invoice Item")
        if submitted:
            total_price = quantity * unit_price
            new_row = {
                mappings['invoice_items']['invoice_id']: invoice_id,
                mappings['invoice_items']['item_name']: item_name,
                mappings['invoice_items']['quantity']: quantity,
                mappings['invoice_items']['unit_price']: unit_price,
                mappings['invoice_items']['total_price']: total_price,
                mappings['invoice_items']['free_quantity']: free_quantity
            }
            try:
                spreadsheet = gspread_client.open_by_url(spreadsheet_url)
                invoice_items_sheet = spreadsheet.worksheet("InvoiceItems")

                sheet_headers = invoice_items_sheet.row_values(1)
                row_to_append = [new_row.get(header, '') for header in sheet_headers]

                invoice_items_sheet.append_row(row_to_append)
                st.success(f"Item '{item_name}' added to invoice '{invoice_id}' successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error adding invoice item: {e}")

# Functions for updating/deleting invoices/invoice items would also go here.
