import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

def sheet_info_module():
    st.subheader("🧾 Sheet Info Manager")

    # Connect to Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # ➕ Create new sheet
    with st.expander("➕ Create New Sheet"):
        new_sheet_name = st.text_input("New Sheet Name")
        if st.button("📄 Create Sheet"):
            try:
                spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=20)
                st.success(f"Sheet '{new_sheet_name}' created. Refresh to see it.")
            except Exception as e:
                st.error(f"Failed to create sheet: {e}")

    # Select sheet
    sheet_names = [ws.title for ws in spreadsheet.worksheets()]
    selected_sheet = st.selectbox("📄 Select a sheet to manage:", sheet_names)
    ws = spreadsheet.worksheet(selected_sheet)

    # ✏️ Rename sheet
    with st.expander("✏️ Rename this sheet"):
        new_name = st.text_input("New name:", value=selected_sheet)
        if new_name and new_name != selected_sheet:
            if st.button(f"✅ Rename '{selected_sheet}' → '{new_name}'"):
                ws.update_title(new_name)
                st.success(f"✅ Sheet renamed to '{new_name}'. Refresh to continue.")
                st.stop()

    headers = ws.row_values(1)

    # ➖ Column delete/insert
    with st.expander("🗂 Column Management"):
        col_to_delete = st.selectbox("Select column to delete", headers)
        if st.button("🗑️ Delete Column"):
            idx = headers.index(col_to_delete) + 1
            ws.delete_columns(idx)
            st.success(f"Deleted column: {col_to_delete}")
            st.stop()

        new_col_name = st.text_input("Insert new column name")
        insert_at = st.number_input("Insert at position", min_value=1, max_value=len(headers)+1, value=len(headers)+1)
        if st.button("➕ Insert Column"):
            ws.insert_cols([[new_col_name]], col=insert_at)
            st.success(f"Inserted '{new_col_name}' at position {insert_at}")
            st.stop()

    # 🧾 Edit headers
    st.markdown("### ✏️ Edit header aliases")
    edited_headers = []
    for i, col in enumerate(headers):
        new_val = st.text_input(f"{i+1}. {col}", value=col, key=f"header_{i}")
        edited_headers.append(new_val)

    if st.button("💾 Save Edited Headers to Sheet"):
        ws.update("1:1", [edited_headers])
        st.success("✅ Headers updated successfully.")

    # 🕒 Backup + Generate config.py
    if st.button("⚙️ Regenerate config.py with updated aliases"):
        # Backup first
        config_dir = os.getcwd()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(config_dir, f"config_backup_{timestamp}.py")
        main_path = os.path.join(config_dir, "config.py")

        if os.path.exists(main_path):
            with open(main_path, "r", encoding="utf-8") as f:
                with open(backup_path, "w", encoding="utf-8") as b:
                    b.write(f.read())

        # Generate new config.py
        with open(main_path, "w", encoding="utf-8") as f:
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
        st.success("✅ config.py regenerated with backup saved.")

    # Preview config.py content
    with st.expander("🔎 Preview config.py aliases"):
        preview = {
            sheet.title: {
                h.strip().lower().replace(" ", "_"): h
                for h in sheet.row_values(1)
            }
            for sheet in spreadsheet.worksheets()
        }
        st.code(f"HEADER_ALIASES = {json.dumps(preview, indent=4)}", language="python")
