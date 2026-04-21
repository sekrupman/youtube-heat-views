Make sure you have installed:

Python 3.9+
yt-dlp
ffmpeg

Installation
1. Install Python dependencies
pip install yt-dlp requests
2. Install FFmpeg (Windows)
Download from: https://www.gyan.dev/ffmpeg/builds/
Extract to:
C:\ffmpeg\
3. Add to PATH:
C:\ffmpeg\bin
4. Restart terminal

Verify installation
ffmpeg -version
yt-dlp --version

Setup Cookies (IMPORTANT)
    Some YouTube videos require login and will fail with:

Sign in to confirm you’re not a bot
    Recommended solution: Use Chrome extension
    Install Chrome extension:
        Get cookies.txt LOCALLY
        Open YouTube and make sure you're logged in
        Click the extension → click Export
        Save the file as:
        cookies.txt

        Place it in your project root:
        project/
        ├── youtube.py
        ├── cookies.txt 
        └── clips/

When to refresh cookies
    Re-export cookies if:
        Downloads fail suddenly
        You see bot/authentication errors again

using CMD : 
Run the script with a video ID:

python youtube.py VIDEO_ID

python youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"

Output
project/
│
├── clips/
│   ├── clip_1_630.mp4
│   ├── clip_2_805.mp4
│   └── clip_3_3770.mp4
│
├── VIDEO_ID.mp4
└── youtube.py