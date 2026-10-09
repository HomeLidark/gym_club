@echo off
title Nadi Al-Hadid - Gym Management System

:: ===== Colors =====
color 0E

:: ===== Clear screen =====
cls

:: ===== Program title =====
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║      🏋️ Nadi Al-Hadid - Gym Management System VIP    ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📌 Version: 2.0
echo 📅 Date: %date%
echo ⏰ Time: %time%
echo.

:: ===== Check Python =====
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

:: ===== Check Django =====
echo 🔍 Checking Django...
python -c "import django" > nul 2>&1
if errorlevel 1 (
    echo ⚠️ Django not found... Installing
    pip install -r requirements.txt
)
echo ✅ Django is ready
echo.

:: ===== Check Database =====
echo 🔄 Checking database...
if not exist db.sqlite3 (
    echo ⚠️ Database not found... Creating
    python manage.py makemigrations
    python manage.py migrate
    echo ✅ Database created
)
echo.

:: ===== Start Server =====
echo 🚀 Starting server...
echo 📱 URL: http://127.0.0.1:8000
echo.
echo ════════════════════════════════════════════════════════
echo.

:: Run server in background
start /b python manage.py runserver

:: Wait for server
timeout /t 3 /nobreak > nul

:: Open browser
start http://127.0.0.1:8000

echo ✅ Server is running! ✅
echo.
echo ════════════════════════════════════════════════════════
echo.
echo 💡 Instructions:
echo    • Browser will open automatically in a few seconds
echo    • To stop server: Press Ctrl+C in this window
echo    • You can now use the system 🎉
echo.
echo ════════════════════════════════════════════════════════
echo.

:: Keep window open
pause