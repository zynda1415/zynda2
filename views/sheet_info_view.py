import streamlit as st
import data

def sheet_info_module():
    st.title("📋 Sheet Info")

    # Pull Google Sheet object from data.py
    gsheet = data.sheet  # uses the authenticated gspread client

    try:
        worksheets = gsheet.worksheets()

        for ws in worksheets:
            sheet_name = ws.title
            headers = ws.row_values(1)  # get first row (column names)

            with st.expander(f"🗂 {sheet_name}"):
                st.write("**Headers:**", headers)

    except Exception as e:
        st.error(f"Failed to load sheet info: {e}")
