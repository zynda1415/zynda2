import streamlit as st
import data

def sheet_info_module():
    st.title("🛠️ Sheet & Header Editor")

    gsheet = data.sheet
    worksheets = gsheet.worksheets()

    for ws in worksheets:
        sheet_name = ws.title
        with st.expander(f"📄 {sheet_name}"):
            # 📝 Rename Sheet
            new_name = st.text_input(f"Rename Sheet '{sheet_name}'", value=sheet_name, key=f"rename_{sheet_name}")
            if new_name != sheet_name:
                if st.button(f"✅ Rename: {sheet_name} → {new_name}", key=f"btn_{sheet_name}"):
                    ws.update_title(new_name)
                    st.success("✅ Sheet renamed. Refresh the page.")
                    st.stop()

            # 🔠 Edit headers
            headers = ws.row_values(1)
            st.markdown("### ✏️ Edit Column Headers:")
            new_headers = []

            if headers:
                cols = st.columns(min(len(headers), 10))  # cap at 10 columns
                for i, h in enumerate(headers):
                    col = cols[i % 10]  # rotate layout every 10
                    new_val = col.text_input(f"Col {i+1}", value=h, key=f"{sheet_name}_{i}")
                    new_headers.append(new_val)
            else:
                st.warning("⚠️ No headers found in this sheet.")
                new_headers = []

            if headers and new_headers != headers:
                if st.button(f"💾 Save Header Changes for {sheet_name}", key=f"save_{sheet_name}"):
                    ws.delete_rows(1)
                    ws.insert_row(new_headers, index=1)
                    st.success("✅ Headers updated.")
                    st.stop()
