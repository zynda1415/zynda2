import streamlit as st
import pandas as pd
import data

# =====================
# Invoice Main Module
# =====================

def render_invoice_section():
    st.title("🧾 Invoices")

    # Load invoices
    invoices_df = data.load_invoices()

    # Show invoices table
    st.write("### All Invoices")
    st.dataframe(invoices_df)

    # Add new invoice
    with st.expander("➕ Add New Invoice"):
        add_invoice_form()


# =====================
# Add Invoice Form
# =====================

def add_invoice_form():
    with st.form("add_invoice_form"):
        date = st.date_input("Date")
        client = st.text_input("Client Name")
        amount = st.number_input("Amount", min_value=0.0)
        due_date = st.date_input("Due Date")
        status = st.selectbox("Status", ["Paid", "Unpaid", "Overdue"])

        submit = st.form_submit_button("Save Invoice")

        if submit:
            invoice_data = {
                'Date': str(date),
                'Client Name': client,
                'Amount': amount,
                'Due Date': str(due_date),
                'Status': status
            }

            data.add_invoice(invoice_data)
            st.success("Invoice added successfully!")


# =====================
# Data Layer Functions
# =====================

# You will add these to your existing data.py:

# def load_invoices():
#     ws = sheet.worksheet("Invoices")
#     data = ws.get_all_records()
#     df = pd.DataFrame(data)
#     return df

# def add_invoice(invoice_data):
#     ws = sheet.worksheet("Invoices")
#     ws.append_row(list(invoice_data.values()))
