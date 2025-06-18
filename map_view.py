import streamlit as st
import pandas as pd
import altair as alt

def render_map_view(clients_df, mappings):
    """
    Renders the client map view using Altair.
    """
    st.subheader("Client Locations on Map")

    lat_col = mappings['clients']['latitude']
    lon_col = mappings['clients']['longitude']
    name_col = mappings['clients']['name']
    address_col = mappings['clients']['address']

    if not clients_df.empty and lat_col in clients_df.columns and lon_col in clients_df.columns:
        # Ensure latitude and longitude are numeric
        clients_df[lat_col] = pd.to_numeric(clients_df[lat_col], errors='coerce')
        clients_df[lon_col] = pd.to_numeric(clients_df[lon_col], errors='coerce')

        # Drop rows with NaN in lat/lon for mapping
        map_data = clients_df.dropna(subset=[lat_col, lon_col])

        if not map_data.empty:
            # Altair map visualization
            # Base chart for the map, specifying the DataFrame
            base = alt.Chart(map_data).properties(
                title="Client Locations"
            )

            # Define the points on the map
            points = base.mark_circle().encode(
                latitude=alt.Latitude(lat_col),
                longitude=alt.Longitude(lon_col),
                size=alt.value(100), # Adjust marker size
                tooltip=[
                    alt.Tooltip(name_col, title="Client Name"),
                    alt.Tooltip(address_col, title="Address"),
                    alt.Tooltip(lat_col, title="Latitude", format=".4f"),
                    alt.Tooltip(lon_col, title="Longitude", format=".4f")
                ]
            )

            # Add text labels for client names (optional, can clutter map)
            # text = base.mark_text(dy=-10, dx=5, align='left').encode(
            #     latitude=alt.Latitude(lat_col),
            #     longitude=alt.Longitude(lon_col),
            #     text=name_col,
            #     color=alt.value('black')
            # )

            # Combine points and text (if using text) or just display points
            chart = points.interactive() # Enable zooming and panning

            st.altair_chart(chart, use_container_width=True)
            st.dataframe(map_data[[name_col, address_col, lat_col, lon_col]])
        else:
            st.warning("No client data with valid latitude and longitude for map view.")
    else:
        st.info("No 'Clients' sheet found or missing 'Latitude'/'Longitude' columns for map view.")
