from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse
from pytube import YouTube
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins (change "*" to your domain for better security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "YouTube Downloader API is running"}

@app.get("/download")
async def download_video(url: str = Query(...), resolution: str = Query("720p")):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()
        if not stream:
            return JSONResponse(status_code=404, content={"error": f"Resolution {resolution} not available"})
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        headers = {
            "Content-Disposition": f"attachment; filename={yt.title}.mp4"
        }
        return StreamingResponse(buffer, media_type="video/mp4", headers=headers)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
