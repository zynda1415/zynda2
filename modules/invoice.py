import streamlit as st
import pandas as pd
from modules.header_mapper import get_headers
from data import load_invoice_data, save_invoice_data

H = get_headers("Invoices")

def render_invoice_section():
    st.title("🧾 Invoice Manager")

    try:
        df = load_invoice_data()
    except Exception as e:
        st.error(f"Failed to load invoice data: {e}")
        return

    st.sidebar.header("🔍 Filter Invoices")
    statuses = ["All"] + sorted(df[H["status"]].dropna().unique())
    selected_status = st.sidebar.selectbox("Status", statuses)

    if selected_status != "All":
        df = df[df[H["status"]] == selected_status]

    st.write(f"### Total Invoices: {len(df)}")
    st.dataframe(df)

    with st.expander("➕ Create New Invoice"):
        with st.form("invoice_form", clear_on_submit=True):
            client = st.text_input("Client Name")
            amount = st.number_input("Amount", min_value=0.0, step=0.1)
            due_date = st.date_input("Due Date")
            status = st.selectbox("Status", ["Pending", "Paid", "Overdue"])

            if st.form_submit_button("✅ Save Invoice"):
                new_invoice = {
                    H["client"]: client,
                    H["amount"]: amount,
                    H["due"]: due_date.strftime("%Y-%m-%d"),
                    H["status"]: status
                }
                df = pd.concat([df, pd.DataFrame([new_invoice])], ignore_index=True)
                save_invoice_data(df)
                st.success("✅ Invoice added successfully!")
