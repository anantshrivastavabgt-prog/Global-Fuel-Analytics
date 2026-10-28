@echo off
title Global Fuel Analytics Dashboard
echo ===================================================
echo   GLOBAL FUEL ANALYTICS - EXPLORING MARKET DATA
echo   College Capstone Project by Anant Shrivastava
echo ===================================================
echo.
echo Launching your dashboard web application...
echo The app will open in your default browser at http://127.0.0.1:5000
echo.
echo (Keep this window open while using the dashboard. Close it to stop.)
echo.
timeout /t 2 >nul
start "" "http://127.0.0.1:5000"
python app.py
pause
