import streamlit as st
import pandas as pd

def get_clients_df(sheet_data):
    """
    Retrieves the Clients DataFrame.
    """
    return sheet_data.get("Clients", pd.DataFrame())

def display_clients_data(clients_df, mappings):
    """
    Displays the clients data.
    """
    st.subheader("Clients List")
    if not clients_df.empty:
        display_cols = [
            mappings['clients']['client_id'],
            mappings['clients']['name'],
            mappings['clients']['phone'],
            mappings['clients']['address'],
            mappings['clients']['type'],
            mappings['clients']['latitude'],
            mappings['clients']['longitude']
        ]
        existing_cols = [col for col in display_cols if col in clients_df.columns]
        st.dataframe(clients_df[existing_cols])
    else:
        st.info("No client data available.")

def add_client(gspread_client, spreadsheet_url, new_client_data, mappings):
    """
    Adds a new client to the Clients sheet.
    """
    st.subheader("Add New Client")
    with st.form("add_client_form"):
        client_id = st.text_input(f"{mappings['clients']['client_id'].replace('_', ' ').title()}")
        name = st.text_input(f"{mappings['clients']['name'].replace('_', ' ').title()}")
        phone = st.text_input(f"{mappings['clients']['phone'].replace('_', ' ').title()}")
        address = st.text_area(f"{mappings['clients']['address'].replace('_', ' ').title()}")
        client_type = st.selectbox(f"{mappings['clients']['type'].replace('_', ' ').title()}", ["Individual", "Business", "Wholesale"])
        latitude = st.number_input(f"{mappings['clients']['latitude'].replace('_', ' ').title()}", format="%.6f")
        longitude = st.number_input(f"{mappings['clients']['longitude'].replace('_', ' ').title()}", format="%.6f")

        submitted = st.form_submit_button("Add Client")
        if submitted:
            new_row = {
                mappings['clients']['client_id']: client_id,
                mappings['clients']['name']: name,
                mappings['clients']['phone']: phone,
                mappings['clients']['address']: address,
                mappings['clients']['type']: client_type,
                mappings['clients']['latitude']: latitude,
                mappings['clients']['longitude']: longitude
            }
            try:
                spreadsheet = gspread_client.open_by_url(spreadsheet_url)
                clients_sheet = spreadsheet.worksheet("Clients")

                sheet_headers = clients_sheet.row_values(1)
                row_to_append = [new_row.get(header, '') for header in sheet_headers]

                clients_sheet.append_row(row_to_append)
                st.success(f"Client '{name}' added successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error adding client: {e}")

# Functions for updating/deleting clients would go here.
