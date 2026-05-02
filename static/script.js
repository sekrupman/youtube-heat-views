// API Base URL
const API_BASE = "http://localhost:8000/api";

// Tab Navigation
document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    const tabName = button.getAttribute("data-tab");

    // Remove active class from all buttons and contents
    document
      .querySelectorAll(".tab-button")
      .forEach((btn) => btn.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));

    // Add active class to clicked button and corresponding content
    button.classList.add("active");
    document.getElementById(tabName).classList.add("active");
  });
});

// ===== Download Full Video =====
document
  .getElementById("download-video-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const videoUrl = document.getElementById("video-url").value.trim();

    if (!videoUrl) {
      showError("download-video", "Please enter a YouTube URL or video ID");
      return;
    }

    await submitRequest("download-video", {
      video_url: videoUrl,
    });
  });

// ===== Generate Clips =====
document
  .getElementById("generate-clips-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const videoPath = document.getElementById("video-path").value.trim();
    console.log("Generate clips form submitted, videoPath:", videoPath);
    if (!videoPath) {
      showError("generate-clips", "Please enter a video file path");
      return;
    }

    await submitRequest("generate-clips", {
      video_id: videoPath,
    });
  });

// ===== Download Section =====
document
  .getElementById("download-section-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const videoUrl = document.getElementById("section-video-url").value.trim();
    const startTime = document.getElementById("start-time").value.trim();
    const endTime = document.getElementById("end-time").value.trim();
    console.log("download section")
    if (!videoUrl || !startTime || !endTime) {
      showError("download-section", "Please fill in all fields");
      return;
    }

    await submitRequest("download-section", {
      video_url: videoUrl,
      start_time: startTime,
      end_time: endTime,
    });
  });

// ===== View Clips =====
document
  .getElementById("refresh-clips-btn")
  .addEventListener("click", loadClips);

// Load clips on page load
loadClips();

// ===== Helper Functions =====

async function submitRequest(type, data) {
  const statusId = `${type}-status`;
  const resultId = `${type}-result`;
  const errorId = `${type}-error`;
  const endpoint = getEndpoint(type);

  // Show status, hide results
  document.getElementById(statusId).style.display = "block";
  document.getElementById(resultId).style.display = "none";
  document.getElementById(errorId).style.display = "none";
  clearLogs(type);

  try {
    addLog(type, `Sending request to ${endpoint}...`, "info");
    console.log("SENDING DATA:", data);
    const response = await fetch(`${API_BASE}/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log("API Response:", result);

    if (!response.ok) {
      throw new Error(result.detail || "Request failed");
    }

    addLog(type, `✓ ${result.message}`, "success");

    // Hide status, show result
    document.getElementById(statusId).style.display = "none";
    document.getElementById(resultId).style.display = "block";

    // Format and display result
    let html = "";
    for (const [key, value] of Object.entries(result)) {
      if (key !== "status" && key !== "message") {
        if (key === "clip_count" || key === "file_size") {
          html += `<p><strong>${formatKey(key)}:</strong> ${value}</p>`;
        } else if (key === "clips" && Array.isArray(value)) {
          html += `<p><strong>Generated Clips:</strong> ${value.join(", ")}</p>`;
        } else if (typeof value === "string" || typeof value === "number") {
          html += `<p><strong>${formatKey(key)}:</strong> ${value}</p>`;
        }
      }
    }

    document.getElementById(`${type}-content`).innerHTML = html;
  } catch (error) {
    addLog(type, `✗ Error: ${error.message}`, "error");

    // Hide status, show error
    document.getElementById(statusId).style.display = "none";
    document.getElementById(errorId).style.display = "block";
    document.getElementById(`${type}-error-content`).innerHTML =
      `<p>${error.message}</p>`;
  }
}

async function loadClips() {
  const loading = document.getElementById("clips-loading");
  const container = document.getElementById("clips-container");
  const noClips = document.getElementById("no-clips");

  loading.style.display = "block";
  container.innerHTML = "";
  noClips.style.display = "none";

  try {
    const response = await fetch(`${API_BASE}/clips`);
    const data = await response.json();

    loading.style.display = "none";

    if (data.clips && data.clips.length > 0) {
      container.innerHTML = data.clips
        .map((clip) => createClipCard(clip))
        .join("");
    } else {
      noClips.style.display = "block";
    }
  } catch (error) {
    loading.style.display = "none";
    noClips.innerHTML = `<p>Error loading clips: ${error.message}</p>`;
    noClips.style.display = "block";
  }
}

function createClipCard(clip) {
  return `
        <div class="clip-card">
            <div class="clip-thumbnail">🎬</div>
            <div class="clip-info">
                <div class="clip-name">${clip.name}</div>
                <div class="clip-size">${clip.size_mb} MB</div>
                <a href="/${clip.path}" class="clip-download" download>Download</a>
            </div>
        </div>
    `;
}

function getEndpoint(type) {
  const endpoints = {
    "download-video": "download-video",
    "generate-clips": "generate-clips",
    "download-section": "download-section",
  };
  return endpoints[type] || "";
}

function addLog(type, message, level = "info") {
  const logsContainer = document.getElementById(`${type}-logs`);
  if (!logsContainer) return;

  const entry = document.createElement("div");
  entry.className = `log-entry ${level}`;
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;

  logsContainer.appendChild(entry);
  logsContainer.scrollTop = logsContainer.scrollHeight;
}

function clearLogs(type) {
  const logsContainer = document.getElementById(`${type}-logs`);
  if (logsContainer) {
    logsContainer.innerHTML = "";
  }
}

function showError(type, message) {
  const errorId = `${type}-error`;
  const errorContent = `${type}-error-content`;

  document.getElementById(`${type}-status`).style.display = "none";
  document.getElementById(`${type}-result`).style.display = "none";
  document.getElementById(errorId).style.display = "block";
  document.getElementById(errorContent).innerHTML = `<p>${message}</p>`;
}

function formatKey(key) {
  return key
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
