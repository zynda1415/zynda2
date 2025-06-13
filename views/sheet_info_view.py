import streamlit as st
import data
import json
from datetime import datetime
import os

def generate_config_py_from_headers(header_snapshot):
    path = "config.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated config from Sheet Info View\n")
        f.write("HEADER_ALIASES = {\n")
        for sheet, headers in header_snapshot.items():
            f.write(f'    "{sheet}": {{\n')
            for h in headers:
                key = h.lower().strip().replace(" ", "_").replace("(", "").replace(")", "")
                f.write(f'        "{key}": "{h}",\n')
            f.write("    },\n")
        f.write("}\n")


# 👇 Add this to bottom of sheet_info_module()
    st.markdown("---")
    if st.button("💡 Rebuild config.py from live headers"):
        generate_config_py_from_headers(header_snapshot)
        st.success("✅ config.py regenerated from current sheets.")

def sheet_info_module():
    st.title("🛠️ Sheet & Header Editor Pro")

    gsheet = data.sheet
    worksheets = gsheet.worksheets()
    header_snapshot = {}

    for ws in worksheets:
        sheet_name = ws.title
        headers = ws.row_values(1)
        header_snapshot[sheet_name] = headers

        with st.expander(f"📄 {sheet_name}"):
            # 🔁 Rename Sheet
            new_name = st.text_input(f"Rename Sheet", value=sheet_name, key=f"rename_{sheet_name}")
            if new_name != sheet_name:
                if st.button(f"✅ Rename Sheet: {sheet_name} → {new_name}", key=f"btn_{sheet_name}"):
                    ws.update_title(new_name)
                    log_change("Rename Sheet", sheet_name, new_name)
                    st.success("Sheet renamed. Please refresh.")
                    st.stop()

            # ✏️ Header Editing Section
            st.markdown("### ✏️ Column Headers:")
            new_headers = []
            if headers:
                cols = st.columns(min(len(headers), 10))
                for i, h in enumerate(headers):
                    col = cols[i % len(cols)]
                    color = "red" if not h.strip() or headers.count(h) > 1 else "black"
                    new_val = col.text_input(f"Col {i+1}", value=h, key=f"{sheet_name}_h{i}")
                    new_headers.append(new_val.strip())
            else:
                st.warning("⚠️ No headers found in this sheet.")

            # 🧠 Check for issues
            if headers:
                if len(set(new_headers)) != len(new_headers):
                    st.warning("⚠️ Duplicate column names detected.")
                if any(h == "" for h in new_headers):
                    st.warning("⚠️ Empty header names are not allowed.")

            # 👀 Preview Mode
            preview_mode = st.checkbox("Preview only (no changes)", value=True, key=f"preview_{sheet_name}")

            if headers and new_headers != headers and not preview_mode:
                if st.button(f"💾 Save Header Changes for {sheet_name}", key=f"save_{sheet_name}"):
                    ws.delete_rows(1)
                    ws.insert_row(new_headers, index=1)
                    log_change("Update Headers", sheet_name, f"{headers} → {new_headers}")
                    st.success("✅ Headers updated.")
                    st.stop()

            elif headers and new_headers != headers and preview_mode:
                st.info("🧪 Preview mode enabled. No changes saved.")
                st.write("Old:", headers)
                st.write("New:", new_headers)

    # ⬇️ Export all headers
    st.download_button(
        "⬇️ Export All Headers as JSON",
        data=json.dumps(header_snapshot, indent=2),
        file_name="sheet_headers.json",
        mime="application/json"
    )

def log_change(action, sheet, detail):
    """Append change to 'Log' worksheet if exists, or create it"""
    try:
        log_ws = data.sheet.worksheet("Log")
    except:
        log_ws = data.sheet.add_worksheet(title="Log", rows=1000, cols=5)
        log_ws.append_row(["Timestamp", "Action", "Sheet", "Details"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_ws.append_row([now, action, sheet, detail])
