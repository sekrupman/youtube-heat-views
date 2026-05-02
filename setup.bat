@echo off
REM YouTube Video Processor - Setup Script for Windows

echo ========================================
echo YouTube Video Processor Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python is installed. Installing dependencies...
echo.

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found in PATH
    echo Please install FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
    echo And add C:\ffmpeg\bin to your PATH
    pause
)

echo.
echo Checking yt-dlp installation...
yt-dlp --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: yt-dlp not installed properly
    echo It should have been installed with pip
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   python api.py
echo.
echo Then open: http://localhost:8000
echo.
pause
