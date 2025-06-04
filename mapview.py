elif menu == "Map":
    st.subheader("📍 Inventory Map View")

    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        # Prepare dataframe for map
        map_data = df[['Latitude', 'Longitude']].dropna()
        st.map(map_data)
    else:
        st.warning("No latitude/longitude data found in your sheet.")
