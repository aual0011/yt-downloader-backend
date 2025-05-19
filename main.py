from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import subprocess

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["https://yourdomain.com"] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "YouTube downloader using yt-dlp"}

@app.get("/download")
def download_video(url: str = Query(...), resolution: str = Query("720p")):
    try:
        output_filename = f"{uuid.uuid4()}.mp4"
        command = [
            "yt-dlp",
            "-f", f"bestvideo[height={resolution[:-1]}]+bestaudio/best[height={resolution[:-1]}]",
            "-o", output_filename,
            url
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return JSONResponse(status_code=400, content={"error": result.stderr})

        return FileResponse(
            output_filename,
            media_type="video/mp4",
            filename=output_filename,
            background=lambda: os.remove(output_filename)  # auto delete after send
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
