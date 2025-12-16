"""
BBC Documentary TTS Web App
FastAPI backend for text-to-speech with British narrator voices
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os

from tts_service import tts_service

app = FastAPI(
    title="BBC Documentary TTS",
    description="Convert text to speech with professional British narrator voices",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to synthesize")
    voice: str = Field(default="en-GB-Neural2-B", description="Voice ID")
    speaking_rate: float = Field(default=0.9, ge=0.25, le=4.0, description="Speaking rate")
    pitch: float = Field(default=-2.0, ge=-20.0, le=20.0, description="Voice pitch")


@app.get("/api/voices")
async def get_voices():
    """Get available voices"""
    return tts_service.get_available_voices()


@app.post("/api/synthesize")
async def synthesize(request: SynthesizeRequest):
    """Synthesize text to speech"""
    try:
        audio_content = tts_service.synthesize(
            text=request.text,
            voice_name=request.voice,
            speaking_rate=request.speaking_rate,
            pitch=request.pitch
        )
        
        return Response(
            content=audio_content,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=narration.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Serve the main page"""
    return FileResponse(os.path.join(static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
