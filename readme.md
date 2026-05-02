## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn api:app --reload

# 3. Open your browser
http://localhost:8000
```

Done! Start downloading videos right now.

## Prerequisites

### Required Software

- **Python 3.9+** - Programming language
- **FFmpeg** - Video processing tool
- **yt-dlp** - YouTube downloader
- **pip** - Python package manager

### Verification

Check if you have everything installed:

```bash
python --version        # Should be 3.9 or higher
ffmpeg -version         # Should show FFmpeg version
yt-dlp --version        # Should show yt-dlp version
pip --version           # Should show pip version

## Installation

### Step 1: Install Python Dependencies

```bash
cd "ver 2.0"
pip install -r requirements.txt
```

This installs:

- `fastapi` - Web framework
- `uvicorn` - Web server
- `requests` - HTTP requests
- `pydantic` - Data validation
- `python-multipart` - File uploads
- `urllib3` - HTTP client

### Step 2: Install FFmpeg

**Windows:**

1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to: `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin` to your PATH environment variable
4. Restart your terminal
5. Verify: `ffmpeg -version`

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Step 3: Verify Installation (Optional)

Run the setup verification script:

```bash
python setup.py
```

This will check:

- ✓ Python version
- ✓ Required modules
- ✓ System commands (ffmpeg, yt-dlp)
- ✓ Directory structure

### Step 4: YouTube Authentication (Optional but Recommended)

Some YouTube videos require login. To fix this:

1. **Install Chrome Extension:**
   - Go to: https://chrome.google.com/webstore/detail/cookiestxt/bakpesbnggaiagapehbocjdcjj62jgmf
   - Click "Add to Chrome"

2. **Export Cookies:**
   - Open YouTube and log in
   - Click the extension icon
   - Click "Export"
   - Save as `cookies.txt` in the project root

3. **Verify:**

   ```
   ver-2.0
   ├── api.py
   ├── youtube.py
   ├── cookies.txt    ← Place here
   └── ...
   ```

4. **When to Refresh:**
   - If downloads fail with "Sign in to confirm"
   - If you see bot/authentication errors
   - Periodically for security (monthly recommended)

---

## Starting the Application

### Method 1: Direct Python

```bash
python api.py
```

Expected output:

```
[SETUP] Copied index.html to static/
[SETUP] Copied style.css to static/
[SETUP] Copied script.js to static/
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Method 2: Windows Batch Script

```bash
setup.bat
python api.py
```

### Method 3: With Custom Port

Edit `api.py` (last line) and change the port:

```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change 8000 to 8080
```

Then start normally:

```bash
python api.py
```

### Accessing the Application

**Local Access:**

```
http://localhost:8000
http://127.0.0.1:8000
```

**Remote Access** (if on network):

```
http://YOUR_IP_ADDRESS:8000
# Example: http://192.168.1.100:8000
```

---

## 💻 Using the Web Interface

### Tab 1: Download Full Video

**Purpose:** Download an entire YouTube video in high quality

**Steps:**

1. Click the "Download Full Video" tab
2. Enter YouTube URL or video ID:
   - Full URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Short URL: `https://youtu.be/dQw4w9WgXcQ`
   - Just ID: `dQw4w9WgXcQ`
3. Click "Download Video"
4. Watch the progress bar and logs
5. View results when complete

**Output:**

- File: `dQw4w9WgXcQ.mp4`
- Quality: 1080p (if available)
- Location: Project root directory
- Time: 2-10 minutes (depends on video length)

**Example:**

```
Input: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Output: dQw4w9WgXcQ.mp4 (52 MB)
Status: Download complete!
```

### Tab 2: Generate Clips

**Purpose:** Automatically create clips from the most-watched moments

**Prerequisites:**

- You must have downloaded a video first
- Video file must be in the project root

**Steps:**

1. Click the "Generate Clips" tab
2. Enter the video file path:
   - Example: `dQw4w9WgXcQ.mp4`
   - Path: Just the filename if in project root
3. Click "Generate Clips"
4. Watch progress (this takes longer)
5. View results when complete

**How It Works:**

1. Fetches YouTube's heatmap data
2. Identifies peak engagement moments
3. Expands clips with padding for context
4. Encodes each clip using FFmpeg
5. Saves to `clips/` folder

**Output:**

- Files: `clip_1_630.mp4`, `clip_2_805.mp4`, etc.
- Quality: Automatically encoded
- Location: `clips/` subdirectory
- Time: 5-20 minutes (depends on video length)

**Example:**

```
Input: dQw4w9WgXcQ.mp4
Clips Generated: 5
Output: clips/clip_1_630.mp4, clips/clip_2_805.mp4, ...
Status: 5 clips generated successfully!
```

### Tab 3: Download Video Section

