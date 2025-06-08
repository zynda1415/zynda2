import streamlit as st
import data
import pandas as pd

def clients_module():
    st.header("👥 Clients Management")

    menu = st.radio("Select Action", ["View Clients", "Add Client", "Edit Client", "Delete Client"])

    df = data.load_clients()

    if menu == "View Clients":
        st.subheader("📋 All Clients")
        st.dataframe(df)

    elif menu == "Add Client":
        st.subheader("➕ Add New Client")
        id = st.text_input("Client ID")
        name = st.text_input("Client Name")
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        owner = st.text_input("Owner Name")
        type_ = st.text_input("Type")
        role = st.text_input("Role")
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")

        if st.button("Add Client"):
            ws = data.sheet.worksheet("Clients")
            ws.append_row([id, name, phone, address, owner, type_, role, lat, lon])
            st.success("✅ Client added successfully!")

    elif menu == "Edit Client":
        st.subheader("✏️ Edit Client")
        client_names = df['Client name'].tolist()
        selected_client = st.selectbox("Select Client to Edit", client_names)

        client_row = df[df['Client name'] == selected_client].iloc[0]

        id = st.text_input("Client ID", client_row['ID'])
        name = st.text_input("Client Name", client_row['Client name'])
        phone = st.text_input("Phone", client_row['Phone'])
        address = st.text_input("Address", client_row['Address'])
        owner = st.text_input("Owner Name", client_row['Owner'])
        type_ = st.text_input("Type", client_row['Type'])
        role = st.text_input("Role", client_row['Role'])
        lat = st.number_input("Latitude", format="%.6f", value=float(client_row['Latitude']))
        lon = st.number_input("Longitude", format="%.6f", value=float(client_row['Longitude']))

        if st.button("Update Client"):
            ws = data.sheet.worksheet("Clients")
            row_idx = df[df['Client name'] == selected_client].index[0] + 2  # +2 because sheet rows start at 1 plus header
            ws.update(f"A{row_idx}:I{row_idx}", [[id, name, phone, address, owner, type_, role, lat, lon]])
            st.success("✅ Client updated successfully!")

    elif menu == "Delete Client":
        st.subheader("🗑️ Delete Client")
        client_names = df['Client name'].tolist()
        selected_client = st.selectbox("Select Client to Delete", client_names)

        if st.button("Delete Client"):
            ws = data.sheet.worksheet("Clients")
            row_idx = df[df['Client name'] == selected_client].index[0] + 2
            ws.delete_rows(row_idx)
            st.success("✅ Client deleted successfully!")
