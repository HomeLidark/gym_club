@echo off
title Stop Server

echo ╔════════════════════════════════════════════════════════╗
echo ║         🔴 Stopping Nadi Al-Hadid Server              ║
echo ╚════════════════════════════════════════════════════════╝
echo.

:: Kill all Python processes related to runserver
taskkill /f /im python.exe /fi "windowtitle eq *runserver*"

echo ✅ Server stopped successfully
echo.
pause