**Purpose:** Download a specific time range from YouTube

**Steps:**

1. Click the "Download Section" tab
2. Enter YouTube URL or ID
3. Enter start time (format: `HH:MM:SS` or `MM:SS`)
   - Example: `00:30:00` (30 seconds)
   - Or: `30:00` (30 seconds)
4. Enter end time (same format)
   - Example: `00:35:00` (35 seconds)
   - Or: `35:00` (35 seconds)
5. Click "Download Section"
6. View results when complete

**Output:**

- File: `VIDEO_ID_HH-MM-SS_HH-MM-SS.mp4`
- Example: `dQw4w9WgXcQ_00-30-00_00-35-00.mp4`
- Location: Project root directory
- Time: 1-5 minutes (depends on section length)

**Example:**

```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Start: 00:30:00
End: 00:35:00
Output: dQw4w9WgXcQ_00-30-00_00-35-00.mp4 (5 MB)
Status: Section downloaded successfully!
```

### Tab 4: View Clips

**Purpose:** See all generated clips with download links

**Features:**

- Lists all clips in `clips/` folder
- Shows file sizes
- Direct download links
- Refresh button to update list

**Steps:**

1. Click the "View Clips" tab
2. Click "🔄 Refresh List" to update
3. Browse generated clips
4. Click download link on any clip

**Display:**

```
Clip Name: clip_1_630.mp4
Size: 5.0 MB
[Download]

Clip Name: clip_2_805.mp4
Size: 4.5 MB
[Download]
```

---

## 🔌 Using the REST API

### Overview

**Base URL:** `http://localhost:8000/api`

**Format:** JSON request/response

**Headers:** `Content-Type: application/json`

### Endpoint 1: Download Full Video

**Request:**

```bash
curl -X POST http://localhost:8000/api/download-video \
  -H "Content-Type: application/json" \
  -d '{"video_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

**Response:**

```json
{
  "status": "success",
  "message": "Video downloaded successfully",
  "video_id": "dQw4w9WgXcQ",
  "output_file": "dQw4w9WgXcQ.mp4",
  "file_size": 52428800
}
```

### Endpoint 2: Generate Clips

**Request:**

```bash
curl -X POST http://localhost:8000/api/generate-clips \
  -H "Content-Type: application/json" \
  -d '{"video_path":"dQw4w9WgXcQ.mp4"}'
```

**Response:**

```json
{
  "status": "success",
  "message": "Generated 5 clips",
  "clip_count": 5,
  "clips": [
    "clip_1_630.mp4",
    "clip_2_805.mp4",
    "clip_3_1200.mp4",
    "clip_4_1850.mp4",
    "clip_5_2500.mp4"
  ],
  "clips_directory": "clips"
}
```

### Endpoint 3: Download Video Section

**Request:**

```bash
curl -X POST http://localhost:8000/api/download-section \
  -H "Content-Type: application/json" \
  -d '{
    "video_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "start_time":"00:30:00",
    "end_time":"00:35:00"
  }'
```

**Response:**

```json
{
  "status": "success",
  "message": "Video section downloaded successfully",
  "video_id": "dQw4w9WgXcQ",
  "start_time": "00:30:00",
  "end_time": "00:35:00",
  "output_file": "dQw4w9WgXcQ_00-30-00_00-35-00.mp4",
  "file_size": 5242880
}
```

### Endpoint 4: List Clips

**Request:**

```bash
curl http://localhost:8000/api/clips
```

**Response:**

```json
{
  "clips": [
    {
      "name": "clip_1_630.mp4",
      "path": "clips/clip_1_630.mp4",
      "size": 5242880,
      "size_mb": 5.0
    },
    {
      "name": "clip_2_805.mp4",
      "path": "clips/clip_2_805.mp4",
      "size": 4718592,
      "size_mb": 4.5
    }
  ],
  "count": 2
}
```

### Endpoint 5: Health Check

**Request:**

```bash
curl http://localhost:8000/api/health
```

**Response:**

```json
{
  "status": "healthy"
}
```

### API Error Handling

**Bad Request Example:**

```json
{
  "detail": "[HEATMAP] No valid heatmap segments parsed"
}
```

**HTTP Status Codes:**

- `200` - Success
- `400` - Bad request
- `500` - Server error

---

## 🐛 Troubleshooting

### Installation Issues

**Problem: "Python not found"**

```
Solution: Install Python 3.9+ from https://www.python.org/
Make sure to add Python to PATH during installation
```

**Problem: "ffmpeg not found"**

```
Solution:
Windows: Download from https://www.gyan.dev/ffmpeg/builds/
        Add C:\ffmpeg\bin to PATH
