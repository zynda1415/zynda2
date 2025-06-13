import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os

def sheet_info_module():
    st.subheader("🧾 Sheet Info Manager")

    # Connect to Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Select sheet
    sheet_names = [ws.title for ws in spreadsheet.worksheets()]
    selected_sheet = st.selectbox("📄 Select a sheet to manage:", sheet_names)
    ws = spreadsheet.worksheet(selected_sheet)

    # Sheet rename
    with st.expander("✏️ Rename this sheet"):
        new_name = st.text_input("New name:", value=selected_sheet)
        if new_name and new_name != selected_sheet:
            if st.button(f"✅ Rename '{selected_sheet}' → '{new_name}'"):
                ws.update_title(new_name)
                st.success(f"✅ Sheet renamed to '{new_name}'. Refresh to continue.")
                st.stop()

    headers = ws.row_values(1)

    # Display + editable alias mapping
    st.markdown("### ✏️ Edit header aliases")
    edited_headers = []
    for i, col in enumerate(headers):
        new_val = st.text_input(f"{i+1}. {col}", value=col, key=f"header_{i}")
        edited_headers.append(new_val)

    # Save changes back to the sheet
    if st.button("💾 Save Edited Headers to Sheet"):
        ws.update("1:1", [edited_headers])
        st.success("✅ Headers updated successfully.")

    # Regenerate config.py
    if st.button("⚙️ Regenerate config.py with updated aliases"):
        config_path = os.path.join(os.getcwd(), "config.py")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated header alias config\n")
            f.write("HEADER_ALIASES = {\n")
            for sheet in spreadsheet.worksheets():
                hdrs = sheet.row_values(1)
                f.write(f'    "{sheet.title}": {{\n')
                for h in hdrs:
                    alias = h.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
                    f.write(f'        "{alias}": "{h}",\n')
                f.write("    },\n")
            f.write("}\n")
        st.success("✅ config.py regenerated.")

    # Preview current generated config
    with st.expander("🔎 Preview config.py aliases"):
        preview = {
            sheet.title: {
                h.strip().lower().replace(" ", "_"): h
                for h in sheet.row_values(1)
            }
            for sheet in spreadsheet.worksheets()
        }
        st.code(f"HEADER_ALIASES = {json.dumps(preview, indent=4)}", language="python")
