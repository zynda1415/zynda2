import streamlit as st
import pandas as pd
import data

def render_invoice_section():
    st.title("🧾 Invoices")

    invoices_df = data.load_invoices()
    st.write("### All Invoices")
    st.dataframe(invoices_df)

    with st.expander("➕ Add New Invoice"):
        add_invoice_form()

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
