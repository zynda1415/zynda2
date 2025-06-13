import streamlit as st
import pandas as pd
from config import HEADER_ALIASES
from data import load_invoice_data, save_invoice_data

H = HEADER_ALIASES["Invoices"]

def render_invoice_section():
    st.title("🧾 Invoices")

    df = load_invoice_data()

    if df.empty:
        st.warning("No invoice data found.")
        return

    # === Filters ===
    col1, col2 = st.columns(2)
    with col1:
        client_filter = st.selectbox("Filter by Client", ["All"] + sorted(df[H["client"]].dropna().unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df[H["status"]].dropna().unique()))

    filtered_df = df.copy()

    if client_filter != "All":
        filtered_df = filtered_df[filtered_df[H["client"]] == client_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df[H["status"]] == status_filter]

    st.dataframe(filtered_df)

    with st.expander("➕ Add New Invoice"):
        with st.form("invoice_form", clear_on_submit=True):
            invoice_id = st.text_input("Invoice ID")
            client = st.text_input("Client Name")
            amount = st.number_input("Amount", min_value=0.0, step=1.0)
            due_date = st.date_input("Due Date")
            status = st.selectbox("Status", ["Pending", "Paid", "Overdue"])

            if st.form_submit_button("✅ Save Invoice"):
                new_invoice = {
                    H["invoice_id"]: invoice_id,
                    H["client"]: client,
                    H["amount"]: amount,
                    H["due"]: due_date.strftime("%Y-%m-%d"),
                    H["status"]: status
                }
                df = pd.concat([df, pd.DataFrame([new_invoice])], ignore_index=True)
                save_invoice_data(df)
                st.success("Invoice saved successfully.")
