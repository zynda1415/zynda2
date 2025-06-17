import streamlit as st
import pandas as pd
import altair as alt
from modules.header_mapper import get_headers
from data import load_invoice_data

H = get_headers("Invoices")

def statistics_view():
    st.title("📊 Invoice Statistics")

    try:
        df = load_invoice_data()
    except Exception as e:
        st.error(f"Failed to load invoice data: {e}")
        return

    if df.empty:
        st.info("No invoice data available.")
        return

    df[H["amount"]] = pd.to_numeric(df[H["amount"]], errors="coerce")
    df[H["status"]] = df[H["status"]].fillna("Unknown")

    total = df[H["amount"]].sum()
    count = df.shape[0]
    paid = df[df[H["status"]] == "Paid"][H["amount"]].sum()
    pending = df[df[H["status"]] == "Pending"][H["amount"]].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invoices", count)
    col2.metric("Total Collected", f"${paid:,.2f}")
    col3.metric("Pending Amount", f"${pending:,.2f}")

    st.subheader("📊 Amount by Status")
    chart_data = df.groupby(H["status"])[H["amount"]].sum().reset_index()
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X(H["status"], title="Status"),
        y=alt.Y(H["amount"], title="Total Amount"),
        tooltip=[H["status"], H["amount"]]
    )
    st.altair_chart(chart, use_container_width=True)
