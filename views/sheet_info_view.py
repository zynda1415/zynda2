import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

def sheet_info_module():
    st.title("🗂️ Sheet Info Manager")
    st.markdown("Manage sheets, headers, and configuration for dynamic integration.")

    # Authenticate & Load Google Sheet
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # === Create New Sheet ===
    with st.expander("➕ Create New Sheet"):
        new_sheet_name = st.text_input("New Sheet Name", placeholder="e.g. Products2025")
        if st.button("📄 Create Sheet"):
            try:
                spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=20)
                st.success(f"✅ Sheet '{new_sheet_name}' created. Refresh to view.")
            except Exception as e:
                st.error(f"❌ Failed to create sheet: {e}")

    # === Sheet Selection & Metadata ===
    sheet_names = [ws.title for ws in spreadsheet.worksheets()]
    selected_sheet = st.selectbox("📑 Select Sheet to Edit", sheet_names)
    ws = spreadsheet.worksheet(selected_sheet)
    headers = ws.row_values(1)

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"### 📝 Header Aliases ({len(headers)} columns)")
    with col2:
        if st.button("🔄 Refresh Sheet List"):
            st.rerun()

    # === Edit Header Aliases (Compact Grid) ===
   st.markdown("### ✏️ Edit Header Aliases")
   edited_headers = []
   num_cols = 3  # adjust to 4 or 5 for tighter fit

   for i in range(0, len(headers), num_cols):
       row = headers[i:i+num_cols]
       cols = st.columns(len(row))
       for j, h in enumerate(row):
           with cols[j]:
               new_val = st.text_input(f"{i+j+1}", value=h, key=f"header_{i+j}")
               edited_headers.append(new_val)


    # === Column Insert/Delete Section ===
    with st.expander("🛠️ Column Management"):
        col1, col2 = st.columns(2)

        with col1:
            col_to_delete = st.selectbox("🗑️ Delete column", headers, key="del_col")
            if st.button("Delete Selected Column"):
                idx = headers.index(col_to_delete) + 1
                ws.delete_columns(idx)
                st.success(f"✅ Deleted column: {col_to_delete}")
                st.stop()

        with col2:
            new_col_name = st.text_input("➕ Column Name", key="new_col")
            insert_at = st.number_input("Insert at (1-indexed)", min_value=1, max_value=len(headers)+1, value=len(headers)+1)
            if st.button("Insert Column"):
                ws.insert_cols([[new_col_name]], col=int(insert_at))
                st.success(f"✅ Inserted '{new_col_name}' at position {insert_at}")
                st.stop()

    # === Sheet Rename Section ===
    with st.expander("✏️ Rename Sheet"):
        new_name = st.text_input("Rename To", value=selected_sheet, key="rename_sheet")
        if new_name and new_name != selected_sheet:
            if st.button("✅ Apply Rename"):
                ws.update_title(new_name)
                st.success(f"✅ Renamed sheet to: {new_name}")
                st.stop()

    # === Regenerate Config.py with Backup ===
    if st.button("⚙️ Regenerate config.py (with backup)"):
        config_dir = os.getcwd()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(config_dir, f"config_backup_{timestamp}.py")
        main_path = os.path.join(config_dir, "config.py")

        # Backup old config
        if os.path.exists(main_path):
            with open(main_path, "r", encoding="utf-8") as f:
                with open(backup_path, "w", encoding="utf-8") as b:
                    b.write(f.read())

        # Generate new config
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

    # === Preview Config ===
    with st.expander("📁 Preview Generated config.py"):
        preview = {
            sheet.title: {
                h.strip().lower().replace(" ", "_"): h
                for h in sheet.row_values(1)
            }
            for sheet in spreadsheet.worksheets()
        }
        st.code(f"HEADER_ALIASES = {json.dumps(preview, indent=4)}", language="python")