Mac: brew install ffmpeg
Linux: sudo apt-get install ffmpeg
```

**Problem: "Module not found"**

```
Solution: pip install -r requirements.txt
```

### Runtime Issues

**Problem: "Port 8000 already in use"**

```
Solution 1: Kill the process using port 8000
Solution 2: Change port in api.py (last line)
           uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Problem: "ModuleNotFoundError: No module named 'fastapi'"**

```
Solution: pip install -r requirements.txt
```

**Problem: "Permission denied"**

```
Windows: Run Command Prompt as Administrator
Linux/Mac: Use sudo pip install ...
```

### Download Issues

**Problem: "No heatmap markers found"**

```
Reason: Video doesn't have YouTube engagement data
Solution: Try another video (popular videos usually have this)
Note: Download will still work, but clips won't generate
```

**Problem: "Sign in to confirm you're not a bot"**

```
Solution 1: Set up cookies.txt (see Installation Step 4)
Solution 2: Try again later (YouTube temporarily blocking)
Solution 3: Use a different network/VPN
```

**Problem: "HTTP 403 Forbidden"**

```
Solution: Update cookies.txt
         Refresh with Chrome extension if you have it
         Wait a few hours if rate-limited
```

### Output Issues

**Problem: "No clips generated"**

```
Possible reasons:
1. Video doesn't have heatmap data
2. Video is too short
3. Not enough popular moments
Solution: Try another video
```

**Problem: "Clips folder is empty"**

```
Solution: Generate clips first using Tab 2
         Make sure video file exists and path is correct
```

---

## 📂 Output Files

### Download Full Video

```
d:\Master\file yaya\AI\ver 2.0\
├── dQw4w9WgXcQ.mp4          ← Downloaded video
├── api.py
└── youtube.py
```

### Generate Clips

```
d:\Master\file yaya\AI\ver 2.0\
├── clips/
│   ├── clip_1_630.mp4       ← Generated clips
│   ├── clip_2_805.mp4
│   ├── clip_3_1200.mp4
│   └── ...
├── dQw4w9WgXcQ.mp4          ← Original video
└── api.py
```

### Download Section

```
d:\Master\file yaya\AI\ver 2.0\
├── dQw4w9WgXcQ_00-30-00_00-35-00.mp4  ← Section file
├── api.py
└── youtube.py
```

---

## ⚙️ Configuration

### Change Server Port

Edit `api.py` (last line):

```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change 8000 to 8080
```

### Adjust Clip Generation

Edit `youtube.py`:

```python
MIN_SCORE = 0.7          # Higher = fewer clips (0-1)
gap_threshold = 60       # Seconds between clips
padding = 10             # Padding around clips
max_duration = 90        # Max seconds per clip
MAX_CLIPS = 100          # Maximum clips to generate
```

### Server Network Access

Edit `api.py` (last line):

```python
# Local only (current):
uvicorn.run(app, host="0.0.0.0", port=8000)

# Remote access from network:
# http://YOUR_IP:8000
```

---

## 📚 Additional Resources

- **Full Documentation:** See `README_NEW.md`
- **API Reference:** See `API_README.md`
- **Architecture:** See `ARCHITECTURE.md`
- **Quick Start:** See `QUICKSTART.md`
- **File List:** See `MANIFEST.md`

---

## ✅ Checklist Before First Use

- [ ] Python 3.9+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] FFmpeg installed: `ffmpeg -version`
- [ ] yt-dlp available: `yt-dlp --version`
- [ ] Cookies.txt set up (optional)
- [ ] Server starts: `python api.py`
- [ ] Web interface loads: `http://localhost:8000`

---

## 🎯 Common Workflows

### Workflow 1: Complete Video Processing

1. Download Full Video (Tab 1)
2. Generate Clips (Tab 2)
3. View Clips (Tab 4)
4. Download individual clips

### Workflow 2: Quick Section Extraction

1. Download Video Section (Tab 3)
2. Done! File is ready

### Workflow 3: API Integration

1. POST to `/api/download-video`
2. POST to `/api/generate-clips`
3. GET `/api/clips` to list results

---

## 🆘 Getting Help

**Quick Questions?**

- Check the Troubleshooting section above

**Need API Details?**

- See API_README.md

**Want to Understand Code?**

- See ARCHITECTURE.md

**Looking for Specific File?**

- See MANIFEST.md

**Something Not Working?**

1. Check troubleshooting
2. Verify installation with `python setup.py`
3. Check the documentation files
4. Verify all prerequisites are installed

---

## 🎉 You're Ready!

Everything is set up. Start using it:

```bash
python api.py
```

Then visit: **http://localhost:8000**

Enjoy downloading and processing YouTube videos! 🎬
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
│ ├── clip_1_630.mp4
│ ├── clip_2_805.mp4
│ └── clip_3_3770.mp4
│
├── VIDEO_ID.mp4
└── youtube.py
