import streamlit as st
import data

def sheet_info_module():
    st.title("🛠️ Sheet & Header Editor")

    gsheet = data.sheet
    worksheets = gsheet.worksheets()

    for ws in worksheets:
        old_name = ws.title

        with st.expander(f"🗂 {old_name}"):
            new_name = st.text_input(f"Rename Sheet '{old_name}'", value=old_name, key=f"rename_{old_name}")

            if new_name != old_name:
                if st.button(f"✅ Apply Sheet Rename: {old_name} → {new_name}", key=f"btn_{old_name}"):
                    ws.update_title(new_name)
                    st.success("Sheet renamed! Please reload app.")

            headers = ws.row_values(1)
            st.markdown("### ✏️ Edit Column Headers:")
            new_headers = []

            cols = st.columns(len(headers))
            for i, h in enumerate(headers):
                new = cols[i].text_input(f"Col {i+1}", value=h, key=f"header_{old_name}_{i}")
                new_headers.append(new)

            if new_headers != headers:
                if st.button(f"💾 Update Headers for {new_name}", key=f"save_headers_{old_name}"):
                    ws.delete_rows(1)
                    ws.insert_row(new_headers, index=1)
                    st.success("Headers updated successfully.")
