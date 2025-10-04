# PowerHEX - AI Image Detection Platform 🛡️

## Smart India Hackathon 2024 - Problem Statement ID: 25161

**Team:** PowerHEX  
**Theme:** Blockchain & Cybersecurity  
**Category:** Software  

### Problem Statement
Mitigating National Security Risks Posed by Large Language Models (LLMs) in AI-Driven Malign Information Operations

### Solution Overview
PowerHEX is a comprehensive tampering detection and awareness platform that enables users to upload and scan images for AI manipulation. Our solution combines multiple detection APIs, metadata analysis, reverse image search, and community reporting to create a robust defense against deepfakes and AI-generated misinformation.

## Features ✨

### 🔍 Core Detection Capabilities
- **Multi-API Integration**: Combines Deepware API and FaceForensics++ for comprehensive detection
- **Metadata Analysis**: Extracts and analyzes EXIF data to identify manipulation signatures
- **Confidence Scoring**: Provides probability scores for AI-generation likelihood
- **Real-time Processing**: Fast analysis with visual progress indicators

### 📊 Analytics Dashboard
- **Scan Statistics**: Track total scans, fake detection rates, and confidence metrics
- **Visual Analytics**: Interactive charts showing detection patterns and trends
- **Timeline Analysis**: Monitor scanning activity over time
- **Community Insights**: Aggregate data on flagged content

### 🎓 Educational Center
- **Detection Guides**: Learn how to spot AI-generated images manually
- **Interactive Quizzes**: Test knowledge about deepfake detection
- **Best Practices**: Guidelines for image verification and reporting
- **Technical Insights**: Understanding metadata and compression artifacts

### 🚩 Community Reporting
- **User Flagging**: Report suspicious images for community review
- **Admin Dashboard**: Review and manage flagged content
- **Collaborative Verification**: Community-driven content validation

### 🔄 Reverse Image Search
- **Multi-platform Search**: Integration with TinEye and Google Images
- **Timeline Tracking**: Identify earliest appearances of images online
- **Source Verification**: Cross-reference against known image databases

## Technical Architecture 🏗️

### Frontend
- **Framework**: Streamlit with custom CSS styling
- **Interface**: Responsive web application with intuitive navigation
- **Visualization**: Plotly-powered interactive charts and analytics

### Backend
- **Language**: Python 3.8+
- **Database**: SQLite for local data storage
- **APIs**: Mock implementations of detection services (easily replaceable with real APIs)
- **Processing**: PIL/Pillow for image handling and metadata extraction

### Detection Services
- **Deepware API**: AI-generated image detection
- **FaceForensics++**: Deepfake and manipulation detection
- **Metadata Analysis**: EXIF data extraction and analysis
- **Reverse Search**: TinEye and Google Images integration

## Installation & Setup 🚀

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Clone or download the project files**
   ```bash
   # Ensure you have all project files in a directory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run powerhex_app.py
   ```

4. **Access the platform**
   - Open your browser to `http://localhost:8501`
   - Start uploading and analyzing images!

### Alternative Installation
If you encounter any issues with the requirements.txt, install packages individually:
```bash
pip install streamlit pandas plotly pillow requests
```

## How to Use 📱

### 1. Image Analysis
- Navigate to the "🔍 Image Scanner" page
- Upload a PNG, JPG, or JPEG image
- Click "🔍 Analyze Image" to start detection
- Review comprehensive results including confidence scores and metadata

### 2. View Analytics
- Go to "📊 Analytics Dashboard"
- Monitor scan statistics and detection patterns
- Analyze trends and community activity

### 3. Learn & Educate
- Visit "🎓 Education Center"
- Read guides on detecting AI-generated images
- Take interactive quizzes to test your knowledge

### 4. Report Suspicious Content
- Use "🚩 Reporting System" to flag concerning images
- Review community reports and contribute to verification

## Demo Features 🎯

The current implementation includes:
- **Mock API Integration**: Simulates real detection services for demonstration
- **Realistic Results**: Generates believable confidence scores and detection outcomes
- **Full Database**: Complete scan history and analytics tracking
- **Educational Content**: Comprehensive learning materials and quizzes
- **Community Features**: Reporting and flagging system

