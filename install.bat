@echo off
title Install Requirements

echo ╔════════════════════════════════════════════════════════╗
echo ║      📦 Installing Nadi Al-Hadid Requirements         ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed!
    echo.
    echo 📥 Download Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)
echo ✅ Python is installed
echo.

echo 📦 Installing requirements...
pip install -r requirements.txt

echo.
echo 🔄 Creating database...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🧑 Creating admin user...
python manage.py createsuperuser

echo.
echo ✅ Installation complete!
echo.
echo 🚀 Run "start.bat" to start the system
echo.
pause