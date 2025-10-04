@echo off
echo PowerHEX - AI Image Detection Platform
echo Smart India Hackathon 2024 - Team PowerHEX
echo =====================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting PowerHEX Platform...
echo Open your browser to: http://localhost:8501
echo.

streamlit run powerhex_app.py

pause