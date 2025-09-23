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
import random

# Set page configuration
st.set_page_config(
    page_title="GPS Data Visualization Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations
lottie_loading = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_raiw2hpe.json")
lottie_map = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_kyOW06.json")
lottie_plotting = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ot6erjsc.json")

# High-quality, relevant images for the tool
slideshow_images = [
    "https://images.unsplash.com/photo-1543286386-713bdd548da4?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",  # GPS mapping on smartphone
    "https://images.unsplash.com/photo-1587560699334-cc4ff634909a?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",  # Data visualization charts
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"   # Data analytics dashboard
]

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 4.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 0.2rem;
        font-weight: 900;
        padding: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 2.2rem;
        color: #A23B72;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    .developer-name {
        font-size: 1.5rem;
        color: #F18F01;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
        font-weight: 600;
    }
    .info-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #2E86AB;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: #333333;
    }
    .info-box h4 {
        color: #2E86AB;
        margin-bottom: 15px;
        font-size: 1.4rem;
    }
    .info-box ul {
        color: #333333;
    }
    .info-box p {
        color: #333333;
    }
    .stProgress > div > div > div > div {
        background-color: #2E86AB;
    }
    .stButton>button {
        background-color: #2E86AB;
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 8px;
        margin: 8px 0;
        width: 100%;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1B5E80;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .success-message {
        padding: 20px;
        background-color: #E8F5E9;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin: 15px 0px;
        color: #2E7D32;
    }
    .warning-message {
        padding: 20px;
        background-color: #FFF3E0;
        border-radius: 10px;
        border-left: 6px solid #FF9800;
        margin: 15px 0px;
        color: #EF6C00;
    }
    .error-message {
        padding: 20px;
        background-color: #FFEBEE;
        border-radius: 10px;
        border-left: 6px solid #F44336;
        margin: 15px 0px;
        color: #C62828;
    }
    .image-slideshow {
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        height: 200px;
    }
    .image-slideshow img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2E86AB;
    }
    .stExpander {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2E86AB;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .coming-soon {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
    }
    .contact-info {
    background-color: #2E86AB;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin: 15px 0;
    color: #ffffff;
    }
    .contact-info a {
    color: #ffffff !important;   /* White text for links */
    text-decoration: underline;  /* Optional: underline for visibility */
    }
    .contact-info a:hover {
    color: #FFD700 !important;   /* Gold highlight on hover */
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<p class="main-header">🌍 GPS DATA VISUALIZATION TOOL</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Mapping and Data Analysis Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="developer-name">Developed by Milan Seemon</p>', unsafe_allow_html=True)

# Coming soon notice for analysis features
st.markdown("""
<div class="coming-soon">
    <h3>🚀 Coming Soon: Advanced Data Analysis Interface</h3>
    <p>We're working on adding powerful analytical capabilities including clustering, heatmaps, route optimization, and statistical analysis!</p>
</div>
""", unsafe_allow_html=True)

# Image slideshow with reduced spacing
st.markdown("### 📸 Application Preview")
cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        st.markdown(f'<div class="image-slideshow"><img src="{slideshow_images[i]}" alt="Preview {i+1}"></div>', unsafe_allow_html=True)

# Sidebar for additional information
with st.sidebar:
    st.markdown("### ℹ️ Instructions:")
    st.info("""
    1. Upload your dataset (Excel or CSV format)
    2. Ensure your file contains columns named **'latitude'** and **'longitude'** for map visualization
    3. Select variables for grouping or labeling
    4. Generate visualizations and download results
    """)
    
    if lottie_map:
        st_lottie(lottie_map, height=180, key="map_animation")
    
    st.markdown("---")
    st.markdown("### 📊 Data Sample Format")
    
    sample_data = pd.DataFrame({
    'city': ['Delhi', 'Mumbai', 'Bengaluru', 'Kolkata', 'Chennai', 'Jaipur'],
    'state': ['Delhi', 'Maharashtra', 'Karnataka', 'West Bengal', 'Tamil Nadu', 'Rajasthan'],
    'latitude': [28.6139, 19.0760, 12.9716, 22.5726, 13.0827, 26.9124],
    'longitude': [77.2090, 72.8777, 77.5946, 88.3639, 80.2707, 75.7873],
    'category': ['Metro', 'Metro', 'Metro', 'Metro', 'Metro', 'Tourist'],
    'population_million': [30.3, 20.7, 12.7, 14.8, 11.2, 3.1],
    'avg_temp_c': [25, 27, 23, 26, 29, 24]
    })
    
    st.dataframe(sample_data, use_container_width=True)

    
    # Contact information in sidebar
    st.markdown("---")
    st.markdown("""
    <div class="contact-info">
        <h4>💡 Suggestions Welcome!</h4>
        <p>We're continuously improving this tool. Share your ideas and feedback:</p>
        <p><strong>milanseemon0912@gmail.com</strong></p>
    </div>
    """, unsafe_allow_html=True)

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
    <p>Your file header should include <strong>latitude</strong> and <strong>longitude</strong> for map visualization.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("**Upload your Excel or CSV file**", type=["xlsx", "csv"], help="Supported formats: Excel (.xlsx) or CSV (.csv)")

if uploaded_file:
    # Show loading animation
    with st.spinner('Processing your data...'):
        if lottie_loading:
            st_lottie(lottie_loading, height=100, key="loading")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Load data
        status_text.text("📂 Reading uploaded file...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        try:
            if uploaded_file.name.endswith('xlsx'):
                df = pd.read_excel(uploaded_file, dtype=str)
            else:
                df = pd.read_csv(uploaded_file, dtype=str)
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                <h4>❌ Error Reading File</h4>
                <p>There was an error reading your file: {str(e)}</p>
                <p>Please ensure you've uploaded a valid Excel or CSV file.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        
        progress_bar.progress(50)
        time.sleep(0.5)
        
        st.markdown(f"""
        <div class="success-message">
            <h4>✅ File Successfully Uploaded!</h4>
            <p>Found {len(df)} rows and {len(df.columns)} columns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display data preview
        with st.expander("🔍 Preview Data", expanded=True):
            st.dataframe(df.head(10))
        
        status_text.text("🔍 Analyzing data structure...")
        progress_bar.progress(70)
        
        # Detect latitude and longitude columns (case insensitive)
        lat_col = next((col for col in df.columns if 'latitude' in col.lower() or 'lat' in col.lower()), None)
        lon_col = next((col for col in df.columns if 'longitude' in col.lower() or 'lon' in col.lower() or 'lng' in col.lower()), None)
        
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
        else:
            st.markdown(f"""
            <div class="success-message">
                <h4>✅ GPS Coordinates Detected</h4>
                <p>Found latitude column: <strong>{lat_col}</strong></p>
                <p>Found longitude column: <strong>{lon_col}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Selection options
        st.markdown("### 🔧 Visualization Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            group_vars = st.multiselect(
                "**Select grouping variables (optional)**", 
                options=df.columns.tolist(),
                help="Select columns to group your data by (creates multiple maps)"
            )
        
        with col2:
            label_vars = st.multiselect(
                "**Select labeling variables**", 
                options=df.columns.tolist(),
                help="Select columns to display when clicking on map points"
            )
        
        visualize_map = False
        if lat_col and lon_col:
            visualize_map = st.checkbox("🗺️ Visualize map using GPS coordinates", value=True)
        
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        if st.button("🚀 Generate Visualization", use_container_width=True):
            if not label_vars and not group_vars:
                st.markdown("""
                <div class="error-message">
                    <h4>❌ Selection Required</h4>
                    <p>Please select at least one labeling variable or grouping variable.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Create a status container
                status_text = st.empty()
                
                # If map visualization requested and GPS coordinates are detected
                if visualize_map and lat_col and lon_col:
                    status_text.text("🧹 Cleaning coordinate data...")
                    
                    # Clean coordinates
                    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
                    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
                    df_clean = df.dropna(subset=[lat_col, lon_col])
                    
                    if df_clean.empty:
                        st.markdown("""
                        <div class="error-message">
                            <h4>❌ No Valid Coordinates</h4>
                            <p>No valid coordinates found after cleaning. Please check your data.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        status_text.text("🗺️ Creating maps...")
                        
                        # Show plotting animation
                        if lottie_plotting:
                            st_lottie(lottie_plotting, height=200, key="plotting")
                        
                        map_files = {}
                        progress_bar = st.progress(0)
                        
                        # Determine if we're creating a single map or multiple grouped maps
                        if group_vars:
                            # Use first grouping variable for map creation
                            group_var = group_vars[0]
                            unique_groups = df_clean[group_var].unique()
                            
                            for i, grp in enumerate(unique_groups):
                                df_grp = df_clean[df_clean[group_var] == grp]
                                if df_grp.empty:
                                    continue
                                
                                center = [df_grp[lat_col].median(), df_grp[lon_col].median()]
                                m = folium.Map(location=center, zoom_start=12)
                                
                                for _, row in df_grp.iterrows():
                                    # Create popup text with all label variables
                                    popup_text = "<br>".join([f"<b>{var}:</b> {row[var]}" for var in label_vars]) if label_vars else f"{group_var}: {row[group_var]}"
                                    
                                    folium.CircleMarker(
                                        location=[row[lat_col], row[lon_col]],
                                        radius=5,
                                        color='#2E86AB',
                                        fill=True,
                                        fill_color='#2E86AB',
                                        fill_opacity=0.7,
                                        popup=popup_text
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
                        else:
                            # Create a single map with all points
                            center = [df_clean[lat_col].median(), df_clean[lon_col].median()]
                            m = folium.Map(location=center, zoom_start=12)
                            
                            for _, row in df_clean.iterrows():
                                # Create popup text with all label variables
                                popup_text = "<br>".join([f"<b>{var}:</b> {row[var]}" for var in label_vars]) if label_vars else "Location"
                                
                                folium.CircleMarker(
                                    location=[row[lat_col], row[lon_col]],
                                    radius=5,
                                    color='#2E86AB',
                                    fill=True,
                                    fill_color='#2E86AB',
                                    fill_opacity=0.7,
                                    popup=popup_text
                                ).add_to(m)
                            
                            # Add title to map
                            title_html = '''
                                <h3 align="center" style="font-size:16px"><b>All Locations</b></h3>
                                '''
                            m.get_root().html.add_child(folium.Element(title_html))
                            
                            html_str = m.get_root().render()
                            map_files["all_locations_map.html"] = html_str
                            progress_bar.progress(100)
                        
                        status_text.text("📦 Finalizing download package...")
                        
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
                            <p>{'Maps created for groups' if group_vars else 'Single map created'} with {len(label_vars)} labeling variables.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            "📥 Download All Maps (ZIP)",
                            data=zip_buffer,
                            file_name="generated_maps.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
                        # Show sample map
                        if map_files:
                            sample_key = list(map_files.keys())[0]
                            st.markdown("### 🗺️ Map Preview")
                            st.components.v1.html(map_files[sample_key], height=400)
                else:
                    status_text.text("📊 Generating summary...")
                    st.markdown("""
                    <div class="warning-message">
                        <h4>📊 Data Summary</h4>
                        <p>Map visualization skipped or unavailable. Showing data summary instead.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if group_vars:
                        summary = df[group_vars].drop_duplicates()
                        st.write("**Unique combinations:**")
                        st.dataframe(summary)
                    
                    # Show basic statistics if numerical columns exist
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        st.write("**Basic statistics:**")
                        st.dataframe(df[numeric_cols].describe())
                    
                    status_text.empty()

# Footer with enhanced contact information
st.markdown("---")
st.markdown("""
<div style="text-align: center; max-width: 600px; margin: auto;">
    <p>Developed with ❤️ by <strong>Milan Seemon</strong></p>
    <div class="contact-info">
        <h4>📧 Contact & Suggestions</h4>
        <p>This tool is continuously evolving. We welcome your feedback and suggestions for new features!</p>
        <p>Email: <a href="mailto:milanseemon0912@gmail.com">milanseemon0912@gmail.com</a></p>
        <p>LinkedIn: <a href="https://www.linkedin.com/in/milanseemon-ms/" target="_blank" rel="noopener noreferrer">linkedin.com/in/milanseemon-ms/</a></p>
        <p>Data Analysis Module - <strong>In Development</strong> - Coming Soon!</p>
    </div>
</div>
""", unsafe_allow_html=True)













