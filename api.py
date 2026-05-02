import os
import sys
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from youtube import (
    extract_video_id,
    download_video,
    download_video_section,
    generate_clips,
    find_heatmap,
)

# Setup static files directory
def setup_static_files():
    """Copy static files to static directory if needed"""
    os.makedirs("static", exist_ok=True)
    
    # Copy HTML, CSS, JS files to static directory if they exist in root
    files_to_copy = ['index.html', 'style.css', 'script.js']
    for filename in files_to_copy:
        src = filename
        dst = os.path.join('static', filename)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"[SETUP] Copied {filename} to static/")

setup_static_files()

app = FastAPI(title="YouTube Video Processor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class DownloadVideoRequest(BaseModel):
    video_url: str


class GenerateClipsRequest(BaseModel):
    video_id: str


class DownloadSectionRequest(BaseModel):
    video_url: str
    start_time: str
    end_time: str


@app.get("/")
def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html", media_type="text/html")


@app.post("/api/download-video")
async def api_download_video(request: DownloadVideoRequest):
    """
    Download full video from YouTube

    Args:
        video_url: YouTube URL or video ID

    Returns:
        JSON with video file path and status
    """
    try:
        video_id = extract_video_id(request.video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL or ID")

        print(f"[API] Downloading full video: {video_id}")
        output_file = download_video(video_id)

        return JSONResponse(
            {
                "status": "success",
                "message": f"Video downloaded successfully",
                "video_id": video_id,
                "output_file": output_file,
                "file_size": (
                    os.path.getsize(output_file) if os.path.exists(output_file) else 0
                ),
            }
        )

    except Exception as e:
        print(f"[API ERROR] Download video failed: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-clips")
async def api_generate_clips(request: GenerateClipsRequest):
    try:
        video_id = extract_video_id(request.video_id)

        print(f"[API] Start processing: {video_id}")

        # STEP 1: download
        video_path = download_video(video_id)

        print(f"[API] Video ready: {video_path}")

        # STEP 2: heatmap
        segments = find_heatmap(video_id)

        # STEP 3: generate clips
        generate_clips(video_path, segments)
        
        # STEP 4: return clips
        clips_dir = "clips"
        clip_files = sorted([
            f for f in os.listdir(clips_dir)
            if f.endswith(".mp4") and video_id in f
        ])
        print(f"[API] Generated clips: {clip_files}")

        return JSONResponse({
            "status": "success",
            "message": f"Generated {len(clip_files)} clips",
            "video_id": video_id,
            "clips": clip_files,
        })

    except Exception as e:
        print(f"[API ERROR] {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/download-section")
async def api_download_section(request: DownloadSectionRequest):
    """
    Download specific section of video from YouTube

    Args:
        video_url: YouTube URL or video ID
        start_time: Start time (format: HH:MM:SS or MM:SS)
        end_time: End time (format: HH:MM:SS or MM:SS)

    Returns:
        JSON with downloaded video section file path
    """
    try:
        video_id = extract_video_id(request.video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL or ID")

        print(
            f"[API] Downloading section {request.start_time}-{request.end_time}: {video_id}"
        )
        output_file = download_video_section(
            video_id, request.start_time, request.end_time
        )

        return JSONResponse(
            {
                "status": "success",
                "message": f"Video section downloaded successfully",
                "video_id": video_id,
                "start_time": request.start_time,
                "end_time": request.end_time,
                "output_file": output_file,
                "file_size": (
                    os.path.getsize(output_file) if os.path.exists(output_file) else 0
                ),
            }
        )

    except Exception as e:
        print(f"[API ERROR] Download section failed: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/clips")
async def api_list_clips():
    """List all generated clips"""
    try:
        clips_dir = "clips"
        if not os.path.exists(clips_dir):
            return JSONResponse({"clips": [], "count": 0})

        clip_files = sorted([f for f in os.listdir(clips_dir) if f.endswith(".mp4")])

        clips_with_size = []
        for clip in clip_files:
            clip_path = os.path.join(clips_dir, clip)
            size = os.path.getsize(clip_path) if os.path.exists(clip_path) else 0
            clips_with_size.append(
                {
                    "name": clip,
                    "path": clip_path,
                    "size": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                }
            )

        return JSONResponse({"clips": clips_with_size, "count": len(clips_with_size)})

    except Exception as e:
        print(f"[API ERROR] List clips failed: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
