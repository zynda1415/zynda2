import streamlit as st
import pandas as pd
from modules.header_mapper import get_headers
from data import load_clients_data, save_clients_data

H = get_headers("Clients")

def render_client_section():
    st.title("👥 Clients Management")

    try:
        df = load_clients_data()
    except Exception as e:
        st.error(f"Failed to load client data: {e}")
        return

    # Sidebar filters
    st.sidebar.header("🔍 Filter Clients")
    client_types = ["All"] + sorted(df[H["type"]].dropna().unique())
    selected_type = st.sidebar.selectbox("Client Type", client_types)

    if selected_type != "All":
        df = df[df[H["type"]] == selected_type]

    st.write(f"### Total Clients: {len(df)}")
    st.dataframe(df)

    # Add new client form
    with st.expander("➕ Add New Client"):
        with st.form("add_client_form", clear_on_submit=True):
            client_id = st.text_input("Client ID")
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            type_ = st.selectbox("Type", ["Retail", "Wholesale", "Other"])

            if st.form_submit_button("✅ Save Client"):
                new_client = {
                    H["id"]: client_id,
                    H["name"]: name,
                    H["phone"]: phone,
                    H["address"]: address,
                    H["type"]: type_
                }
                df = pd.concat([df, pd.DataFrame([new_client])], ignore_index=True)
                save_clients_data(df)
                st.success("✅ Client added successfully!")
