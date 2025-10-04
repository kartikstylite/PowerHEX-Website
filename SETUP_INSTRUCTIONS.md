# PowerHEX Setup Instructions 🚀

## Quick Start Guide

### Option 1: Automated Setup (Recommended)

#### For Windows:
1. Download all files to a folder
2. Double-click `run_powerhex.bat`
3. Wait for installation to complete
4. Application will open in your browser at `http://localhost:8501`

#### For Mac/Linux:
1. Download all files to a folder
2. Open terminal in the folder
3. Run: `./run_powerhex.sh`
4. Application will open in your browser at `http://localhost:8501`

### Option 2: Manual Setup

#### Prerequisites:
- Python 3.8 or higher
- pip package manager
- Internet connection (for initial setup)

#### Step-by-step:
1. **Install Dependencies**
   ```bash
   pip install streamlit pandas plotly pillow requests
   ```

2. **Run Application**
   ```bash
   streamlit run powerhex_app.py
   ```

3. **Open Browser**
   - Navigate to `http://localhost:8501`
   - Start using PowerHEX!

## File Structure
```
PowerHEX_Platform/
├── powerhex_app.py          # Main application
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── demo_guide.md           # Demonstration script
├── SETUP_INSTRUCTIONS.md   # This file
├── run_powerhex.bat        # Windows launcher
└── run_powerhex.sh         # Mac/Linux launcher
```

## Troubleshooting

### Common Issues:

#### "Module not found" errors:
```bash
pip install --upgrade pip
pip install streamlit pandas plotly pillow requests
```

#### Port already in use:
```bash
streamlit run powerhex_app.py --server.port 8502
```

#### Permission denied (Mac/Linux):
```bash
chmod +x run_powerhex.sh
```

### System Requirements:
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: 500MB free space
- **OS**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Browser**: Chrome, Firefox, Safari, Edge

## Demo Preparation

### Before Demonstration:
1. ✅ Test run the application
2. ✅ Prepare 2-3 sample images
3. ✅ Review demo_guide.md
4. ✅ Practice key talking points
5. ✅ Test all major features

### Sample Images to Use:
- Portrait photos (for deepfake detection demo)
- Screenshots (for AI-generated content demo)  
- Mixed content (for comprehensive analysis)

## Features Overview

### 🔍 Image Scanner
Upload and analyze images for AI manipulation detection

### 📊 Analytics Dashboard  
View scan statistics, trends, and community insights

### 🎓 Education Center
Learn about deepfake detection and take interactive quizzes

### 🚩 Reporting System
Flag suspicious images and review community reports

## API Integration Notes

Current version uses **mock APIs** for demonstration purposes. 

For production deployment:
- Replace mock functions with real API endpoints
- Add API key management
- Implement rate limiting and error handling

## Support & Contact

**Team PowerHEX**  
Smart India Hackathon 2024  
Problem Statement ID: 25161  

For technical support during SIH:
- Check README.md for detailed documentation
- Review demo_guide.md for presentation tips
- Test all features before demonstration

---

**Ready to impress the judges? Let's go! 🏆**