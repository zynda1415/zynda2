# ----------- clients.py -----------
import streamlit as st
import data
import pandas as pd

def clients_management():
    st.header("Clients Management")
    df = data.load_clients()

    with st.form("client_form"):
        client_id = st.number_input("Client ID", 0)
        name = st.text_input("Client Name")
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        lat = st.number_input("Latitude", 0.0)
        lon = st.number_input("Longitude", 0.0)
        submitted = st.form_submit_button("Add Client")
        
        if submitted:
            new_row = pd.DataFrame([[client_id, name, phone, address, lat, lon]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            data.save_clients(df)
            st.success("Client Added Successfully!")
