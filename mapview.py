st.subheader("📍 Inventory Map View")

if 'Latitude' in df.columns and 'Longitude' in df.columns:
    map_data = df[['Latitude', 'Longitude']].dropna()
    st.map(map_data)
else:
    st.warning("No Latitude/Longitude columns found in your sheet.")
