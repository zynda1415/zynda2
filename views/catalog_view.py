from config import HEADER_ALIASES as H

...

def catalog_module():
    ...
    col = H["Inventory"]
    df = data.load_inventory()

    ...

    if search:
        df = df[df.apply(lambda row: search.lower() in str(row[col["name"]]).lower()
                         or search.lower() in str(row[col["category"]]).lower()
                         or search.lower() in str(row.get(col["note"], "")).lower(), axis=1)]

    if category_filter != "All":
        df = df[df[col["category"]] == category_filter]

    # ✅ Proper indentation of Export Button
    if st.button("📄 Export Visual Catalog to PDF"):
        try:
            pdf_df = df.copy()

            if col["brand"] in pdf_df.columns and "Brand" not in pdf_df.columns:
                pdf_df["Brand"] = pdf_df[col["brand"]]
            if col["stock"] in pdf_df.columns and "Stock" not in pdf_df.columns:
                pdf_df["Stock"] = pdf_df[col["stock"]]
            if col["category"] in pdf_df.columns and "Category 1" not in pdf_df.columns:
                pdf_df["Category 1"] = pdf_df[col["category"]]
            if col["note"] in pdf_df.columns and "Note" not in pdf_df.columns:
                pdf_df["Note"] = pdf_df[col["note"]]

            required_columns = {
                col["name"]: "Unknown Item",
                col["price"]: 0.0,
                "Stock": 0,
                "Brand": "Unknown Brand",
                "Category 1": "Uncategorized",
                "Note": "",
                col["image"]: "",
                col["barcode"]: ""
            }
            for c, default_val in required_columns.items():
                if c not in pdf_df.columns:
                    pdf_df[c] = default_val

            # ⬇️ Customize layout and generate PDF
            pdf_options = pdf_customization_controls()
            pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
                pdf_df,
                image_position=pdf_options["image_position"],
                name_font_size=pdf_options["name_font_size"],
                stack_text=pdf_options["stack_text"],
                show_barcode=pdf_options["show_barcode_pdf"]
            )

            st.success("PDF Generated Successfully!")
            st.download_button("Download PDF", data=pdf_bytes, file_name=filename)

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.write("DataFrame columns available:", list(df.columns))
