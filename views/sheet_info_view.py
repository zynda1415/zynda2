def sheet_info_module():
    import gspread
    from google.oauth2.service_account import Credentials
    import json
    import os

    st.subheader("🧾 Sheet Info Manager")

    # Load credentials and spreadsheet
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)

    SPREADSHEET_ID = "1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Step 1: Choose sheet
    sheets = spreadsheet.worksheets()
    sheet_names = [ws.title for ws in sheets]
    selected_sheet_name = st.selectbox("📄 Select Sheet", sheet_names)

    ws = spreadsheet.worksheet(selected_sheet_name)
    headers = ws.row_values(1)

    # Step 2: Edit headers
    st.markdown("### ✏️ Edit Header Aliases")
    alias_map = {}
    for col in headers:
        alias = st.text_input(f"Label for **{col}**", value=col)
        alias_map[col] = alias

    # Step 3: Generate config.py
    if st.button("💾 Save & Generate config.py"):
        config_path = os.path.join(os.getcwd(), "config.py")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated header alias config\n")
            f.write("HEADER_ALIASES = {\n")
            for sheet in sheet_names:
                sheet_ws = spreadsheet.worksheet(sheet)
                hdrs = sheet_ws.row_values(1)
                f.write(f'    "{sheet}": {{\n')
                for h in hdrs:
                    label = alias_map.get(h, h)
                    key = label.lower().replace(" ", "_").replace("(", "").replace(")", "")
                    f.write(f'        "{key}": "{h}",\n')
                f.write("    },\n")
            f.write("}\n")
        st.success("✅ config.py generated successfully.")

    # Optional Preview
    with st.expander("🧬 Preview Generated HEADER_ALIASES"):
        st.code(f"HEADER_ALIASES = { {s: {k.lower().replace(' ', '_'): k for k in spreadsheet.worksheet(s).row_values(1)} for s in sheet_names} }", language="python")
