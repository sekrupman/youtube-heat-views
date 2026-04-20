import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess
import os
import re
import json
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

# progress tracker
class Progress:
    def __init__(self):
        self.total = 100
        self.current = 0

    def step(self, name, percent):
        self.current += percent
        if self.current > 100:
            self.current = 100
        print(f"[{self.current:>6.2f}%] {name}", flush=True)

    def sub(self, name, i, total):
        percent = (i / total) * 100
        print(f"{name}: {percent:.1f}% ({i}/{total})", flush=True)

progress = Progress()

def fail(step, message):
    print(f"[ERROR:{step}] {message}", file=sys.stderr, flush=True)
    sys.exit(1)


# step 1: fetch HTML
def fetch_video_page(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    progress.step("Fetching video page...", 10)

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        fail("FETCH", str(e))

    return res.text


# step 2: extract ytInitialData
def extract_yt_initial_data(html):
    progress.step("Parsing ytInitialData...", 15)

    match = re.search(r"ytInitialData\s*=\s*(\{.*?\});", html)
    if not match:
        fail("PARSE", "ytInitialData not found")

    try:
        return json.loads(match.group(1))
    except Exception as e:
        fail("PARSE", f"JSON decode failed: {e}")


# step 3: find heatmap
def find_heatmap(video_id):
    progress.step("Fetching heatmap...", 15)

    # import requests, re, json

    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # html = requests.get(url, headers=headers, timeout=20).text
        html = fetch_html(url)
    except Exception as e:
        fail("NETWORK", str(e))

    # ----------------------------
    # 1. Extract markers from HTML
    # ----------------------------
    match = re.search(
        r'"markers":\s*(\[.*?\])\s*,\s*"?markersMetadata"?',
        html,
        re.DOTALL
    )

    if not match:
        fail("HEATMAP", "No heatmap markers found (video may not have most replayed data)")

    try:
        markers = json.loads(match.group(1).replace('\\"', '"'))
    except Exception as e:
        fail("PARSE", str(e))

    # ----------------------------
    # 2. Normalize segments
    # ----------------------------
    segments = []

    for marker in markers:
        marker = marker.get("heatMarkerRenderer", marker)

        try:
            segments.append({
                "start": float(marker["startMillis"]) / 1000,
                "duration": float(marker["durationMillis"]) / 1000,
                "score": float(marker.get("intensityScoreNormalized", 0))
            })
        except Exception:
            continue

    if not segments:
        fail("HEATMAP", "No valid heatmap segments parsed")

    print(f"[DEBUG] Raw segments: {len(segments)}")

    # ----------------------------
    # 3. Filter weak segments
    # ----------------------------
    MIN_SCORE = 0.5
    segments = [s for s in segments if s["score"] >= MIN_SCORE]

    # ----------------------------
    # 4. Merge nearby segments
    # ----------------------------
    def merge_segments(segments, gap_threshold=60):
        merged = []

        for seg in sorted(segments, key=lambda x: x["start"]):
            if not merged:
                merged.append(seg)
                continue

            prev = merged[-1]

            if seg["start"] <= prev["start"] + prev["duration"] + gap_threshold:
                end_time = max(
                    prev["start"] + prev["duration"],
                    seg["start"] + seg["duration"]
                )

                prev["duration"] = end_time - prev["start"]
                prev["score"] = max(prev["score"], seg["score"])
            else:
                merged.append(seg)

        return merged

    segments = merge_segments(segments)

    # ----------------------------
    # 5. Expand segments (better clips)
    # ----------------------------
    def expand_segments(segments, padding=10, max_duration=90):
        results = []

        for seg in segments:
            start = max(0, seg["start"] - padding)
            duration = min(seg["duration"] + padding * 2, max_duration)

            results.append({
                "start": start,
                "duration": duration,
                "score": seg["score"]
            })

        return results

    segments = expand_segments(segments)

    # ----------------------------
    # 6. Take top N clips
    # ----------------------------
    MAX_CLIPS = 100
    segments = sorted(segments, key=lambda x: x["score"], reverse=True)[:MAX_CLIPS]

    print(f"[SUCCESS] Final clips: {len(segments)}")

    return segments

# fetch url 
def fetch_html(url):
    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    session.mount("https://", HTTPAdapter(max_retries=retries))

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.youtube.com/",
    }

    try:
        response = session.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text

    except Exception as e:
        fail("NETWORK", str(e))

