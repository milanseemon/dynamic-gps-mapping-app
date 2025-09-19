import streamlit as st
import pandas as pd
import folium
from pathlib import Path
import zipfile
import io

st.title("Flexible GPS & Data Visualization Tool")

st.markdown("""
Upload your dataset (Excel or CSV). The app will detect columns.
- Select variable(s) for grouping or analysis.
- Map visualization will be available if GPS coordinates are found.
- Download generated maps if applicable.
""")

uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith('xlsx'):
        df = pd.read_excel(uploaded_file, dtype=str)
    else:
        df = pd.read_csv(uploaded_file, dtype=str)
    
    st.write("Detected columns:", df.columns.tolist())
    
    # Detect latitude and longitude columns (case insensitive)
    lat_col = next((col for col in df.columns if 'latitude' in col.lower()), None)
    lon_col = next((col for col in df.columns if 'longitude' in col.lower()), None)
    
    group_vars = st.multiselect("Select variable(s) for grouping or analysis", options=df.columns.tolist())
    
    visualize_map = False
    if lat_col and lon_col:
        visualize_map = st.checkbox("Visualize map using GPS coordinates?")
    else:
        st.info("GPS coordinates columns not found. Map visualization not available.")
    
    if st.button("Generate Visualization"):
        if len(group_vars) == 0:
            st.error("Please select at least one variable for grouping or analysis.")
        else:
            # If map visualization requested and GPS coordinates are detected
            if visualize_map and lat_col and lon_col:
                # Clean coordinates
                df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
                df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
                df_clean = df.dropna(subset=[lat_col, lon_col])
                
                # Use first grouping variable for map creation
                group_var = group_vars[0]
                unique_groups = df_clean[group_var].unique()
                
                map_files = {}
                
                for grp in unique_groups:
                    df_grp = df_clean[df_clean[group_var] == grp]
                    if df_grp.empty:
                        continue
                    center = [df_grp[lat_col].median(), df_grp[lon_col].median()]
                    m = folium.Map(location=center, zoom_start=12)
                    for _, row in df_grp.iterrows():
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=3,
                            color='blue',
                            fill=True,
                            fill_color='blue',
                            popup=f"{group_var}: {row[group_var]}"
                        ).add_to(m)
                    
                    safe_name = "".join(c if c.isalnum() else "_" for c in str(grp))
                    html_str = m.get_root().render()
                    map_files[f"{safe_name}_map.html"] = html_str
                
                # Package maps as ZIP for download
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    for fname, html_str in map_files.items():
                        zf.writestr(fname, html_str)
                zip_buffer.seek(0)
                
                st.success(f"Generated {len(map_files)} map(s) for groups based on '{group_var}'.")
                st.download_button(
                    "Download All Maps (ZIP)",
                    data=zip_buffer,
                    file_name="generated_maps.zip",
                    mime="application/zip"
                )
            else:
                st.warning("Map visualization skipped or unavailable. Currently showing grouping summary instead.")
                summary = df[group_vars].drop_duplicates()
                st.write("Sample summary (unique combinations):")
                st.dataframe(summary.head(10))