## Future Enhancements 🔮

### Phase 2 Features
- **Blockchain Registry**: Immutable image provenance tracking
- **Real API Integration**: Connection to live detection services
- **Advanced Analytics**: ML-powered trend analysis
- **Mobile App**: Native iOS/Android applications
- **API Endpoints**: RESTful API for third-party integration

### Scalability Improvements
- **Cloud Deployment**: AWS/Azure hosting for production use
- **Load Balancing**: Handle high-volume image processing
- **CDN Integration**: Fast global content delivery
- **Advanced Security**: Enhanced data protection and privacy

## Technical Highlights 💡

### Innovation Points
- **Multi-API Fusion**: Combines multiple detection algorithms for higher accuracy
- **User-Centric Design**: Intuitive interface requiring minimal technical knowledge
- **Educational Integration**: Not just detection, but user awareness and education
- **Community-Driven**: Collaborative verification and reporting system
- **Extensible Architecture**: Easy integration of new detection APIs and features

### Competition Advantages
- **Comprehensive Solution**: End-to-end platform from detection to education
- **Rapid Deployment**: Ready-to-use prototype with full functionality
- **Real-World Applicable**: Addresses actual national security concerns
- **Scalable Design**: Architecture supports growth and feature expansion
- **User Empowerment**: Focuses on educating users, not just providing results

## Project Structure 📁

```
powerhex_platform/
├── powerhex_app.py          # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── powerhex_data.db        # SQLite database (created automatically)
└── screenshots/            # Demo screenshots (if needed)
```

## Demonstration Script 🎪

### For Judges/Evaluators
1. **Show Homepage**: Explain the problem and solution approach
2. **Upload Test Image**: Demonstrate detection capabilities
3. **Review Results**: Walk through confidence scores and metadata analysis
4. **Show Analytics**: Display dashboard with scan statistics
5. **Educational Tour**: Demonstrate learning features and quizzes
6. **Community Features**: Show reporting and flagging system
7. **Technical Deep-dive**: Explain architecture and scalability

### Key Talking Points
- **National Security Relevance**: Direct impact on misinformation campaigns
- **Technical Sophistication**: Multi-API integration and comprehensive analysis
- **User Accessibility**: No technical knowledge required for operation
- **Educational Value**: Empowers users with detection knowledge
- **Scalability**: Ready for production deployment and expansion

## API Integration Notes 📡

The current version uses mock APIs for demonstration purposes. To integrate with real services:

### Deepware API
```python
# Replace MockDetectionAPIs.deepware_detection() with:
def real_deepware_detection(image_data):
    response = requests.post(
        'https://api.deepware.ai/analyze',
        files={'image': image_data},
        headers={'Authorization': 'Bearer YOUR_API_KEY'}
    )
    return response.json()
```

### FaceForensics++
```python
# Integration code for FaceForensics++ API
def real_faceforensics_detection(image_data):
    # Implement actual API call
    pass
```

## Database Schema 📊

### Scans Table
- `id`: Primary key
- `filename`: Original filename
- `file_hash`: MD5 hash for duplicate detection
- `scan_result`: Detection outcome (LIKELY FAKE/GENUINE/SUSPICIOUS)
- `confidence_score`: Probability score (0.0-1.0)
- `timestamp`: Scan datetime
- `metadata`: JSON-stored image metadata
- `flagged`: Community flagging status
- `flag_reason`: Reason for flagging

### Educational Stats Table
- `id`: Primary key
- `quiz_taken`: Boolean flag
- `score`: Quiz score
- `timestamp`: Completion datetime

## Contributing 🤝

This project was developed for SIH 2024. For production deployment:
1. Replace mock APIs with real service integrations
2. Implement proper authentication and security measures
3. Add comprehensive error handling and logging
4. Optimize database queries for high-volume usage
5. Implement caching for frequently accessed data

## License & Usage 📝

Developed for Smart India Hackathon 2024  
Team PowerHEX  
Problem Statement ID: 25161  

For educational and demonstration purposes. Production deployment requires proper API licenses and security implementations.

---

**PowerHEX Team**: Creating innovative solutions for national cybersecurity challenges! 🇮🇳