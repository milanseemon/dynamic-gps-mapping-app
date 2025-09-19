import streamlit as st
import pandas as pd
import folium
from pathlib import Path
import zipfile
import io
import time
import base64
from streamlit_lottie import st_lottie
import json
import requests

# Set page configuration
st.set_page_config(
    page_title="GPS Data Visualization Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
lottie_loading = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_raiw2hpe.json")
lottie_map = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kyOW06.json")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        text-align: center;
        margin-bottom: 2rem;
    }
    .developer-name {
        font-size: 1.2rem;
        color: #546E7A;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #1E88E5;
    }
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
    .css-1v0mbdj {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        margin: 5px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0D47A1;
        color: white;
    }
    .success-message {
        padding: 15px;
        background-color: #E8F5E9;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0px;
    }
    .warning-message {
        padding: 15px;
        background-color: #FFF8E1;
        border-radius: 5px;
        border-left: 5px solid #FFC107;
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<p class="main-header">Flexible GPS & Data Visualization Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Mapping and Data Analysis Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="developer-name">Developed by Milan Seemon</p>', unsafe_allow_html=True)

# Sidebar for additional information
with st.sidebar:
    st.info("""
    ### Instructions:
    1. Upload your dataset (Excel or CSV format)
    2. Ensure your file contains columns named **'latitude'** and **'longitude'** for map visualization
    3. Select variables for grouping/analysis
    4. Generate visualizations and download results
    """)
    
    if lottie_map:
        st_lottie(lottie_map, height=200, key="map_animation")

# Main content
st.markdown("""
<div class="info-box">
    <h4>📋 Data Requirements</h4>
    <p>For optimal performance and map visualization, please ensure your dataset includes:</p>
    <ul>
        <li>Columns named <strong>latitude</strong> and <strong>longitude</strong> (case insensitive)</li>
        <li>Numerical values in coordinate columns</li>
        <li>Clean data with minimal missing values</li>
    </ul>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("**Upload your Excel or CSV file**", type=["xlsx", "csv"])

if uploaded_file:
    # Show loading animation
    with st.spinner('Processing your data...'):
        if lottie_loading:
            st_lottie(lottie_loading, height=100, key="loading")
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Load data
        progress_bar.progress(20)
        time.sleep(0.5)
        
        if uploaded_file.name.endswith('xlsx'):
            df = pd.read_excel(uploaded_file, dtype=str)
        else:
            df = pd.read_csv(uploaded_file, dtype=str)
        
        progress_bar.progress(50)
        time.sleep(0.5)
        
        st.success(f"✅ File successfully uploaded! Found {len(df)} rows and {len(df.columns)} columns.")
        
        # Display data preview
        with st.expander("Preview Data"):
            st.dataframe(df.head())
        
        progress_bar.progress(70)
        
        # Detect latitude and longitude columns (case insensitive)
        lat_col = next((col for col in df.columns if 'latitude' in col.lower()), None)
        lon_col = next((col for col in df.columns if 'longitude' in col.lower()), None)
        
        progress_bar.progress(90)
        
        if not lat_col or not lon_col:
            st.markdown("""
            <div class="warning-message">
                <h4>⚠️ GPS Coordinates Not Found</h4>
                <p>We couldn't detect columns named 'latitude' and 'longitude' in your dataset.</p>
                <p>Map visualization will not be available. Please check your column names and try again.</p>
                <p>Available columns: {}</p>
            </div>
            """.format(", ".join(df.columns.tolist())), unsafe_allow_html=True)
        
        group_vars = st.multiselect("**Select variable(s) for grouping or analysis**", options=df.columns.tolist())
        
        visualize_map = False
        if lat_col and lon_col:
            visualize_map = st.checkbox("Visualize map using GPS coordinates", value=True)
        
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        
        if st.button("🚀 Generate Visualization", use_container_width=True):
            if len(group_vars) == 0:
                st.error("Please select at least one variable for grouping or analysis.")
            else:
                # Create a status container
                status_text = st.empty()
                
                # If map visualization requested and GPS coordinates are detected
                if visualize_map and lat_col and lon_col:
                    status_text.text("Cleaning coordinate data...")
                    
                    # Clean coordinates
                    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
                    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
                    df_clean = df.dropna(subset=[lat_col, lon_col])
                    
                    if df_clean.empty:
                        st.error("No valid coordinates found after cleaning. Please check your data.")
                    else:
                        status_text.text("Creating maps...")
                        
                        # Use first grouping variable for map creation
                        group_var = group_vars[0]
                        unique_groups = df_clean[group_var].unique()
                        
                        map_files = {}
                        progress_bar = st.progress(0)
                        
                        for i, grp in enumerate(unique_groups):
                            df_grp = df_clean[df_clean[group_var] == grp]
                            if df_grp.empty:
                                continue
                            
                            center = [df_grp[lat_col].median(), df_grp[lon_col].median()]
                            m = folium.Map(location=center, zoom_start=12)
                            
                            for _, row in df_grp.iterrows():
                                folium.CircleMarker(
                                    location=[row[lat_col], row[lon_col]],
                                    radius=5,
                                    color='#1E88E5',
                                    fill=True,
                                    fill_color='#1E88E5',
                                    fill_opacity=0.7,
                                    popup=f"{group_var}: {row[group_var]}"
                                ).add_to(m)
                            
                            # Add group name to map
                            title_html = f'''
                                <h3 align="center" style="font-size:16px"><b>{group_var}: {grp}</b></h3>
                                '''
                            m.get_root().html.add_child(folium.Element(title_html))
                            
                            safe_name = "".join(c if c.isalnum() else "_" for c in str(grp))
                            html_str = m.get_root().render()
                            map_files[f"{safe_name}_map.html"] = html_str
                            
                            progress_bar.progress((i + 1) / len(unique_groups))
                        
                        status_text.text("Finalizing download package...")
                        
                        # Package maps as ZIP for download
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w") as zf:
                            for fname, html_str in map_files.items():
                                zf.writestr(fname, html_str)
                        zip_buffer.seek(0)
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.markdown(f"""
                        <div class="success-message">
                            <h4>✅ Successfully Generated {len(map_files)} Map(s)</h4>
                            <p>Maps created for groups based on '{group_var}'. Click below to download.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            "📥 Download All Maps (ZIP)",
                            data=zip_buffer,
                            file_name="generated_maps.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                else:
                    status_text.text("Generating summary...")
                    st.markdown("""
                    <div class="warning-message">
                        <h4>📊 Data Summary</h4>
                        <p>Map visualization skipped or unavailable. Showing grouping summary instead.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    summary = df[group_vars].drop_duplicates()
                    st.write("**Unique combinations:**")
                    st.dataframe(summary)
                    
                    # Show basic statistics if numerical columns exist
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        st.write("**Basic statistics:**")
                        st.dataframe(df[numeric_cols].describe())
                    
                    status_text.empty()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Developed with ❤️ by <strong>Milan Seemon</strong></p>
    <p>For support or questions, please contact: milan.seemon@example.com</p>
</div>
""", unsafe_allow_html=True)