# step 4: normalize heatmap
def normalize_heatmap(heatmap):
    progress.step("Normalizing heatmap...", 20)

    points = []
    max_score = 0
    total = len(heatmap)

    for i, h in enumerate(heatmap, 1):
        score = h["heatMarkerRenderer"]["heatMarkerIntensityScoreNormalized"]
        start = h["heatMarkerRenderer"]["timeRangeStartMillis"] / 1000

        points.append({
            "time": start,
            "score": score
        })

        if score > max_score:
            max_score = score

        # show sub progress every 10 items
        if i % 10 == 0 or i == total:
            progress.sub("Normalizing", i, total)

    return points


# step 5: filter peaks
def filter_peaks(points, video_id, threshold=0.7, min_gap=10):
    progress.step("Filtering peaks...", 20)

    peaks = []
    last_time = -999
    total = len(points)

    for i, p in enumerate(points, 1):
        if p["score"] >= threshold:
            if p["time"] - last_time >= min_gap:
                p["url"] = f"https://www.youtube.com/watch?v={video_id}&t={int(p['time'])}s"
                peaks.append(p)
                last_time = p["time"]

        if i % 20 == 0 or i == total:
            progress.sub("Filtering", i, total)

    print(f"Selected {len(peaks)} peaks")
    return peaks


# step 6: save results
def save_output(video_id, points, peaks):
    progress.step("Saving output...", 60)

    filename = f"{video_id}_clips.csv"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("start,duration,score,url\n")

        for p in peaks:
            start = p["start"]
            duration = p["duration"]
            score = p["score"]

            # build YouTube timestamp URL
            url = f"https://www.youtube.com/watch?v={video_id}&t={int(start)}s"

            f.write(f"{start},{duration},{score},{url}\n")

    print(f"[SUCCESS] Saved to {filename}")

# download full video
def download_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    output = f"{video_id}.mp4"

    print("[INFO] Downloading video (force 1080p)...")

    cmd = [
        "yt-dlp",
        "-f", "137+140",
        "--merge-output-format", "mp4",
        "--no-cache-dir",
        "-o", f"{video_id}.%(ext)s",
        url
    ]

    subprocess.run(cmd, check=True)

    return output

# cut video per clip
def generate_clips(video_path, segments):
    os.makedirs("clips", exist_ok=True)

    for i, seg in enumerate(segments, start=1):
        start = seg["start"]
        duration = seg["duration"]

        output_file = f"clips/clip_{i}_{int(start)}.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-ss", str(start),
            "-t", str(duration),

            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",

            "-c:a", "aac",
            "-b:a", "192k",

            "-movflags", "+faststart",

            output_file
        ]

        print(f"[INFO] Creating clip {i} ({start}s)...")

        subprocess.run(cmd, check=True)

# extrack video id
def extract_video_id(input_str):
    # full URL
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", input_str)
    if match:
        return match.group(1)

    # short URL
    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", input_str)
    if match:
        return match.group(1)

    # assume raw ID
    if len(input_str) == 11:
        return input_str

    return None

# main
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python youtube.py <video_id_or_url>")
        sys.exit(1)

    raw_input = sys.argv[1]
    video_id = extract_video_id(raw_input)

    if not video_id:
        fail("INPUT", "Invalid YouTube URL or ID")

    print(f"[INFO] Using video_id = {video_id}")

    start_time = time.time()

    html = fetch_video_page(video_id)
    data = extract_yt_initial_data(html)
    heatmap = find_heatmap(video_id)
    points = heatmap
    peaks = heatmap
    video_path = download_video(video_id)
    generate_clips(video_path, heatmap)

    # save_output(video_id, points, peaks)

    progress.step("Done", 0)

    elapsed = time.time() - start_time
    print(f"\n Finished in {elapsed:.2f}s")


if __name__ == "__main__":
    main()