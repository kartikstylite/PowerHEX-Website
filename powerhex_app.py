import streamlit as st
import requests
import hashlib
import json
import os
from datetime import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import io
import base64
import time
import random

# Page configuration
st.set_page_config(
    page_title="PowerHEX - AI Image Detection Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
    }
    .result-box {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .genuine-result {
        background: #d4edda;
        border-left: 5px solid #28a745;
    }
    .fake-result {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    .suspicious-result {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_database():
    conn = sqlite3.connect('powerhex_data.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_hash TEXT,
            scan_result TEXT,
            confidence_score REAL,
            timestamp DATETIME,
            metadata TEXT,
            flagged BOOLEAN DEFAULT FALSE,
            flag_reason TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS educational_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_taken BOOLEAN,
            score INTEGER,
            timestamp DATETIME
        )
    ''')
    
    conn.commit()
    conn.close()

# Mock AI Detection APIs (simulating real APIs for demo)
class MockDetectionAPIs:
    @staticmethod
    def deepware_detection(image_data):
        """Simulate Deepware API response"""
        # Simulate processing time
        time.sleep(2)
        
        # Random but realistic results for demo
        confidence = random.uniform(0.15, 0.95)
        is_fake = confidence > 0.6
        
        return {
            "is_fake": is_fake,
            "confidence": confidence,
            "api_name": "Deepware API",
            "details": {
                "face_detected": True,
                "manipulation_type": "deepfake" if is_fake else "none",
                "processing_time": "2.1s"
            }
        }
    
    @staticmethod
    def faceforensics_detection(image_data):
        """Simulate FaceForensics detection"""
        time.sleep(1.5)
        
        confidence = random.uniform(0.2, 0.9)
        is_fake = confidence > 0.55
        
        return {
            "is_fake": is_fake,
            "confidence": confidence,
            "api_name": "FaceForensics++",
            "details": {
                "compression_artifacts": random.choice([True, False]),
                "temporal_consistency": random.choice(["consistent", "inconsistent"]),
                "neural_network_traces": is_fake
            }
        }

# Image metadata extraction
def extract_metadata(image):
    """Extract EXIF metadata from image"""
    try:
        exifdata = image.getexif()
        metadata = {}
        
        if exifdata:
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                
                if isinstance(data, bytes):
                    data = data.decode()
                    
                metadata[tag] = data
        
        # Add basic image info
        metadata.update({
            "Image Size": f"{image.size[0]} x {image.size[1]}",
            "Image Mode": image.mode,
            "Image Format": image.format
        })
        
        return metadata
    except Exception as e:
        return {"Error": f"Could not extract metadata: {str(e)}"}

# Reverse image search simulation
def reverse_image_search(image_hash):
    """Simulate reverse image search"""
    time.sleep(1)
    
    # Mock results
    results = [
        {"source": "TinEye", "matches": random.randint(0, 15), "earliest_date": "2023-03-15"},
        {"source": "Google Images", "matches": random.randint(0, 25), "earliest_date": "2023-01-20"}
    ]
    
    return results

# Main detection function
def perform_detection(image, filename):
    """Perform comprehensive image detection"""
    
    # Convert image to bytes for API calls
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Create file hash
    file_hash = hashlib.md5(img_byte_arr).hexdigest()
    
    # Run multiple detection APIs
    st.info("🔍 Running AI detection algorithms...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.spinner("Deepware API analyzing..."):
            deepware_result = MockDetectionAPIs.deepware_detection(img_byte_arr)
    
    with col2:
        with st.spinner("FaceForensics++ analyzing..."):
            faceforensics_result = MockDetectionAPIs.faceforensics_detection(img_byte_arr)
    
    # Extract metadata
    st.info("📊 Extracting image metadata...")
    metadata = extract_metadata(image)
    
    # Reverse image search
    st.info("🔄 Performing reverse image search...")
    reverse_results = reverse_image_search(file_hash)
    
    # Combine results
    avg_confidence = (deepware_result["confidence"] + faceforensics_result["confidence"]) / 2
    is_likely_fake = avg_confidence > 0.6
    
    # Determine overall result
    if avg_confidence > 0.8:
        result_type = "LIKELY FAKE"
        result_class = "fake-result"
        result_icon = "🚨"
    elif avg_confidence > 0.6:
        result_type = "SUSPICIOUS"
        result_class = "suspicious-result"
        result_icon = "⚠️"
    else:
        result_type = "LIKELY GENUINE"
        result_class = "genuine-result"
        result_icon = "✅"
    
    # Store in database
    conn = sqlite3.connect('powerhex_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scans (filename, file_hash, scan_result, confidence_score, timestamp, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, file_hash, result_type, avg_confidence, datetime.now(), json.dumps(metadata)))
    conn.commit()
    conn.close()
    
    return {
        "result_type": result_type,
        "result_class": result_class,
        "result_icon": result_icon,
        "confidence": avg_confidence,
        "deepware": deepware_result,
        "faceforensics": faceforensics_result,
        "metadata": metadata,
        "reverse_search": reverse_results,
        "file_hash": file_hash
    }

# Dashboard analytics
def show_analytics():
    """Display analytics dashboard"""
    st.markdown('<div class="main-header"><h1>📊 Analytics Dashboard</h1></div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('powerhex_data.db')
    
    # Get scan statistics
    df_scans = pd.read_sql_query("SELECT * FROM scans", conn)
    
    if len(df_scans) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Scans", len(df_scans))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            fake_count = len(df_scans[df_scans['scan_result'] == 'LIKELY FAKE'])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Fake Images", fake_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            flagged_count = len(df_scans[df_scans['flagged'] == True])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Flagged Images", flagged_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            avg_confidence = df_scans['confidence_score'].mean()
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg. Confidence", f"{avg_confidence:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Results distribution
            result_counts = df_scans['scan_result'].value_counts()
            fig_pie = px.pie(values=result_counts.values, names=result_counts.index,
                           title="Detection Results Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Confidence score distribution
            fig_hist = px.histogram(df_scans, x='confidence_score', nbins=20,
                                  title="Confidence Score Distribution")
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Timeline
        df_scans['timestamp'] = pd.to_datetime(df_scans['timestamp'])
        daily_scans = df_scans.groupby(df_scans['timestamp'].dt.date).size().reset_index()
        daily_scans.columns = ['date', 'count']
        
        fig_line = px.line(daily_scans, x='date', y='count', title='Daily Scan Activity')
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Recent scans table
        st.subheader("Recent Scans")
        recent_scans = df_scans.tail(10)[['filename', 'scan_result', 'confidence_score', 'timestamp']]
        st.dataframe(recent_scans, use_container_width=True)
    
    else:
        st.info("No scan data available yet. Upload and scan some images to see analytics!")
    
    conn.close()

# Educational section
def show_education():
    """Educational content and quiz"""
    st.markdown('<div class="main-header"><h1>🎓 Learn About AI-Generated Images</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📚 Educational Content", "🧠 Take Quiz"])
    
    with tab1:
        st.markdown("""
        ## How to Spot AI-Generated Images
        
        ### Common Signs of Deepfakes:
        1. **Inconsistent lighting** - Check if light sources match across the face
        2. **Blurring around face edges** - Look for unnatural smoothing
        3. **Inconsistent skin texture** - AI often struggles with realistic skin
        4. **Eye problems** - Mismatched eyes, strange reflections, or focus issues
        5. **Temporal artifacts** - In videos, watch for flickering or inconsistencies
        
        ### Technical Indicators:
        - **Metadata inconsistencies** - Check EXIF data for anomalies
        - **Compression artifacts** - Look for unusual compression patterns
        - **Reverse image search** - Check if the image appears elsewhere online
        
        ### Tips for Verification:
        ✅ Always check multiple sources  
        ✅ Look for official verification  
        ✅ Use reverse image search tools  
        ✅ Check metadata and technical details  
        ✅ Be skeptical of sensational content  
        """)
        
        # Sample images section
        st.subheader("Sample Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Real Image Characteristics:**\n- Natural skin texture\n- Consistent lighting\n- Proper eye reflections\n- Authentic metadata")
        
        with col2:
            st.warning("**AI-Generated Indicators:**\n- Overly smooth skin\n- Inconsistent shadows\n- Strange eye behavior\n- Missing/altered metadata")
    
    with tab2:
        st.subheader("Test Your Knowledge")
        
        questions = [
            {
                "question": "What is a common sign of a deepfake image?",
                "options": ["High resolution", "Inconsistent lighting", "Bright colors", "Large file size"],
                "correct": 1
            },
            {
                "question": "Which metadata field can help identify AI-generated images?",
                "options": ["File size", "Camera model", "Creation software", "All of the above"],
                "correct": 3
            },
            {
                "question": "What should you do when you suspect an image is fake?",
                "options": ["Share it immediately", "Ignore it", "Verify through multiple sources", "Delete it"],
                "correct": 2
            }
        ]
        
        score = 0
        for i, q in enumerate(questions):
            st.write(f"**Question {i+1}:** {q['question']}")
            answer = st.radio(f"Select answer for Q{i+1}:", q['options'], key=f"q{i}")
            
            if st.button(f"Check Answer {i+1}", key=f"check{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success("Correct! ✅")
                    score += 1
                else:
                    st.error(f"Incorrect. The right answer is: {q['options'][q['correct']]}")
        
        if st.button("Submit Quiz"):
            # Store quiz results
            conn = sqlite3.connect('powerhex_data.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO educational_stats (quiz_taken, score, timestamp)
                VALUES (?, ?, ?)
            ''', (True, score, datetime.now()))
            conn.commit()
            conn.close()
            
            st.success(f"Quiz completed! Your score: {score}/{len(questions)}")

# Reporting system
def show_reporting():
    """Community reporting interface"""
    st.markdown('<div class="main-header"><h1>🚩 Report Suspicious Images</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Report Image", "📋 Review Reports"])
    
    with tab1:
        st.subheader("Report a Suspicious Image")
        
        # Get scan history for reporting
        conn = sqlite3.connect('powerhex_data.db')
        df_scans = pd.read_sql_query("SELECT id, filename, scan_result FROM scans WHERE flagged = FALSE", conn)
        conn.close()
        
        if len(df_scans) > 0:
            selected_scan = st.selectbox("Select an image to report:", 
                                       options=df_scans['id'].tolist(),
                                       format_func=lambda x: df_scans[df_scans['id']==x]['filename'].iloc[0])
            
            reason = st.selectbox("Reason for reporting:", [
                "Suspected deepfake",
                "Identity theft",
                "Misinformation",
                "Inappropriate content",
                "Other"
            ])
            
            additional_info = st.text_area("Additional information (optional):")
            
            if st.button("Submit Report"):
                # Update database
                conn = sqlite3.connect('powerhex_data.db')
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE scans SET flagged = TRUE, flag_reason = ? WHERE id = ?
                ''', (f"{reason}: {additional_info}", selected_scan))
                conn.commit()
                conn.close()
                
                st.success("Report submitted successfully! ✅")
                st.rerun()
        else:
            st.info("No images available to report. Scan some images first!")
    
    with tab2:
        st.subheader("Flagged Images Review")
        
        conn = sqlite3.connect('powerhex_data.db')
        df_flagged = pd.read_sql_query("SELECT * FROM scans WHERE flagged = TRUE", conn)
        conn.close()
        
        if len(df_flagged) > 0:
            for _, row in df_flagged.iterrows():
                with st.expander(f"🚩 {row['filename']} - {row['scan_result']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Confidence:** {row['confidence_score']:.2f}")
                        st.write(f"**Timestamp:** {row['timestamp']}")
                    with col2:
                        st.write(f"**Reason:** {row['flag_reason']}")
                        if st.button(f"Resolve Report", key=f"resolve_{row['id']}"):
                            # Update database to remove flag
                            conn = sqlite3.connect('powerhex_data.db')
                            cursor = conn.cursor()
                            cursor.execute('UPDATE scans SET flagged = FALSE WHERE id = ?', (row['id'],))
                            conn.commit()
                            conn.close()
                            st.success("Report resolved!")
                            st.rerun()
        else:
            st.info("No flagged images to review.")

# Main application
def main():
    init_database()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🛡️ PowerHEX Navigation")
    page = st.sidebar.selectbox("Choose a page:", [
        "🔍 Image Scanner",
        "📊 Analytics Dashboard", 
        "🎓 Education Center",
        "🚩 Reporting System"
    ])
    
    # Main content based on page selection
    if page == "🔍 Image Scanner":
        st.markdown('<div class="main-header"><h1>🛡️ PowerHEX - AI Image Detection Platform</h1><p>Upload images to detect AI manipulation and deepfakes</p></div>', unsafe_allow_html=True)
        
        # File upload
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload PNG, JPG, or JPEG images for analysis"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(image, caption=f"Uploaded: {uploaded_file.name}", use_column_width=True)
            
            with col2:
                st.info(f"**File:** {uploaded_file.name}\n**Size:** {len(uploaded_file.getvalue())} bytes\n**Dimensions:** {image.size[0]} x {image.size[1]}")
            
            # Perform detection
            if st.button("🔍 Analyze Image", type="primary"):
                results = perform_detection(image, uploaded_file.name)
                
                # Display results
                st.markdown(f'<div class="result-box {results["result_class"]}">', unsafe_allow_html=True)
                st.markdown(f"## {results['result_icon']} {results['result_type']}")
                st.markdown(f"**Confidence Score:** {results['confidence']:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Detailed results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🤖 AI Detection Results")
                    
                    # Deepware results
                    st.markdown("**Deepware API:**")
                    st.write(f"- Fake: {'Yes' if results['deepware']['is_fake'] else 'No'}")
                    st.write(f"- Confidence: {results['deepware']['confidence']:.2f}")
                    st.write(f"- Processing time: {results['deepware']['details']['processing_time']}")
                    
                    # FaceForensics results
                    st.markdown("**FaceForensics++:**")
                    st.write(f"- Fake: {'Yes' if results['faceforensics']['is_fake'] else 'No'}")
                    st.write(f"- Confidence: {results['faceforensics']['confidence']:.2f}")
                    st.write(f"- Neural traces: {'Detected' if results['faceforensics']['details']['neural_network_traces'] else 'None'}")
                
                with col2:
                    st.subheader("📊 Image Metadata")
                    for key, value in results['metadata'].items():
                        if key not in ['MakerNote', 'UserComment']:  # Skip binary data
                            st.write(f"**{key}:** {value}")
                
                # Reverse search results
                st.subheader("🔄 Reverse Image Search Results")
                for result in results['reverse_search']:
                    st.write(f"**{result['source']}:** {result['matches']} matches (earliest: {result['earliest_date']})")
                
                st.success("✅ Analysis complete! Results saved to database.")
    
    elif page == "📊 Analytics Dashboard":
        show_analytics()
    
    elif page == "🎓 Education Center":
        show_education()
    
    elif page == "🚩 Reporting System":
        show_reporting()
    
    # Footer
    st.markdown("---")
    st.markdown("**PowerHEX** - Developed for Smart India Hackathon 2025 | Team PowerHEX | Problem Statement ID: 25161")

if __name__ == "__main__":
    main()